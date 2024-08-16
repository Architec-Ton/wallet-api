from typing import List
from uuid import UUID

from pydantic import Field

from ..base import ArchitectonBase
from ..wallet.coin import CoinOut


class BankBuyInfo(ArchitectonBase):
    assets: List[CoinOut]
