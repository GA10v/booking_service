import string
from random import choice

from flask import Blueprint, current_app, redirect, request
from flask_api import status

from core.config import settings
from models.shorturls import ShortUrl
from shortener_service import db

ID_LENGTH = settings.url_shortner.ID_LENGTH
URL_PREFIX = settings.url_shortner.PREFIX

bp = Blueprint('shortener', __name__, url_prefix=URL_PREFIX)


def generate_short_id(link_length: int):
    return ''.join(choice(string.ascii_letters + string.digits) for _ in range(link_length))


@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.get_json().get('url')
        if not url:
            return 'No url found', status.HTTP_400_BAD_REQUEST
        current_app.logger.debug(f'JSON_USER: {url}')
        short_id = generate_short_id(ID_LENGTH)
        new_link = ShortUrl(original_url=url, short_id=short_id)
        db.session.add(new_link)
        db.session.commit()
        short_url = request.host_url.rstrip('/') + URL_PREFIX + short_id
        return {'url': short_url}, status.HTTP_201_CREATED, {'ContentType': 'application/json'}


@bp.route('/<short_id>')
def get_full_link(short_id):
    link = ShortUrl.query.filter_by(short_id=short_id).first()
    if link:
        return redirect(link.original_url)
    else:
        return status.HTTP_404_NOT_FOUND
