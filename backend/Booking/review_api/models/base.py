from datetime import datetime
from uuid import UUID
from typing import Any

import orjson
from pydantic import BaseModel


def orjson_dumps(obj_to_serialize: Any, *, default: Any) -> Any:
    return orjson.dumps(obj_to_serialize, default=default).decode()


class DefaultModel(BaseModel):
    id: str | UUID
    created: datetime
    modified: datetime

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps

    def dict(self, *args, **kwargs) -> dict:
        _dict: dict = super().dict(*args, **kwargs)
        _dict['id'] = str(_dict['id'])
        _dict['created'] = _dict['created'].strftime('%Y-%m-%d %H:%M:%S')
        _dict['modified'] = _dict['modified'].strftime('%Y-%m-%d %H:%M:%S')
        return _dict
