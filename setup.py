from setuptools import setup, find_packages
from os import getcwd

setup(
    name='FigmaPy',
    version='2018.1.0',

    description='Figma API wrapper.',

    # The project's main homepage.
    url='https://www.IamGregAmato.com',

    # Author details.
    author='Greg Amato',
    author_email='amatobahn@gmail.com',

    # License
    license='Apache License v2.0',

    # Classifiers
    classifiers=[
        # Project Stage:
        'Development Status :: 4 - Beta',

        # Intended for:
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Tools',

        # License:
        'License :: Apache License v2.0',

        # Supported Python versions:
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    # Keywords
    keywords='development tools api',

    # Packages
    packages=['FigmaPy'],

    # Required dependencies. Will be installed by pip
    # when the project is installed.
    install_requires=['requests'],
)
