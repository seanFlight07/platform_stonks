from pydantic import BaseModel, field_validator

class CompanyCreate(BaseModel):
    code: str
    name: str
    exchange: str
    active: bool

    @field_validator("code", "exchange")
    @classmethod
    def uppercase_fields(cls, value):
        return value.upper()

class SearchCompany(BaseModel):
    code: str
    exchange: str
    sector: str
    long_name: str
    previous_close: float
    open: float
    day_low: float
    day_high: float
    timezone: str

    @field_validator("code","exchange")
    @classmethod
    def uppercase_fields(cls, value):
        return value.upper()



