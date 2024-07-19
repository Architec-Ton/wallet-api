from enum import Enum
from typing import Union, List

from ..base import ArchitectonBase, BaseModel
from .coin import CoinOut
from pydantic import Field
from uuid import UUID

from ..transaction.history import HistoryItemOut


class WalletOut(ArchitectonBase):
    usd_price: float = Field(default=None)
    change_price: float = Field(default=None)
    address: str = Field(default=None)
    assets: List[CoinOut] = Field(default=[])
    history: List[HistoryItemOut] = Field(default=[])


class InfoOut(ArchitectonBase):
    current_wallet: int = Field(default=-1)
    wallets: List[WalletOut] = Field(default=[])
