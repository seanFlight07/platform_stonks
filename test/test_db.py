from unittest.mock import MagicMock, patch

from utils import db


def test_check_db_success():
    mock_connection = MagicMock()

    with patch("utils.db.engine.connect") as mock_connect:
        mock_connect.return_value.__enter__.return_value = mock_connection

        result = db.check_db()

    assert result is True
    mock_connection.execute.assert_called_once()


def test_check_db_failure():
    with patch(
        "utils.db.engine.connect",
        side_effect=Exception("Database unavailable"),
    ):
        result = db.check_db()

    assert result is False

def test_get_company_success():
    mock_connection = MagicMock()
    mock_result = MagicMock()
    mock_row = MagicMock()

    mock_row.code = "CCP"
    mock_row.name = "Credit Corp Group"
    mock_row.exchange = "AX"

    mock_result.first.return_value = mock_row
    mock_connection.execute.return_value = mock_result

    with patch("utils.db.engine.connect") as mock_connect:
        mock_connect.return_value.__enter__.return_value = mock_connection

        result = db.get_company("CCP")

    assert result == {
        "code": "CCP",
        "name": "Credit Corp Group",
        "exchange": "AX",
    }

def test_get_company_not_found():
    mock_connection = MagicMock()
    mock_result = MagicMock()

    mock_result.first.return_value = None
    mock_connection.execute.return_value = mock_result

    with patch("utils.db.engine.connect") as mock_connect:
        mock_connect.return_value.__enter__.return_value = mock_connection

        result = db.get_company("XYZ")

    assert result is None

def test_insert_company_success():
    company = {
        "code": "CCP",
        "name": "Credit Corp Group",
        "exchange": "AX",
        "active": True,
    }

    mock_connection = MagicMock()

    with (
        patch("utils.db.company_exists") as mock_exists,
        patch("utils.db.engine.begin") as mock_begin,
    ):
        mock_exists.return_value = False
        mock_begin.return_value.__enter__.return_value = mock_connection

        result = db.insert_company(company)

    assert result is True
    mock_connection.execute.assert_called_once()

def test_insert_company_duplicate():
    company = {
        "code": "CCP",
        "name": "Credit Corp Group",
        "exchange": "AX",
        "active": True,
    }

    with (
        patch("utils.db.company_exists") as mock_exists,
        patch("utils.db.engine.begin"),
    ):
        mock_exists.return_value = True

        result = db.insert_company(company)

    assert result is False

def test_get_last_prices():
    mock_connection = MagicMock()

    row_one = MagicMock()
    row_one.code = "CCP"
    row_one.close = 12.50

    row_two = MagicMock()
    row_two.code = "WBC"
    row_two.close = 35.20

    mock_connection.execute.return_value = [
        row_one,
        row_two,
    ]

    with patch("utils.db.engine.connect") as mock_connect:
        mock_connect.return_value.__enter__.return_value = mock_connection

        result = db.get_last_prices()

    assert result == {
        "CCP": 12.50,
        "WBC": 35.20,
    }

def test_get_exchange_success():
    mock_connection = MagicMock()
    mock_result = MagicMock()
    mock_row = MagicMock()

    mock_row.timezone = "Australia/Sydney"
    mock_row.blackout_start = "08:30"
    mock_row.blackout_end = "18:00"

    mock_result.first.return_value = mock_row
    mock_connection.execute.return_value = mock_result

    with patch("utils.db.engine.connect") as mock_connect:
        mock_connect.return_value.__enter__.return_value = mock_connection

        result = db.get_exchange("AX")

    assert result == {
        "timezone": "Australia/Sydney",
        "blackout_start": "08:30",
        "blackout_end": "18:00",
    }

def test_get_exchange_not_found():
    mock_connection = MagicMock()
    mock_result = MagicMock()

    mock_result.first.return_value = None
    mock_connection.execute.return_value = mock_result

    with patch("utils.db.engine.connect") as mock_connect:
        mock_connect.return_value.__enter__.return_value = mock_connection

        result = db.get_exchange("XX")

    assert result is None

def test_create_user_success():
    mock_connection = MagicMock()

    with (
        patch("utils.db.get_user_by_email") as mock_get_user,
        patch("utils.db.engine.begin") as mock_begin,
    ):
        mock_get_user.return_value = None
        mock_begin.return_value.__enter__.return_value = mock_connection

        result = db.create_user(
            "test@example.com",
            "fake-password-hash",
        )

    assert result is True
    mock_connection.execute.assert_called_once()

def test_create_user_duplicate():
    with (
        patch("utils.db.get_user_by_email") as mock_get_user,
        patch("utils.db.engine.begin"),
    ):
        mock_get_user.return_value = {
            "id": 1,
            "email": "test@example.com",
        }

        result = db.create_user(
            "test@example.com",
            "fake-password-hash",
        )

    assert result is False
