import requests

from generator.src.utils.auth import get_access_token


class AuthenticatedSession:
    def __init__(self):
        self.session = requests.Session()
        self._set_auth_header()

    def _set_auth_header(self):
        _token = get_access_token()
        self.session.headers.update({'Authorization': f'Bearer {_token}'})

    def get(self, url, **kwargs):
        resp = self.session.get(url=url, **kwargs)
        return resp.json()

    def post(self, url, payload=None, **kwargs):
        resp = self.session.post(url=url, data=payload, **kwargs)
        return resp.json()

    def close(self):
        self.session.close()
