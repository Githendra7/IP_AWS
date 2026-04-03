# Deployment Playbook

This repository is designed to be shipped out via continuous integration using **Vercel** and **Render**. This separation ensures that the massive AI compute limits of the backend Python models don't throttle the rendering speed of the edge-delivered frontend interface.

## 1. Backend (Render)

The FastAPI engine is deployed using a Render Web Service.

**Render Settings:**
* **Build Command**: `pip install -r requirements.txt`
* **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
* **Root Directory**: `backend`

**Required Environment Variables**:
* `SUPABASE_URL`: Your Supabase project URL.
* `SUPABASE_ANON_KEY`: Supabase connection key.
* `SUPABASE_SERVICE_ROLE_KEY`: Service role for protected database mutations.
* `GROQ_API_KEY`: Groq API token for LLM operation.
* `JWT_SECRET`: The encryption salt for manual JSON Web Tokens.

> [!TIP]
> Ensure you assign the Root Directory directly in the Render dashboard configuration! Failing to set the root to `backend` will cause pip install to immediately fail as it won't locate `requirements.txt`.

## 2. Frontend (Vercel)

The Next.js user interface is deployed strictly utilizing Vercel's zero-config pipeline.

**Vercel Settings:**
* **Framework Preset**: Next.js
* **Root Directory**: `frontend`
* **Build Command**: `npm run build`

**Required Environment Variables**:
* `NEXT_PUBLIC_API_URL`: Crucial flag pointing to the Live Render backend domain (e.g., `https://your-backend-api.onrender.com/api`).

> [!WARNING]
> Do NOT use `localhost` or `http://` for your live `NEXT_PUBLIC_API_URL` setting. Ensure there are no trailing slashes at the end of the URL before appending `/api`.

---

## Deployment Logic Flow

Pushing a new commit directly onto your target deployment branch (e.g., `main` or `master`) connected inside your respective dashboards triggers a synchronized rebuild. Vercel automatically creates cache limits and purges static generation dependencies, while Render safely rebuilds the Python virtual environment and executes new endpoints.
