import hashlib
import hmac
import logging
import os

from fastapi import Depends, Request, Security
from fastapi.exceptions import HTTPException
from fastapi.security import APIKeyHeader, HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from wallet.config import ADMIN_AUTH_KEY
from wallet.errors import APIException
from wallet.view.auth.auth import AuthIn
from wallet.view.auth.user import UserOut

import hmac
import hashlib
from urllib.parse import unquote

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



# def validate(hash_str, init_data, token, c_str="WebAppData"):
#     """
#     Validates the data received from the Telegram web app, using the
#     method documented here:
#     https://core.telegram.org/bots/webapps#validating-data-received-via-the-web-app
#     hash_str - the has string passed by the webapp
#     init_data - the query string passed by the webapp
#     token - Telegram bot's token
#     c_str - constant string (default = "WebAppData")
#     """
#     init_data = sorted([ chunk.split("=")
#           for chunk in unquote(init_data).split("&")
#             if chunk[:len("hash=")]!="hash="],
#         key=lambda x: x[0])
#     init_data = "\n".join([f"{rec[0]}={rec[1]}" for rec in init_data])
#     secret_key = hmac.new(c_str.encode(), token.encode(),
#         hashlib.sha256 ).digest()
#     data_check = hmac.new( secret_key, init_data.encode(),
#         hashlib.sha256)
#     return data_check.hexdigest() == hash_str

def telegram_validate(hash_str, init_data: AuthIn, token):
    init_data_raw = init_data.init_data_raw.model_dump(exclude_unset=True)
    logging.info(init_data_raw)
    init_data_sorted = dict(sorted(init_data_raw.items()))

    logging.info(f"sortted: {init_data_sorted}")

    init_data_sorted = "\n".join([f"{k}={v}" for k, v in init_data_sorted.items()])
    # secret_key = hmac.new(c_str.encode(), token.encode(),
    #                       hashlib.sha256 ).digest()
    logging.info(f"sortted2: {init_data_sorted}")
    secret_key = token.encode()
    data_check = hmac.new( secret_key, init_data_sorted.encode(),
                           hashlib.sha256)
    logging.info(f"data_check.hexdigest(): {data_check.hexdigest()}")
    return data_check.hexdigest() == hash_str

    data_check_string = (
        f"auth_date={init_data.init_data_raw.auth_date}\n"
        f"query_id={init_data.init_data_raw.query_id}\n"
        f"user={init_data.init_data_raw.user.username}"
        # f"user={ ''.join([ f"{k}={v}"for k, v in init_data.init_data_raw.user.items()])}\n"
    )

    signature = hmac.new(str("").encode(), msg=data_check_string.encode(), digestmod=hashlib.sha256).hexdigest()

    return signature
