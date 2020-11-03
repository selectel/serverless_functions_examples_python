from io import BytesIO
import urllib.request
from pyzbar.pyzbar import decode
from PIL import Image


# For runtime "Python 3.7 with libraries for image processing" only.
# In standard python runtime it will not work because on dependency on libzbar.


def main(image_url):
    with BytesIO() as img_bytes:
        img_bytes.write(urllib.request.urlopen(image_url).read())
        decoded = decode(Image.open(img_bytes))
        return {"codes": [d.data.decode('utf-8') for d in decoded]}


if __name__ == "__main__":
    # Just for local testing.
    print(f"{main(image_url='https://418511.selcdn.ru/images/kabachki.jpg')}")
