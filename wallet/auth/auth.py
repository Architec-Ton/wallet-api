import logging
import os
from fastapi.exceptions import HTTPException

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Request, Depends
from jose import jwt

from wallet.errors import APIException
from wallet.view.auth.user import UserOut

ALGORITHM = os.getenv("WALLET_API_ALGORITHM", "RS256")

def load_jwt_key(filename: str):
    with open(filename) as key_file:
        return key_file.read()



pubk = load_jwt_key('./security/api.crt')

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise APIException(
                    status_code=401, error="Invalid authentication scheme."
                )
            payload = self.verify_jwt(credentials.credentials)
            if not payload:
                raise APIException(
                    status_code=401, error="Invalid token or expired token."
                )
            return payload
        else:
            raise APIException(status_code=401, error="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        try:
            payload = jwt.decode(jwtoken, pubk, algorithms=['RS256'])
        except Exception as e:
            logging.error(e)
            payload = None

        return payload


def get_user(token_data=Depends(JWTBearer())) -> UserOut:

    user =  UserOut.model_validate({
        "name" : token_data['name'],
        "tgId": int(token_data['sub']),
        "sessionId":token_data['iss'],
        "net": token_data['net'],
        "lang": token_data['lang'],
        "address": token_data['address'],
        }
    )

    logging.info(f"{user}")
    return user
