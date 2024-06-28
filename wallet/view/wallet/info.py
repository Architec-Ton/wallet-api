from enum import Enum
from typing import Union, List

from ..base import ArchitectonBase, BaseModel
from .coin import CoinOut
from pydantic import Field
from uuid import UUID


class InfoOut(ArchitectonBase):
    usd_price: float = Field(default=None)
    change_price: float = Field(default=None)
    address: str = Field(default=None)
    assets: List[CoinOut] = Field(default=[])
    history: List[CoinOut] = Field(default=[])
