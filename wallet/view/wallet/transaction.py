from enum import Enum
from typing import List, Union
from uuid import UUID

from pydantic import Field

from ..base import ArchitectonBase, BaseModel
from .coin import CoinOut


class TransactionOut(ArchitectonBase):
    assets: List[CoinOut] = Field(default=[])
