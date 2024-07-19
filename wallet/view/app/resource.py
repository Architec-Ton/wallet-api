from enum import Enum
from typing import Dict
from uuid import UUID

from pydantic import Field, field_validator

from wallet.models import Attachment
from wallet.view.base import ArchitectonBase


class AppResourceTextIn(ArchitectonBase):
    title: str = Field()


class AppResourceType(str, Enum):
    telegram = "telegram"
    website = "website"
    jetton = "jetton"


class AppResourceCreateIn(ArchitectonBase):
    type: AppResourceType = Field(default=AppResourceType.telegram)
    icon_id: UUID | None = Field(default=None, example=None)
    title_en: str = Field()
    url: str = Field()
    translation: Dict[str, AppResourceTextIn] | None = Field(
        default=None,
        example={
            "ru": {
                "title": "Заголовок ресурса игры ",
            }
        },
    )


class AppResourceUpdateIn(AppResourceCreateIn):
    type: AppResourceType | None = Field(default=None)
    title_en: str | None = Field(default=None)
    url: str | None = Field(default=None)


class AppResourceOut(ArchitectonBase):
    type: str = Field()
    icon: str | None = Field(default=None, example=None)
    title: str = Field()
    url: str = Field()

    @field_validator("icon", mode="before")
    @classmethod
    def validate_icon(cls, value):
        if isinstance(value, Attachment):
            return value.url
