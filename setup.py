from setuptools import find_packages, setup

setup(
    name='money',
    packages=find_packages(exclude=['scripts', 'tests']),
    version='0.01')
