from core.logger import get_logger
from models.notifications import DeliveryType, TemplateToSender
from v1.workers.generic_worker import Worker
from v1.workers.mail_worker import EmailWorker

logger = get_logger(__name__)


async def get_worker(data: TemplateToSender) -> Worker:
    logger.info('Get worker...')
    if data.delivery_type == DeliveryType.email.value:
        worker = EmailWorker()
        logger.info('EmailWorker')

    return worker
