from gevent import monkey

monkey.patch_all()

from shortener_service import create_app  # noqa: E402

app = create_app()
