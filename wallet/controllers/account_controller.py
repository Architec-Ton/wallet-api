from ..models import AccountWalletConnection, Wallet
from ..models.account.account import Account
from ..view.auth.auth import AuthIn, InitDataIn


class AccountController:
    @staticmethod
    async def get_or_create(init_data_raw : InitDataIn ):
        if init_data_raw and init_data_raw.user and init_data_raw.user.id:
            account = await Account.get_or_none(id=int(init_data_raw.user.id))
            if account is not None:
                return account
            account_in = init_data_raw.user.model_dump()
            account = await Account.create(**account_in)
            return account

    @staticmethod
    async def get_or_create_wallet_connection(account: Account, wallet: Wallet):
        if account is not None and wallet is not None:
            connection = await AccountWalletConnection.get_or_none(account=account, wallet=wallet)
            if connection is not None:
                return account
            connection = await AccountWalletConnection.create(account=account, wallet=wallet)
            return connection
