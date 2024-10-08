import logging

from tonsdk.utils import Address
from TonTools.Providers.TonCenterClient import GetMethodError

from .ton.ton_client import TonClient

client = TonClient()


class TonController:
    def __init__(self):
        self.ton_client = client

    async def get_balance(self, address: Address):
        try:
            balance = await self.ton_client.tc_client.get_balance(address.to_string())
            if balance is not None:
                return balance / (10**9)
        except BaseException as error:
            logging.exception(error)

    async def get_jetton_wallet_address(self, master_address: Address, address: Address):
        address = await self.ton_client.tc_client.get_jetton_wallet_address(
            master_address.to_string(), address.to_string()
        )
        return address

    async def get_jetton_wallet(self, address: Address):
        try:
            jetton_wallet = await self.ton_client.tc_client.get_jetton_wallet(address.to_string())
            return jetton_wallet
        except GetMethodError as e:
            logging.error(f"Error getting jetton wallet data for address {address=}: {e=}")
            return None
        except Exception as e:
            logging.error(f"Error getting jetton wallet data for address {address=}: {e=}")
            return None

    async def get_jetton_data(self, master_address: Address):
        return await self.ton_client.tc_client.get_jetton_data(master_address.to_string())

    async def get_transactions(self, address: Address, limit: int = 3):
        try:
            transactions = await self.ton_client.tc_client.get_transactions(
                address.to_string(is_user_friendly=True), limit
            )
        except BaseException as e:
            logging.exception(e)
            return []

        trx = [t.to_dict_user_friendly() for t in transactions]
        return trx

    async def get_wallet_info(self, address: Address):
        try:
            wallet_info = await self.ton_client.get_by_api(
                "getAddressInformation", {"address": address.to_string(is_user_friendly=True)}
            )
        except BaseException as e:
            logging.exception(e)
            return []

        return wallet_info
