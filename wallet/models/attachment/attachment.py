import os
from typing import Optional
from uuid import UUID, uuid4

from tortoise import fields, Model

# from stretchcore.models.storage.attachment_connection import AttachmentConnection
from .attachment_type import (
    AttachmentFileType,
)

from .attachment_connection import AttachmentConnection

STORAGE_URL = os.getenv("STORAGE_URL", "/storage")
STORAGE_PATH = os.getenv("STORAGE_PATH", "./storage")


class Attachment(Model):
    id = fields.UUIDField(
        pk=True,
        index=True,
        unique=True,
        default=uuid4,
    )
    title: str = fields.CharField(
        max_length=360, null=True, default=None, description="Title for file object"
    )
    description: str = fields.CharField(max_length=1024, null=True, default=None)
    source: str = fields.CharField(max_length=16, default="local")
    filename: str = fields.CharField(max_length=256)
    origin_filename: str = fields.CharField(max_length=256, null=True, default=None)

    filesize: int = fields.BigIntField(null=True, default=None)
    file_type = fields.CharEnumField(AttachmentFileType, max_length=16, index=True)
    content_type: Optional[str] = fields.CharField(
        max_length=32, default=None, null=True
    )
    entities: fields.ReverseRelation
    duration = fields.IntField(
        default=None, null=True, index=True, description="Duration in seconds"
    )
    status = fields.CharField(max_length=16, default="approved", index=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    # def __repr__(self):
    #     return self.url

    @property
    def url(self) -> str:
        """
        Returns the URL
        """
        return f"{STORAGE_URL}/{self.file_type.value}/{self.filename}"

    @property
    def thumb(self) -> str:
        """
        Returns the URL
        """
        return f"{STORAGE_URL}/storage/{self.file_type}/thumb/{self.filename}"

    def filepath(
        self, file_type: AttachmentFileType = AttachmentFileType.icon, is_exist=False
    ) -> str | None:
        """
        Returns path
        """

        filebase = self.filename
        filetype = file_type.value
        if file_type == AttachmentFileType.thumb:
            filebase = f"{os.path.splitext(self.filename)[0]}.webp"
            filename = os.path.join(
                STORAGE_PATH,
                filetype,
                "thumb",
                filebase,
            )
        elif file_type == AttachmentFileType.orig:
            filename = os.path.join(
                STORAGE_PATH,
                filetype,
                "orig",
                filebase,
            )
        else:
            filename = os.path.join(
                STORAGE_PATH,
                filetype,
                "web",
                filebase,
            )
        if not is_exist:
            return filename

        if os.path.isfile(filename):
            return filename

    async def remove(self, entity_id: UUID | None = None):
        # Drop connection
        if entity_id is not None:
            await AttachmentConnection.filter(
                attachment_id=self.id, entity_id=entity_id
            ).delete()
        count = await AttachmentConnection.filter(attachment_id=self.id).count()
        # if count == 0:
        #     for file in AttachmentFileType:
        #         filepath = self.filepath(file, is_exist=True)
        #         if filepath is not None:
        #             os.remove(filepath)
        #     await self.delete()
        #     return True
        return False
