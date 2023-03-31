from uuid import uuid4

import jwt

JWT_SECRET_KEY = '245585dbb5cbe2f151742298d61d364880575bff0bdcbf4ae383f0180e7e47dd'
JWT_ALGORITHM = 'HS256'

data = {
    'sub': str(uuid4()),
    'permissions': [0, 3],
    'is_super': True,
}
access_token = jwt.encode(data, JWT_SECRET_KEY, JWT_ALGORITHM)
print('user: ', data.get('sub'))  # noqa: T201
print('access_token: ', access_token)  # noqa: T201
