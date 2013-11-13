#!/usr/bin/env python
# -*- coding: utf-8

import os.path
import shutil
import tempfile
from nose.plugins.skip import SkipTest
from pywebstack import utils


__all__ = [
    'ALL_FORMULAE_NAMES', 'PROJECT_NAME', 'TEMP_DIR',
    'MockedArguments',
    'skipped', 'create_tempdir', 'cleanup_tempdir'
]


ALL_FORMULAE_NAMES = (
    'django', 'Django'
)

PROJECT_NAME = 'omega_directive'

TEMP_DIR = os.path.join(tempfile.gettempdir(), 'pywebstack_test')


class MockedArguments(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        self[key] = value


def create_tempdir():
    utils.mkdir_p(TEMP_DIR)


def cleanup_tempdir():
    shutil.rmtree(TEMP_DIR)


def skipped(f):
    """Decorator for instructing nose to skip the decorated test"""
    def _():
        raise SkipTest
    _.__name__ = f.__name__
    return _
