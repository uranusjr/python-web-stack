#!/usr/bin/env python
# coding: utf-8

import os.path
import sys
# StringIO must be tried first because Python 2 also has "io"
try:
    from StringIO import StringIO   # Python 2
except ImportError:
    from io import StringIO         # Python 3
from nose.tools import (
    eq_, with_setup, assert_raises, assert_true, assert_false, raises
)
from pywebstack.formulae import Formula
from pywebstack import utils
from . import *


def test_normalize():
    eq_(utils.normalize('..', 'tests', ), os.path.dirname(__file__))


def test_environment_object():
    env = utils._Environment({'answer': 42})
    eq_(env.answer, 42)
    eq_(env['answer'], 42)
    with assert_raises(AttributeError):
        env.fail
    with assert_raises(KeyError):
        env['fail']
    env.fail = 'epic'
    eq_(env['fail'], 'epic')


def test_chdir():
    current = os.getcwd()
    outer = os.path.abspath(utils.normalize(current, '..'))
    with utils.chdir('..'):
        eq_(os.getcwd(), outer)
    eq_(os.getcwd(), current)
    try:
        with(utils.chdir('you_shall_not_pass')):
            assert_true(False)      # Shouldn't enter here
    except OSError:
        eq_(os.getcwd(), current)


@with_setup(teardown=cleanup_tempdir)
def test_mkdir_p():
    target = os.path.join(TEMP_DIR, 'create_me')
    assert_false(os.path.exists(target))
    utils.mkdir_p(target)
    assert_true(os.path.exists(target))
    utils.mkdir_p(target)   # Should not fail even if the target exists
    assert_true(os.path.exists(target))


def test_run():
    stdout = sys.stdout
    try:
        sys.stdout = StringIO()
        eq_(utils.run('echo'), 0)
        eq_(sys.stdout.getvalue(), 'Running echo\n')
        sys.stdout = StringIO()
        eq_(utils.run('echo', quiet=True), 0)
        eq_(sys.stdout.getvalue(), '')
    finally:
        sys.stdout = stdout


def test_get_formula_class():
    for name in ALL_FORMULAE_NAMES:
        assert_true(issubclass(utils.get_formula_class(name), Formula))


@raises(utils.UnrecognizedFormulaError)
def test_get_formula_class_fail():
    utils.get_formula_class('rails')


def test_get_formula():
    for name in ALL_FORMULAE_NAMES:
        formula = utils.get_formula(name, 'test_project')
        assert_true(isinstance(formula, Formula))


if __name__ == '__main__':
    import nose
    nose.run(argv=[__file__, '--with-doctest', '-vv'])
