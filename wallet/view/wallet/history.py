from enum import Enum
from typing import List, Union

from pydantic import Field

from ..base import ArchitectonBase, BaseModel


class TransactionsHistory(ArchitectonBase):
    wallet: str = Field(default=None)
