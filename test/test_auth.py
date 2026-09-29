from datetime import datetime, timedelta, timezone

import jwt

from utils.security import (
    JWT_ALGORITHM,
    JWT_SECRET,
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)

def test_hash_password():
    password = "TestPassword123!"

    password_hash = hash_password(password)

    assert password_hash != password

def test_verify_correct_password():
    password = "TestPassword123!"
    password_hash = hash_password(password)

    result = verify_password(password_hash, password)

    assert result is True

def test_verify_incorrect_password():
    password_hash = hash_password("CorrectPassword123!")

    result = verify_password(
        password_hash,
        "WrongPassword123!",
    )

    assert result is False

def test_access_token_returns_correct_user():
    token = create_access_token(42)

    result = decode_access_token(token)

    assert result == 42

def test_invalid_access_token():
    result = decode_access_token("this-is-not-a-valid-token")

    assert result is None

def test_expired_access_token():
    payload = {
        "sub": "42",
        "exp": datetime.now(timezone.utc) - timedelta(minutes=1),
    }

    token = jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )

    result = decode_access_token(token)

    assert result is None
