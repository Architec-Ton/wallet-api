from tortoise import fields

from wallet.models.base_address_model import BaseTonAddress


class Wallet(BaseTonAddress):
    class Meta:
        table = "wallet"
        unique_together = ("address_base64", "mainnet")

    id = fields.UUIDField(pk=True)

    type = fields.CharField(max_length=8, null=True, default="v4r")
    workchain = fields.BigIntField(default=0, index=True, null=True)
    balance = fields.DecimalField(max_digits=49, decimal_places=9, null=True, default=None, index=True)
    last_seqno = fields.BigIntField(default=None, index=True, null=True)
    last_lt = fields.BigIntField(default=None, index=True, null=True)
    last_sync = fields.BigIntField(default=None, index=True, null=True)
    last_block_seqno = fields.BigIntField(default=None, index=True, null=True)
    last_transaction = fields.CharField(default=None, index=True, null=True, max_length=128)
    transaction = fields.BooleanField(default=True, index=True, null=True)
    transaction_expire_at = fields.DatetimeField(default=None, null=True)

    decimals = fields.IntField(default=None, index=True, null=True)
    symbol = fields.CharField(max_length=12, null=True, index=True)
    usd_ratio = fields.FloatField(default=0)
    change_ratio = fields.FloatField(default=0)
    active = fields.BooleanField(default=False, index=True)
    wallet_code = fields.TextField(default=None, null=True)
    info = fields.JSONField(default=None, null=True)
    payload = fields.JSONField(default=None, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
