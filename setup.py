# -*- coding: utf-8 -*-

import re
from setuptools import setup, find_packages

# determine version and the authors
code = open('sklikapiclient/__init__.py', 'r').read(1000)
version = re.search(r'__version__ = \'([^\']*)\'', code).group(1)
authors = eval(re.search(r'__authors__ = (\[[^\]\[]*\])', code).group(1))

setup(
    name='sklik-api-client',
    version=version,
    author=', '.join(authors),
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=[
        'requests',
    ],
    zip_safe=False,
)
