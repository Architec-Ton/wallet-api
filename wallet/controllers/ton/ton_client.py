import logging

import aiohttp
from TonTools import TonCenterClient, TonApiClient

from wallet.config import (
    TON_CLIENT_API_URL,
    TON_CLIENT_API_URL_PREFIX,
    TON_CLIENT_API_GET_URL,
)


class TonClient:

    def __init__(self):
        self.tc_client = TonCenterClient(
            base_url="https://ton.architecton.site/",
            # base_url=f"{TON_CLIENT_API_URL}{TON_CLIENT_API_URL_PREFIX}/",
            key="88d5912ad2394e5cbae97a351bb6a3e1174e09f7956d096beaae3acab91324da",
        )
        # self.tc_client.base_url = f"{TON_CLIENT_API_URL}{TON_CLIENT_API_URL_PREFIX}/"
        # self.api_client = aiohttp.ClientSession(base_url=TON_CLIENT_API_URL)

    async def get_by_api(self, url: str, params=None):
        async with aiohttp.ClientSession(
            base_url="https://ton.architecton.site"
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
