import aiohttp
from aiohttp.client_exceptions import ClientError
from models.events import Event
from models.payloads import NewScoreContext
from service.enrich.protocol import PayloadsProtocol
from utils.auth import _headers

from core.config import settings
from core.logger import get_logger

logger = get_logger(__name__)


class NewScorePayloads(PayloadsProtocol):
    def __init__(self, data: Event) -> None:
        self.data = data
        self.auth_endpoint = f'{settings.auth.uri}user_info/'
        self.admin_panel_endpoint = f'{settings.admin_panel.uri}movie/'
        self.ugc_endpoint = f'{settings.ugc.uri}announcement/'
        self._headers = _headers()

    async def payload(self) -> NewScoreContext:
        try:
            async with aiohttp.ClientSession() as session:

                async with session.post(
                    f'{self.ugc_endpoint}{self.data.context.announcement_id}/{self.data.context.guest_id}',  # noqa: E501
                    headers=self._headers,
                ) as resp:
                    _review = await resp.json()

        except ClientError as ex:  # noqa: F841
            logger.debug(f'Except <{ex}>')
            return None

        return NewScoreContext(
            announcement_id=_review.get('announcement_id'),
            author_name=_review.get('author_name'),
            announce_title=_review.get('announcement_title'),
            movie_title=_review.get('announcement_title'),
            guest_name=_review.get('guest_name'),
        )
