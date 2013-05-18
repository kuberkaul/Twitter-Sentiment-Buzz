#!/usr/bin/env python
#
# Xiao Yu - Montreal - 2010
# Based on googlemaps by John Kleint
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.


"""
Distutils setup script for pygeocoder module.
"""

import os
from distutils.core import setup

import pygeocoder

setup(
    name='pygeocoder',
    version=pygeocoder.VERSION,
    author='Xiao Yu',
    author_email='xiao@xiao-yu.com',
    url='http://code.xster.net/pygeocoder',
    download_url='http://code.xster.net/pygeocoder/downloads',
    description='Python interface for Google Geocoding API V3. Can be used to easily geocode, reverse geocode, validate and format addresses.',
    long_description=file(
        os.path.join(os.path.dirname(__file__), 'README.txt')
    ).read(),
    py_modules=['pygeocoder'],
    provides=['pygeocoder'],
    requires=['simplejson', 'functools'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='google maps ajax api geocode geocoding address gps json validation formatting',
    license='Lesser General Public License v3',
)