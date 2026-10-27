from integrations import api_fetcher
from utils import db, transforms, validation
from web.repositories.company_repository import CompanyRepository
from web.services import price_service

company_repository = CompanyRepository()

def get_company():
    return company_repository.get_all_companies()

def create_company(company_data: dict) -> bool:
    inserted = company_repository.insert_company(company_data)
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

def onboard_company(code: str, exchange: str):
    code = code.upper()
    exchange = exchange.upper()

    # 1. Search for company and validate exchange
    company_info, error = search_company(code, exchange)

    if error:
        return None, error

    # 2. Transform company information
    transformed_company = transforms.transform_company(company_info)

    # 3. Retrieve exchange configuration
    exchange_info = db.get_exchange(exchange)

    # 4. Determine blackout status
    blackout = validation.is_black_out(exchange_info)

    # 5. Insert company
    inserted = create_company(transformed_company)

    if not inserted:
        return None, "company_exists"

    # 6. Load historical prices
    _, error = price_service.load_historical_prices(code,blackout=blackout)

    if error:
        return None, error

    return {
        "detail": f"Company {code} successfully inserted"
    }, None
