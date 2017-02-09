#!/usr/bin/env python3

from cuckoopy import __version__, __author__
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.rst') as f:
        readme = f.read()

setup(name='cuckoopy',
      version=__version__,
      description='Cuckoo Filter implementation in Python',
      long_description=readme,
      author=__author__,
      author_email='rajathagasthya@gmail.com',
      url='https://github.com/rajathagasthya/cuckoopy',
      license='MIT',
      packages=['cuckoopy'],
      install_requires=[],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6'
      ],
)
