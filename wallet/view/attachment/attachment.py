from typing import List
from uuid import UUID

from pydantic import Field

from ..base import ArchitectonBase


class AttachmentOut(ArchitectonBase):
    id: UUID = Field()
    title: str | None = Field(default=None)
    description: str | None = Field(default=None)
    origin_filename: str | None = Field(default=None)
    url: str | None = Field(default=None)
