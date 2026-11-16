from datetime import UTC, datetime

import pandas as pd
import yfinance as yf

from utils.logger import setup_logger

logger = setup_logger(__name__)


class YahooFinanceClient:

    def __init__(self):
        self.provider = "yfinance"

    

    def get_price_history(self, ticker: str, exchange: str, period: str = "2y", blackout: bool = False,) -> pd.DataFrame:

        ticker = ticker.upper()
        exchange = exchange.upper()
        unique_code = f"{ticker}.{exchange}"

        try:
            if blackout:
                data = yf.download(
                    tickers=unique_code,
                    period=period,
                    end=datetime.now(UTC).date(),
                )
            else:
                data = yf.download(
                    tickers=unique_code,
                    period=period,
                )

            if data is None or data.empty:
                logger.warning(
                    "No price data returned for %s",
                    unique_code,
                )
                return pd.DataFrame()

            logger.info(
                "Price data fetched for %s",
                unique_code,
            )

            return data

        except Exception:
            logger.exception(
                "Failed to fetch prices for %s",
                unique_code,
            )
            raise

    def get_company_info(self, ticker: str, exchange: str,) -> dict:

        ticker = ticker.upper()
        exchange = exchange.upper()
        unique_code = f"{ticker}.{exchange}"

        try:
            data = yf.Ticker(unique_code).info

            if not data or not data.get("symbol"):
                logger.warning(
                    "No company information returned for %s",
                    unique_code,
                )
                return {}

            return {
                "code": ticker,
                "exchange": exchange,
                "sector": data.get("sector"),
                "long_name": data.get("longName"),
                "previous_close": data.get("previousClose"),
                "open": data.get("open"),
                "day_low": data.get("dayLow"),
                "day_high": data.get("dayHigh"),
            }

        except Exception:
            logger.exception(
                "Failed to fetch company information for %s",
                unique_code,
            )
            raise
