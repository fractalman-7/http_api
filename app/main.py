from datetime import date

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from app import config
from app.services import get_currency_codes, get_currency_rate
from app.utils import http_client

app = FastAPI(title=config.PROJECT_NAME, debug=config.DEBUG, version=config.VERSION)
app.add_middleware(CORSMiddleware, allow_origins=config.ALLOWED_HOSTS)


@app.on_event("shutdown")
async def shutdown():
    await http_client.close()


@app.get("/")
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
