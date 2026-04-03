# ProtoStruc: Backend Repository

This is the central compute hub for ProtoStruc. Driven seamlessly by FastAPI and LangGraph, it parses user-commands into multi-layered product decomposition steps.

## Development Setup

The backend utilizes Python 3.10+ environments. Ensure you instantiate a virtual playground to guarantee dependency locking.

```bash
# 1. Create and hook the environment
python -m venv venv
.\venv\Scripts\activate

# 2. Download dependencies
pip install -r requirements.txt

# 3. Align environment configuration inside `.env` utilizing identical keys from production

# 4. Boot the server and API documentation route
uvicorn app.main:app --reload
```

## Testing Protocol

To manually interface with the database or LLMs outside the Vercel Frontend environment, utilize FastAPI's native swagger generation.

1. Navigate to `http://127.0.0.1:8000/docs`
2. **Authorizing:** If hitting secured routes like `/api/projects`, authenticate via standard JWT exchange mappings in the auth portal located at the top of the swagger hub.
3. Once fully authorized, you can simulate payload pushes directly utilizing the "Try it out" parameters.

## Automated End-to-End Scenarios

The framework allows for rigorous simulation via Python. You can trigger simulated data-pipelines verifying everything from Phase 1 Node Decomposition through Phase 3 FMEA execution running:

```powershell
python test_flow.py
```
> Note: Make sure development JWT access controls are bypassed inside the test script headers, as test_flow runs independently of local storage protocols!
