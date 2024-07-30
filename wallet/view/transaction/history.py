from enum import Enum

from tonsdk.utils import Address

from ..base import ArchitectonBase, BaseModel
from pydantic import Field, field_validator
from uuid import UUID

from ..wallet.coin import CoinType


class HistoryItemType(str, Enum):
    received = "received"
    send = "send"
    swap = "swap"


class HistoryItemOut(ArchitectonBase):
    type: str
    utime: int
    address_from: str | None = Field(default=None)
    address_to: str | None = Field(default=None)
    status: bool
    value: float | None = Field(default=None)
    symbol: str | None = Field(default="TON")
    comment: str | None = Field(default=None)
