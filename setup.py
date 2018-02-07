#!/usr/bin/env python

import shlex
import sys
from setuptools import setup
from setuptools.command.test import test


class TestCmd(test):
    user_options = [
        ('pytest-args=', 'a', "Arguments to pass to pytest")
    ]

    def initialize_options(self):
        test.initialize_options(self)
        self.pytest_args = ''

    def run_tests(self):
        import pytest
        sys.exit(pytest.main(shlex.split(self.pytest_args)))


setup(
    cmdclass={
        'test': TestCmd,
    })
