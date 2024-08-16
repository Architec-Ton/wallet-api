from typing import Dict, List
from uuid import UUID

from pydantic import Field

from ..base import ArchitectonBase


class CategoryCreateIn(ArchitectonBase):
    title_en: str = Field()
    translation: Dict[str, str] | None = Field(default=None, example={"ru": "Translation for RU"})


class CategoryUpdateIn(CategoryCreateIn):
    title_en: str | None = Field(default=None)


class CategoryOut(ArchitectonBase):
    id: UUID = Field()
    title: str = Field()


class CategoryDetailOut(CategoryOut):
    translation: Dict[str, str] | None = Field(default=None, example={"ru": "Translation for RU"})
    slug: str = Field()
