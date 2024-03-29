import re
from http import HTTPStatus
from typing import Optional

import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import DecodeError, ExpiredSignatureError

from core.config import settings
from core.logger import get_logger

logger = get_logger(__name__)


class AuthHandler:
    security = HTTPBearer()
    secret = settings.jwt.SECRET_KEY

    async def decode_token(self, token):
        try:
            token = jwt.decode(token, self.secret, algorithms=settings.jwt.ALGORITHM)
            return {
                'user_id': token['sub'],
                'claims': {
                    'permissions': token['permissions'],
                    'is_super': token['is_super'],
                },
            }
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Signature has expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Token is invalid')

    async def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return await self.decode_token(auth.credentials)


def _parse_auth_header(
    auth_header: str,
    access_token_title: str = 'Bearer',
    refresh_token_title: str = 'Refresh',
) -> dict:
    """Parses a Authorization/Authentication http header and extracts the access + request
    tokens if present.
    Example header:
    "Authorization: Bearer AAA, Refresh BBB"
    """

    def _match_token(token_title: str) -> Optional[str]:
        expression = re.escape(token_title) + r' ([^\s,]+)'
        match = re.search(expression, auth_header)
        try:
            return match.group(1)
        except (AttributeError, IndexError):
            return None

    return {'access_token': _match_token(access_token_title), 'refresh_token': _match_token(refresh_token_title)}


def parse_header(auth_header) -> dict:
    jwt_token = _parse_auth_header(auth_header)['access_token']
    try:
        decoded_jwt = jwt.decode(
            jwt=jwt_token,
            key=settings.jwt.SECRET_KEY,
            algorithms=[settings.jwt.ALGORITHM],
        )
        return {
            'user_id': decoded_jwt.identity,
            'claims': decoded_jwt.additional_claims,
        }
    except (DecodeError, ExpiredSignatureError) as ex:
        logger.exception('Error while decode access_token: \n %s', str(ex))
