from setuptools import setup

setup(
    name='coseto',
    author="Jared Coleman",
    author_email="jaredraycoleman@gmail.com",
    version='0.0.2',
    packages=['coseto'],
    include_package_data=True,
    install_requires=[
        "pandas",
        "thefuzz[speedup]",
        "pyperclip",
    ],
    entry_points={
        'console_scripts': [
            'coseto = coseto:main',
            'venues = coseto.conferences:main',
            'conferences = coseto.conferences:main',
            'authors = coseto.authors:main',
        ],
    }
)