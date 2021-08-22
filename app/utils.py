from asyncio import sleep
from typing import Optional
from urllib.parse import urlparse
from xml.etree import ElementTree

from aiohttp import ClientSession, ClientConnectionError
from fastapi import HTTPException

from app.config import NUMBER_OF_CONNECTION_ATTEMPTS

http_client = ClientSession()


async def fetch_raw_data(url: str, params: dict[str, str] = None) -> str:
    """Receiving raw data from external api, if connection is not established, reconnection occurs"""

    connected = False
    attempt = 0
    while not connected:
        try:
            async with http_client.get(url, params=params) as response:
                connected = True
                return await response.text()
        except ClientConnectionError:
            attempt += 1
        if attempt > NUMBER_OF_CONNECTION_ATTEMPTS:
            break
        await sleep(0.3)
    hostname = urlparse(url).hostname
    raise HTTPException(400, f"Failed to connection with {hostname}")


def parse_currency_codes(raw_data: str) -> set[str]:
    """Retrieves currency codes from xml"""

    root = ElementTree.fromstring(raw_data)
    currency_codes = set()
    for elem in root.findall("Item/ISO_Char_Code"):
        code = elem.text
        if code is not None:
            currency_codes.add(code)
    return currency_codes


def parse_currency_rate(raw_data: str, code: str) -> Optional[str]:
    """Retrieves currency rate from xml"""

    root = ElementTree.fromstring(raw_data)
    elem = root.find(f"Valute[CharCode='{code}']")
    if elem is not None:
        return elem.find("Value").text.replace(",", ".")
    return None
