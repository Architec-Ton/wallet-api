from ..models.account.account import Account
from ..view.auth.auth import AuthIn


class AccountController:

    @staticmethod
    async def get_or_create(auth_in: AuthIn):
        if auth_in.init_data_raw and auth_in.init_data_raw.user and auth_in.init_data_raw.user.id:
            account = await Account.get_or_none(id=int(auth_in.init_data_raw.user.id))
            if account is not None:
                return account
            account_in = auth_in.init_data_raw.user.model_dump()
            account = await Account.create(**account_in)
            return account
