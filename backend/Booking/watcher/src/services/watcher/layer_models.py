from uuid import UUID

from pydantic import BaseModel


class UpdateStatus(BaseModel):
    announcement_id: str | UUID
    status: bool
