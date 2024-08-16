from tonsdk.utils import Address
from tortoise import fields
from tortoise.models import Model


class BaseTonAddress(Model):
    address_raw = fields.CharField(max_length=128, null=True, default=None, index=True)
    address_hash = fields.CharField(max_length=128, null=True, default=None, index=True)
    address_base64: str = fields.CharField(max_length=48, null=True, default=None, index=True)

    mainnet = fields.BooleanField(default=True, index=True)
    network: str = fields.CharField(max_length=16, null=True, default="ton")

    @staticmethod
    def _address_setter(value):
        if isinstance(value, str):
            value = Address(value)
        if isinstance(value, Address):
            address_base64 = value.to_string(is_user_friendly=True, is_bounceable=True)
            address_raw = value.to_string(is_user_friendly=False)
            address_hash = value.hash_part.hex()
            mainnet = not value.is_test_only

            return address_base64, address_raw, address_hash, mainnet
        return None, None, None, True

    @property
    def address(self) -> Address:
        return Address(self.address_base64)

    @address.setter
    def address(self, value):
        self.address_base64, self.address_raw, self.address_hash, self.mainnet = BaseTonAddress._address_setter(value)

    @classmethod
    async def get_by_address(cls, owner_addres: Address):
        return await cls.get_or_none(address_hash=owner_addres.hash_part.hex())
