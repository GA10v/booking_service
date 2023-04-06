"""Class to implement late."""
import abc

from models.notifications import TemplateToSender


class Worker(abc.ABC):
    """Class to implement."""

    @abc.abstractmethod
    def send_message(self, notification: TemplateToSender) -> None:
        """Send general message.

        Args:
            recipients: list - List of email reciepents
            subject: str - Subject of email
            template: str - Template to compose email bodys
            fields: dict - Dictionary with fields to fill in template

        Raises:
            NotImplementedError: abstract instance
        """
        ...
