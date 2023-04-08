import json
from contextlib import suppress

import asyncclick as click
import trio
from models.db.notifications import Notification
from models.notifications import TemplateToSender
from sqlalchemy import create_engine, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session
from trio_websocket import ConnectionClosed, serve_websocket
from v1.workers.generic_worker import Worker

from core.config import settings
from core.logger import get_logger

WEBSOCKET_CHECK_TIMEOUT = 10

logger = get_logger(__name__)


class WebSocketWorker(Worker):
    def __init__(self, uri: str = settings.postgres.uri):
        self.settings = uri
        self.engine = create_engine(self.settings)

    def send_message(self, notification: TemplateToSender):
        with Session(self.engine) as session:
            notification_object = Notification(
                id=notification.notification_id,
                user_id=notification.user_id,
                ws_body=notification.ws_body,
                subject=notification.subject,
            )
            session.add(notification_object)
            session.commit()


async def notification_server(request):
    engine = create_async_engine(settings.postgres.uri)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    ws = await request.accept()
    # getting user_id
    user_id = None
    while True:
        try:
            with trio.move_on_after(WEBSOCKET_CHECK_TIMEOUT):
                message = await ws.get_message()
                if message.lower() == 'list_notifications':
                    stmt = select(Notification).filter_by(user_id=user_id)
                    async with async_session() as session:
                        messages_list = [obj.as_dict() for obj in session.execute(stmt).scalars.all()]
                    await ws.send_message(json.dumps(messages_list))
            continue
        except ConnectionClosed:
            break


@click.command()
@click.option('--port', default=8000, help='Port to listen')
@click.option('--ip', default='127.0.0.1', help='Address to use')
async def main(port: int, ip: str):
    await serve_websocket(
        notification_server,
        ip,
        port,
        ssl_context=None,
    )


if __name__ == '__main__':
    with suppress(KeyboardInterrupt):
        main(_anyio_backend='trio')
