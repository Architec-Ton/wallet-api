import json
import logging
import os

from fastapi import Depends, Request, Security
from fastapi.exceptions import HTTPException
from fastapi.security import APIKeyHeader, HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from wallet.config import ADMIN_AUTH_KEY
from wallet.errors import APIException
from wallet.view.auth.auth import AuthIn, InitDataIn
from wallet.view.auth.user import UserOut


import hashlib
import hmac
from urllib.parse import urlencode, parse_qsl

ALGORITHM = os.getenv("WALLET_API_ALGORITHM", "RS256")


admin_api = APIKeyHeader(name="ApiKey", auto_error=True)


async def api_admin_key_auth(key=Security(admin_api)):
    if key != ADMIN_AUTH_KEY:
        raise HTTPException(status_code=401)


def load_jwt_key(filename: str):
    with open(filename) as key_file:
        return key_file.read()


pubk = load_jwt_key("./security/api.crt")


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise APIException(status_code=401, error="Invalid authentication scheme.")
            payload = self.verify_jwt(credentials.credentials)
            if not payload:
                raise APIException(status_code=401, error="Invalid token or expired token.")
            return payload
        else:
            raise APIException(status_code=401, error="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        try:
            payload = jwt.decode(jwtoken, pubk, algorithms=["RS256"])
        except Exception as e:
            logging.error(e)
            payload = None

        return payload


def get_user(token_data=Depends(JWTBearer())) -> UserOut:
    user = UserOut.model_validate(
        {
            "name": token_data["name"] if "name" in token_data else None,
            "tgId": int(token_data["sub"]) if "sub" in token_data else None,
            "sessionId": token_data["iss"],
            "net": token_data["net"] if "net" in token_data else None,
            "lang": token_data["lang"] if "lang" in token_data else None,
            "address": token_data["address"] if "address" in token_data else None,
        }
    )
    logging.info(f"{user}")
    return user


def validate_telegram_init_data(init_data : AuthIn) -> InitDataIn | None:
    init_data_dict = dict(parse_qsl(init_data.init_data_raw, keep_blank_values=True))
    init_data_parsed_dict = { key: json.loads(value) if key=='user' else value for key, value in init_data_dict.items()}
    init_data_hash = init_data_dict.pop('hash', None)
    if not init_data_hash:
        return None

    bot_token = os.getenv("BOT_SECRET_KEY")
    data_check_array = [f"{key}={value}" for key, value in init_data_dict.items()]
    data_check_array.sort()
    secret_key = hmac.new(b'WebAppData', bot_token.encode('utf-8'), hashlib.sha256).digest()
    data_string = '\n'.join(data_check_array).encode('utf-8')
    calculated_hash = hmac.new(secret_key, data_string, hashlib.sha256).hexdigest()
    is_valid =  hmac.compare_digest(calculated_hash, init_data_hash)

    if not is_valid:
        return None

    return InitDataIn.model_validate(init_data_parsed_dict)

