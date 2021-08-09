from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in ofstest/__init__.py
from ofstest import __version__ as version

setup(
	name='ofstest',
	version=version,
	description='OFS integration',
	author='mds',
	author_email='keith.yang@mdscsi.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
