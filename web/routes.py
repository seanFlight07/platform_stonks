from fastapi import APIRouter, HTTPException, status
from utils import db
from web.models import CompanyCreate

router = APIRouter()

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

@router.post("/companies/{code}/prices")
#need to get the company and the data to send the data
def post_prices(code: str):
    new_prices = db.upload_data(code)
    return new_prices

