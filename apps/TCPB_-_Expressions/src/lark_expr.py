#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Lark based expression grammar """

# pylint: disable=no-self-use,import-outside-toplevel,too-many-return-statements
try:
    import readline
except Exception:
    readline = None

import ast
import json
import traceback
import sys
import operator

from lark import Lark, Transformer, v_args
import lark.exceptions

from methods import coerce, ExpressionMethods
from literal import literal, tcvar


class kwarg(object):
    """kwarg function parameter"""

    def __init__(self, name, value):
        """init"""
        self.name = name
        self.value = value


__notfound__ = []
__notfound2__ = []


class open_list(list):
    """open_list"""


@v_args(inline=True)
class Evaluate(Transformer):
    """ Walk the parse tree and evaluate the result """

    num_float = float
    num_int = int

    def __init__(self, namespace=None, redis_helper=None):
        """ init """

        self.namespace = namespace or {}
        self.redis_helper = redis_helper

    @coerce
    @staticmethod
    def concat(a: str, b: str):
        """concat"""
        return literal(a + b)

    # all of these methods have literal in their signature so that
    # literal values (quoted values) never get converted, and allowing
    # the underlaying operator to raise an error

    @coerce
    @staticmethod
    def mul(a: (int, float, literal), b: (int, float, literal)):
        """mul"""

        return a * b

    @coerce
    @staticmethod
    def div(a: (int, float, literal), b: (int, float, literal)):
        """div"""

        return a / b

    @coerce
    @staticmethod
    def int_div(a: (int, float, literal), b: (int, float, literal)):
        """int_div"""

        return a // b

    @coerce
    @staticmethod
    def add(a: (int, float, literal), b: (int, float, literal)):
        """add"""

        return a + b

    @coerce
    @staticmethod
    def sub(a: (int, float, literal), b: (int, float, literal)):
        """sub"""

        return a - b

    @coerce
    @staticmethod
    def pow(a: (int, float, literal), b: (int, float, literal)):
        """pow"""

        return a ** b

    @coerce
    @staticmethod
    def neg(a: (int, float, literal)):
        """neg"""

        return -a

    @coerce
    @staticmethod
    def mod(a: (int, float, literal), b: (int, float, literal)):
        """mod"""

        return a % b

    def set_kwarg(self, name, value):
        """kwarg"""
        return kwarg(name, value)

    def list_(self, *args):
        """ list """
        # print(f'>>> list {args!r}')

        result = open_list()
        for arg in args:
            if isinstance(arg, open_list):
                result.extend(arg)
            else:
                result.append(arg)

        return result

    def get(self, ob, key):
        """get"""

        result = operator.getitem(ob, key)
        return result

    def dict_freeze(self, a):
        """freeze (produce) a dictionary"""

        if not isinstance(a, list):
            a = [a]
        result = {}
        for kw in a:
            result[kw.name] = kw.value
        return result

    def list_freeze(self, a):
        """freeze a into a list"""
        if not isinstance(a, open_list):
            return a
        # print(f'>>> list_freeze {a!r}')
        return list(a)

    def tuple_freeze(self, a):
        """freeze a into a tuple"""
        if not isinstance(a, open_list):
            return a
        # print(f'>>> tuple_freeze {a!r}')
        return tuple(a)

    def function(self, name, args):
        """ call function """

        if not isinstance(args, open_list):
            args = (args,)
        # print(f'>>> call {name!r} {args!r}')

        kwargs = {}

        arglist = []
        for arg in args:
            if isinstance(arg, kwarg):
                kwargs[arg.name] = arg.value
            else:
                if kwargs:
                    raise SyntaxError(
                        f'Positional parameter {arg} must not follow keyword parameters'
                    )
                arglist.append(arg)

        f = self.namespace.get(name, __notfound__)
        if f is __notfound__:
            raise ValueError(f'Function {name} not found')
        if not callable(f):
            raise TypeError(f'{name} is not a function')

        # TODO: check signatures
        result = f(*arglist, **kwargs)
        # print(f'>>> = {result!r}')
        return result

    def concat_string(self, a, b):
        """Concatenate two strings"""

        return literal(str(a) + str(b))

    def tcvariable(self, name):
        """ Look up variable in REDIS """

        if self.redis_helper:
            return self.redis_helper(name)
        return None

    def getattr(self, base, name):
        """ getattr """
        if isinstance(base, tcvar):
            try:
                base = json.loads(tcvar)
            except Exception:
                pass
        if isinstance(base, dict):
            return base.get(name)
        return getattr(base, name)

    def get_slice(self, base, start=None, end=None):
        """ get_slice """

        # print(f'>>> get slice {base!r}[{start!r}:{end!r}]')
        return base[start:end]

    def none(self):
        """ None """
        return None

    def literal_(self, a):
        """literal"""
        return literal(ast.literal_eval(a))

    def logical_or(self, a, b):
        """logical_or"""

        return a or b

    def logical_and(self, a, b):
        """logical_and"""

        return a and b

    def equals(self, a, b):
        """equals"""

        # print(f'>>> {a!r} == {b!r}')
        return a == b

    def not_equals(self, a, b):
        """not equals"""

        return a != b

    def less_than(self, a, b):
        """less than"""

        return a < b

    def greater_than(self, a, b):
        """greater_than"""

        return a > b

    def less_than_equal_to(self, a, b):
        """less than or equal to"""
        return a <= b

    def greater_than_equal_to(self, a, b):
        """greater than or equal to"""
        return a >= b

    def not_(self, a):
        """not"""

        return not a

    def in_(self, a, b):
        """in"""

        return a in b

    def not_in_(self, a, b):
        """not in"""

        return a not in b

    def var(self, name):
        """ look up variable in the namespace """

        # print(f'>>> lookup {name!r}')
        result = self.namespace.get(name, __notfound__)
        if callable(name):
            raise TypeError(f'{name} is a function, not a variable')
        if result is __notfound__:
            raise NameError(name)

        return result


class Expression(ExpressionMethods):
    """expression parser"""

    def __init__(self, tcex=None):
        self.variables = {}
        self.evaluator = Evaluate(self, self.redis_fetch)
        self.parser = Lark.open(
            'grammar.lark', parser='lalr', start='start', transformer=self.evaluator
        )
        self.tcex = tcex
        self.cache = {}

    true = True
    false = False
    null = None
    none = None

    def encapsulate(self, ob):
        """ Enapsulate strings in object as tcvar """

        if ob is None:
            return ob

        if isinstance(ob, (int, float)):
            return ob

        if isinstance(ob, str):
            return tcvar(ob)

        if isinstance(ob, tuple):
            result = [self.encapsulate(x) for x in ob]
            return tuple(result)

        if isinstance(ob, list):
            return [self.encapsulate(x) for x in ob]

        if isinstance(ob, dict):
            result = {}
            for key, value in ob.items():
                result[key] = self.encapsulate(value)
            return result

        return ob

    def deencapsulate(self, ob):
        """ deencapsulate tcvars """

        if ob is None:
            return ob

        if isinstance(ob, (int, float)):
            return ob

        if isinstance(ob, tcvar):
            try:
                return self.eval(ob)
            except Exception:
                pass
            return str(ob)

        if isinstance(ob, tuple):
            result = [self.deencapsulate(x) for x in ob]
            return tuple(result)

        if isinstance(ob, list):
            return [self.deencapsulate(x) for x in ob]

        if isinstance(ob, dict):
            result = {}
            for key, value in ob.items():
                result[key] = self.deencapsulate(value)
            return result

        return ob

    def redis_fetch(self, variable):
        """Fetch a TC variable from Redis"""

        if variable in self.cache:
            return self.cache[variable]

        if self.tcex:
            result = self.tcex.playbook.read(variable)
        else:
            result = None

        # first, see if we can parse what we got

        if isinstance(result, str):
            try:
                result = self.eval(result)
                self.cache[variable] = result
                return result
            except Exception:
                pass  # nope!

        # Now, walk through result and encapsulate any strings as tcvar
        result = self.encapsulate(result)

        self.cache[variable] = result
        return result

    def get(self, variable, default=None):
        """Get a variable"""

        # first, if the variable is in self.variables, thats it!

        if variable in self.variables:
            return self.variables[variable]

        # second, sniff for functions we have named f_variable

        fname = f'f_{variable}'

        result = getattr(self, fname, None)
        if result is not None:
            return result

        # third, it could be an attribute on ourself, but only if
        # it is NOT callable

        result = getattr(self, variable.lower(), __notfound2__)
        if result is not __notfound2__ and not callable(result):
            return result

        return default

    def set(self, variable, value):
        """set a variable"""

        self.variables[variable] = value

    def eval(self, expression):
        """Evaluate an expression"""
        try:
            result = self.parser.parse(expression)
        except lark.exceptions.UnexpectedToken as e:
            raise SyntaxError(
                f'Unexpected token {e.token} at line {e.line}, column {e.column}.'
            ) from e

        result = self.deencapsulate(result)

        return result


def interactive(record=False):
    """interactive expression evaluator"""

    if readline is not None:
        pass

    engine = Expression()

    if record:
        fh = open('local-expr-record.txt', 'a')

    def setfcn(name, value):
        """Set a variable"""
        engine.set(name, value)
        return value

    engine.set('set', setfcn)  # add a set function so you can set(name, value)

    while True:
        try:
            expr = input('>>> ')
        except EOFError:
            print()
            break

        if not expr:
            continue

        try:
            result = engine.eval(expr)
            print(result)
            if record:
                fh.write(f'    ({expr!r}, {result!r}),\n')
        except lark.exceptions.UnexpectedCharacters as e:
            msg = str(e).split('\n')[0][24:]
            print(f'Unexpected character: {msg}')
            if record:
                fh.write(f'    ({expr!r}, lark.exceptions.UnexpectedCharacters),\n')
        except lark.exceptions.LarkError:
            print(traceback.format_exc())
            if record:
                fh.write(f'    ({expr!r}, lark.exceptions.LarkError),\n')
        except Exception as e:
            print(traceback.format_exc(limit=0).rstrip().split('\n')[-1])
            if record:
                args = tuple([str(x) for x in e.args])  # pylint: disable=consider-using-generator
                fh.write(f'    ({expr!r}, {e.__class__.__name__}{args!r}),\n')


if __name__ == '__main__':
    record_flag = bool('--record' in sys.argv)
    interactive(record_flag)
