from pydantic import Field

from ..base import ArchitectonBase


class TransactionMsgDataOut(ArchitectonBase):
    type: str | None = Field(default=None)
    text: str | None = Field(default=None)
    body: str | None = Field(default=None)
    init_state: str | None = Field(default=None)


class TransactionMsgInOut(ArchitectonBase):
    created_lt: int | None = Field(default=None)
    destination: str | None = Field(default=None)
    source: str | None = Field(default=None)
    value: str | None = Field(default=None)
    body_hash: str | None = Field(default=None)
    # msg_data: TransactionMsgDataOut | None = Field(default=None)


class TransactionItemOut(ArchitectonBase):
    hash: str | None = Field(default=None)
    utime: int | None = Field(default=None)
    amount: float | None = Field(default=None)
    amountUsd: float | None = Field(default=None)
    status: bool = Field(default=False)
    symbol: str | None = Field(default=None)
    commission_amount: float | None = Field(default=None)
    return_amount: float | None = Field(default=None)
    commission_usd: float | None = Field(default=None)
    return_usd: float | None = Field(default=None)
    comment: str | None = Field(default=None)
    icon_src: str | None = Field(default=None)
    icon_dst: str | None = Field(default=None)
    source: str | None = Field(default=None)
    destination: str | None = Field(default=None)


class TransactionItemCreateIn(ArchitectonBase):
    destination: str = Field(example="EQCkaGQTCUMUzu5b9IDYY4EjGI4hLIrnnKa5oAhgymxp9iqY")
    value: int = Field(example=7 * 10**6)
    seqno: int = Field(example=1)
    body: str | None = Field(default=None)


class TransactionItemCreateOut(ArchitectonBase):
    destination: str = Field()
    lt: int | None = Field(default=None)
    trx_id: str | None = Field(default=None)


ton_icon = (
    "PHN2ZyB3aWR0aD0iNDYiIGhlaWdodD0iNDYiIHZpZXdCb3g9IjAgMCA0NiA0NiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3Jn"
    "LzIwMDAvc3ZnIj4NCjxyZWN0IHdpZHRoPSI0NiIgaGVpZ2h0PSI0NiIgcng9IjIzIiBmaWxsPSIjMDA5OEVBIi8+DQo8cGF0aCBkPSJNMzAuOD"
    "U1NiAxMi42NUgxNS4xNDg2QzEyLjI2MDYgMTIuNjUgMTAuNDMwMSAxNS43NjUzIDExLjg4MyAxOC4yODM3TDIxLjU3NjkgMzUuMDg1OUMy"
    "Mi4yMDk0IDM2LjE4MjkgMjMuNzk0OCAzNi4xODI5IDI0LjQyNzMgMzUuMDg1OUwzNC4xMjMyIDE4LjI4MzdDMzUuNTc0MSAxNS43NjkzID"
    "MzLjc0MzYgMTIuNjUgMzAuODU3NiAxMi42NUgzMC44NTU2Wk0yMS41NjkgMzAuMDQ3MkwxOS40NTc4IDI1Ljk2MTNMMTQuMzYzOCAxNi44N"
    "TA2QzE0LjAyNzggMTYuMjY3NCAxNC40NDI5IDE1LjUyMDIgMTUuMTQ2NiAxNS41MjAySDIxLjU2N1YzMC4wNDkyTDIxLjU2OSAzMC4wNDcy"
    "Wk0zMS42MzY0IDE2Ljg0ODZMMjYuNTQ0NCAyNS45NjMzTDI0LjQzMzMgMzAuMDQ3MlYxNS41MTgzSDMwLjg1MzdDMzEuNTU3NCAxNS41MTg"
    "zIDMxLjk3MjUgMTYuMjY1NSAzMS42MzY0IDE2Ljg0ODZaIiBmaWxsPSJ3aGl0ZSIvPg0KPC9zdmc+DQo="
)
