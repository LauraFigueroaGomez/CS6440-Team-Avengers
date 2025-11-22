import os
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

JWT_SECRET = os.environ.get("SUPABASE_JWT_SECRET")
JWT_AUD = "authenticated"  # Supabase default
bearer_scheme = HTTPBearer(auto_error=False)

if not JWT_SECRET:
    raise RuntimeError("Missing SUPABASE_JWT_SECRET in environment")

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    print("✅ NEW LOCAL JWT verify_token RUNNING")
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

        # Supabase places user id in sub
        user = {
            "id": payload.get("sub"),
            "email": payload.get("email"),
            "role": payload.get("role"),
            "raw": payload
        }

        return user

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
