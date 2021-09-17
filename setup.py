import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

BASE = os.path.realpath(os.path.dirname(__file__))

with open(os.path.join(BASE, "requirements.txt"), "r") as f:
    requirements = f.readlines()

with open(os.path.join(BASE, "VERSION"), "r") as f:
    version = f.read()

with open(os.path.join(BASE, "LICENSE"), "r") as f:
    license = f.read()

setup(
    name="time_splitter",
    version=version,
    description="Time Splitter GUI",
    author="Mitch Gates",
    author_email="mitchgates@outlook.com",
    url="https://github.com/mistergates/time_splitter",
    license=license,
    packages=["time_splitter", "time_splitter.bin"],
    install_requires=requirements,
    entry_points={"console_scripts": ["timesplitter=time_splitter.bin.time_splitter:main"]},
)
