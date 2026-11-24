import logging
import os

from dotenv import load_dotenv
from utils import db, security

load_dotenv()

logger = logging.getLogger(__name__)

def seed_admin():
    email = os.getenv("SEED_ADMIN_EMAIL")
    password = os.getenv("SEED_ADMIN_PWD")

    if not email:
        raise ValueError("SEED_ADMIN_EMAIL is required")

    existing_user = db.get_user_by_email(email)

    if existing_user:
        if existing_user["role"] != "admin":
            raise ValueError(
                "Seed account exists but is not an admin"
            )

        if not existing_user["active"]:
            raise ValueError("Seed admin account is disabled")

        logger.info("Admin account already exists")
        return

    if not password:
        raise ValueError("SEED_ADMIN_PASSWORD is required")

    password_hash = security.hash_password(password)

    created = db.create_user(
        email,
        password_hash,
        role="admin",
    )

    if not created:
        raise RuntimeError("Failed to create admin account")

    logger.info("Admin account successfully created")


def seed_exchanges():
    pass


def seed_companies():
    SEED_COMPANIES = [
        {"code": "BHP", "exchange": "AX"},
        {"code": "CBA", "exchange": "AX"},
        {"code": "WES", "exchange": "AX"},
        {"code": "WAA", "exchange": "AX"},
    ]


def main():
    logger.info("Starting database seed")

    seed_admin()
    seed_exchanges()
    seed_companies()

    logger.info("Database seed completed")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
