from worker import api_fetcher
from utils import db, transforms, validation,logger
logger = logger.setup_logger(__name__)

def main():
    companies = db.get_active_companies()
    last_prices = db.get_last_prices()
    successful = 0
    skipped = 0 
    failed = 0
    logger.info("Starting Worker | Processing %s of companies",len(companies))
    for company in companies:
        try:
            print(company["code"])
            prices = api_fetcher.api_fetch_stock(company["code"],company["exchange"])
            
            if prices.empty:
                skipped += 1
                continue

            last_price = last_prices.get(company["code"])
            
            if last_price is None:
                logger.warning("No preivous price was returned for %s",company["code"])
                failed += 1
                continue
            
            fetched_data = transforms.transform_api_data(prices,company["code"],last_price)

            if validation.validation(fetched_data):
                db.insert_data(fetched_data)
                successful += 1
            else:
                failed += 1
        except Exception:
            failed += 1
            logger.exception("Failed to process data for %s",company['code'])
    
    logger.info("Worker completed | Total: %s | Successful: %s | Skipped: %s | Failed: %s",
    len(companies),
    successful,
    skipped,
    failed
)

if __name__ == "__main__":
    main()
