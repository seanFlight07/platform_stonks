from pydantic import BaseModel


class CompanyCreate(BaseModel):
    code: str
    name: str
    exchange: str
    active: bool

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
