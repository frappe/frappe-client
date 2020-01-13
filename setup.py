from setuptools import setup

version = '0.1.0dev'

with open('requirements.txt') as requirements:
    install_requires = requirements.read().split()

setup(
    name='frappeclient',
    version=version,
    author='Rushabh Mehta',
    author_email='rushabh@erpnext.com',
    packages=[
        'frappeclient'
    ],
    install_requires=install_requires,
    tests_requires=[
        'httmock<=1.2.2',
        'nose<=1.3.4'
    ],
)
