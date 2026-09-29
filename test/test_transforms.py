
import pandas as pd

from utils.transforms import (
    add_code,
    calculate_dollar_change,
    calculate_percentage_change,
    transform_api_data,
    transform_company,
)


def test_add_code():
    data = pd.DataFrame({"Close": [10.0]})

    result = add_code(data, "CCP")

    assert result["code"].iloc[0] == "CCP"

def test_dollar_change():
    data = pd.DataFrame(
        {
            "Close": [12.50, 8.00]
        }
    )

    last_close = 10.00

    result = calculate_dollar_change(data, last_close)

    assert result["change_dollar"].iloc[0] == 2.50
    assert result["change_dollar"].iloc[1] == -2.00

def test_percentage_change():
    data = pd.DataFrame(
        {
            "change_dollar": [2.50]
        }
    )
    
    last_close = 10.00
    result = calculate_percentage_change(data,last_close)

    assert result["change_pct"].iloc[0] == 25.00

def test_transform_company():
    data = {
            "code": "CCP",
            "long_name": "Credit Corp Group Limited",
            "exchange": "AX"
        }

    result = transform_company(data)

    assert result == {
        'code': "CCP",
        'name': "Credit Corp Group Limited",
        'exchange': "AX",
        'active': True
    }

def test_transform_api_data():
    data = pd.DataFrame(
        {
            "Open": [10.0],
            "High": [13.0],
            "Low": [9.0],
            "Close": [12.0],
            "Volume": [1000],
        },
        index=pd.to_datetime(["2026-09-29"]),
    )

    data.index.name = "Date"

    result = transform_api_data(
        data,
        code="CCP",
        last_close=10.0,
    )

    assert result["code"].iloc[0] == "CCP"
    assert result["open"].iloc[0] == 10.0
    assert result["high"].iloc[0] == 13.0
    assert result["low"].iloc[0] == 9.0
    assert result["close"].iloc[0] == 12.0
    assert result["volume"].iloc[0] == 1000
    assert result["change_dollar"].iloc[0] == 2.0
    assert result["change_pct"].iloc[0] == 20.0
