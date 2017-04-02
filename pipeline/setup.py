import os

from setuptools import setup

setup(
    name='pipeline',
    version='0.0.2',
    description='Luigi pipeline for pycon',
    packages=[
        'pipeline'
    ],
    install_requires=[
        'requests',
        'luigi',
        'python-daemon==2.1.1',
        'tornado<5,>=4.0',
    ]
)
