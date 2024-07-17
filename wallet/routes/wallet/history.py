import logging
import random
import uuid
from typing import List
from faker import Faker
from tonsdk.utils import Address

from wallet.auth import get_user
from wallet.controllers.ton_controller import TonController
from wallet.controllers.wallet_controller import WalletController
from wallet.models.base_transaction_model import BaseTransaction
from wallet.view.auth.user import UserOut
from wallet.view.wallet.info import InfoOut

fake = Faker()

from fastapi import APIRouter, Depends

router = APIRouter()


def load_transaction(tr: dict) -> BaseTransaction:
    transaction = BaseTransaction()
    temp = {
        'utime': tr['utime'],
        'fee': tr['fee'],
        'data': tr['data'],
        'hash': tr['transaction_id']['hash'],
        'lt': tr['transaction_id']['lt'],
        'in_msg': {
            'created_lt': tr['in_msg']['created_lt'],
            'source': self._process_address(tr['in_msg']['source']) if tr['in_msg']['source'] else '',
            'destination': self._process_address(tr['in_msg']['destination']) if tr['in_msg']['destination'] else '',
            'value': tr['in_msg']['value'],
            'msg_data': tr['in_msg']['msg_data']['text'] if 'text' in tr['in_msg']['msg_data'] else
            tr['in_msg']['msg_data']['body']
        },
        'out_msgs': [
            {
                'created_lt': out_msg['created_lt'],
                'source': self._process_address(out_msg['source']) if out_msg['source'] else '',
                'destination': self._process_address(out_msg['destination']) if out_msg['destination'] else '',
                'value': out_msg['value'],
                'msg_data': out_msg['msg_data']['text'] if 'text' in out_msg['msg_data'] else out_msg['msg_data'][
                    'body']
            }
            for out_msg in tr['out_msgs']
        ]
    }

    transaction.transaction_date = tr['utime']
    transaction.transaction_fee = tr['fee']
    transaction.transaction_hash = tr['hash']



@router.get("", response_model=InfoOut)
async def get_wallet_info(
    user: UserOut = Depends(get_user),
):
    logging.info(user)

    transactions = await TonController().get_transactions(Address(user.address))
    clear_transactions = []

    for t in transactions:
        clear_transactions.append(load_transaction(t))

    return {"current_wallet": 0, "wallets": clear_transactions}
