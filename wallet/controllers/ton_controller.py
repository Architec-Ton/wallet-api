from TonTools import TonCenterClient, LsClient, TonApiClient
from tonsdk.utils import Address

from .ton.ton_client import TonClient

client = TonClient()


class TonController:

    def __init__(self):
        self.ton_client = client

    async def get_balance(self, address: Address):
        balance = await self.ton_client.tc_client.get_balance(address.to_string())
        if balance is not None:
            return balance / (10**9)

    async def get_transactions(self, address: Address, limit: int = 3):
        transactions = await self.ton_client.tc_client.get_transactions(
            address.to_string(), limit
        )
        return transactions
