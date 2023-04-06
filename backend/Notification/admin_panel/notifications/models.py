import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from .mixins import TimeStampedMixin, UUIDMixin

TEXT_FIELD_LEN = 255
MSG_FIELD_LEN = 4096
PROMO_FIELD_LEN = 4096


class EventType(models.TextChoices):
    WELCOME = 'welcome_message'
    NEW_CONTENT = 'new_content'
    NEW_LIKES = 'new_likes'
    PROMO = 'promo'


class Template(UUIDMixin, TimeStampedMixin):  # type: ignore[misc]

    title = models.CharField(_('title'), max_length=TEXT_FIELD_LEN, unique=True)
    event_type = models.CharField(max_length=TEXT_FIELD_LEN, choices=EventType.choices, default=EventType.NEW_CONTENT)
    subject = models.TextField(_('subject'), max_length=TEXT_FIELD_LEN, default='')
    template_files = models.FilePathField(path='templates/', allow_folders=True, allow_files=False)
    text_msg = models.TextField(max_length=MSG_FIELD_LEN, blank=True, default='')

    def __str__(self):
        return f'{self.event_type}:<{self.pkid}>'

    class Meta:
        verbose_name = _('Template')
        verbose_name_plural = _('Templates')
        ordering = ['title']


class Task(UUIDMixin, TimeStampedMixin):  # type: ignore[misc]
    class UserGroup(models.TextChoices):
        ALL_USER = 'all'
        GROUP_1 = 'group_1'
        GROUP_2 = 'group_2'
        GROUP_3 = 'group_3'
        GROUP_4 = 'group_4'

    title = models.CharField(_('title'), max_length=TEXT_FIELD_LEN, unique=True)
    template_pkid = models.ForeignKey(Template, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=TEXT_FIELD_LEN, choices=EventType.choices, default=EventType.NEW_CONTENT)
    user_group = models.CharField(max_length=TEXT_FIELD_LEN, choices=UserGroup.choices, default=UserGroup.ALL_USER)
    movie_id = models.CharField(max_length=TEXT_FIELD_LEN, blank=True, default='')
    text_to_promo = models.CharField(max_length=PROMO_FIELD_LEN, blank=True, default='')

    def __str__(self):
        return f'{self.title}:<{self.pkid}>'

    class Meta:
        ordering = ['title']


class ReviewInfo(UUIDMixin, TimeStampedMixin):  # type: ignore[misc]

    movie_id = models.UUIDField(default=uuid.uuid4, unique=True)
    author_id = models.UUIDField(default=uuid.uuid4, unique=True)
    review_id = models.UUIDField(default=uuid.uuid4, unique=True)
    likes_count = models.IntegerField(default=0)

    def __str__(self):
        return str(f'{self.review_id}')

    class Meta:
        ordering = ['review_id']


class ReviewStorage(UUIDMixin, TimeStampedMixin):  # type: ignore[misc]
    review_id = models.UUIDField(default=uuid.uuid4, unique=True)

    def __str__(self):
        return self.review_id

    class Meta:
        ordering = ['review_id']
