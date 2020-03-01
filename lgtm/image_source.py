import requests
from io import BytesIO
from pathlib import Path


class LocalImage:
    def __init__(self, path):
        self.path = path

    def get_image(self):
        return open(self.path, 'rb')


class RemoteImage:
    """Get an image from URL"""
    def __init__(self, path):
        self._url = path

    def get_image(self):
        data = requests.get(self._url)
        return BytesIO(data.content)


class _LoremFlickr(RemoteImage):
    LOREM_FLICKR_URL = 'https://loremflickr.com'
    WIDTH = 800
    HEIGHT = 600

    def __init__(self, keyword):
        super().__init__(self._build_url(keyword))

    def _build_url(self, keyword):
        return (f'{self.LOREM_FLICKR_URL}/'
                f'{self.WIDTH}/{self.HEIGHT}/{keyword}')


KeywordImage = _LoremFlickr


def ImageSource(keyword):
    if keyword.startswith(('http://', 'https://')):
        return RemoteImage(keyword)
    elif Path(keyword).exists():
        return LocalImage(keyword)
    else:
        return KeywordImage(keyword)


def get_image(keyword):
    return ImageSource(keyword).get_image()