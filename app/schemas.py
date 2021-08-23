from pydantic import BaseModel


class CurrencyRateDifferenceModel(BaseModel):
    rate1: float
    rate2: float
    diff: float

