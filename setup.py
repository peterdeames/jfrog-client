"""
Package setup for the egg
"""

import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='jfrog-client',
    version='1.0.0',
    description='Package that creates simple APIs to interact with Jfrog',
    packages=setuptools.find_packages(),
    url='https://github.com/peterdeames/jfrog-client',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='jfrog',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Utilities',
        'Operating System :: OS Independent'
    ],
    install_requires=[
        'requests',
        'tabulate',
        'logging',
        'packaging'
    ]
)
