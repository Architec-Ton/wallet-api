from uuid import uuid4

from tortoise import fields
from tortoise.models import Model


class AppCategory(Model):
    class Meta:
        table = "app_category"
        table_description = "This table contains a app categories "

    id = fields.UUIDField(
        pk=True,
        index=True,
        unique=True,
        default=uuid4,
    )
    title_en = fields.CharField(
        max_length=128,
    )
    slug = fields.CharField(max_length=128, index=True, unique=True)
    payload = fields.JSONField(default=None, null=True)
    parent = fields.relational.ForeignKeyField(
        "models.AppCategory", index=True, null=True, default=None
    )
    app_count: int = fields.SmallIntField(index=True, default=0)
    order: int = fields.SmallIntField(index=True, default=1000)
    active: int = fields.BooleanField(index=True, default=True)

    @property
    def title(self):
        return self.title_en

    @property
    def translation(self):
        return self.payload["translation"]
