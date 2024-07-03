from tortoise import fields
from wallet.models.base_address_model import BaseTonAddress


class JettonMaster(BaseTonAddress):

    class Meta:
        table = "jetton_master"
        unique_together = ("address_base64", "mainnet")

    id = fields.IntField(pk=True)
    name: str = fields.CharField(max_length=256, null=True, default=None)
    description: str = fields.CharField(max_length=1028, null=True, default=None)
    image: str = fields.CharField(max_length=1028, null=True, default=None)
    image_data: str = fields.CharField(max_length=1028, null=True, default=None)
    url: str = fields.CharField(max_length=1028, null=True, default=None)
    symbol = fields.CharField(max_length=12, null=True, index=True)
    decimals = fields.IntField(default=9)
    supply = fields.DecimalField(
        max_digits=39, decimal_places=9, null=True, default=None
    )
    token_supply = fields.DecimalField(
        max_digits=39, decimal_places=9, null=True, default=None
    )
    primary = fields.BooleanField(default=True, index=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)


# Jetton({"supply": 80000000000000000, "address": "EQDnRHbK5vJBLQyAnS6V8XNoRerCebnn9A2FlVlHtFVLFGZ-", "decimals": 6, "symbol": "USDT", "name": "USD Tether", "description": "Testnet USDT Jetto
# n", "image": "https://cryptologos.cc/logos/tether-usdt-logo.png?v=025", "token_supply": 80000000000.0})


# EQDnRHbK5vJBLQyAnS6V8XNoRerCebnn9A2FlVlHtFVLFGZ
