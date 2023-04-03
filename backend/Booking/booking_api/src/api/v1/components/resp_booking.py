from pydantic import BaseModel


class UpdatePayload(BaseModel):
    my_status: bool
