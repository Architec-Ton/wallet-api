from typing import List
from uuid import UUID

from pydantic import Field

from ..base import ArchitectonBase
from .resources import GameResourceOut


class GameItemOut(ArchitectonBase):
    id: UUID = Field()
    title: str = Field()
    description: str = Field()
    thumb: str = Field()


class GameOut(GameItemOut):
    gallery: List[str] = Field()
    resources: List[GameResourceOut] = Field()
