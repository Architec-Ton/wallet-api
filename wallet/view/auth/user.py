from tonsdk.utils import Address

from ..base import ArchitectonBase, BaseModel
from pydantic import Field, field_validator
from uuid import UUID


class UserIn(ArchitectonBase):
    allows_write_to_pm: bool
    first_name: str
    id: int
    is_premium: bool
    language_code: str
    last_name: str
    username: str


class UserOut(ArchitectonBase):
    name: str | None
    session_id: UUID
    tg_id: int | None
    lang: str | None
    net: str | None
    address: str | None

    # @field_validator("address")
    # @classmethod
    # def address_validate(cls, v) -> Address | None:
    #     if isinstance(v, str):
    #         return Address(v)
