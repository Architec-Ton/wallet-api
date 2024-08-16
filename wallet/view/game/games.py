from typing import List
from uuid import UUID

from pydantic import Field

from ..base import ArchitectonBase
from .game import GameItemOut


class GameCategoryOut(ArchitectonBase):
    id: UUID = Field()
    title: str = Field()
    items: List[GameItemOut]
