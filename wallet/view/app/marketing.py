from uuid import UUID

from pydantic import Field, field_validator

from ...models import Attachment
from ..base import ArchitectonBase


class AppMarketingCreateIn(ArchitectonBase):
    url: str = Field(example="https://t.me/satochi_bot/game")
    title: str | None = Field(default=None)
    image_id: UUID | None = Field(default=None, example=None)


class AppMarketingOut(ArchitectonBase):
    id: UUID = Field()
    title: str = Field()
    url: str = Field()
    image: str | None = Field(default=None)

    @field_validator("image", mode="before")
    @classmethod
    def validate_icon(cls, value):
        if isinstance(value, Attachment):
            return value.url
