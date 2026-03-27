import jwt
import bcrypt
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from passlib.context import CryptContext
from app.core.config import settings

# Use argon2 for new hashes, keep bcrypt for old ones
# Note: we keep bcrypt in the context for scheme detection, 
# but we handle verification manually below to skip passlib's 72-byte bug.
pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # If it's a bcrypt hash ($2a$, $2b$, $2y$), use bcrypt library directly
    # This avoids the passlib 72-byte ValueError bug entirely
    if hashed_password.startswith(("$2a$", "$2b$", "$2y$")):
        try:
            # bcrypt.checkpw handles any length by standard bcrypt truncation
            return bcrypt.checkpw(
                plain_password.encode('utf-8'), 
                hashed_password.encode('utf-8')
            )
        except Exception:
            return False
            
    # For argon2 or other schemes, use passlib as normal
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    # Use argon2 for all NEW hashes
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")

def verify_supabase_jwt(token: str) -> Dict[str, Any]:
    """
    Deprecated: Used to verify Supabase Auth tokens. 
    Use verify_token for new custom JWTs.
    """
    try:
        # We still have this for transitional purposes if needed
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        return decoded_token
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
