from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in senbagam_paints/__init__.py
from senbagam_paints import __version__ as version

setup(
	name="senbagam_paints",
	version=version,
	description="Senbagam Paints",
	author="Thirvusoft",
	author_email="ts@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
