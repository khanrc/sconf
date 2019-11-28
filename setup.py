from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import setuptools


setuptools.setup(
    name='sconf',
    version='0.1',
    description='Simple config supporting CLI modification',
    install_requires=[
        'ruamel.yaml'
    ],
    url='https://github.com/khanrc/sconf',
    author='khanrc',
    author_email='khanrc@naver.com',
    license='MIT',
    packages=['sconf']
    #  package_dir={},
    #  packages=setuptools.find_packages(exclude=['tests']),
)
