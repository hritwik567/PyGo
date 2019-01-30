from os import path

import setuptools

here = path.abspath(path.dirname(__file__))

setuptools.setup(
    name="lexer",
    version="0.0.1",
    author="Arpit, Ayush, Hritvik",
    author_email="ayushb268@gmail.com",
    description="Lexer for compiler project",
    url="https://github.com/ayush268/cs335a",
    packages=setuptools.find_packages(),
    license='Unlicensed',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=['numpy==1.16.0','ply==3.11','yattag==1.10.1'],
    entry_points={
        'console_scripts': [
            'lexer=lexer:main',
        ],
    },
)
