from models import payloads
from models.template import TemplateFromDB
from service.render.protocol import RenderProtocol


class TextRender(RenderProtocol):
    async def render(self, template: TemplateFromDB, data: payloads.payload, **kwargs) -> str:
        if isinstance(data, payloads.NewUserContext):
            return None

        elif isinstance(data, payloads.NewReviewsLikesContext):
            return (
                template.text_msg.replace('{{user_name}}', data.user_name)
                .replace('{{movie_title}}', data.movie_title)
                .replace('{{likes}}', str(data.likes))
            )

        elif isinstance(data, payloads.NewContentContext):
            return template.text_msg.replace('{{user_name}}', data.user_name).replace(
                '{{movie_title}}',
                data.movie_title,
            )

        elif isinstance(data, payloads.NewPromoContext):
            return template.text_msg.replace('{{user_name}}', data.user_name).replace(
                '{{text_to_promo}}',
                data.text_to_promo,
            )

        elif isinstance(data, payloads.NewAnnounceContext):
            return (
                template.text_msg.replace('{{user_name}}', data.user_name)
                .replace('{{author_name}}', data.author_name)
                .replace('{{announce_title}}', data.announce_title)
                .replace('{{event_time}}', data.event_time)
                .replace('{{movie_title}}', data.movie_title)
                .replace('{{link}}', data.link)
            )

        elif isinstance(data, payloads.PutAnnounceContext):  # noqa: SIM114
            return (
                template.text_msg.replace('{{user_name}}', data.user_name)
                .replace('{{author_name}}', data.author_name)
                .replace('{{announce_title}}', data.announce_title)
                .replace('{{link}}', data.link)
            )

        elif isinstance(data, payloads.DeleteAnnounceContext):  # noqa: SIM114
            return (
                template.text_msg.replace('{{user_name}}', data.user_name)
                .replace('{{author_name}}', data.author_name)
                .replace('{{announce_title}}', data.announce_title)
                .replace('{{link}}', data.link)
            )

        elif isinstance(data, payloads.DoneAnnounceContext):
            return (
                template.text_msg.replace('{{user_name}}', data.user_name)
                .replace('{{announce_title}}', data.announce_title)
                .replace('{{link}}', data.link)
            )

        elif isinstance(data, payloads.DeleteBookingContext):
            return (
                template.text_msg.replace('{{user_name}}', data.user_name)
                .replace('{{guest_name}}', data.guest_name)
                .replace('{{announce_title}}', data.del_booking_announce_title)
            )

        elif isinstance(data, payloads.NewBookingContext):
            return (
                template.text_msg.replace('{{user_name}}', data.user_name)
                .replace('{{guest_name}}', data.guest_name)
                .replace('{{announce_title}}', data.new_booking_announce_title)
                .replace('{{link}}', data.link)
            )

        elif isinstance(data, payloads.StatusBookingContext):
            return (
                template.text_msg.replace('{{user_name}}', data.user_name)
                .replace('{{another_name}}', data.another_name)
                .replace('{{announce_title}}', data.announce_title)
                .replace('{{link}}', data.link)
            )
