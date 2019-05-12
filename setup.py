#!/usr/bin/env python3
# encoding: utf-8

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='distest',
      version='0.1.0dev',
      description='Automate the testing of discord bots',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://github.com/JacobCover/distest',
      author='Jake Cover',
      author_email='python@jakecover.me',
      license='MIT',
      packages=['distest'],
      install_requires=['discord.py'],
      zip_safe=False
)
