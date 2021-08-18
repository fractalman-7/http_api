from datetime import date

from fastapi import FastAPI, HTTPException

from services import get_currency_codes, get_currency_rate

app = FastAPI()


@app.get("/currency_codes")
async def currency_codes():
    return await get_currency_codes()


@app.get("/currency_rates_diff")
async def currency_rates_diff(code: str, date1: date, date2: date):
    if date1 <= date2 and code in await get_currency_codes():
        diff = abs(await get_currency_rate(code, date1) - await get_currency_rate(code, date2))
        return round(diff, 4)
    else:
        raise HTTPException(status_code=400, detail="Invalid parameters")
