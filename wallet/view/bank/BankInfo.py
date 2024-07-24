from typing import List

from ..base import ArchitectonBase
from pydantic import Field

from ..transaction.history import HistoryItemOut


class BankInfo(ArchitectonBase):
    bnk_amount: int = Field(default=0)
    bnk_stacked_amount: int = Field(default=0)
    arc_amount: float = Field(default=0)
    arc_stacked_amount: float = Field(default=0)
    can_stake: bool = Field(default=True)
    referrals: int = Field(default=0)
    bankers: int = Field(default=0)
    free_banks: int = Field(default=0)
    total_banks: int = Field(default=0)
    history: List[HistoryItemOut] = Field(default=[])
