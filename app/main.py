from datetime import date

from fastapi import FastAPI, HTTPException, Query

from app.services import get_currency_codes, get_currency_rate

app = FastAPI()


@app.get("/currency_codes", response_model=list[str])
async def currency_codes():
    """Getting a list of all available currencies"""

    return await get_currency_codes()


@app.get("/currency_rates_diff", response_model=float)
async def currency_rates_diff(
        code: str = Query(..., regex=r"^[A-Z]{3}$", description="ISO currency code"),
        date1: date = Query(..., description="First date"),
        date2: date = Query(..., description="Second date")
):
    """Getting the difference in the currency rate between two dates"""

    if date1 < date2 and code in await get_currency_codes():
        diff = abs(await get_currency_rate(code, date1) - await get_currency_rate(code, date2))
        return diff
    raise HTTPException(status_code=400, detail="Invalid parameters")
