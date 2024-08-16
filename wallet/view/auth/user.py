from uuid import UUID

from pydantic import Field

from ..base import ArchitectonBase


class UserIn(ArchitectonBase):
    allows_write_to_pm: bool | None = Field(default=None)
    first_name: str
    id: int | None = Field(default=None)
    is_premium: bool | None = Field(default=None)
    language_code: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
    username: str | None = Field(default=None)


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
