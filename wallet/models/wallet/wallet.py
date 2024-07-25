from tonsdk.utils import Address
from tortoise import fields
from tortoise.expressions import Q

from wallet.models import JettonMaster
from wallet.models.base_address_model import BaseTonAddress


class Wallet(BaseTonAddress):
    class Meta:
        table = "wallet"
        unique_together = ("address_base64", "mainnet")

    id = fields.UUIDField(pk=True)

    type = fields.CharField(max_length=8, null=True, default="v4r")

    balance = fields.DecimalField(
        max_digits=49, decimal_places=9, null=True, default=None, index=True
    )
    last_seqno = fields.BigIntField(default=None, index=True, null=True)
    transaction = fields.BooleanField(default=True, index=True, null=True)
    transaction_expire_at = fields.DatetimeField(default=None, null=True)

    decimals = fields.IntField(default=None, index=True, null=True)
    symbol = fields.CharField(max_length=12, null=True, index=True)
    usd_ratio = fields.FloatField(default=0)
    change_ratio = fields.FloatField(default=0)
    active = fields.BooleanField(default=False, index=True)
    wallet_code = fields.TextField(default=None, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
