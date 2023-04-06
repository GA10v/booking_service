from uuid import uuid4

import jwt

from core.config import settings


def _headers() -> str:
    data = {
        'sub': str(uuid4()),
        'permissions': [0, 3],
        'is_super': True,
    }
    access_token = jwt.encode(data, settings.jwt.SECRET_KEY, settings.jwt.ALGORITHM)
    return {'Authorization': 'Bearer ' + access_token}
