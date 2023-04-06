from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class NotificationToDelivery(BaseModel):
    id: UUID
    subject: str
    message_body: str
    recepient: str


class DeliveryType(str, Enum):
    email = 'email'
    sms = 'sms'
    push = 'push'

    def __repr__(self) -> str:
        return f'{self.value}'


class TemplateToSender(BaseModel):
    notification_id: str
    user_id: str | None
    subject: str
    email_body: str
    ws_body: str | None
    recipient: list[str]
    delivery_type: DeliveryType
