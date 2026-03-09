from setuptools import setup

version = '0.1.2'

with open('requirements.txt') as requirements:
    install_requires = requirements.read().split()

setup(
    name='ctg-frappeclient',
    version=version,
    author='ctgalega',
    author_email='soporte@ctgalega.com',
    packages=[
        'ctgfrappeclient'
    ],
    install_requires=install_requires,
    tests_requires=[
        'httmock<=1.2.2',
        'nose<=1.3.4'
    ],
)
