import os
from dotenv import load_dotenv
from pydantic import BaseModel
import aiohttp

load_dotenv()

SECRET_AUTH = os.environ.get("SECRET_AUTH")

SECRET_SYSTEM = os.environ.get("SECRET_SYSTEM")

URL = os.environ.get("URL")


class Settings(BaseModel):
    authjwt_secret_key: str = SECRET_AUTH
    authjwt_algorithm: str = "HS256"
    authjwt_access_token_expires: int = 60 * 60 * 72  # default 15 minute
    authjwt_refresh_token_expires: int = 31000000  # default 30 days


async def fetch_data(route, method, **params):
    async with aiohttp.ClientSession() as session:
        if method == "GET":
            async with session.get(
                    f"{URL}/{route}",
                    **params
            ) as response:
                if response.status == 200:
                    return await response.json()
        elif method == "POST":
            async with session.post(
                    f"{URL}/{route}",
                    **params
            ) as response:
                if response.status == 200:
                    return await response.json()
