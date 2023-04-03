from datetime import datetime as dt

from shortener_service import db


class ShortUrl(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # noqa: VNE003
    original_url = db.Column(db.String(500), nullable=False)
    short_id = db.Column(db.String(20), nullable=False, unique=True)
    created_at = db.Column(db.DateTime(), default=dt.now(), nullable=False)
