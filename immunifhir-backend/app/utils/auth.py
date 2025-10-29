import os
from fastapi import Security, HTTPException
from fastapi.security import HTTPBearer
from supabase import create_client

security = HTTPBearer()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
_sb = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None

BYPASS_AUTH = os.getenv("BYPASS_AUTH", "false").lower() == "true"

def verify_token(credentials = Security(security)):
    if BYPASS_AUTH:
        return {"email": "dev@local", "id": "dev-user"}

    if _sb is None:
        raise HTTPException(status_code=500, detail="Supabase not configured")

    token = credentials.credentials
    try:
        user = _sb.auth.get_user(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    if not user or not user.user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return {"email": user.user.get("email"), "id": user.user.get("id")}
