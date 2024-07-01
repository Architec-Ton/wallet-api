from tortoise import fields
from tortoise.models import Model


class BaseTonAddress(Model):

    address_raw = fields.CharField(max_length=128, null=True, default=None, index=True)
    address_hash = fields.CharField(max_length=128, null=True, default=None, index=True)
    address_base64: str = fields.CharField(
        max_length=48, null=True, default=None, index=True
    )
