from enum import Enum
from typing import Union, List

from ..base import ArchitectonBase, BaseModel
from pydantic import Field


class TransactionsHistory(ArchitectonBase):
    wallet: str = Field(default=None)
