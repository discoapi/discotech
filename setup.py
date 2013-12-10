#!/usr/bin/env python

from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='discotech',
      version='0.4',
      description='python library to help working with social media providers',
      long_description=readme(),
      author='discoAPI Team',
      author_email='groovy@discoapi.com',
      url='http://github.com/storborg/funniest',
      packages=['discotech'],
      install_requires=[
          'requests-oauthlib',
      ],
      test_suite='nose.collector',
      tests_require=['nose', 'nose-cover3'],
      include_package_data=True)
