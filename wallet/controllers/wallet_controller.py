import asyncio
import logging
from typing import List, Optional

from TonTools import TonCenterClient, LsClient, TonApiClient
from tonsdk.utils import Address

from .ton.ton_client import TonClient
from .ton_controller import TonController
from ..models import JettonMaster, JettonWallet
from ..view.wallet.coin import CoinOut


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

        #  "EQBTaitfymnhdz6fMQaN5LvvpETOE6Mn-A9rcCSSJpZ-PD2T"

    async def get_wallets(
        self, owner_address: Address, include_symbols=None
    ) -> List[JettonWallet]:
        jettons, owner_wallets = await asyncio.gather(
            (
                JettonMaster.all()
                if include_symbols is None
                else JettonMaster.filter(symbol__in=include_symbols)
            ),
            JettonWallet.get_wallets(owner_address, include_symbols),
        )

        if len(jettons) != len(owner_wallets):
            for w in owner_wallets:
                await w.delete()
            owner_wallets = []
            for j in jettons:
                jetton_wallet_address = await self.ton.get_jetton_wallet_address(
                    j.address, owner_address
                )
                if jetton_wallet_address:
                    owner_wallet = await JettonWallet.new(
                        owner_address, Address(jetton_wallet_address), j
                    )
                    owner_wallets.append(owner_wallet)

        # jetton_wallet = await self.ton.get_jetton_wallet(Address(jetton_wallet_address))
        return owner_wallets

    async def get_assets(
        self,
        owner_address: Address,
        only_active=True,
        include_symbols: Optional[List[str]] = None,
    ) -> List[CoinOut]:
        if include_symbols is None or "TON" in include_symbols:
            balance, wallets = await asyncio.gather(
                TonController().get_balance(owner_address),
                self.get_wallets(owner_address, include_symbols=include_symbols),
            )
        else:
            wallets = await self.get_wallets(owner_address, include_symbols)

        assets_tsk = [self.ton.get_jetton_wallet(w.wallet_address) for w in wallets]

        assets_wallets = await asyncio.gather(*assets_tsk)

        for aw_idx, aw in enumerate(assets_wallets):
            if aw is not None:
                wallets[aw_idx].active = True
                wallets[aw_idx].balance = aw.balance
                if wallets[aw_idx].jetton.name == "BNK jetton":
                    wallets[aw_idx].usd_ratio = 0
                    wallets[aw_idx].change_ratio = 0
                wallets[aw_idx].wallet_code = aw.jetton_wallet_code
                await wallets[aw_idx].save()
            elif aw is None and wallets[aw_idx].active:
                wallets[aw_idx].active = False
                await wallets[aw_idx].save(update_fields="active")
        if only_active:
            coins = [CoinOut.model_validate(w) for w in wallets if w.active]
        else:
            coins = [CoinOut.model_validate(w) for w in wallets]

        if include_symbols is None or "TON" in include_symbols:
            ton_asset = CoinOut(
                type="ton",
                amount=balance,
                usd_price=balance * 7.44,
                change_price=0,
                meta={
                    "name": "TON",
                    "symbol": "TON",
                    "decimals": "9",
                    "image": "/wallet/images/symbols/ton.svg",
                    "description": "TON ",
                },
            )
            coins.insert(0, ton_asset)

        return coins
