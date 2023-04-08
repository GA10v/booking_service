"""Django settings for admin_panel project."""

from pathlib import Path

from split_settings.tools import include

from core.config import settings

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = settings.django.SECRET_KEY
DEBUG = settings.django.DEBUG
ALLOWED_HOSTS = settings.django.ALLOWED_HOSTS
include('components/_apps_middleware.py')
ROOT_URLCONF = 'admin_panel.urls'
WSGI_APPLICATION = 'admin_panel.wsgi.application'
include('components/_templates.py')
include('components/_database.py')
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
include('components/_localization.py')
STATIC_URL = 'static/'
STATIC_ROOT = '/code/static/'
MEDIA_URL = 'media/'
MEDIA_ROOT = '/code/media/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users.User'
CELERY_BROKER_URL = settings.rabbit.uri
CELERY_RESULT_BACKEND = 'rpc://'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_IMPORTS = ('notifications.tasks',)
TINYMCE_DEFAULT_CONFIG = {
    'height': '320px',
    'width': '960px',
    'menubar': 'file edit view insert format tools table help',
    'plugins': 'advlist autolink lists link image charmap print preview '
    'anchor searchreplace visualblocks code fullscreen insertdatetime '
    'media table paste code help wordcount template',
    'toolbar': 'undo redo | bold italic underline strikethrough | '
    'fontselect fontsizeselect formatselect | alignleft aligncenter '
    'alignright alignjustify | outdent indent |  numlist bullist checklist | '
    'forecolor backcolor casechange permanentpen formatpainter removeformat '
    '| pagebreak | charmap emoticons | fullscreen  preview save print | '
    'insertfile image media pageembed template link anchor codesample | '
    'a11ycheck ltr rtl | showcomments addcomment code',
    'custom_undo_redo_levels': 10,
    'browser_spellcheck': 'true',
    'contextmenu': 'false',
}
LOCALE_PATHS = (BASE_DIR / 'locale',)
