from pydantic import Field

from ..base import ArchitectonBase, BaseModel
from .user import UserIn


class InitDataIn(ArchitectonBase):
    auth_date: str
    hash: str
    query_id: str | None = Field(default=None)
    user: UserIn


class InitTonIn(ArchitectonBase):
    address: str = Field()
    # public_key: str = Field(default="full")
    signature: str | None = Field(default="full")


class AuthIn(ArchitectonBase):
    init_data_raw: InitDataIn | str | None = Field(default=None)
    init_ton: InitTonIn | None = Field(default=None)
    auth_type: str = Field(default="telegram")


class AuthOut(BaseModel):
    access_token: str
