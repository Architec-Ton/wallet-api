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


def telegram_validate(init_data: AuthIn):

    data_check_string = (
        f"auth_date={init_data.init_data_raw.auth_date}\n"
        f"query_id={init_data.init_data_raw.query_id}\n"
        f"user={init_data.init_data_raw.user.username}"
        # f"user={ ''.join([ f"{k}={v}"for k, v in init_data.init_data_raw.user.items()])}\n"
    )

    signature = hmac.new(str("").encode(), msg=data_check_string.encode(), digestmod=hashlib.sha256).hexdigest()

    return signature
