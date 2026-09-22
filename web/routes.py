from fastapi import APIRouter, HTTPException, status
from requests import post, status_codes
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from utils import db, transforms, validation 
from utils import logger as logger_utils
from web.models import CompanyCreate, LoadCompanyData, SearchCompany
from integrations import api_fetcher

router = APIRouter()
logger = logger_utils.setup_logger(__name__)
#############################################################
# Health check
#############################################################
@router.get("/health",status_code=status.HTTP_200_OK)
def health():
    if not db.check_db():
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Please contact admin")
    return {"status": "healthy"}



#############################################################
# Get functions from DB                                             
#############################################################
@router.get("/companies")
def get_companies():
    companies = db.get_all_companies()
    if not companies:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="No companies found")
    return companies

@router.get("/companies/{code}/prices")
def get_price(code: str):
    return db.get_prices(code)

#############################################################
# Post functions to DB
#############################################################
@router.post("/companies",status_code=status.HTTP_201_CREATED)
#post the company data to send to the db.
def post_company(company: CompanyCreate):
    company_data = company.model_dump()
    inserted = db.insert_company(company_data)
    if inserted:
        return {
            "detail": f"Company {company.code} successfully inserted"
        }
    
    raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Company {company.code} already exists in db")

@router.post("/companies/{code}/prices", status_code=status.HTTP_201_CREATED)
def post_prices(code: str):
    company = db.get_company(code)
    if company is None:
        logger.warning("Company %s does not exist in db", code)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company {code} does not exist")
    logger.info("Starting historical data insert for company %s",company["code"])
    data = api_fetcher.api_fetch_stock_history(company["code"],company['exchange']) 
    data = transforms.transform_api_historical(data,company["code"])
    if validation.validation(data):
        db.insert_data(data)
        return {
            "detail": f"Company {company["code"]} successfully inserted"
        }
    else:
        logger.warning("Failed validation for company %s",company['code'])
    logger.info("Historical upload completed")


@router.post("/companies/load/", status_code=HTTP_201_CREATED)
def load_company_and_data(code, exchange):
    code = code.upper()
    exchange = exchange.upper()

    # Check company exists in yfinance
    raw_company_data = api_fetcher.api_search_company(code, exchange)

    if not raw_company_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company {code}.{exchange} not found"
        )

    # Convert yfinance company data to our database format
    transformed_company = transforms.transform_company(raw_company_data)

    # Get exchange configuration
    exchange_info = db.get_exchange(exchange)

    if exchange_info is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Exchange {exchange} is not supported"
        )

    # Check whether we can ingest now
    black_out_validation = validation.is_black_out(exchange_info)

    if black_out_validation:
        queued = db.insert_into_queue(code, exchange)

        if not queued:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Company {code}.{exchange} could not be queued"
            )

        return {
            "detail": f"Company {code}.{exchange} has been queued"
        }

    # No blackout - insert immediately
    insert_data = db.insert_company(transformed_company)

    if not insert_data:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Company {code} already exists in db"
        )

    # Fetch historical prices
    price_data = api_fetcher.api_fetch_stock_history(code, exchange)
    price_data = transforms.transform_api_historical(price_data, code)

    if not validation.validation(price_data):
        logger.warning(
            "Failed validation for company %s",
            code
        )

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Historical data for {code} failed validation"
        )

    # Insert historical prices
    db.insert_data(price_data)

    return {
        "detail": f"Company {code} successfully inserted"
    }



#############################################################
# GET functions from yfinance
#############################################################
@router.get("/companie-search/{code}.{exchange}", response_model=SearchCompany)
def search_company(code, exchange):
    code = code.upper()
    exchange = exchange.upper()
    company_info = api_fetcher.api_search_company(code,exchange)
    exchange_info = db.get_exchange(exchange)
    if company_info is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail=f"Company {code}.{exchange} not found")
    
    if exchange_info is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail=f"Exchange {exchange} is not supported")


    company_info["timezone"] = exchange_info.get("timezone")

    return company_info

