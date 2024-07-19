from uuid import uuid4

from tortoise import fields
from tortoise.models import Model


class AppResource(Model):
    class Meta:
        table = "app_resource"
        table_description = "This table contains a app categories "

    id = fields.UUIDField(
        pk=True,
        index=True,
        unique=True,
        default=uuid4,
    )
    app = fields.relational.ForeignKeyField(
        "models.App",
        index=True,
        null=True,
        default=None,
        on_delete=fields.SET_NULL,
        related_name="resources",
    )

    icon = fields.relational.ForeignKeyField(
        "models.Attachment",
        index=True,
        null=True,
        default=None,
        on_delete=fields.SET_NULL,
    )

    type = fields.CharField(max_length=64)
    url = fields.CharField(max_length=1024)
    title_en = fields.CharField(max_length=128, index=True)
    payload = fields.JSONField(default=None, null=True)
    order: int = fields.SmallIntField(index=True, default=1000)

    @property
    def title(self):
        return self.title_en

    @property
    def translation(self):
        return self.payload["translation"]
