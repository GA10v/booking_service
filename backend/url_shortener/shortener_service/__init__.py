from logging.config import dictConfig

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from core.config import settings

dictConfig(
    {
        'version': 1,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            },
        },
        'handlers': {
            'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'default',
            },
        },
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi'],
        },
    },
)

db = SQLAlchemy()


def create_app() -> Flask:
    global db
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DEBUG=settings.url_shortner.DEBUG,
        TESTING=settings.url_shortner.TESTING,
        SQLALCHEMY_DATABASE_URI=settings.db.uri,
    )

    db.init_app(app)
    migrate = Migrate(app, db)  # noqa: F841
    from blueprints import routes

    app.register_blueprint(routes.bp)
    app.app_context().push()

    return app
