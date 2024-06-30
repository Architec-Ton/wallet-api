from TonTools import TonCenterClient, LsClient, TonApiClient
from tonsdk.utils import Address

from .ton.ton_client import TonClient
from .ton_controller import TonController


class WalletController:

    def __init__(self):
        self.ton = TonController()

    async def get_jetton(self, jetton_master_address: Address, owner_address: Address):
        # TODO get from db or network
        jetton_wallet_address = await self.ton.get_jetton_wallet_address(
            jetton_master_address, owner_address
        )
        jetton_wallet = await self.ton.get_jetton_wallet(Address(jetton_wallet_address))
        return jetton_wallet

        "EQBTaitfymnhdz6fMQaN5LvvpETOE6Mn-A9rcCSSJpZ-PD2T"
