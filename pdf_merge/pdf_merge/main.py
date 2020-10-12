import os
import swiftclient
from io import BytesIO
from PyPDF2 import PdfFileMerger

# Connect to Selectel Cloud Storage.
conn = swiftclient.client.Connection(
    authurl='https://api.selcdn.ru/auth/v1.0',
    user=os.environ.get("SELECTEL_STORAGE_CLIENT_NAME"),
    key=os.environ.get("SELECTEL_STORAGE_CLIENT_PASSWORD"),
    auth_version=1,
)


def main(container_name, obj_a, obj_b):
    # Fetch objects.
    _, obj_a_body = conn.get_object(container_name, obj_a)
    _, obj_b_body = conn.get_object(container_name, obj_b)
    obj_a_bytes = BytesIO(obj_a_body)
    obj_b_bytes = BytesIO(obj_b_body)

    # Process objects.
    merger = PdfFileMerger()
    merger.append(obj_a_bytes, pages=(0, 3))
    merger.append(obj_b_bytes)

    # Generate new file name.
    file_name_a, _ = os.path.splitext(obj_a)
    file_name_b, _ = os.path.splitext(obj_b)
    obj_new_name = f"{file_name_a}_{file_name_b}_merged.pdf"

    # Upload new object.
    result_bytes = BytesIO()
    merger.write(result_bytes)
    result_bytes.seek(0)
    conn.put_object(container_name, obj_new_name, result_bytes)

    # Close streams.
    obj_a_bytes.close()
    obj_b_bytes.close()
    result_bytes.close()

    print(f"File {obj_new_name} created.")


if __name__ == '__main__':
    main("images", "selectel_habr_telegram.pdf", "jpeg.pdf")

"""
{
    "container_name": "images",
    "obj_a": "selectel_habr_telegram.pdf",
    "obj_b": "jpeg.pdf"
}
"""
