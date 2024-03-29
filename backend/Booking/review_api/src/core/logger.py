import logging
import logging.config

from src.core.config import settings

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_DEFAULT_HANDLERS = [
    'console',
]


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {'format': LOG_FORMAT},
        'default': {
            '()': 'uvicorn.logging.DefaultFormatter',
            'fmt': '%(levelprefix)s %(message)s',
            'use_colors': None,
        },
        'access': {
            '()': 'uvicorn.logging.AccessFormatter',
            'fmt': "%(levelprefix)s %(client_addr)s - '%(request_line)s' %(status_code)s",
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'default': {
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'access': {
            'formatter': 'access',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'logstash': {
            'class': 'logstash.LogstashHandler',
            'level': 'INFO',
            'host': settings.logging.LOGSTASH_HOST,
            'port': settings.logging.LOGSTASH_PORT,
        },
    },
    'loggers': {
        'fast_api_service': {
            'handlers': ['logstash', 'console'],
            'level': 'INFO',
        },
        'uvicorn.error': {
            'level': 'INFO',
            'handlers': ['logstash', 'console'],
        },
        'uvicorn.access': {
            'handlers': ['access', 'logstash', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    'root': {
        'level': 'INFO',
        'formatter': 'verbose',
        'handlers': LOG_DEFAULT_HANDLERS,
    },
}
logging.config.dictConfig(LOGGING)


def get_logger(_name_: str) -> logging.Logger:
    """Логгер."""
    return logging.getLogger(_name_)
