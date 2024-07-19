from typing import List

from uuid import UUID

from ..base import ArchitectonBase
from pydantic import Field

from ..wallet.coin import CoinOut


class BankBuyInfo(ArchitectonBase):
    assets: List[CoinOut]
