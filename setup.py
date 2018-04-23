# -*- coding: utf-8 -*-
from setuptools import setup
import os
import re

# Lovingly adapted from https://github.com/kennethreitz/requests/blob/39d693548892057adad703fda630f925e61ee557/setup.py#L50-L55
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eventflit/version.py'), 'r') as fd:
    VERSION = re.search(r'^VERSION = [\']([^\']*)[\']',
                        fd.read(), re.MULTILINE).group(1)

if not VERSION:
    raise RuntimeError('Ensure `VERSION` is correctly set in ./eventflit/version.py')

setup(
    name='eventflit',
    version=VERSION,
    description='A Python library to interract with the Eventflit API',
    url='https://github.com/eventflit/eventflit-http-python',
    author='Eventflit',
    author_email='support@eventflit.com',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    keywords='eventflit rest realtime websockets service',
    license='MIT',

    packages=[
        'eventflit'
    ],

    install_requires=[
        'six',
        'requests>=2.3.0',
        'urllib3',
        'pyopenssl',
        'ndg-httpsclient',
        'pyasn1'
    ],

    tests_require=['nose', 'mock', 'HTTPretty'],

    extras_require={
        'aiohttp': ['aiohttp>=0.20.0'],
        'tornado': ['tornado>=4.0.0']
    },

    package_data={
        'eventflit': ['cacert.pem']
    },

    test_suite='eventflit_tests',
)
