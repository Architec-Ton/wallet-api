from typing import List
from uuid import UUID, uuid4

from tortoise import fields, Model

from wallet.errors import APIException
from .attachment import Attachment
from .attachment_connection import AttachmentConnection


class AttachmentMixin(Model):
    entity: str = "assets"
    # _attachments: List[Attachment] = []

    id = fields.UUIDField(
        pk=True,
        index=True,
        unique=True,
        default=uuid4,
    )

    attachments = fields.ManyToManyField(
        "models.Attachment",
        through="attachment_connection",
        backward_key="entity_id",
        forward_key="attachment_id",
        related_name=entity,
    )

    # async def fetch_attachment(self):
    #     ac = await AttachmentConnection.filter(entity_id=self.id).prefetch_related("attachment").order_by("order")
    #     self._attachments = [a.attachment for a in ac]
    #     return self

    @staticmethod
    async def verify_attachments(attachment_ids: List[UUID] | None):
        if attachment_ids is None or len(attachment_ids) == 0:
            return
        count_add = await Attachment.filter(id__in=attachment_ids).count()
        if len(attachment_ids) != count_add:
            raise APIException("attachment_not_found", 404)

    async def update_attachments(self, attachment_ids: List[UUID] | None):
        if attachment_ids is None:
            return
        current_attachments = await AttachmentConnection.filter(
            entity_id=self.id
        ).prefetch_related("attachment")
        current_attachments_ids = set([a.attachment_id for a in current_attachments])

        # drop old
        remove_attachment_ids = current_attachments_ids - set(attachment_ids)
        for rid in remove_attachment_ids:
            ra = next(
                a.attachment for a in current_attachments if a.attachment_id == rid
            )
            await ra.remove(self.id)

        # add new
        add_attachment_ids = set(attachment_ids) - current_attachments_ids
        for aid in add_attachment_ids:
            await AttachmentConnection.create(
                attachment_id=aid,
                entity_id=self.id,
            )
        await self.fetch_related("attachments")
        return self

    async def delete_attachments(self):
        return await self.update_attachments([])
