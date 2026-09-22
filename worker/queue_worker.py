from utils import db, validation, transforms
from integrations import api_fetcher
from utils.logger import setup_logger

logger = setup_logger(__name__)


def process_pending_jobs():
    jobs = db.get_pending_jobs()

    for job in jobs:
        try:
            job_id = job["id"]
            code = job["code"].upper()
            exchange = job["exchange"].upper()

            # Get exchange information
            exchange_info = db.get_exchange(exchange)

            if exchange_info is None:
                raise ValueError(f"Exchange {exchange} is not supported")

            # Check whether exchange is still in blackout
            blackout = validation.is_black_out(exchange_info)

            if blackout:
                logger.info("Job %s for %s.%s is still in blackout", job_id, code, exchange)
                continue

            # Get company information
            raw_company_data = api_fetcher.api_search_company(code, exchange)

            if not raw_company_data:
                raise ValueError(
                    f"No company data found for {code}.{exchange}"
                )

            # Transform and insert company
            transformed_company = transforms.transform_company(raw_company_data)

            company_inserted = db.insert_company(transformed_company)

            if not company_inserted:
                raise ValueError(
                    f"Company {code} could not be inserted"
                )

            # Fetch historical price data
            raw_price_data = api_fetcher.api_fetch_stock_history(code, exchange)

            if raw_price_data.empty:
                raise ValueError(
                    f"No historical data found for {code}.{exchange}"
                )

            # Transform historical price data
            transformed_price_data = transforms.transform_api_historical(raw_price_data, code)

            # Validate historical price data
            if not validation.validation(transformed_price_data):
                raise ValueError(
                    f"Historical data validation failed for {code}.{exchange}"
                )

            # Insert historical price data
            db.insert_data(transformed_price_data)

            # Job completed successfully, remove it from queue
            db.delete_pending_jobs(job_id)

            logger.info("Queue job %s for %s.%s completed successfully", job_id, code, exchange)

        except Exception:
            logger.exception(
                "Queue job %s failed",
                job["id"]
            )

            db.queue_job_failed(job["id"])
