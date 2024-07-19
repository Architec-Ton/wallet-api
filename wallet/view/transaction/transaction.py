from tonsdk.utils import Address

from ..base import ArchitectonBase, BaseModel
from pydantic import Field, field_validator
from uuid import UUID

from ..wallet.coin import CoinType


class TransactionItemOut(ArchitectonBase):
    icon: str | None
    allows_write_to_pm: bool | None = Field(default=None)
    first_name: str
    id: int | None = Field(default=None)
    is_premium: bool | None = Field(default=None)
    language_code: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
    username: str | None = Field(default=None)
    #
    # type: CoinType = Field(default=CoinType.jetton)
    # meta: JettonMetaOut | None = Field(default=None)
    # amount: float | None = Field(default=0)
    # usd_price: float | None = Field(default=0)
    # change_price: float | None = Field(default=0)
