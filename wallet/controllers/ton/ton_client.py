import aiohttp
from TonTools import TonCenterClient

from wallet.config import (
    TON_CLIENT_API_GET_URL, TON_CLIENT_API_KEY,
)


class TonClient:

    def __init__(self):
        self.tc_client = TonCenterClient(
            base_url=TON_CLIENT_API_GET_URL,
            # base_url=f"{TON_CLIENT_API_URL}{TON_CLIENT_API_URL_PREFIX}/",
            key=TON_CLIENT_API_KEY,
        )
        # self.tc_client.base_url = f"{TON_CLIENT_API_URL}{TON_CLIENT_API_URL_PREFIX}/"
        # self.api_client = aiohttp.ClientSession(base_url=TON_CLIENT_API_URL)

    async def get_by_api(self, url: str, params=None):
        async with aiohttp.ClientSession(
            base_url=TON_CLIENT_API_GET_URL
        ) as session:
            # params = {"address": address, "limit": 3, "archival": 1}
            response = await session.get(url=f"/{url}", params=params)
            data_income = await response.json()
            # logging.info(data_income)
            if "ok" in data_income:
                if not data_income["ok"]:
                    return
            if "result" in data_income:
                return data_income["result"]
