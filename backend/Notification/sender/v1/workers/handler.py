from models.notifications import DeliveryType, TemplateToSender
from v1.workers.generic_worker import Worker
from v1.workers.mail_worker import EmailWorker
from v1.workers.sms_worker import SMSWorker
from v1.workers.websocket_worker import WebSocketWorker

from core.logger import get_logger

logger = get_logger(__name__)


async def get_worker(data: TemplateToSender) -> Worker:
    logger.info('Get worker...')
    if data.delivery_type == DeliveryType.email.value:
        worker = EmailWorker
        logger.info('EmailWorker')
    elif data.delivery_type == DeliveryType.sms.value:
        worker = SMSWorker
        logger.info('SMSWorker')
    elif data.delivery_type == DeliveryType.push:
        worker = WebSocketWorker
        logger.info('WebSocketWorker')

    return worker
