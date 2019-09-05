import random
from io import BytesIO
import requests
from PIL import Image

from RWfile import ReadWriteFile


class GetGettyDownloader:
    def __init__(self, orig_url):
        """ Инициализация """
        self.orig_url = orig_url

    @property
    def __wm_urls(self):
        """ Генерируем необходимые URL-ы """
        # Получаем URL без параметров:
        c0 = self.orig_url.rfind('?')
        # Добавляем к URL размер:
        url_w_size = f'{self.orig_url[:c0]}?s=2048x2048'

        # Генерируем URL-ы c разными копирайтами:
        # getty
        wm1_url = f'{url_w_size}&w=5'
        # wire
        wm2_url = f'{url_w_size}&w=125'

        return wm1_url, wm2_url

    @property
    def filename(self):
        """ Получаем имя файла из URL """
        c0 = self.orig_url.rfind('/')
        c1 = self.orig_url.rfind('?', c0)

        return f'{self.orig_url[c0 + 1:c1]}.jpg'

    @property
    def __random_user_agent(self):
        """ Получаем случайный User-Agent """
        user_agents = ReadWriteFile('UserAgents.txt').read()

        return random.choice(user_agents)

    def __download(self, url):
        """ Скачиваем изображение """
        request_content = requests.get(url, headers={'User-Agent': self.__random_user_agent}, timeout=15).content

        return BytesIO(request_content)

    def get_converted(self):
        """ Немного магии и генерация готового изображения, возвращается BytesIO """

        # Скачиваем исходники:
        wm_url1, wm_url2 = self.__wm_urls
        wm1_img_bytes = self.__download(wm_url1)
        wm2_img_bytes = self.__download(wm_url2)

        # Открываем их с Pillow:
        wm1_img = Image.open(wm1_img_bytes)
        wm2_img = Image.open(wm2_img_bytes)

        # Делаем некоторые вычисления геометрии:
        width, height = wm1_img.size
        borders = _calc_borders(width, height)

        # Сшиваем исходники и получаем готовое изображение:
        done_img = _crop_and_paste_img(wm1_img, wm2_img, borders)
        done_img_bytes = BytesIO()
        done_img.save(done_img_bytes, format='JPEG', quality=95)

        # return done_img_bytes
        return done_img_bytes.getvalue()


def _calc_borders(width, height):
    """ Высчитываем геометрию для преобразования """
    banner_width = 300
    banner_height = 90

    seek_width = (width - banner_width) / 2
    seek_height = (height - banner_height) / 2

    left = _pixels_to_int_with_seek(seek_width)
    top = _pixels_to_int_with_seek(seek_height)
    right = int(width - seek_width)
    bottom = int(height - seek_height)

    assert (left + right == width)
    assert (top + bottom == height)

    return left, top, right, bottom


def _pixels_to_int_with_seek(fl):
    """ Преобразовываем float в int, с учётом условий """
    decim = str(fl).split('.')[1]

    if decim == '0':
        fl = int(fl)
    elif decim == '5':
        fl = int(fl) + 1
    else:
        raise AssertionError

    return fl


def _crop_and_paste_img(wm1_img, wm2_img, borders):
    """ Склеивание изображений из разных источников """
    img_cropped_center = wm1_img.crop(borders)
    wm2_img.paste(img_cropped_center, borders)

    return wm2_img
