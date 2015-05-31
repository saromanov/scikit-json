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


def get_version(filename):
    with open(filename) as f:
        tree = ast.parse(f.read(), filename)
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target, = node.targets
            if isinstance(target, ast.Name) and target.id == '__version__':
                return node.value.s
    raise ValueError('__version__ not found from {0}'.format(filename))


def requirements(filename):
    with open(filename) as f:
        return [x.strip() for x in f.readlines() if x.strip()]


def run_tests(self):
    raise SystemExit(__import__('pytest').main(['-v']))
test.run_tests = run_tests


setup(
    name='scikit-json',
    version=get_version('__init__.py'),
    license='BSD',
    author='Sergey Romanov',
    maintainer='Sergey Romanov',
    maintainer_email='xxsmotur@gmail.com',
    platforms='linux',
    packages=['scikit-json'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
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

