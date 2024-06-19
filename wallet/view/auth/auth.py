from typing import List


from ..base import ArchitectonBase, BaseModel
from pydantic import Field
from uuid import UUID


class UserIn(ArchitectonBase):
    allows_write_to_pm: bool
    first_name: str
    id: int
    is_premium: bool
    language_code: str
    last_name: str
    username: str


class InitDataIn(ArchitectonBase):
    auth_date: str
    hash: str
    query_id: str
    user: UserIn


class InitTonIn(ArchitectonBase):
    address: str = Field(default="UQAeV4crAaUoCJo5igUIzosJXcOjtb4W7ff7Qr0DrgXPRle_")
    # public_key: str = Field(default="full")
    signature: str | None = Field(default="full")


class AuthIn(ArchitectonBase):
    init_data_raw: InitDataIn | None = Field(default=None)
    init_ton: InitTonIn | None = Field(default=None)
    auth_type: str = Field(default="telegram")


class AuthOut(BaseModel):
    access_token: str
