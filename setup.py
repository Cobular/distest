#!/usr/bin/env python3
# encoding: utf-8

from setuptools import setup
from __about__ import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="distest",
    version=__version__,
    description="Automate the testing of discord bots... With discord bots!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/JakeCover/distest",
    author="Jake Cover",
    author_email="python@jakecover.me",
    license="MIT",
    packages=["distest", "distest.TestInterface"],
    install_requires=["discord.py>=1.5.0,<1.7.0"],
    zip_safe=False,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet',
        "Topic :: Software Development :: Testing :: Unit",
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    keywords=[
        "Discord",
        "Discord.py",
        "Unit Test",
        "Test",
        "Distest",
        "Discord Testing",
        "Testing"
    ],

)
