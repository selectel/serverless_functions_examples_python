from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name="pdf_create",
    packages=["pdf_create"],
    entry_points={
        "console_scripts": [
            "pdf_create = pdf_create.pdf_create:main",
            ],
        },
    )
