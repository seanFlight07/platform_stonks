from integrations import api_fetcher
from utils import db, transforms, validation
from utils import logger as logger_utils

logger = logger_utils.setup_logger(__name__)

def get_prices(code: str):
    return db.get_prices(code)

def load_historical_prices(code: str, blackout: bool = False):
    company = db.get_company(code)

    if company is None:
        return None, "company_not_found"

    logger.info(
        "Starting historical data insert for company %s",
        company["code"]
    )

    data = api_fetcher.api_fetch_stock_history(
        company["code"],
        company["exchange"],
        blackout=blackout
    )

    data = transforms.transform_api_historical(
        data,
        company["code"]
    )

    if not validation.validation(data):
        logger.warning(
            "Failed validation for company %s",
            company["code"]
        )
        return None, "validation_failed"

    db.insert_data(data)

    logger.info(
        "Historical upload completed for %s",
        company["code"]
    )

    return company, None
