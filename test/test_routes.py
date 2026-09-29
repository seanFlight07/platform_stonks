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
        patch("web.routes.db.get_user_by_email") as mock_get_user,
        patch("web.routes.security.hash_password") as mock_hash,
        patch("web.routes.db.create_user") as mock_create_user,
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
    with patch("web.routes.db.get_user_by_email") as mock_get_user:
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
        patch("web.routes.db.get_user_by_email") as mock_get_user,
        patch("web.routes.security.verify_password") as mock_verify,
        patch("web.routes.security.create_access_token") as mock_token,
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
    assert response.json() == {
        "access_token": "fake-access-token",
        "token_type": "bearer",
    }

def test_login_unknown_email(client):
    with patch("web.routes.db.get_user_by_email") as mock_get_user:
        mock_get_user.return_value = None

        response = client.post(
            "/user/login",
            json={
                "email": "test@example.com",
                "password": "TestPassword123!",
            },
        )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Invalid email or password",
    }

def test_login_wrong_password(client):
    with (
        patch("web.routes.db.get_user_by_email") as mock_get_user,
        patch("web.routes.security.verify_password") as mock_verify,
        patch("web.routes.security.create_access_token") as mock_token,
    ):
        mock_get_user.return_value = {
            "id": 1,
            "email": "test@example.com",
            "password_hash": "fake-hash",
            "active": True,
        }
        mock_verify.return_value = False
        mock_token.return_value = "fake-access-token"

        response = client.post(
            "/user/login",
            json={
                "email": "test@example.com",
                "password": "TestPassword123!",
            },
        )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Invalid email or password",
    }

def test_get_me_success(client):
    with (
        patch("web.routes.security.decode_access_token") as mock_decode,
        patch("web.routes.db.get_user_by_id") as mock_get_user,
    ):
        mock_decode.return_value = 1
        mock_get_user.return_value = {
            "id": 1,
            "email": "test@example.com",
            "role": "user",
            "active": True,
        }

        response = client.get(
            "/user/me",
            headers={
                "Authorization": "Bearer fake-access-token"
            },
        )

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "email": "test@example.com",
        "role": "user",
    }

def test_get_me_invalid_token(client):
    with patch(
        "web.routes.security.decode_access_token") as mock_decode:
        mock_decode.return_value = None

        response = client.get(
            "/user/me",
            headers={
                "Authorization": "Bearer fake-access-token"
            },
        )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Invalid or expired token",
    }

def test_normal_user_cannot_post_prices(client):
    with (
        patch("web.routes.security.decode_access_token") as mock_decode,
        patch("web.routes.db.get_user_by_id") as mock_get_user,
    ):
        mock_decode.return_value = 1
        mock_get_user.return_value = {
            "id": 1,
            "email": "user@example.com",
            "role": "user",
            "active": True,
        }

        response = client.post(
            "/companies/CCP/prices",
            headers={
                "Authorization": "Bearer fake-access-token"
            },
        )

    assert response.status_code == 403
    assert response.json() == {
        "detail": "Admin access required"
    }

def test_admin_can_post_prices(client, valid_price_data):
    with (
        patch("web.routes.security.decode_access_token") as mock_decode,
        patch("web.routes.db.get_user_by_id") as mock_get_user,
        patch("web.routes.db.get_company") as mock_get_company,
        patch("web.routes.api_fetcher.api_fetch_stock_history") as mock_fetch,
        patch("web.routes.transforms.transform_api_historical") as mock_transform,
        patch("web.routes.validation.validation") as mock_validation,
        patch("web.routes.db.insert_data") as mock_insert,
    ):
        mock_decode.return_value = 1

        mock_get_user.return_value = {
            "id": 1,
            "email": "admin@example.com",
            "role": "admin",
            "active": True,
        }

        mock_get_company.return_value = {
            "code": "CCP",
            "exchange": "AX",
        }

        mock_fetch.return_value = "fake-raw-data"
        mock_transform.return_value = valid_price_data
        mock_validation.return_value = True
        mock_insert.return_value = True

        response = client.post(
            "/companies/CCP/prices",
            headers={
                "Authorization": "Bearer fake-access-token"
            },
        )

    assert response.status_code == 201
    assert response.json() == {
        "detail": "Company CCP successfully inserted"
    }

def test_get_companies_success(client):
    with patch("web.routes.db.get_all_companies") as mock_get_companies:
        mock_get_companies.return_value = [
            {
                "code": "CCP",
                "name": "Credit Corp Group",
                "exchange": "AX",
                "active": True,
            },
            {
                "code": "WBC",
                "name": "Westpac",
                "exchange": "AX",
                "active": True,
            },
        ]

        response = client.get("/companies")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["code"] == "CCP"
    assert data[1]["code"] == "WBC"

def test_get_companies_empty(client):
    with patch("web.routes.db.get_all_companies") as mock_get_companies:
        mock_get_companies.return_value = []

        response = client.get("/companies")

    assert response.status_code == 200
    assert response.json() == []

def test_post_company_success(client):
    with patch("web.routes.db.insert_company") as mock_insert:
        mock_insert.return_value = True

        response = client.post(
            "/companies",
            json={
                "code": "CCP",
                "name": "Credit Corp Group",
                "exchange": "AX",
                "active": True,
            },
        )

    assert response.status_code == 201
    assert response.json() == {
        "detail": "Company CCP successfully inserted"
    }

def test_post_company_duplicate(client):
    with patch("web.routes.db.insert_company") as mock_insert:
        mock_insert.return_value = False

        response = client.post(
            "/companies",
            json={
                "code": "CCP",
                "name": "Credit Corp Group",
                "exchange": "AX",
                "active": True,
            },
        )

    assert response.status_code == 409
    assert response.json() == {
        "detail": "Company CCP already exists in db"
    }

def test_search_company_success(client):
    with (
        patch("web.routes.api_fetcher.api_search_company") as mock_search,
        patch("web.routes.db.get_exchange") as mock_exchange,
    ):
        mock_search.return_value = {
            "code": "ccp",
            "exchange": "ax",
            "sector": "Financial Services",
            "long_name": "Credit Corp Group Limited",
            "previous_close": 12.50,
            "open": 12.60,
            "day_low": 12.40,
            "day_high": 12.80,
        }

        mock_exchange.return_value = {
            "timezone": "Australia/Sydney"
        }

        response = client.get("/companie-search/ccp.ax")

    assert response.status_code == 200

    assert response.json() == {
        "code": "CCP",
        "exchange": "AX",
        "sector": "Financial Services",
        "long_name": "Credit Corp Group Limited",
        "previous_close": 12.50,
        "open": 12.60,
        "day_low": 12.40,
        "day_high": 12.80,
        "timezone": "Australia/Sydney",
    }

def test_search_company_not_found(client):
    with (
        patch("web.routes.api_fetcher.api_search_company") as mock_search,
        patch("web.routes.db.get_exchange") as mock_exchange,
    ):
        mock_search.return_value = None
        mock_exchange.return_value = {
            "timezone": "Australia/Sydney"
        }

        response = client.get("/companie-search/ccp.ax")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Company CCP.AX not found"
    }

def test_search_company_unsupported_exchange(client):
    with (
        patch("web.routes.api_fetcher.api_search_company") as mock_search,
        patch("web.routes.db.get_exchange") as mock_exchange,
    ):
        mock_search.return_value = {
            "code": "CCP",
            "exchange": "AX",
            "sector": "Financial Services",
            "long_name": "Credit Corp Group Limited",
            "previous_close": 12.50,
            "open": 12.60,
            "day_low": 12.40,
            "day_high": 12.80,
        }

        mock_exchange.return_value = None

        response = client.get("/companie-search/ccp.ax")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Exchange AX is not supported"
    }
