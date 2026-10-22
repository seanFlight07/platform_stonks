from utils import db, security


def create_user(email: str, password: str):
    existing_user = db.get_user_by_email(email)

    if existing_user:
        return None, "user_exists"

    password_hash = security.hash_password(password)

    created = db.create_user(email, password_hash)

    if not created:
        return None, "creation_failed"

    return {"detail": "New user successfully created"}, None


def login_user(email: str, password: str):
    user = db.get_user_by_email(email)

    if not user:
        return None, "invalid_credentials"

    valid_password = security.verify_password(
        user["password_hash"],
        password
    )

    if not valid_password:
        return None, "invalid_credentials"

    if not user["active"]:
        return None, "account_disabled"

    access_token = security.create_access_token(user["id"])

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }, None

def get_user_from_token(token: str):
    user_id = security.decode_access_token(token)

    if user_id is None:
        return None, "invalid_token"

    user = db.get_user_by_id(user_id)

    if not user:
        return None, "user_not_found"

    if not user["active"]:
        return None, "account_disabled"

    return user, None
