from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from integrations import api_fetcher
from utils import db, security, transforms, validation
from utils import logger as logger_utils
from web.models import (
    CompanyCreate,
    SearchCompany,
    UserCreate,
    UserLogin,
)

router = APIRouter()
logger = logger_utils.setup_logger(__name__)
bearer_scheme = HTTPBearer()
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
# Authentication functions
#############################################################
@router.post("/user/create-user", status_code=HTTP_201_CREATED)
def create_user(user: UserCreate):
    new_user = user.model_dump()
    user_exist = db.get_user_by_email(new_user["email"])

    if user_exist:
        logger.warning("User already exists")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="User already exists")
    
    password_hash = security.hash_password(new_user['password'])
    create_new_user = db.create_user(new_user['email'],password_hash)

    if create_new_user:
        return{ "detail": "New user successfully created"}


@router.post("/user/login")
def login(user: UserLogin):
    current_user = user.model_dump()
    user_exist = db.get_user_by_email(current_user["email"])
    
    if not user_exist:
        raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED,
                             detail="Invalid email or password"
                             )

    validate_password = security.verify_password(user_exist['password_hash'],current_user["password"])

    if not validate_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid email or passowrd"
                            )
    access_token = security.create_access_token(user_exist["id"])

    if not user_exist["active"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User account is disabled")

    return{
        "access_token": access_token,
        "token_type": "bearer"
    }

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
    ):
    token = credentials.credentials
    user_id = security.decode_access_token(token)

    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token")

    user = db.get_user_by_id(user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found")
    if not user["active"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail="User account is disabled")

    return user

def require_admin(
    current_user = Depends(get_current_user)
):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return current_user

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
def post_prices(code: str, current_user=Depends(require_admin)):
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
def load_company_and_data(code, exchange, current_user=Depends(require_admin)):
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

    # No blackout - insert immediately
    insert_data = db.insert_company(transformed_company)

    if not insert_data:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Company {code} already exists in db"
        )

    # Fetch historical prices
    price_data = api_fetcher.api_fetch_stock_history(code, exchange,blackout=black_out_validation)
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

