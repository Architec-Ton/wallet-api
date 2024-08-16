from enum import Enum
from typing import List, Union
from uuid import UUID

from pydantic import Field

from ..base import ArchitectonBase, BaseModel
from ..transaction.history import HistoryItemOut
from .coin import CoinOut


class WalletOut(ArchitectonBase):
    usd_price: float = Field(default=None)
    change_price: float = Field(default=None)
    address: str = Field(default=None)
    seqno: int | None = Field(default=None)
    assets: List[CoinOut] = Field(default=[])
    history: List[HistoryItemOut] = Field(default=[])


class InfoOut(ArchitectonBase):
    current_wallet: int = Field(default=-1)
    wallets: List[WalletOut] = Field(default=[])
