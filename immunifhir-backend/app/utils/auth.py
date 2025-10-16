from fastapi import Security, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

def verify_token(credentials=Security(security)):
    token = credentials.credentials
    if not token:
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    # TODO: Replace with Supabase auth validation later
    return {"email": "demo@example.com"}
