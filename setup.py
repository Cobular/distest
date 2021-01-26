#!/usr/bin/env python3
# encoding: utf-8

from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="distest",
    version="0.5.0",
    description="Automate the testing of discord bots... With discord bots!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/JakeCover/distest",
    author="Jake Cover",
    author_email="python@jakecover.me",
    license="MIT",
    packages=["distest", "distest.TestInterface"],
    install_requires=["discord.py>=1.5.0"],
    zip_safe=False,
    classifiers=["Topic :: Software Development :: Testing :: Unit"],
    keywords=[
        "Discord",
        "Discord.py",
        "Unit Test",
        "Test",
        "Distest",
        "Discord Testing",
    ],
)
