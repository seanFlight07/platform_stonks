from fastapi import APIRouter, HTTPException, status
from utils import db, transforms, validation, logger
from web.models import CompanyCreate
from integrations import api_fetcher
router = APIRouter()
logger = logger.setup_logger(__name__)

@router.get("/health",status_code=status.HTTP_200_OK)
def health():
    if not db.check_db():
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Please contact admin")
    return {"status": "healthy"}



#############################################################
# Get functions                                             
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
# Post functions
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
        inserted = db.insert_data(data)
        return {
            "detail": f"Company {company["code"]} successfully inserted"
        }
    else:
        logger.warning("Failed validation for company %s",company['code'])
    logger.info("Historical upload completed")
