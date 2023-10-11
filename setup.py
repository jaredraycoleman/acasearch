from setuptools import setup
from coseto.__version__ import __version__

install_requires = []
with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')

setup(
    name="coseto",
    author="Jared Coleman",
    author_email="jaredraycoleman@gmail.com",
    version=__version__,
    packages=["coseto"],
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "coseto = coseto:main",
            "venues = coseto.conferences:main",
            "conferences = coseto.conferences:main",
            "conf = coseto.conferences:main",
            "authors = coseto.authors:main",
        ],
    },
)
