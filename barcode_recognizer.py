from io import BytesIO
import urllib.request
from pyzbar.pyzbar import decode
from PIL import Image

"""
Функция создана только для выполнения в среде "Python с библиотеками для
обработки изображений", так как зависит от предустановленной в ней
библиотеки libzbar (https://github.com/herbyme/zbar).

Function is for runtime "Python with libraries for image processing" only
because of dependency on libzbar (https://github.com/herbyme/zbar) preinstalled
only there.
"""


def main(image_url):
    """
    Функция ожидает на вход URL с изображением.

    Function expects an URL with image.
    """
    with BytesIO() as img_bytes:
        img_bytes.write(urllib.request.urlopen(image_url).read())
        decoded = decode(Image.open(img_bytes))
        return {"codes": [d.data.decode('utf-8') for d in decoded]}
