from core.config import settings

POSTGRES_DB_PORT = 5432

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': settings.django.POSTGRES_DB,
        'USER': settings.django.POSTGRES_USER,
        'PASSWORD': settings.django.POSTGRES_PASSWORD,
        'HOST': settings.django.POSTGRES_HOST,
        'PORT': settings.django.POSTGRES_PORT,
        'OPTIONS': {
            'options': '-c search_path=voucher_app,public',
        },
    },
}
