from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if token != "secreto-super-token":  # Aquí va lógica JWT real
        raise HTTPException(status_code=403, detail="Token inválido o expirado")
    return {"user": "authenticated"}
