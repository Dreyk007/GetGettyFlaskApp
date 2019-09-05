from flask import request, send_file, abort
from app.models import User
from app import app, db
from GetGettyDownloader import GetGettyDownloader
from io import BytesIO
from functools import wraps


def token_required(func):
    """ Проверяем наличие токена """

    @wraps(func)
    def wrapped(*args, **kwargs):
        token = request.args.get('key')
        user = User.query.filter_by(token=token).first()

        if user is not None:
            return func(user, *args, **kwargs)
        else:
            abort(404)

    return wrapped


@app.route('/get_img', methods=['GET', 'POST'])
@token_required
def get_img(user):
    """ Принимаем ссылку на целевое изображение,
    скачиваем его, обрабатываем и возвращаем """
    img_url = request.args.get('img')
    if img_url and app.config['CHECK_API_URL_PATTERN'].match(img_url):
        img = GetGettyDownloader(img_url)

        user.downloads_count += 1
        db.session.commit()

        return send_file(BytesIO(img.get_converted()),
                         mimetype='image/jpeg',
                         as_attachment=True,
                         attachment_filename=img.filename)
    else:
        abort(404)
