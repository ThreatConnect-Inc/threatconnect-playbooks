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


EVAL_TESTS = [
    ('0 || 1', 1),
    ('true || false', True),
    ('True || False', True),
    ('True && False', False),
    ('False && False', False),
    ('True && True', True),
    ('true or false', True),
    ('true and false', False),
    ('true and (true or false)', True),
    ('1 < 2', True),
    ('3 < 2', False),
    ('1 <= 2', True),
    ('2 <= 2', True),
    ('3 <= 2', False),
    ('1 > 2', False),
    ('3 > 2', True),
    ('1 >= 2', False),
    ('2 >= 2', True),
    ('3 >= 2', True),
    ('one == 1', True),
    ('one == 1.0', True),
    ('two == 1.0', False),
    ('two == 1', False),
    ('one != 1', False),
    ('one != 1.0', False),
    ('two != 1.0', True),
    ('two != 1', True),
    ('1, 2, 3', SyntaxError),
    ('not False', True),
    ('not True', False),
    ('"a" in name', True),
    ('"e" in name', False),
    ('"e" not in name', True),
    ('"a" not in name', False),
    ('not "e" in name', True),
    ('1 in 1,2,3', TypeError),
    ('1 in (1,2,3)', True),
    ('(true)', True),
    ('(true', SyntaxError),
    ('(true,)', (True,)),
    ('(true,)', AssertionError(True)),
    ('{"foo": null}.foo', None),
]


class TestEval(object):
    """Test eval values"""

    def setup_class(self):
        """setup"""

        self.expr = Expression()
        self.expr.set('name', 'Matt')
        self.expr.set('one', 1)
        self.expr.set('two', 2.0)

    @pytest.mark.parametrize('expression,result', EVAL_TESTS)
    def test_eval(self, expression, result):
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
