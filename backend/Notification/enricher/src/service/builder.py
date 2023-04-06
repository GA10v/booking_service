from abc import ABC, abstractmethod

from models.payloads import NewUserContext, payload
from models.template import TemplateFromDB, TemplateToSender
from service.render.mail_render import JiniaRender
from service.render.ws_render import TextRender


class BuilderProtocol(ABC):
    @abstractmethod
    async def build(self, data: payload, template: TemplateFromDB, **kwargs):
        ...


class BuilderService(BuilderProtocol):
    async def build(self, data: payload, template: TemplateFromDB, notification_id: str, **kwargs):
        if isinstance(data, NewUserContext):
            return TemplateToSender(
                notification_id=notification_id,
                user_id=None,
                subject=template.subject,
                email_body=await JiniaRender().render(template=template, data=data),
                ws_body=None,
                recipient=[data.email],
                delivery_type=data.delivery_type,
            ).dict()

        return TemplateToSender(
            notification_id=notification_id,
            user_id=data.user_id,
            subject=template.subject,
            email_body=await JiniaRender().render(template=template, data=data),
            ws_body=await TextRender().render(template=template, data=data),
            recipient=[data.email],
            delivery_type=data.delivery_type,
        ).dict()
