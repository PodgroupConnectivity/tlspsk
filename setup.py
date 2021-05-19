#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4
###
#
# Copyright (c) 2020-2021 Pod Group Ltd
# Authors : Kostiantyn Chertov <kostiantyn.chertov@podgroup.com>

from setuptools import setup

REQUIREMENTS = open('requirements.txt', 'rt').read().splitlines()
LONG_DESCRIPTION = open('README.md', 'rt').read()

setup(name='tlspsk',
      version='0.1.0',
      description='TLSv1.3 client fork, configured as PSK fork from tls1.3 client',
      long_description=LONG_DESCRIPTION,
      author='Kostiantyn Chertov',
      author_email='kostiantyn.chertov@podgroup.com',
      url='https://github.com/PodgroupConnectivity/tlspsk-client',
      packages=['tlspsk'],
      platforms=['win32', 'linux2'],
      license='MIT License',
      install_requires=REQUIREMENTS
)
