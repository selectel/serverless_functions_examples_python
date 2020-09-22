from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name="image_convert",
    packages=["image_convert"],
    entry_points={
        "console_scripts": [
            "image_convert = image_convert.image_convert:main",
            ],
        },
    )
