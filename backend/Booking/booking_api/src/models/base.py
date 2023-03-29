from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class DefaultModel(BaseModel):
    id: str | UUID
    created: datetime
    modified: datetime

    def dict(self, *args, **kwargs) -> dict:
        _dict: dict = super().dict(*args, **kwargs)
        _dict['id'] = str(_dict['id'])
        _dict['created'] = _dict['created'].strftime('%Y-%m-%d %H:%M:%S')
        _dict['modified'] = _dict['modified'].strftime('%Y-%m-%d %H:%M:%S')
        return _dict
