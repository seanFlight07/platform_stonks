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

class PriceCreate(BaseModel):
    code: str
    date: date
    open: float
    high: float
    low: float
    close: float
    change_dollar: float
    change_pct: float
    volume: int

