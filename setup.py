"""Setup file for structpp."""

from setuptools import setup, find_packages
from version import version

setup(
    name="structpp",
    packages=find_packages(exclude=("test",)),
    version=version,
    license="LGPLv3",
    install_requires=[
        "future>=0.16.0",
    ],
    description="A typechecking and shell generation program for python APIs",
    author="Arch",
    author_email="info@arch-iot.com",
    url="https://github.com/iotile/structpp",
    keywords=[""],
    classifiers=[
        "Programming Language :: Python",
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules"
        ],
    long_description="""\
Struct++
---------

Struct++ (also called structpp) provides a wrapper around the struct module in the python
standard library will additional support for packed bitfields and decoding structs into
a named tuple by annotated field names.

It is a 100%% drop in replacement for struct and its format string syntax is a superset of
the syntax used inside the struct module.
"""
)
