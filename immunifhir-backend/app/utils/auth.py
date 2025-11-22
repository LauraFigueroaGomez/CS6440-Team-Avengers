import os
from supabase import create_client
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.utils.config import supabase

security = HTTPBearer()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
bearer_scheme = HTTPBearer(auto_error=False)
_sb = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None

BYPASS_AUTH = os.getenv("BYPASS_AUTH", "false").lower() == "true"

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),):
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token = credentials.credentials

    # Ask Supabase to validate token and return user
    res = supabase.auth.get_user(token)

    # supabase-py returns user data in res.user; if invalid, it raises or returns None
    user = getattr(res, "user", None)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return user
