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


class UserOut(ArchitectonBase):
    name: str
    session_id: UUID | None
    tg_id: int
    lang: str
    net: str
    address: str
