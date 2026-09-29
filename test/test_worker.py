from unittest.mock import patch

import pandas as pd

from worker import api_worker


def test_worker_success(valid_price_data):
    raw_prices = pd.DataFrame({
        "Close": [12.50],
    })

    companies = [
        {
            "code": "CCP",
            "name": "Credit Corp Group",
            "exchange": "AX",
        }
    ]

    with (
        patch("worker.api_worker.db.get_active_companies") as mock_companies,
        patch("worker.api_worker.db.get_last_prices") as mock_last_prices,
        patch("worker.api_worker.api_fetcher.api_fetch_stock") as mock_fetch,
        patch("worker.api_worker.transforms.transform_api_data") as mock_transform,
        patch("worker.api_worker.validation.validation") as mock_validation,
        patch("worker.api_worker.db.insert_data") as mock_insert,
    ):
        mock_companies.return_value = companies
        mock_last_prices.return_value = {"CCP": 12.00}
        mock_fetch.return_value = raw_prices
        mock_transform.return_value = valid_price_data
        mock_validation.return_value = True

        api_worker.main()

    mock_insert.assert_called_once_with(valid_price_data)

def test_worker_skips_empty_api_data():
    companies = [
        {
            "code": "CCP",
            "name": "Credit Corp Group",
            "exchange": "AX",
        }
    ]

    with (
        patch("worker.api_worker.db.get_active_companies") as mock_companies,
        patch("worker.api_worker.db.get_last_prices") as mock_last_prices,
        patch("worker.api_worker.api_fetcher.api_fetch_stock") as mock_fetch,
        patch("worker.api_worker.db.insert_data") as mock_insert,
    ):
        mock_companies.return_value = companies
        mock_last_prices.return_value = {"CCP": 12.00}
        mock_fetch.return_value = pd.DataFrame()

        api_worker.main()

    mock_insert.assert_not_called()

def test_worker_skips_when_no_last_price():
    companies = [
        {
            "code": "CCP",
            "name": "Credit Corp Group",
            "exchange": "AX",
        }
    ]

    raw_prices = pd.DataFrame({
        "Close": [12.50],
    })

    with (
        patch("worker.api_worker.db.get_active_companies") as mock_companies,
        patch("worker.api_worker.db.get_last_prices") as mock_last_prices,
        patch("worker.api_worker.api_fetcher.api_fetch_stock") as mock_fetch,
        patch("worker.api_worker.db.insert_data") as mock_insert,
    ):
        mock_companies.return_value = companies
        mock_last_prices.return_value = {}
        mock_fetch.return_value = raw_prices

        api_worker.main()

    mock_insert.assert_not_called()

def test_worker_does_not_insert_invalid_data(valid_price_data):
    companies = [
        {
            "code": "CCP",
            "name": "Credit Corp Group",
            "exchange": "AX",
        }
    ]

    raw_prices = pd.DataFrame({
        "Close": [12.50],
    })

    with (
        patch("worker.api_worker.db.get_active_companies") as mock_companies,
        patch("worker.api_worker.db.get_last_prices") as mock_last_prices,
        patch("worker.api_worker.api_fetcher.api_fetch_stock") as mock_fetch,
        patch("worker.api_worker.transforms.transform_api_data") as mock_transform,
        patch("worker.api_worker.validation.validation") as mock_validation,
        patch("worker.api_worker.db.insert_data") as mock_insert,
    ):
        mock_companies.return_value = companies
        mock_last_prices.return_value = {"CCP": 12.00}
        mock_fetch.return_value = raw_prices
        mock_transform.return_value = valid_price_data
        mock_validation.return_value = False

        api_worker.main()

    mock_insert.assert_not_called()

def test_worker_continues_after_company_failure(valid_price_data):
    companies = [
        {
            "code": "CCP",
            "name": "Credit Corp Group",
            "exchange": "AX",
        },
        {
            "code": "WBC",
            "name": "Westpac",
            "exchange": "AX",
        },
    ]

    raw_prices = pd.DataFrame({
        "Close": [35.00],
    })

    with (
        patch("worker.api_worker.db.get_active_companies") as mock_companies,
        patch("worker.api_worker.db.get_last_prices") as mock_last_prices,
        patch("worker.api_worker.api_fetcher.api_fetch_stock") as mock_fetch,
        patch("worker.api_worker.transforms.transform_api_data") as mock_transform,
        patch("worker.api_worker.validation.validation") as mock_validation,
        patch("worker.api_worker.db.insert_data") as mock_insert,
    ):
        mock_companies.return_value = companies

        mock_last_prices.return_value = {
            "CCP": 12.00,
            "WBC": 34.00,
        }

        mock_fetch.side_effect = [
            Exception("API failure"),
            raw_prices,
        ]

        mock_transform.return_value = valid_price_data
        mock_validation.return_value = True

        api_worker.main()

    mock_insert.assert_called_once_with(valid_price_data)
