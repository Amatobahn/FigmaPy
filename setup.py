from setuptools import setup, find_packages
from os import getcwd

setup(
    name='FigmaPy',
    version='2018.1.0',

    description='Figma API wrapper.',

    # Keywords
    keywords=['Amatobahn', 'Figma', 'pypi', 'package'],

    # The project's main homepage.
    url='https://www.IamGregAmato.com',

    # Author details.
    author='Greg Amato',
    author_email='amatobahn@gmail.com',

    # License
    license='Apache License v2.0',

    # Classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3 :: Only',
    ],

    # Packages
    packages=['FigmaPy'],

    # Required dependencies. Will be installed by pip
    # when the project is installed.
    install_requires=['requests'],
    extra_requires = {
        "async": ["aiohttp"]
    }
)
