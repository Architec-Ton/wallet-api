import logging

from tonsdk.utils import Address

from ..config import TON_CLIENT_API_URL
from ..view.transaction.history import HistoryItemOut
from .ton.ton_client import TonClient
from .ton_controller import TonController


class TransactionController:

    def __init__(self):
        self.client = TonClient()

    async def get_transactions(self, address: Address, limit=10) -> int | None:
        params = {"address": address.to_string(), "limit": limit}  # , "archival": 1}
        return await self.client.get_by_api("getTransactions", params=params)

    def processing_transaction(self, data):
        tx = {"utime": data["utime"]}
        if "out_msgs" in data and len(data["out_msgs"]) > 0:
            out_msg = data["out_msgs"][0]
            tx["type"] = "out"
            tx["address_from"] = out_msg["source"] if "source" in out_msg else None
            tx["address_to"] = out_msg["destination"] if "destination" in out_msg else None
            tx["status"] = True
            tx["value"] = int(out_msg["value"]) / (10**9) if "value" in out_msg else None
            tx["symbol"] = "TON"
        elif "in_msg" in data:
            in_msg = data["in_msg"]
            tx["type"] = "in"
            tx["address_from"] = in_msg["source"] if "source" in in_msg else None
            tx["address_to"] = in_msg["destination"] if "destination" in in_msg else None
            tx["status"] = True
            tx["value"] = int(in_msg["value"]) / (10**9) if "value" in in_msg else None
            tx["symbol"] = "TON"

        #
        # tx =  {
        #             "type" : "",
        #             "utime": "",
        #             "address_from": "",
        #             "address_to": "",
        #             "status": True,
        #             "value" : "",
        #             "symbol" "TON"
        #         }
        return [tx]

    async def get_trx(self, address: Address, limit=10):
        trx = await self.get_transactions(address, limit)
        logging.info(trx)
        # type: str
        # utime: int
        # address_from: str | None = Field(default=None, alias="from")
        # address_to: str | None = Field(default=None, alias="to")
        # status: bool
        # value: float | None = Field(default=None)
        # symbol: str | None = Field(default="TON")
        # comment: str | None = Field(default=None)

        transactions = []
        if trx:
            for tx in trx:
                logging.info(tx)
                tdata = self.processing_transaction(tx)
                transactions.extend(tdata)
        return transactions

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

    async def get_outcomig_trx(self, source: Address, destination: Address, lt: int) -> int | None:
        params = {
            "source": source.to_string(),
            "destination": destination.to_string(),
            "created_lt": lt,
        }
        trx = await self.client.get_by_api("tryLocateSourceTx", params=params)
        return trx

    # async def get_transaction(self, address: Address, limit: int = 3):
