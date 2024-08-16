from typing import List

from pydantic import Field

from ..base import ArchitectonBase
from .coin import CoinOut


class TransactionOut(ArchitectonBase):
    assets: List[CoinOut] = Field(default=[])
