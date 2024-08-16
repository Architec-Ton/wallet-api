from uuid import uuid4

from tortoise import fields
from tortoise.models import Model


class AccountWalletConnection(Model):

    class Meta:
        table = "account_wallet_connection"
        unique_together = ("account", "wallet")

    id = fields.UUIDField(
        pk=True,
        index=True,
        unique=True,
        default=uuid4,
    )
    account = fields.ForeignKeyField("models.Account", index=True, null=True, default=None)
    wallet = fields.ForeignKeyField("models.Wallet", index=True, null=True, default=None)
    created_at = fields.DatetimeField(auto_now_add=True)
