#!/usr/bin/env python
# coding: utf-8

import os.path
from nose.tools import eq_, assert_raises, assert_true, raises
from pywebstack.formulae import Formula
from pywebstack import utils
from . import ALL_FORMULAE_NAMES


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
