from pydantic import Field

from ..base import ArchitectonBase


class TransactionsHistory(ArchitectonBase):
    wallet: str = Field(default=None)
