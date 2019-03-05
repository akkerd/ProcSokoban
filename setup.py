#!/usr/bin/env python3
from setuptools import setup, find_packages

from setuptools.command.install import install
setup(name='ProcSokoban',
      use_scm_version=True,
      description='Procedural generation algorithm for Sokoban levels',
      author='Diego Tobarra Gonzalez de Lopidana',
      author_email='dtbarra@gmail.com',
      install_requires=[],
      package_dir={'': 'src/searchclient'},
      packages=find_packages('src/'),
      #dependency_links = ['http://effbot.org/downloads/'],
    #   setup_requires=['pytest-runner','setuptools_scm','pytest'],
    #   tests_require=['pytest'],
    #   test_suite='test',
      )