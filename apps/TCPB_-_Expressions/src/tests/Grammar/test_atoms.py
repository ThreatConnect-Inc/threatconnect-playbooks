# -*- coding: utf-8 -*-
"""Test atomic values from expression Parser"""

from inspect import isclass

import math

import pytest
from lark_expr import Expression

# pylint: disable=attribute-defined-outside-init


def fsum(*args):
    """sum"""
    return math.fsum(args)


def psum(*args):
    """sum"""
    return sum(args)


class exactly(object):
    """An identity match with type"""

    def __init__(self, value):
        """init"""
        self.value = value

    def __eq__(self, other):
        """exact comparision"""
        if self.value != other:
            return False
        if self.value.__class__ != other.__class__:
            return False
        return True

    def __repr__(self):
        """repr"""
        return repr(self.value)

    def __str__(self):
        """str"""
        return str(self.value)


ATOMIC_TESTS = [
    ('1', 1),
    ('1.0', 1.0),
    ('"foo"', 'foo'),
    ('-1', -1),
    ('-1.5', -1.5),
    ('name', 'Matt'),
    ('one', 1),
    ('two', 2.0),
    ('name[1]', 'a'),
    ('name[1:-1]', 'at'),
    ('name[:-1]', 'Mat'),
    ('name[1:]', 'att'),
    ('-one', -1),
    ('-two', -2.0),
    ('var', NameError),
    ('self.true', True),
    ('self.false', AttributeError),
    ('sum(1,2,3)', 6),
    ('sum(.1, .1, .1, .1, .1, .1, .1, .1, .1, .1)', 0.9999999999999999),
    ('sum(.1, .1, .1, .1, .1, .1, .1, .1, .1, .1)', AssertionError(exactly(1.0))),
    ('fsum(.1, .1, .1, .1, .1, .1, .1, .1, .1, .1)', exactly(1.0)),
    ('{"a": 1, "b": ["two", "three"]}', {'a': 1, 'b': ['two', 'three']}),
    ('"a" "b"', 'ab'),
    ('{}', exactly({})),
    ('[]', exactly([])),
    ('()', exactly(())),
    ("(json_load('{\"foo\": [1,2,3]}')['foo'], 4)", ([1, 2, 3], 4)),
    (
        "[{'events': [{'source': {'device': {'ipAddress': '1.2.3.4'}}}]}]",
        [{'events': [{'source': {'device': {'ipAddress': '1.2.3.4'}}}]}],
    ),
    (
        "({'events': ({'source': {'device': {'ipAddress': '1.2.3.4'}}},)},)",
        ({'events': ({'source': {'device': {'ipAddress': '1.2.3.4'}}},)},),
    ),
]


class TestAtoms(object):
    """Test atomic values"""

    def setup_class(self):
        """setup"""

        self.expr = Expression()
        self.expr.set('name', 'Matt')
        self.expr.set('one', 1)
        self.expr.set('two', 2.0)
        self.expr.set('self', self)
        self.expr.set('sum', psum)
        self.expr.set('fsum', fsum)

    true = True

    @pytest.mark.parametrize('expression,result', ATOMIC_TESTS)
    def test_atom(self, expression, result):
        """test atomic values"""

        if isclass(result) and issubclass(result, Exception):
            with pytest.raises(result):
                value = self.expr.eval(expression)
        elif isinstance(result, Exception):
            with pytest.raises(result.__class__):
                value = self.expr.eval(expression)
                result = result.args[0]
                assert value == result, f'{expression} == {result}'
        else:
            value = self.expr.eval(expression)
            assert value == result, f'{expression} == {result}'
