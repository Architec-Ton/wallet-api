from tortoise import fields
from tortoise.models import Model


class AttachmentConnection(Model):
    class Meta:
        table = "attachment_connection"
        table_description = "This table contains a connection of entities "

    attachment = fields.ForeignKeyField("models.Attachment", index=True, pk=True)
    order: int = fields.SmallIntField(index=True, default=0)
    active: int = fields.BooleanField(index=True, default=True)
    entity_id = fields.UUIDField(index=True)
