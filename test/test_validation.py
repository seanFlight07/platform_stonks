from datetime import datetime
from unittest.mock import patch
from zoneinfo import ZoneInfo

from utils.validation import is_black_out, validation

SYDNEY = ZoneInfo("Australia/Sydney")

def test_validation_valid_data(valid_price_data):

    result = validation(valid_price_data)

    assert result is True

def test_validation_missing_required_column_data(valid_price_data):
    data = valid_price_data.drop(columns=["change_dollar"])

    result = validation(data)

    assert result is False

def test_validation_extra_column_data(valid_price_data):
    valid_price_data["Extra_Column"] = ["extra column"]
    
    result = validation(valid_price_data)

    assert result is False

def test_validation_missing_value(valid_price_data):
    valid_price_data.loc[0,"low"] = None

    result = validation(valid_price_data)

    assert result is False

def test_blackout_during_weekday(exchange_info):
    fake_now = datetime(2026, 9, 30, 12, 0, tzinfo=SYDNEY)

    with patch("utils.validation.datetime") as mock_datetime:
        mock_datetime.now.return_value = fake_now

        result = is_black_out(exchange_info)

    assert result is True

def test_blackout_before_time_weekday(exchange_info):
    fake_now = datetime(2026, 9, 30, 7,0, tzinfo=SYDNEY)

    with patch("utils.validation.datetime") as mock_datetime:
        mock_datetime.now.return_value = fake_now

        result = is_black_out(exchange_info)

    assert result is False

def test_blackout_after_time_weekday(exchange_info):
    fake_now = datetime(2026, 9, 30, 23, 0, tzinfo=SYDNEY)

    with patch("utils.validation.datetime") as mock_datetime:
        mock_datetime.now.return_value = fake_now

        result = is_black_out(exchange_info)

        assert result is False

def test_blackout_weekend(exchange_info):
    fake_now = datetime(2026, 9, 26, 12, 0, tzinfo=SYDNEY)

    with patch("utils.validation.datetime") as mock_datetime:
        mock_datetime.now.return_value = fake_now

        result = is_black_out(exchange_info)

    assert result is False

def test_blackout_at_exact_start(exchange_info):
    fake_now = datetime(2026, 9, 30, 8, 30, tzinfo=SYDNEY)

    with patch("utils.validation.datetime") as mock_datetime:
        mock_datetime.now.return_value = fake_now

        result = is_black_out(exchange_info)

    assert result is True

def test_blackout_at_exact_end(exchange_info):
    fake_now = datetime(2026, 9, 30, 18, 0, tzinfo=SYDNEY)

    with patch("utils.validation.datetime") as mock_datetime:
        mock_datetime.now.return_value = fake_now

        result = is_black_out(exchange_info)

    assert result is True
