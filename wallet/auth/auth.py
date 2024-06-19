import logging
import os
from fastapi.exceptions import HTTPException

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Request, Depends

from wallet.errors import APIException

ALGORITHM = os.getenv("WALLET_API_ALGORITHM", "RS256")


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
            if not self.verify_jwt(credentials.credentials):
                raise APIException(
                    status_code=401, error="Invalid token or expired token."
                )
            return credentials.credentials
        else:
            raise APIException(status_code=401, error="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = {"token": jwtoken}
            # payload = decode_jwt(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True

        return isTokenValid


async def get_user(token_data=Depends(JWTBearer())):
    logging.info(f"{token_data}")
    return None
