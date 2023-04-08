from enum import Enum


class UserGroup(str, Enum):
    ALL_USER = 'all'
    GROUP_1 = 'group_1'
    GROUP_2 = 'group_2'
    GROUP_3 = 'group_3'
    GROUP_4 = 'group_4'

    def __repr__(self) -> str:
        return f'{self.value}'


class EventType(str, Enum):
    new_content = 'new_content'
    new_likes = 'new_likes'
    promo = 'promo'

    def __repr__(self) -> str:
        return f'{self.value}'


class DeliveryType(str, Enum):
    email = 'email'
    sms = 'sms'
    push = 'push'
