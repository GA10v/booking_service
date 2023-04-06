from enum import Enum


class EventType(str, Enum):
    welcome = 'welcome_message'
    new_content = 'new_content'
    new_likes = 'new_likes'
    promo = 'promo'

    def __repr__(self) -> str:
        return f'{self.value}'


class DeliveryType(str, Enum):
    email = 'email'
    sms = 'sms'
    push = 'push'

    def __repr__(self) -> str:
        return f'{self.value}'
