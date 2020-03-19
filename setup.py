import setuptools


LONG_DESC = open("README.md").read()
setuptools.setup(
    name='sconf',
    version='0.2.0',
    description='Simple config supporting CLI modification',
    long_description=LONG_DESC,
    long_description_content_type="text/markdown",
    install_requires=[
        'ruamel.yaml',
        'munch'
    ],
    url='https://github.com/khanrc/sconf',
    author='khanrc',
    author_email='khanrc@naver.com',
    license='MIT',
    packages=['sconf'],
    python_requires=">=3.6",
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ]
)
