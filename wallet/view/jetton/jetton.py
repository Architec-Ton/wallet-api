from pydantic import Field
from ..base import ArchitectonBase



class AdminAddJettonIn(ArchitectonBase):
    address: str = Field(description="Jetton master address")


