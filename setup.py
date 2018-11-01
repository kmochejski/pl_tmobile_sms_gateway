# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import pl_tmobile_sms_gateway

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name='pl_tmobile_sms_gateway',
    version=pl_tmobile_sms_gateway.__version__,
    description='Dead simple wrapper for T-Mobile Poland SMS gateway',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Krzysztof Mochejski',
    url='https://github.com/krzysztofmo/pl_tmobile_sms_gateway',
    packages=find_packages(exclude=('tests', 'docs')),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
)
