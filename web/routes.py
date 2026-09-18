from fastapi import APIRouter
from utils import db
from web.models import CompanyCreate

router = APIRouter()


@router.get("/companies")
def get_companies():
    companies = db.get_all_companies()
    return companies

@router.get("/companies/{code}/prices")
def get_price(code: str):
    return db.get_prices(code)


@router.post("/companies")
#post the company data to send to the db.
def post_company(company: CompanyCreate):
    company_data = company.model_dump()
    inserted = db.insert_company(company_data)
    if inserted:
        return "success"
    else:
        return"failed"

@router.post("/companies/{code}/prices")
#need to get the company and the data to send the data
def post_prices(code: str):
    new_prices = db.upload_data(code)
    return new_prices

