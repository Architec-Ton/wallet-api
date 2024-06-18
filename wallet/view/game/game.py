from typing import List

from .resources import GameResourceOut
from ..base import ArchitectonBase
from pydantic import Field
from uuid import UUID


class GameItemOut(ArchitectonBase):
    id: UUID = Field()
    title: str = Field()
    description: str = Field()
    thumb: str = Field()


class GameOut(GameItemOut):
    gallery: List[str] = Field()
    resources: List[GameResourceOut] = Field()
