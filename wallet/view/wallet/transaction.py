from enum import Enum
from typing import Union, List

from ..base import ArchitectonBase, BaseModel
from .coin import CoinOut
from pydantic import Field
from uuid import UUID

class TransactionOut(ArchitectonBase):
    assets: List[CoinOut] = Field(default=[])