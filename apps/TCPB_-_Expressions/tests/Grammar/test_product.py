# -*- coding: utf-8 -*-
"""Test atomic values from expression Parser"""

from inspect import isclass

import pytest
from lark_expr import Expression

# pylint: disable=attribute-defined-outside-init


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


PRODUCT_TESTS = [
    ('one + one', 2),
    ('1 + 1', 2.0),
    ('1 + 1', exactly(2)),
    ('1 + 1', AssertionError(exactly(2.0))),
    ('1 + 1.0', 2),
    ('1 + 1.0', 2.0),
    ('1 + 1.0', exactly(2.0)),
    ('1 + 1.0', AssertionError(exactly(2))),
    ('1 + 1 * 2', 3),
    ('1 * 2 + 1', 3),
    ('1 * (2 + 2)', 4),
    ('(1,1)', (1, 1)),
    ('(1,2)', (1, 2)),
    ('(1,2.0)', (1, exactly(2.0))),
    ('("a", 1, 2)', ('a', 1, 2)),
    ('["a", 1, 2]', ['a', 1, 2]),
    ('["a", 1, 2]', AssertionError(('a', 1, 2))),
    ('5 / 1', 5),
    ('5 / 2', 2.5),
    ('5 / 2.0', 2.5),
    ('5 / 0', ZeroDivisionError),
    ('1 + 1 / 5', 1.2),
    ('(1 + 1) / 5', 0.4),
    ('(1 + 1) / name', TypeError),
    ('(1 + 1) / two', exactly(1.0)),
    ('5 % 2', 1),
    ('2 ** 8', 256),
    ('3 * 2 ** 8', 768),
    ('(3 * 2) ** 8', 6 ** 8),
    ('"a" * 5', 'aaaaa'),
    ('three + 1', 4),
    ('four + 1', exactly(5.0)),
    ('three * four', exactly(12.0)),
    ('three / four', exactly(0.75)),
    ('name * three', 'MattMattMatt'),
    ('name * "3"', TypeError),
    ('5//3', 1),
    ('5//"3"', TypeError),
]


class TestProduct(object):
    """Test product values"""

    def setup_class(self):
        """setup"""

        self.expr = Expression()
        self.expr.set('name', 'Matt')
        self.expr.set('one', 1)
        self.expr.set('two', 2.0)
        self.expr.set('three', '3')
        self.expr.set('four', '4.0')

    @pytest.mark.parametrize('expression,result', PRODUCT_TESTS)
    def test_product(self, expression, result):
        """test product values"""

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
