import os
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

JWT_SECRET = os.environ.get("SUPABASE_JWT_SECRET", "")
JWT_AUD = "authenticated"
bearer_scheme = HTTPBearer(auto_error=False)

BYPASS_AUTH = os.getenv("BYPASS_AUTH", "false").lower() == "true"

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    # ✅ BYPASS FOR DEMO/DEV
    if BYPASS_AUTH:
        return {"id": "demo-user", "email": "demo@local", "role": "demo"}

    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=["HS256"],
            audience=JWT_AUD,
            options={"verify_exp": True}
        )
        return {
            "id": payload.get("sub"),
            "email": payload.get("email"),
            "role": payload.get("role"),
            "raw": payload
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
