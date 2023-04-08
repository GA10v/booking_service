"""Module to use to send email."""

import smtplib
from email.message import EmailMessage

from models.notifications import TemplateToSender
from v1.workers.generic_worker import Worker

from core.config import settings


class EmailWorker(Worker):
    """Mail Worker Logic."""

    def __init__(self) -> None:
        """Create instance of MAILWorker."""
        self.server = settings.email.SMTP_SERVER
        self.port = settings.email.SMTP_PORT
        self.user = settings.email.USER
        self.password = settings.email.PASSWORD
        self.connection: smtplib.SMTP | smtplib.SMTP_SSL
        if settings.email.SMTP_SSL:
            self.connection = smtplib.SMTP_SSL(self.server, self.port)
        else:
            self.connection = smtplib.SMTP(self.server, self.port)
        self.connection.login(self.user, self.password)

    def send_message(
        self,
        notification: TemplateToSender,
    ) -> None:
        """Send emails.

        Args:
            notification: TemplateToSender - includes reciepents, subject and body
        """
        message = EmailMessage()
        message['From'] = settings.email.USER
        message['To'] = ';'.join(notification.recipient)
        message['Subject'] = notification.subject
        message.add_alternative(notification.email_body, subtype='html')
        try:
            self.connection.sendmail(
                settings.email.USER,
                notification.recipient,
                message.as_string(),
            )
        finally:
            self.connection.close()
