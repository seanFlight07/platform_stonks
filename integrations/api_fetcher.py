from enum import unique
from datetime import date
from pandas.core.base import ensure_wrapped_if_datetimelike
from sqlalchemy.engine import result
import yfinance as yf
from utils.logger import setup_logger

logger = setup_logger(__name__)

def api_fetch_stock(ticker, exchange):
    unique_code = str(ticker+"."+exchange)
    try:
        data = yf.download(unique_code,period='1d')
        if data.empty:
            logger.warning("No data was pulled back for %s", unique_code)
            return data
        logger.info("Data has been fetched for %s", unique_code)
    except Exception:
        logger.exception("Failed to get any data from yfinance for %s",unique_code)
        raise
    return data

def api_fetch_stock_history(ticker, exchange, blackout=False):
    unique_code = str(ticker+"."+exchange)
    try:
        if blackout:
            data= yf.download(unique_code, period='2y', end=date.today())
        else:
            data = yf.download(unique_code,period='2y')

        if data.empty:
            logger.warning("No data was pulled back for %s", unique_code)
            return data
        logger.info("Data has been fetched for %s", unique_code)
    except Exception:
        logger.exception("Failed to get any data from yfinance for %s",unique_code)
        raise
    return data


def api_search_company(code,exchange):
    company_info = {}
    code, exchange = code.upper(), exchange.upper()
    unique_code = str(code+"."+exchange)
    try:
        data = yf.Ticker(unique_code)
        data = data.info
        if not data or not data.get("symbol"):
            logger.warning("No valid company returned for %s",unique_code)
            return data
        company_info["code"] = code
        company_info["exchange"] = exchange
        company_info["sector"] = data.get("sector")
        company_info["long_name"] = data.get("longName")
        company_info["previous_close"] = data.get("previousClose")
        company_info["open"] = data.get("open")
        company_info["day_low"] = data.get("dayLow")
        company_info["day_high"] = data.get("dayHigh")
    except Exception:
        logger.exception("failed to get any data from yfinance for %s",unique_code)
        raise
    return company_info

