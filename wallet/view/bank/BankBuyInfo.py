from typing import List

from ..base import ArchitectonBase
from ..wallet.coin import CoinOut


class BankBuyInfo(ArchitectonBase):
    assets: List[CoinOut]
