from setuptools import setup

version = '1.1.0dev'

with open('requirements.txt') as requirements:
    install_requires = requirements.read().split()

setup(
    name='pyfrappeclient',
    version=version,
    author='Team RCN',
    author_email='teamrcn@gmx.com',
    packages=[
        'frappeclient'
    ],
    install_requires=install_requires,
    tests_requires=[
        'httmock<=1.2.2',
        'nose<=1.3.4'
    ],
)
