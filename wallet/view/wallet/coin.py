from enum import Enum
from typing import Union, List

from ..base import ArchitectonBase, BaseModel
from pydantic import Field
from uuid import UUID


class NftMetaOut(ArchitectonBase):
    address: str | None = Field(default=None)
    name: str = Field()
    description: str = Field()
    image: str | None = Field(default=None)
    image_data: str | None = Field(default=None)
    uri: str | None = Field(default=None)


class JettonMetaOut(NftMetaOut):
    symbol: str | None= Field(default=None)
    decimals: int | None= Field(default=None)
    amount_style: str | None = Field(default=None)
    render_type: str | None = Field(default=None)


class CoinType(str, Enum):
    jetton = "jetton"
    nft = "nft"
    ton = "ton"


class CoinOut(ArchitectonBase):
    type: CoinType = Field(default=CoinType.jetton)
    meta: JettonMetaOut | None = Field(default=None)
    amount: float | None = Field(default=None)
    usd_price: float | None = Field(default=None)
    change_price: float | None = Field(default=None)


class UserOut(ArchitectonBase):
    name: str
    session_id: UUID | None
    tg_id: int
    lang: str
    net: str
    address: str
