import aiohttp
from aiohttp.client_exceptions import ClientError
from models.events import Event
from models.payloads import NewReviewsLikesContext
from service.enrich.protocol import PayloadsProtocol
from utils.auth import _headers

from core.config import settings
from core.logger import get_logger

logger = get_logger(__name__)


class NewReviewLikesPayloads(PayloadsProtocol):
    def __init__(self, data: Event) -> None:
        self.data = data
        self.auth_endpoint = f'{settings.auth.uri}user_info/'
        self.admin_panel_endpoint = f'{settings.admin_panel.uri}movie/'
        self.ugc_endpoint = f'{settings.ugc.uri}review_info/'
        self._headers = _headers()

    async def payload(self) -> NewReviewsLikesContext:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f'{self.auth_endpoint}{self.data.context.author_id}',
                    headers=self._headers,
                ) as resp:
                    _user = await resp.json()

                async with session.post(
                    f'{self.admin_panel_endpoint}{self.data.context.movie_id}',
                    headers=self._headers,
                ) as resp:
                    _movie = await resp.json()

                async with session.post(
                    f'{self.ugc_endpoint}{self.data.context.movie_id}/{self.data.context.author_id}/{self.data.context.review_id}',  # noqa: E501
                    headers=self._headers,
                ) as resp:
                    _review = await resp.json()

        except ClientError as ex:  # noqa: F841
            logger.debug(f'Except <{ex}>')
            return None

        return NewReviewsLikesContext(
            user_id=_user.get('user_id'),
            user_name=_user.get('name'),
            email=_user.get('email'),
            phone_number=_user.get('phone_number'),
            telegram_name=_user.get('telegram_name'),
            delivery_type=_user.get('delivery_type'),
            movie_title=_movie.get('title'),
            review_id=_review.get('id'),
            likes=_review.get('likes'),
        )
