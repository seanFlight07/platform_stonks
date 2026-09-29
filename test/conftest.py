import os

os.environ.setdefault(
    "JWT_SECRET",
    "test-secret-key-for-platform-stonks"
)

import pandas as pd
import pytest
from datetime import time
from fastapi.testclient import TestClient

from web.main import app


@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def valid_price_data():
    return pd.DataFrame(
        {
            "open": [10.0],
            "high": [12.0],
            "low": [9.0],
            "close": [11.0],
            "change_dollar": [1.0],
            "change_pct": [10.0],
            "volume": [1000],
            "date": ["2026-09-29"],
            "code": ["CCP"],
        }
    )

@pytest.fixture
def exchange_info():
    return {
        "timezone": "Australia/Sydney",
        "blackout_start": time(8,30),
        "blackout_end":time(18,0),
    }


