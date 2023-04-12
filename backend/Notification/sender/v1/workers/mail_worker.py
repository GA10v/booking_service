"""Module to use to send email."""

from email.message import EmailMessage

from aiosmtplib import SMTP, SMTPException

from core.config import settings
from models.notifications import TemplateToSender
from v1.workers.generic_worker import Worker


class EmailWorker(Worker):
    def __init__(self) -> None:
        self.server = settings.email.SMTP_SERVER
        self.port = settings.email.SMTP_PORT
        self.user = settings.email.USER
        self.password = settings.email.PASSWORD
        self.client = SMTP(
            hostname=self.server,
            port=self.port,
            password=self.password,
            username=self.user,
        )

    async def connect(self):
        await self.client.connect()

    async def disconnect(self) -> None:
        await self.client.quit()

    async def _connect(self) -> bool:
        if not self.client.is_connected:
            await self.connect()
        return self.client.is_connected

    async def send_message(self, notification: TemplateToSender) -> None:
        message = EmailMessage()
        message['From'] = settings.email.USER
        message['To'] = notification.recipient
        message['Subject'] = notification.subject
        message.add_alternative(notification.email_body, subtype='html')
        try:
            if await self._connect():
                await self.client.sendmail(
                    sender=self.user,
                    recipients=notification.recipient,
                    message=message.as_string(),
                )
        except SMTPException:
            raise
        finally:
            await self.disconnect()
