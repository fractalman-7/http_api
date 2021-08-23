from datetime import date
from decimal import Decimal

from fastapi import HTTPException

from app.config import CURRENCY_CODES_URL, CURRENCY_RATES_URL
from app.utils import fetch_raw_data, parse_currency_codes, parse_currency_rate


async def get_currency_codes() -> set[str]:
    """Returns currency codes"""

    raw_xml = await fetch_raw_data(CURRENCY_CODES_URL)
    currency_codes = parse_currency_codes(raw_xml)
    return currency_codes


async def get_currency_rate(code: str, for_date: date) -> Decimal:
    """Returns the currency rate relative to the RUB"""

    formatted_date = for_date.strftime("%d/%m/%Y")
    raw_xml = await fetch_raw_data(CURRENCY_RATES_URL, params={"date_req": formatted_date})

    rate = parse_currency_rate(raw_xml, code)
    if rate is None:
        formatted_date = for_date.strftime("%d.%m.%Y")
        raise HTTPException(status_code=400, detail=f"No data on currency {code} for {formatted_date}")
    return Decimal(rate)
