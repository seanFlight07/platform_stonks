from worker import api_fetcher
from utils import db, transforms, validation,logger

logger = logger.setup_logger(__name__)

def main():
    companies = db.get_active_companies()
    last_prices = db.get_last_prices()
    for company in companies:
        try:
            print(company["code"])
            prices = api_fetcher.api_fetch_stock(company["code"],company["exchange"])
            last_price = last_prices.get(company["code"])
            fetched_data = transforms.transform_api_data(prices,company["code"],last_price)
        
            if validation.validation(fetched_data):
                db.insert_data(fetched_data)
        except Exception:
            logger.exception("Failed to process data for %s",company['code'])

if __name__ == "__main__":
    main()
