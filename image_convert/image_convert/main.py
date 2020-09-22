import os
import swiftclient
from PIL import Image, ImageFilter
from io import BytesIO


def main(container_name, object_name, thumb_width=200, format='JPEG'):
    # Connect to Selectel Cloud Storage.
    conn = swiftclient.client.Connection(
        authurl='https://api.selcdn.ru/auth/v1.0',
        user=os.environ.get("SELECTEL_STORAGE_CLIENT_NAME"),
        key=os.environ.get("SELECTEL_STORAGE_CLIENT_PASSWORD"),
        auth_version=1,
    )

    # Generate new file name.
    file_name, file_ext = os.path.splitext(object_name)
    obj_new_name = f"{file_name}_w{thumb_width}.jpg"

    # Fetch image.
    _, obj_body = conn.get_object(container_name, object_name)
    obj_bytes = BytesIO(obj_body)

    # Apply operations to the image.
    img = resize_image_by_width(obj_bytes, thumb_width)
    img = img.convert('L')  # Convert to grayscale.
    img = img.filter(ImageFilter.BLUR)

    # Upload new image.
    img_bytes = image2bytes(img, format)
    conn.put_object(container_name, obj_new_name, img_bytes)

    # Close streams.
    obj_bytes.close()
    img_bytes.close()


# Resize PIL.Image with save proportions.
def resize_image_by_width(img_file, new_width):
    img_raw = Image.open(img_file)
    width, height = img_raw.size
    new_height = int(new_width * height / width)
    return img_raw.resize((new_width, new_height), Image.ANTIALIAS)


# Save PIL.Image into in-memory stream.
def image2bytes(img, format):
    image_content = BytesIO()
    img.seek(0)
    img.save(image_content, format=format)
    image_content.seek(0)
    return image_content


if __name__ == '__main__':
    main('images', 'test.png')
