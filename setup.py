import os
from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='Hausarbeit',
    version='v.1.0',
    packages=[''],
    url='',
    license='',
    author='Manuel Rauch, Anastasiia Vynohradova',
    author_email='manuel.rauch@uni-jena.de, anastasiia.vynohradova@uni-jena.de',
    description=''
    install_requires = required,
)
