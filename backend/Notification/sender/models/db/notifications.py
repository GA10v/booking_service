from sqlalchemy import String
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

TEXT_FIELD_LEN = 255


Base = declarative_base()


class Notification(Base):
    __tablename__ = 'websocket_notifications'

    id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(String(TEXT_FIELD_LEN))
    ws_body: Mapped[str] = mapped_column(String(TEXT_FIELD_LEN))
    subject: Mapped[str] = mapped_column(String(TEXT_FIELD_LEN))
