
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from starlette.status import HTTP_201_CREATED

from utils import db
from utils import logger as logger_utils
from web.dependencies.auth import get_current_user, require_admin
from web.models import (
    CompanyCreate,
    SearchCompany,
    UserCreate,
    UserLogin,
)
from web.services import auth_service, company_service, price_service

router = APIRouter()
logger = logger_utils.setup_logger(__name__)
bearer_scheme = HTTPBearer()
#############################################################
# Health aheck
#############################################################
@router.get("/health",status_code=status.HTTP_200_OK)
def health():
    if not db.check_db():
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Please contact admin")
    return {"status": "healthy"}


#############################################################
# Authentication functions
#############################################################
@router.post("/user/create-user", status_code=HTTP_201_CREATED)
def create_user(user: UserCreate):
    result, error = auth_service.create_user(user.email, user.password)

    if error == "user_exists":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="User already exists")

    if error == "create_failed":
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Unable to create user")

    return result

@router.post("/user/login")
def login(user: UserLogin):
    result , error = auth_service.login_user(user.email, user.password)

    if error == "invalid_credentials":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid email or password")

    if error == "account_disabled":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User account is disabled")

    return result

@router.get("/user/me")
def get_me(current_user = Depends(get_current_user)):
    return {
        "id": current_user["id"],
        "email": current_user["email"],
        "role": current_user["role"]
    }

#############################################################
# Get functions from DB                                             
#############################################################
@router.get("/companies")
def get_companies():
    return company_service.get_company()

@router.get("/companies/{code}/prices")
def get_price(code: str):
    return price_service.get_prices(code)

#############################################################
# Post functions to DB
#############################################################
@router.post("/companies",status_code=status.HTTP_201_CREATED)
#post the company data to send to the db.
def post_company(company: CompanyCreate):
    company_data = company.model_dump()
    inserted = company_service.create_company(company_data)
    if inserted:
        return {
            "detail": f"Company {company.code} successfully inserted"
        }
    
    raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Company {company.code} already exists in db")

@router.post("/companies/{code}/prices", status_code=status.HTTP_201_CREATED)
def post_prices(code: str, current_user=Depends(require_admin)):
    company, error = price_service.load_historical_prices(code)

    if error == "company_not_found":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Company {code} does not exist")

    if error == "validation_failed":
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                            detail=f"Histroical data for {code} failed validation")

    return {
        "detail": f"Company {company['code']} successfully inserted"
    }

@router.post("/companies/load/", status_code=HTTP_201_CREATED)
def load_company_and_data(code, exchange, current_user=Depends(require_admin)):
    result, error = company_service.onboard_company(code, exchange)

    if error == "unsupported_exchange":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Exchange {exchange.upper()} not supported")

    if error == "company_exists":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Company {code.upper()} alread exists in db")

    if error == "validation_failed":
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                            detail=f"Histroical data for {code.upper()} failed validation")

    return result



#############################################################
# GET functions from yfinance
#############################################################
@router.get("/company-search/{code}.{exchange}", response_model=SearchCompany)
def search_company(code, exchange):
    company_info, error = company_service.search_company(code, exchange)

    if error == "unsupported_exchange":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Exchange {exchange.upper()} is not supported")

    if error == "company_not_found":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Company {code.upper()}.{exchange.upper()} not found")

    return company_info
