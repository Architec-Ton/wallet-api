import logging

from tonsdk.utils import Address

from .ton.ton_client import TonClient
from .ton_controller import TonController
from ..config import TON_CLIENT_API_URL


class TransactionController:

    def __init__(self):
        self.client = TonClient()

    async def get_transactions(self, address: Address, limit=10) -> int | None:
        params = {"address": address.to_string(), "limit": limit, "archival": 1}
        return await self.client.get_by_api("getTransactions", params=params)

    async def get_outcoming_last_lt(self, address: Address) -> int | None:
        # TODO: take from DB in future
        params = {"address": address.to_string(), "limit": 10, "archival": 1}
        trxs = await self.client.get_by_api("getTransactions", params=params)
        last_lt = None
        if trxs:
            for trx in trxs:
                logging.info(trx)
                if trx["@type"] == "raw.transaction":
                    if len(trx["out_msgs"]) > 0:
                        if "in_msg" in trx and last_lt is None:
                            last_lt = trx["out_msgs"][0]["created_lt"]
                            return last_lt

    async def get_outcomig_trx(
        self, source: Address, destination: Address, lt: int
    ) -> int | None:
        params = {
            "source": source.to_string(),
            "destination": destination.to_string(),
            "created_lt": lt,
        }
        trx = await self.client.get_by_api("tryLocateSourceTx", params=params)
        return trx

    # async def get_transaction(self, address: Address, limit: int = 3):
