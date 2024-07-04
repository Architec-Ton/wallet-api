from typing import List, Dict

from uuid import UUID

from ..base import ArchitectonBase
from pydantic import Field


class CategoryCreateIn(ArchitectonBase):
    title_en: str = Field()
    translation: Dict[str, str] | None = Field(
        default=None, example={"ru": "Translation for RU"}
    )


class CategoryUpdateIn(CategoryCreateIn):
    title_en: str | None = Field(default=None)


class CategoryOut(ArchitectonBase):
    id: UUID = Field()
    title: str = Field()


class CategoryDetailOut(CategoryOut):
    translation: Dict[str, str] | None = Field(
        default=None, example={"ru": "Translation for RU"}
    )
    slug: str = Field()
