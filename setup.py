#!/usr/bin/env python3.6
# coding: utf-8

import os
import sys
from setuptools import setup
from setuptools.command.test import test

try:
    from ConfigParser import ConfigParser   # py2
except ImportError:
    from configparser import ConfigParser   # py3


NAME = 'crispy-forms-decorator'
ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__)))


# Extract payload from the setup.cfg
setup_cfg = ConfigParser()
setup_cfg.read(os.path.join(ROOT, 'setup.cfg'))


# Customize a "test" command for the setup.py script
class TestCmd(test):
    user_options = [
        ('pytest-args=', 'a', "Arguments to pass to pytest")
    ]

    def initialize_options(self):
        test.initialize_options(self)
        self.pytest_args = ''

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        import shlex
        sys.exit(pytest.main(shlex.split(self.pytest_args)))


setup(name=NAME,
      version=setup_cfg.get('bumpversion:bumpversion', 'current_version'),
      author='Mikhail Porokhovnichenko',
      author_email='marazmiki@gmail.com',
      url='https://github.com/marazmiki/crispy-forms-decorator',
      description=(
          'A syntax sugar for django-crispy-forms that allows simplifying '
          'form creation with @crispy decorator'
      ),
      long_description=open(os.path.join(ROOT, 'README.rst')).read(),
      py_modules=['crispy_forms_decorator'],
      zip_safe=False,
      tests_require=[
          'pytest',
          'pytest-cov',
          'django',
          'django-crispy-forms',
          'flake8',
          'tox',
      ],
      license='BSD',
      include_package_data=True,
      cmdclass={
            'test': TestCmd,
      },
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Intended Audience :: Information Technology',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Topic :: Internet :: WWW/HTTP',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ])
