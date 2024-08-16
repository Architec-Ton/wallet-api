from uuid import uuid4

from tortoise import fields
from tortoise.models import Model

from wallet.models.attachment.attachment_mixin import AttachmentMixin


class App(AttachmentMixin):

    entity: str = "app"

    class Meta:
        table = "app"
        table_description = "This table contains a app categories "

    id = fields.UUIDField(
        pk=True,
        index=True,
        unique=True,
        default=uuid4,
    )
    url = fields.CharField(max_length=256)
    title_en = fields.CharField(max_length=128, index=True)
    subtitle_en = fields.CharField(max_length=128, index=True)
    description_en = fields.CharField(
        max_length=2048,
    )
    slug = fields.CharField(max_length=128, index=True, unique=True)

    rating = fields.FloatField(default=None, null=True, index=True)
    reviews = fields.IntField(default=0, index=True)

    payload = fields.JSONField(default=None, null=True)
    category = fields.relational.ForeignKeyField(
        "models.AppCategory",
        index=True,
        null=True,
        default=None,
        on_delete=fields.SET_NULL,
    )

    icon = fields.relational.ForeignKeyField(
        "models.Attachment",
        index=True,
        null=True,
        default=None,
        on_delete=fields.SET_NULL,
    )

    # resources = fields.ReverseRelation("models.AppResource", "app_id")

    is_top = fields.BooleanField(index=True, default=False)
    is_partner = fields.BooleanField(index=True, default=False)
    order: int = fields.SmallIntField(index=True, default=1000)
    active: int = fields.BooleanField(index=True, default=True)

    @property
    def title(self):
        return self.title_en

    @property
    def subtitle(self):
        return self.subtitle_en

    @property
    def description(self):
        return self.description_en

    @property
    def translation(self):
        return self.payload["translation"]

    @property
    def gallery(self):
        if self.attachments:
            return [a.url for a in self.attachments]
        return []
