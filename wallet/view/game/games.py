from typing import List

from uuid import UUID

from .game import GameItemOut
from ..base import ArchitectonBase
from pydantic import Field


class GameCategoryOut(ArchitectonBase):
    id: UUID = Field()
    title: str = Field()
    items: List[GameItemOut]
