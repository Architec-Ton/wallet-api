from tortoise import fields
from tortoise.models import Model


class Account(Model):
    class Meta:
        table = "account"

    id = fields.BigIntField(index=True, pk=True)
    first_name = fields.CharField(max_length=128, null=True, default=None)
    last_name = fields.CharField(max_length=128, null=True, default=None)
    username = fields.CharField(max_length=128, null=True, default=None)
    photo_url = fields.CharField(max_length=512, null=True, default=None)
    language_code = fields.CharField(max_length=128, null=True, default=None)

    is_premium = fields.BooleanField(default=False, index=True, null=True)
    is_bot = fields.BooleanField(default=False, index=True, null=True)
    added_to_attachment_menu = fields.BooleanField(default=False, index=True)
    allows_write_to_pm = fields.BooleanField(default=False, index=True)
    receiver_id = fields.BigIntField(index=True, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
