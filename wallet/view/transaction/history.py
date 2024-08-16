from enum import Enum

from pydantic import Field

from ..base import ArchitectonBase


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
