#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from distutils.core import setup

setup(name='aiobtname',
    packages=['aiobtname'],
    version='0.1.1',
    author='François Wautier',
    author_email='francois@wautier.eu',
    description='Library for Name Request over Bluetooth with asyncio.',
    url='http://github.com/frawau/aiobtname',
    download_url='http://github.com/frawau/aiolifx/archive/aiobtname/0.1.1.tar.gz',  
    keywords = ['bluetooth', 'mac address', 'presence', 'automation'], 
    license='MIT',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5'
    ])