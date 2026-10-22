from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from web.services import auth_service

bearer_scheme = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    user, error = auth_service.get_user_from_token(credentials.credentials)

    if error == "invalid_token":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid or expired token")

    if error == "user_not_found":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="User not found")

    if error == "account_disabled":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User account is disabled")

    return user


def require_admin(current_user=Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Admin access required"
        )

    return current_user
