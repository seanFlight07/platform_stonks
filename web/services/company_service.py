from utils import db
from integrations import api_fetcher

def get_company():
    return db.get_all_companies()

def create_company(company_data: dict) -> bool:
    inserted = db.insert_company(company_data)
    return inserted

def search_company(code: str, exchange: str):
    code = code.upper()
    exchange = exchange.upper()

    exchange_info = db.get_exchange(exchange)

    if exchange_info is None:
        return None, "unsupported_exchange"

    company_info = api_fetcher.api_search_company(
        code, exchange
    )

    if not company_info:
        return None, "company_not_found"

    company_info["timezone"] = exchange_info.get("timezone")

    return company_info, None
