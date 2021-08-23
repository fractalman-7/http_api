from datetime import date

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from app import config
from app.services import get_currency_codes, get_currency_rate
from app.utils import http_client
from app.schemas import CurrencyRateDifferenceModel

app = FastAPI(title=config.PROJECT_NAME, debug=config.DEBUG, version=config.VERSION)
app.add_middleware(CORSMiddleware, allow_origins=config.ALLOWED_HOSTS)


@app.on_event("startup")
async def startup():
    await http_client.open_session()


@app.on_event("shutdown")
async def shutdown():
    await http_client.close_session()


@app.get("/", response_class=HTMLResponse)
async def main():
    html_content = f"""
    <html>
        <head>
            <title>{config.PROJECT_NAME}</title>
        </head>
        <body>
            <h1>{config.PROJECT_NAME} {config.VERSION}</h1>
            <h2>See <a href="/docs">documentation</a></h2>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/currency_codes", response_model=list[str])
async def currency_codes():
    """Getting a list of all available currencies"""

    return await get_currency_codes()


@app.get("/currency_rate_diff", response_model=CurrencyRateDifferenceModel)
async def currency_rate_difference(
        code: str = Query(..., regex=r"^[A-Z]{3}$", description="ISO currency code"),
        date1: date = Query(..., description="First date"),
        date2: date = Query(..., description="Second date")
):
    """Returns exchange rates for two dates and their difference"""

    if date1 < date2 and code in await get_currency_codes():
        rate1 = await get_currency_rate(code, date1)
        rate2 = await get_currency_rate(code, date2)
        diff = abs(rate1 - rate2)
        return CurrencyRateDifferenceModel(rate1=rate1, rate2=rate2, diff=diff)
    raise HTTPException(status_code=400, detail="Invalid parameters")
