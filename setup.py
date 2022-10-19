from setuptools import setup

setup(
    name='venues',
    author="Jared Coleman",
    author_email="jaredraycoleman@gmail.com",
    version='0.0.1',
    packages=['venues'],
    install_requires=[
        "pandas",
        "thefuzz[speedup]",
        "pyperclip",
    ],
    entry_points={
        'console_scripts': [
            'venues = venues:main',
        ],
    }
)