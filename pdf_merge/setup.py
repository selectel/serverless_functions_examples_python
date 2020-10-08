from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name="pdf_merge",
    packages=["pdf_merge"],
    entry_points={
        "console_scripts": [
            "pdf_merge = pdf_merge.pdf_merge:main",
            ],
        },
    )
