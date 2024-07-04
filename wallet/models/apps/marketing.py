from uuid import uuid4

from tortoise import fields
from tortoise.models import Model


class AppMarketing(Model):
    class Meta:
        table = "app_marketing"
        table_description = "This table contains a app categories "

    id = fields.UUIDField(
        pk=True,
        index=True,
        unique=True,
        default=uuid4,
    )
    url = fields.CharField(max_length=256, null=True, default=None)
    title = fields.CharField(max_length=128, null=True, default=None)
    image = fields.relational.ForeignKeyField(
        "models.Attachment",
        index=True,
        null=True,
        default=None,
        on_delete=fields.SET_NULL,
    )

    order: int = fields.SmallIntField(index=True, default=1000)
    active: int = fields.BooleanField(index=True, default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
