import asyncio
import datetime
import logging
from typing import List, Optional

from tonsdk.utils import Address

from ..config import TON_CLIENT_NETWORK
from ..models import JettonMaster, JettonWallet, Wallet
from ..models.wallet.wallet_code import WalletCode
from ..view.wallet.coin import CoinOut
from .ton_controller import TonController


class WalletController:
    def __init__(self):
        self.ton = TonController()

    async def get_jetton(self, jetton_master_address: Address, owner_address: Address):
        # TODO get from db or network
        jetton_wallet_address = await self.ton.get_jetton_wallet_address(jetton_master_address, owner_address)
        jetton_wallet = await self.ton.get_jetton_wallet(Address(jetton_wallet_address))
        return jetton_wallet

        #  "EQBTaitfymnhdz6fMQaN5LvvpETOE6Mn-A9rcCSSJpZ-PD2T"

    async def get_wallets(self, owner_address: Address, include_symbols=None) -> List[JettonWallet]:
        jettons, owner_wallets = await asyncio.gather(
            (JettonMaster.all() if include_symbols is None else JettonMaster.filter(symbol__in=include_symbols)),
            JettonWallet.get_wallets(owner_address, include_symbols),
        )

        if len(jettons) != len(owner_wallets):
            for w in owner_wallets:
                await w.delete()
            owner_wallets = []
            for j in jettons:
                jetton_wallet_address = await self.ton.get_jetton_wallet_address(j.address, owner_address)
                if jetton_wallet_address:
                    owner_wallet = await JettonWallet.new(owner_address, Address(jetton_wallet_address), j)
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
                logging.info(aw)
                wallets[aw_idx].active = True
                wallets[aw_idx].balance = aw.balance / (10 ** wallets[aw_idx].decimals)
                if wallets[aw_idx].balance is None or wallets[aw_idx].balance == 0:
                    wallets[aw_idx].active = False
                if wallets[aw_idx].jetton.name == "BNK jetton":
                    wallets[aw_idx].usd_ratio = 0
                    wallets[aw_idx].change_ratio = 0
                wallets[aw_idx].wallet_code = aw.jetton_wallet_code
                await wallets[aw_idx].save()
            elif aw is None and wallets[aw_idx].active:
                wallets[aw_idx].active = False
                try:
                    await wallets[aw_idx].save(update_fields=["active"])
                except Exception as e:
                    logging.exception(e)
        if only_active:
            coins = [CoinOut.model_validate(w) for w in wallets if w.active]
        else:
            coins = [CoinOut.model_validate(w) for w in wallets]

        if include_symbols is None or "TON" in include_symbols:
            ton_asset = CoinOut(
                type="ton",
                amount=balance,
                usd_price=balance * 7.44 if balance is not None else 0,
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

    async def get_seqno(self, owner_address: Address):
        try:
            return await self.ton.ton_client.tc_client.get_wallet_seqno(owner_address.to_string())
        except BaseException as e:
            logging.error(e)

    async def get_balance(self, owner_address: Address):
        try:
            return await self.ton.ton_client.tc_client.get_balance(owner_address.to_string())
        except BaseException as e:
            logging.error(e)

    async def update_transaction(self, owner_address: Address) -> int | None:
        wallet = await self.get_or_create(owner_address)
        if wallet and wallet.transaction:
            seqno = await self.get_seqno(owner_address)
            if (
                wallet.last_seqno is None
                or seqno != wallet.last_seqno
                or (
                    wallet.transaction_expire_at is not None
                    and wallet.transaction_expire_at > datetime.datetime.now(datetime.timezone.utc)
                )
            ):
                balance = await self.get_balance(owner_address)
                wallet.balance = balance
                wallet.last_seqno = seqno
                wallet.transaction = False
                wallet.transaction_expire_at = None
                await wallet.save(
                    update_fields=[
                        "last_seqno",
                        "transaction",
                        "transaction_expire_at",
                        "balance",
                    ]
                )
            return wallet.last_seqno if wallet.transaction else None
        return None

    @staticmethod
    async def get_or_create(owner_address: Address) -> Wallet:
        wallet = await Wallet.get_by_address(owner_address)
        if wallet is not None:
            return wallet
        address_base64, address_raw, address_hash, mainnet = Wallet._address_setter(owner_address)

        return await Wallet.create(
            address_base64=address_base64,
            address_raw=address_raw,
            address_hash=address_hash,
            decimals=9,
            mainnet=TON_CLIENT_NETWORK == "mainnet",  # not owner_address.is_test_only,
            symbol="TON",
        )

    @staticmethod
    async def update_from_network(wallet: Wallet | None) -> Wallet | None:
        if wallet:
            wallet_info = await TonController().get_wallet_info(wallet.address)
            if wallet_info:
                wallet.info = wallet_info
                try:
                    if "balance" in wallet_info:
                        wallet.balance = int(wallet_info["balance"]) / 10**9
                    if "code" in wallet_info:
                        wallet.wallet_code = wallet_info["code"]
                        if wallet.wallet_code == WalletCode.v4r.value:
                            wallet.type = "v4r"
                        else:
                            wallet.type = "unknown"
                    if "last_transaction_id" in wallet_info:
                        wallet.last_lt = int(wallet_info["last_transaction_id"]["lt"])
                        wallet.last_transaction = wallet_info["last_transaction_id"]["hash"]
                    if "block_id" in wallet_info:
                        wallet.last_block_seqno = int(wallet_info["block_id"]["seqno"])
                    if "sync_utime" in wallet_info:
                        wallet.last_sync = int(wallet_info["sync_utime"])
                    if "state" in wallet_info and wallet_info["state"] == "active":
                        wallet.active = True

                    await wallet.save()
                except Exception as e:
                    logging.error(f"PArse error: {e}")
            return wallet
