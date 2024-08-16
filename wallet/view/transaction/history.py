from enum import Enum
from uuid import UUID

from pydantic import Field, field_validator
from tonsdk.utils import Address

from ..base import ArchitectonBase, BaseModel
from ..wallet.coin import CoinType


class HistoryItemType(str, Enum):
    received = "received"
    send = "send"
    swap = "swap"
    stack = "stack"
    claim = "claim"


class HistoryItemOut(ArchitectonBase):
    type: str
    utime: int
    address_from: str | None = Field(default=None)
    address_to: str | None = Field(default=None)
    status: bool
    value: float | None = Field(default=None)
    symbol: str | None = Field(default="TON")
    comment: str | None = Field(default=None)
