from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import setuptools


VERSION = '0.1'


setuptools.setup(
    name='sconf',
    version=VERSION,
    description='Simple config supporting CLI modification',
    install_requires=[
        'ruamel.yaml'
    ],
    url='https://github.com/khanrc/sconf',
    author='khanrc',
    author_email='khanrc@naver.com',
    license='MIT',
    packages=['sconf'],
    python_requires=">=3.6",
    tests_require=["pytest"]
)
