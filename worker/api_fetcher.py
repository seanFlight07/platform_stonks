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
    return data
