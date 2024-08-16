from enum import Enum
from typing import Dict, List
from uuid import UUID

from pydantic import Field, field_validator

from ...models import Attachment
from ..base import ArchitectonBase
from ..category.category import CategoryOut
from .marketing import AppMarketingOut
from .resource import AppResourceOut


class AppTextIn(ArchitectonBase):
    title: str = Field()
    subtitle: str = Field()
    description: str = Field()


class AppCreateIn(ArchitectonBase):
    category_id: UUID | None = Field(default=None)
    url: str = Field(example="https://t.me/satochi_bot/game")
    title_en: str = Field()
    subtitle_en: str = Field()
    description_en: str = Field()
    translation: Dict[str, AppTextIn] | None = Field(
        default=None,
        example={
            "ru": {
                "title": "Название игры ",
                "subtitle": "Подзаголовок игры",
                "description": "Длинное описание игры и игрового процесса ",
            }
        },
    )

    icon_id: UUID | None = Field(default=None, example=None)

    attachments_ids: List[UUID] = Field(default=[], example=[])


class AppUpdateIn(AppCreateIn):
    title_en: str | None = Field(default=None)
    subtitle_en: str | None = Field(default=None)
    description_en: str | None = Field(default=None)
    is_partner: bool | None = Field(default=None)
    url: str | None = Field(default=None)


class AppShortOut(ArchitectonBase):
    id: UUID = Field()
    title: str = Field()
    subtitle: str = Field()
    is_partner: bool = Field()
    icon: str | None = Field(default=None)

    @field_validator("icon", mode="before")
    @classmethod
    def validate_icon(cls, value):
        if isinstance(value, Attachment):
            return value.url


class AppOut(AppTextIn, AppShortOut):
    id: UUID = Field()
    category_id: UUID | None = Field(default=None)
    url: str = Field()
    gallery: List[str] = Field(default=[])
    resources: List[AppResourceOut] = Field(default=[])

    @field_validator("gallery", mode="before")
    @classmethod
    def validate_gallery(cls, value):
        if isinstance(value, List):
            return [o for o in value]


class AppDetailOut(AppOut):
    slug: str = Field()
    resources: List[AppResourceOut] = Field(default=[])


class AppsByCategoriesOut(CategoryOut):
    apps: List[AppOut]


class AppsCategoriesOut(CategoryOut):
    apps: List[AppShortOut]


class AppsOut(ArchitectonBase):
    marketings: List[AppMarketingOut]
    categories: List[AppsCategoriesOut]


class AppsFilterIn(ArchitectonBase):
    search: str | None = Field(default=None)
    category_id: UUID | None = Field(default=None)
