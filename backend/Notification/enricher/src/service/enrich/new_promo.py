import aiohttp
from aiohttp.client_exceptions import ClientError
from models.events import Event
from models.payloads import NewPromoContext
from service.enrich.protocol import PayloadsProtocol
from utils.auth import _headers

from core.config import settings
from core.logger import get_logger

logger = get_logger(__name__)


class NewPromoPayloads(PayloadsProtocol):
    def __init__(self, data: Event) -> None:
        self.data = data
        self.auth_endpoint = f'{settings.auth.uri}user_info/'
        self.admin_panel_endpoint = f'{settings.admin_panel.uri}movie/'
        self._headers = _headers()

    async def payload(self) -> NewPromoContext:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f'{self.auth_endpoint}{self.data.context.user_id}',
                    headers=self._headers,
                ) as resp:
                    _user = await resp.json()
        except ClientError as ex:  # noqa: F841
            logger.debug(f'Except <{ex}>')
            return None

        return NewPromoContext(
            user_id=_user.get('user_id'),
            user_name=_user.get('name'),
            email=_user.get('email'),
            phone_number=_user.get('phone_number'),
            telegram_name=_user.get('telegram_name'),
            delivery_type=_user.get('delivery_type'),
            text_to_promo=self.data.context.text_to_promo,
        )
