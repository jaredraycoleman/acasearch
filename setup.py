from setuptools import setup

setup(
    name='acasearch',
    author="Jared Coleman",
    author_email="jaredraycoleman@gmail.com",
    version='0.0.1',
    packages=['acasearch'],
    install_requires=[
        "pandas",
        "thefuzz[speedup]",
        "pyperclip",
    ],
    entry_points={
        'console_scripts': [
            'acasearch = acasearch:main',
            'venues = acasearch.conferences:main',
            'conferences = acasearch.conferences:main',
            'authors = acasearch.authors:main',
        ],
    }
)