from typing_extensions import runtime
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import os
import jwt
from datetime import datetime, timedelta, timezone
from jwt.exceptions import InvalidTokenError
from utils import logger

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"

if not JWT_SECRET:
    raise RuntimeError("JWT_SECRET env variable is not set")

logger = logger.setup_logger(__name__)
ph = PasswordHasher()

def hash_password(password):
    passwordrd_hash = ph.hash(password)
    return passwordrd_hash

def verify_password(password_hash, password):
    try:
        return ph.verify(password_hash, password) 
    except VerifyMismatchError:
        return False

def create_access_token(user_id):
    expiration = datetime.now(timezone.utc) + timedelta(minutes=30)

    payload = {
        "sub": str(user_id),
        "exp": expiration
    }

    token = jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )

    return token

def decode_access_token(token):
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            return None
        return int(user_id)
    except InvalidTokenError:
        logger.warning("Invalid Access Token")
        return None

