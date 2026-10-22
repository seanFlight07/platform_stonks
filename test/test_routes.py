from unittest.mock import patch

from fastapi.testclient import TestClient

from web.main import app

client = TestClient(app)


def test_health_check_success(client):
    with patch("web.routes.db.check_db") as mock_check_db:
        mock_check_db.return_value = True

        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_health_check_database_failure():
    with patch("web.routes.db.check_db") as mock_check_db:
        mock_check_db.return_value = False

        response = client.get("/health")

    assert response.status_code == 500
    assert response.json() == {
        "detail": "Please contact admin"
    }

def test_create_user_success(client):
    with (
        patch("web.services.auth_service.db.get_user_by_email") as mock_get_user,
        patch("web.services.auth_service.security.hash_password") as mock_hash,
        patch("web.services.auth_service.db.create_user") as mock_create_user,
    ):
        mock_get_user.return_value = None
        mock_hash.return_value = "fake-password-hash"
        mock_create_user.return_value = True

        response = client.post(
            "/user/create-user",
            json={
                "email": "test@example.com",
                "password": "TestPassword123!",
            },
        )

    assert response.status_code == 201
    assert response.json() == {
        "detail": "New user successfully created"
    }

def test_create_user_duplicate(client):
    with patch("web.services.auth_service.db.get_user_by_email") as mock_get_user:
        mock_get_user.return_value = {
            "id": 1,
            "email": "test@example.com",
        }

        response = client.post(
            "/user/create-user",
            json={
                "email": "test@example.com",
                "password": "TestPassword123!",
            },
        )

    assert response.status_code == 409
    assert response.json() == {
        "detail": "User already exists"
    }

def test_login_success(client):
    with (
        patch("web.services.auth_service.db.get_user_by_email") as mock_get_user,
        patch("web.services.auth_service.security.verify_password") as mock_verify,
        patch("web.services.auth_service.security.create_access_token") as mock_token,
    ):
        mock_get_user.return_value = {
            "id": 1,
            "email": "test@example.com",
            "password_hash": "fake-hash",
            "active": True,
        }
        mock_verify.return_value = True
        mock_token.return_value = "fake-access-token"

        response = client.post(
            "/user/login",
            json={
                "email": "test@example.com",
                "password": "TestPassword123!",
            },
        )

    assert response.status_code == 200
