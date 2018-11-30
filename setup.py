# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

INSTALL_REQUIREMENTS = [
    'Click>=6.0, <7.0',
    'click-log>=0.3.2, <0.4',
    'orator>=0.9, <1.0',
    'PyMySQL>=0.9, <1.0',
    'mutagen>=1.41, <1.50',
]

setup(
    author='Jonas Ohrstrom',
    author_email='ohrstrom@gmail.com',
    url='https://github.com/ohrstrom/audioasyl-archiver',
    name='AudioasylArchiver',
    version='0.0.2',
    description='...',
    packages=find_packages(),
    install_requires=INSTALL_REQUIREMENTS,
    entry_points='''
        [console_scripts]
        archiver=archiver:cli
    ''',
)
