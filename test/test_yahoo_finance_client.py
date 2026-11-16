from datetime import date
from unittest.mock import patch

import pandas as pd
import pytest

from web.clients.yahoo_finance_client import YahooFinanceClient


@pytest.fixture
def client():
    return YahooFinanceClient()


@pytest.fixture
def sample_prices():
    return pd.DataFrame({
        "Open": [100.0, 102.0],
        "High": [105.0, 106.0],
        "Low": [99.0, 101.0],
        "Close": [103.0, 104.0],
        "Volume": [1000, 1500],
    })


@pytest.fixture
def sample_company():
    return {
        "symbol": "BHP.AX",
        "sector": "Basic Materials",
        "longName": "BHP Group Limited",
        "previousClose": 45.50,
        "open": 46.00,
        "dayLow": 45.20,
        "dayHigh": 46.80,
    }


# --------------------------------------------------
# Price history tests
# --------------------------------------------------

@patch("web.clients.yahoo_finance_client.yf.download")
def test_get_price_history_success(
    mock_download, client, sample_prices
):
    mock_download.return_value = sample_prices

    result = client.get_price_history(
        "bhp", "ax", period="2y"
    )

    pd.testing.assert_frame_equal(result, sample_prices)

    mock_download.assert_called_once_with(
        tickers="BHP.AX",
        period="2y",
    )


@patch("web.clients.yahoo_finance_client.yf.download")
def test_get_latest_price(
    mock_download, client, sample_prices
):
    mock_download.return_value = sample_prices

    result = client.get_price_history(
        "BHP", "AX", period="1d"
    )

    assert not result.empty

    mock_download.assert_called_once_with(
        tickers="BHP.AX",
        period="1d",
    )


@patch("web.clients.yahoo_finance_client.yf.download")
@patch("web.clients.yahoo_finance_client.datetime")
def test_get_price_history_blackout(
    mock_datetime, mock_download, client, sample_prices
):
    mock_datetime.now.return_value.date.return_value = (
        date(2026, 11, 16)
    )
    mock_download.return_value = sample_prices

    result = client.get_price_history(
        "BHP", "AX", period="2y", blackout=True
    )

    assert not result.empty

    mock_download.assert_called_once_with(
        tickers="BHP.AX",
        period="2y",
        end=date(2026, 11, 16),
    )


@patch("web.clients.yahoo_finance_client.yf.download")
def test_get_price_history_empty(
    mock_download, client
):
    mock_download.return_value = pd.DataFrame()

    result = client.get_price_history("BHP", "AX")

    assert isinstance(result, pd.DataFrame)
    assert result.empty


@patch("web.clients.yahoo_finance_client.yf.download")
def test_get_price_history_none(
    mock_download, client
):
    mock_download.return_value = None

    result = client.get_price_history("BHP", "AX")

    assert isinstance(result, pd.DataFrame)
    assert result.empty


@patch("web.clients.yahoo_finance_client.yf.download")
def test_get_price_history_exception(
    mock_download, client
):
    mock_download.side_effect = RuntimeError(
        "Yahoo Finance unavailable"
    )

    with pytest.raises(
        RuntimeError,
        match="Yahoo Finance unavailable",
    ):
        client.get_price_history("BHP", "AX")


# --------------------------------------------------
# Company information tests
# --------------------------------------------------

@patch("web.clients.yahoo_finance_client.yf.Ticker")
def test_get_company_info_success(
    mock_ticker, client, sample_company
):
    mock_ticker.return_value.info = sample_company

    result = client.get_company_info("bhp", "ax")

    assert result == {
        "code": "BHP",
        "exchange": "AX",
        "sector": "Basic Materials",
        "long_name": "BHP Group Limited",
        "previous_close": 45.50,
        "open": 46.00,
        "day_low": 45.20,
        "day_high": 46.80,
    }

    mock_ticker.assert_called_once_with("BHP.AX")


@patch("web.clients.yahoo_finance_client.yf.Ticker")
def test_get_company_info_empty(
    mock_ticker, client
):
    mock_ticker.return_value.info = {}

    result = client.get_company_info("INVALID", "AX")

    assert result == {}


@patch("web.clients.yahoo_finance_client.yf.Ticker")
def test_get_company_info_missing_symbol(
    mock_ticker, client
):
    mock_ticker.return_value.info = {
        "longName": "Unknown Company"
    }

    result = client.get_company_info("INVALID", "AX")

    assert result == {}


@patch("web.clients.yahoo_finance_client.yf.Ticker")
def test_get_company_info_exception(
    mock_ticker, client
):
    mock_ticker.side_effect = RuntimeError(
        "Company lookup failed"
    )

    with pytest.raises(
        RuntimeError,
        match="Company lookup failed",
    ):
        client.get_company_info("BHP", "AX")
