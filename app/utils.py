from typing import Optional
from urllib.parse import urlparse
from xml.etree import ElementTree
from asyncio import sleep

from aiohttp import ClientSession, ClientConnectionError
from fastapi import HTTPException

from app.config import NUMBER_OF_CONNECTION_ATTEMPTS


async def fetch_raw_data(url: str, params: dict[str, str] = None) -> str:
    async with ClientSession() as client:
        connected = False
        attempt = 0
        while not connected:
            try:
                async with client.get(url, params=params) as response:
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
    root = ElementTree.fromstring(raw_data)
    currency_codes = set()
    for elem in root.findall("Item/ISO_Char_Code"):
        code = elem.text
        if code is not None:
            currency_codes.add(code)
    return currency_codes


def parse_currency_rate(raw_data: str, code: str) -> Optional[str]:
    root = ElementTree.fromstring(raw_data)
    elem = root.find(f"Valute[CharCode='{code}']")
    if elem is not None:
        return elem.find("Value").text.replace(",", ".")
    return None
