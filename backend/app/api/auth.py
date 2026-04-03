from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.schemas import UserRegister, UserLogin, Token, ForgotPasswordRequest, ResetPasswordRequest
from app.core.config import supabase_client
import secrets
from datetime import datetime, timedelta, timezone

router = APIRouter()

@router.post("/register", response_model=Token)
def register(user_data: UserRegister):
    # Check if user already exists
    existing_user = supabase_client.table("users").select("*").eq("email", user_data.email).execute()
    if existing_user.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password
    hashed_password = get_password_hash(user_data.password)
    
    # Create user in Supabase public.users table
    new_user = supabase_client.table("users").insert({
        "email": user_data.email,
        "hashed_password": hashed_password
    }).execute()
    
    if not new_user.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )
    
    user = new_user.data[0]
    
    # Create access token
    access_token = create_access_token(data={"sub": str(user["id"]), "email": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
def login(user_data: UserLogin):
    # Find user
    res = supabase_client.table("users").select("*").eq("email", user_data.email).execute()
    if not res.data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = res.data[0]
    
    # Verify password
    if not verify_password(user_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    # We use email as 'sub' for simplicity, or we could use the UUID
    access_token = create_access_token(data={"sub": str(user["id"]), "email": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/forgot-password")
def forgot_password(req: ForgotPasswordRequest):
    # Check if user exists
    existing_user = supabase_client.table("users").select("*").eq("email", req.email).execute()
    if not existing_user.data:
        # Don't reveal if user exists or not for security, but return None for dev_token
        return {"message": "If an account with that email exists, we sent a password reset link.", "dev_reset_token": None}
    
    # Generate token
    token = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    # Save to db
    res = supabase_client.table("password_resets").insert({
        "email": req.email,
        "token": token,
        "expires_at": expires_at.isoformat()
    }).execute()
    
    if not res.data:
        raise HTTPException(status_code=500, detail="Failed to generate reset token")
        
    return {
        "message": "If an account with that email exists, we sent a password reset link.", 
        "dev_reset_token": token
    }

@router.post("/reset-password")
def reset_password(req: ResetPasswordRequest):
    # Find token
    res = supabase_client.table("password_resets").select("*").eq("token", req.token).execute()
    if not res.data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
        
    reset_record = res.data[0]
    
    # Check expiration
    expires_at = datetime.fromisoformat(reset_record["expires_at"].replace('Z', '+00:00'))
    if datetime.now(timezone.utc) > expires_at:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token has expired")
        
    # Hash new password
    hashed_password = get_password_hash(req.new_password)
    
    # Update user password
    update_res = supabase_client.table("users").update({
        "hashed_password": hashed_password
    }).eq("email", reset_record["email"]).execute()
    
    if not update_res.data:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update password")
        
    # Invalidate token
    supabase_client.table("password_resets").delete().eq("token", req.token).execute()
    
    return {"message": "Password has been successfully reset"}
