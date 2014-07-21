from distutils.core import setup
import os

version = '0.1.0dev'

setup(
    name='FrappeClient',
    version=version,
    author='Rushabh Mehta',
    author_email='rmehta@erpnext.com',
    download_url='https://github.com/jevonearth/frappe-client/archive/'+version+'.tar.gz',
    packages=['frappeclient',],
    install_requires=open(os.path.join(os.path.dirname(__file__), 'requirements.txt')).read().split(),
)
