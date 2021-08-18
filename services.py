from datetime import date
from fastapi import HTTPException

currency_rates = {
    date(2021, 8, 2): {"USD": 73.1388, "EUR": 86.9913},
    date(2021, 8, 17): {"USD": 73.3920, "EUR": 86.5072},
}


async def get_currency_codes() -> list[str]:
    """Returns currency codes"""

    return ["USD", "EUR", ]


async def get_currency_rate(code: str, for_date: date) -> float:
    """Returns the currency rate relative to the RUB"""

    try:
        return currency_rates[for_date][code]
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid parameters")
