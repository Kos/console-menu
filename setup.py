# !/usr/bin/env python

from setuptools import setup

setup(
    name='Console Menu',
    version='0.1-dev',
    description='build interactive menus using ncurses',
    author='Tomasz Wesołowski',
    author_email='kosashi@gmail.com',
    url='',
    packages=['console_menu'],
    setup_requires=[
        'pytest-runner',
        'six',
    ],
    tests_require=[
        'pytest',
    ],
)
