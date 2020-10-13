import os
import swiftclient
import cairosvg
from io import BytesIO
from jinja2 import Template
import qrcode
from qrcode.image.svg import SvgPathImage as QrCodeSvgPathImageFactory
try:
    import lxml.etree as ET
except ImportError:
    import xml.etree.ElementTree as ET


COUPONS_CONTAINER = os.environ.get("COUPONS_CONTAINER", "images")


def _read_template(file_name):
    template_file = open(file_name)
    template = Template(template_file.read())
    template_file.close()
    return template


def _create_qr_code(url):
    code = qrcode.make(url, box_size=1000,
                       image_factory=QrCodeSvgPathImageFactory)
    return ET.tostring(code.make_path(), encoding='unicode')


svg_template = _read_template('./pdf_create/coupon.svg')

# Connect to Selectel Cloud Storage.
storage = swiftclient.client.Connection(
    authurl='https://api.selcdn.ru/auth/v1.0',
    user=os.environ.get("SELECTEL_STORAGE_CLIENT_NAME"),
    key=os.environ.get("SELECTEL_STORAGE_CLIENT_PASSWORD"),
    auth_version=1,
)


def main(coupon):
    coupon = coupon.upper()

    # Generate QR code.
    url = 'https://selectel.ru?utm_source=github.com' \
          '&utm_medium=pdf_create_from_svg&utm_campaign=coupon' \
          f'&coupon={coupon}'
    qr_svg = _create_qr_code(url)

    # Generate coupon.
    coupon_svg = svg_template.render(name=coupon,
                                     qr_code=qr_svg,
                                     discount="-30%")
    coupon_pdf = BytesIO()
    cairosvg.svg2pdf(bytestring=bytearray(coupon_svg.encode("utf-8")),
                     write_to=coupon_pdf,
                     scale=2)

    # Upload new image.
    coupon_pdf.seek(0)
    file_name = f"coupon-{coupon}.pdf"
    storage.put_object(COUPONS_CONTAINER, file_name, coupon_pdf)

    # Close streams.
    coupon_pdf.close()
    return file_name


if __name__ == '__main__':
    main("EXAMPLEONLY")
