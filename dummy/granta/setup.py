"""Dummy implementation of the granta distribution.
This is used by the CI to simulate the installation
of the granta distribution that is not open to release
"""

import os
from setuptools import setup, find_packages

VERSION = "0.0.2"


def write_version_py():
    filename = os.path.join(
        os.path.dirname(__file__),
        'granta',
        'version.py')
    ver = "__version__ = '{}'\n"
    with open(filename, 'w') as fh:
        fh.write(ver.format(VERSION))


write_version_py()

setup(
    name="granta",
    version=VERSION,
    packages=find_packages(),
)
