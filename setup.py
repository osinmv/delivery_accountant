from distutils.core import setup
import os
import py2exe

folder = os.path.dirname(os.path.realpath(__file__))
with open("requirements.txt") as file:
    requirements = file.read().splitlines()
setup(
    name="Delivery Assistat",
    version="Pre-Alpha 0.8",
    description="Simple software that stores data, allows to edit it and generate reports",
    author="Maxim Osin",
    author_email="osinmv@gmail.com",
    install_requires=requirements,
    data_files=[("", ["LICENSE.txt"])],
    classifiers=[
        "Development Status :: Pre Alpha",
        "Topic :: Software",
        "License :: OSI Approved :: MIT License",
    ],
    windows=[{"script":"frontend.py"}],
    options={
        "py2exe": {
            "includes": ["backend.py", "pdf_writer.py"]
        }
    }
)
