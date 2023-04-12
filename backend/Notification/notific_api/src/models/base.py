from enum import Enum


class EventType(str, Enum):
    welcome = 'welcome_message'
    new_content = 'new_content'
    new_likes = 'new_likes'
    promo = 'promo'

    announce_new = 'announce_new'  #
    announce_put = 'announce_put'  #
    announce_done = 'announce_done'
    announce_delete = 'announce_delete'

    booking_new = 'booking_new'
    booking_status = 'booking_status'
    booking_delete = 'booking_delete'

    def __repr__(self) -> str:
        return f'{self.value}'
