from enum import Enum

from pydantic import Field

from ..base import ArchitectonBase


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
