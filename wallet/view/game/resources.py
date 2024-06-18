from enum import Enum

from ..base import ArchitectonBase
from pydantic import Field
from uuid import UUID


class GameResourceType(str, Enum):
    telegram = "telegram"
    web = "web"
    coin = "coin"


class GameResourceOut(ArchitectonBase):
    # id: UUID = Field()
    type: GameResourceType = Field()
    title: str = Field()
    description: str = Field()
    link: str = Field()
    thumb: str = Field()
