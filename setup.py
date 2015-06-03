# -*- coding: utf-8 -*-
"""
scikit-json
~~~~~~~~~
"""
from __future__ import with_statement
import ast
from setuptools import setup
from setuptools.command.install import install
from setuptools.command.test import test
from setuptools.extension import Extension
import sys
from textwrap import dedent


INCOMPATIBLE_PYTHON_VERSION_PLACEHOLDER = dedent('''
# -*- coding: utf-8 -*-
raise RuntimeError('Python {version} or later required.')
''').strip()


def requirements(filename):
    with open(filename) as f:
        return [x.strip() for x in f.readlines() if x.strip()]


def run_tests(self):
    raise SystemExit(__import__('pytest').main(['-v']))
test.run_tests = run_tests


setup(
    name='scikit-json',
    version='0.0.1',
    license='MIT',
    author='Sergey Romanov',
    author_email='xxsmotur@gmail.com',
    platforms='linux',
    packages=['scikit_json'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Debuggers',
    ],
    install_requires=requirements('requirements.txt'),
)

