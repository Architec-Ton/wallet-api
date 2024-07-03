from tonsdk.utils import Address
from tortoise import fields

from wallet.models import JettonMaster
from wallet.models.base_address_model import BaseTonAddress


class JettonWallet(BaseTonAddress):

    class Meta:
        table = "jetton_wallet"
        unique_together = ("address_base64", "mainnet", "jetton")

    id = fields.UUIDField(pk=True)

    jetton = fields.ForeignKeyField("models.JettonMaster", index=True)

    wallet_address_raw = fields.CharField(
        max_length=128, null=True, default=None, index=True
    )
    wallet_address_hash = fields.CharField(
        max_length=128, null=True, default=None, index=True
    )
    wallet_address_base64: str = fields.CharField(
        max_length=48, null=True, default=None, index=True
    )

    balance = fields.DecimalField(
        max_digits=49, decimal_places=9, null=True, default=None, index=True
    )
    decimals = fields.IntField(default=None, index=True, null=True)

    usd_ratio = fields.FloatField(default=0)

    change_ratio = fields.FloatField(default=0)

    active = fields.BooleanField(default=False, index=True)

    wallet_code = fields.TextField(default=None, null=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    @staticmethod
    async def new(
        owner_address: Address, wallet_address: Address, jetton: JettonMaster
    ) -> "JettonWallet":
        wallet_address_base64, wallet_address_raw, wallet_address_hash, _ = (
            BaseTonAddress._address_setter(wallet_address)
        )
        address_base64, address_raw, address_hash, mainnet = (
            BaseTonAddress._address_setter(owner_address)
        )

        return await JettonWallet.create(
            address_base64=address_base64,
            address_raw=address_raw,
            address_hash=address_hash,
            wallet_address_base64=wallet_address_base64,
            wallet_address_raw=wallet_address_raw,
            wallet_address_hash=wallet_address_hash,
            jetton=jetton,
            decimals=jetton.decimals,
            mainnet=mainnet,
        )

    @staticmethod
    async def get_wallets(owner_address: Address):
        return await JettonWallet.filter(
            address_hash=owner_address.hash_part.hex(),
            mainnet=not owner_address.is_test_only,
        ).prefetch_related("jetton")

    @property
    def wallet_address(self) -> Address:
        return Address(self.wallet_address_base64)

    @wallet_address.setter
    def wallet_address(self, value):
        (
            self.wallet_address_base64,
            self.wallet_address_raw,
            self.wallet_address_hash,
            self.mainnet,
        ) = BaseTonAddress._address_setter(value)

    @property
    def amount(self):
        return self.balance

    @property
    def usd_price(self):
        return self.balance * self.usd_ratio

    @property
    def change_price(self):
        return self.change_ratio

    @property
    def meta(self):
        return self.jetton


# Jetton({"supply": 80000000000000000, "address": "EQDnRHbK5vJBLQyAnS6V8XNoRerCebnn9A2FlVlHtFVLFGZ-", "decimals": 6, "symbol": "USDT", "name": "USD Tether", "description": "Testnet USDT Jetto
# n", "image": "https://cryptologos.cc/logos/tether-usdt-logo.png?v=025", "token_supply": 80000000000.0})


# EQDnRHbK5vJBLQyAnS6V8XNoRerCebnn9A2FlVlHtFVLFGZ
