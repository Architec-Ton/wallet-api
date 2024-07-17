from tortoise import fields
from tortoise.models import Model


class BaseTransaction(Model):
    transaction_type: str = fields.CharField(max_length=128, null=True, default=None, index=True)
    transaction_address: str = fields.CharField(max_length=128, null=True, default=None, index=True)
    transaction_data: str = fields.CharField(max_length=1028, null=True, default=None)
    transaction_hash = fields.CharField(max_length=128, null=True, default=None, index=True)
    transaction_date = fields.DatetimeField(auto_now_add=True)
    transaction_amount = fields.DecimalField(
        max_digits=39, decimal_places=9, null=True, default=None
    )
    transaction_fee = fields.DecimalField(
        max_digits=39, decimal_places=9, null=True, default=None
    )

    # currency_rate: float = fields.CharField(max_length=128, null=True, default=None, index=True)
    # image: str = fields.CharField(max_length=1028, null=True, default=None)
    # image_data: str = fields.CharField(max_length=1028, null=True, default=None)
    # url: str = fields.CharField(max_length=1028, null=True, default=None)

