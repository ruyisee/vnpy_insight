# -*- coding:utf-8 -*-
"""
@FileName  :setup.py
@Time      :2022/11/3 14:03
@Author    :fsksf
"""
import os
from setuptools import setup, find_packages
import codecs


def read(name):
    return codecs.open(os.path.join(os.path.dirname(__file__), name)).read()


setup(
    name='vnpy_insight',
    version='0.1.1',
    description='用于vnpy获取历史数据的华泰insight接口',
    long_description=read('README.md'),
    author='kangyuqiang',
    author_email='kangyuqiang123@gmail.com',
    packages=find_packages(),
    keywords=['vnpy', 'insight', '华泰', 'huatai'],
    install_requires=read('requirements.txt'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ]
)

