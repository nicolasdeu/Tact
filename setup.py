#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

###
# Project          : Tact
# FileName         : setup.py
# -----------------------------------------------------------------------------
# Author           : Nicolas Deutschmann
# E-Mail           : nicolas.deutschmann@abase.fr
##

# Add sources of Tact in path
import sys
source_dir = "Sources"
sys.path.append(source_dir)

from os import path

from codecs import open

from setuptools import setup
from setuptools import find_packages

from tact import util


here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="Tact",
    version=util.find_version(),
    description="Tact is a command-line program for storing contacts into "
                "an address book.",
    long_description=long_description,
    author="Nicolas Deutschmann",
    author_email="nicolas.deutschmann@abase.fr",
    keywords=["Address Book", "Contact"],
    package_dir={'': source_dir},
    packages=find_packages(source_dir),
    entry_points={
        'console_scripts': [
            'tact = tact:main',
        ],
    },
    license="Proprietary License",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Environment :: Console",
        "Intended Audience :: Other Audience",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Topic :: Office/Business",
        "Topic :: Utilities",
    ],
    install_requires=[],
    data_files=[
        ('Config', ['Config/logging.conf']),
    ],
    test_suite='nose.collector',
    tests_require=['nose>=1.3.0'],
)

# EOF
