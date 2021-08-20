# -*- coding: utf-8 -*-
"""Test atomic values from expression Parser"""

from inspect import isclass
import locale
import math
from json import JSONDecodeError

import pytest
import lark.exceptions

from lark_expr import Expression
from methods import list_methods

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


class nearly(object):
    """An identity match with type"""

    def __init__(self, value):
        """init"""
        self.value = value

    def __eq__(self, other):
        """exact comparision"""
        if isinstance(self.value, float) and isinstance(other, float):
            if not math.isclose(self.value, other):
                return False
        elif self.value != other:
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


class sametype(object):
    """Match any value of same type"""

    def __init__(self, value):
        """init"""
        self.value = value

    def __eq__(self, other):
        """exact comparision"""
        if type(other) == type(self.value):  # pylint: disable=C0123
            return True
        return False

    def __repr__(self):
        """repr"""
        return repr(self.value)

    def __str__(self):
        """str"""
        return str(self.value)


class SkipIf(object):
    """Skip test if subexpression fails"""

    def __init__(self, value, skip_condition):
        """init"""

        self.value = value
        self.skip_condition = skip_condition

    def check_skip(self):
        """check_skip"""

        if callable(self.skip_condition):
            try:
                self.skip_condition()
            except Exception:
                pytest.skip('Unsupported test')

        return self.value


# pylint: disable=line-too-long
FUNCTION_TESTS = [
    ('join(", ", "one", "two", "three")', 'one, two, three'),
    ('split("one,two,three", ",")', ['one', 'two', 'three']),
    ('copysign(1,-5)', -1),
    ('printf("%5.3f", 0.2)', '0.200'),
    ('abs(-5)', 5),
    ('factorial(5)', 120),
    ('len(1,2,3)', TypeError),
    ('len([1,2,3])', 3),
    ('len(name)', 4),
    ('ceil(.5)', 1),
    ('ceil(".5")', 1),
    ('sum(.1, .1, .1, .1, .1, .1, .1, .1, .1, .1)', exactly(1.0)),
    ('sum([.1, .1, .1, .1, .1, .1, .1, .1, .1, .1])', exactly(1.0)),
    ('sum(".1", ".1", ".1", ".1", ".1", ".1", ".1", ".1", ".1", ".1")', exactly(1.0)),
    ('gcd(24, 36)', 12),
    ('gcd(24, "a")', TypeError),
    (
        'locale_currency(5000.99, grouping=True)',
        SkipIf('$5,000.99', lambda: locale.setlocale(locale.LC_ALL, 'EN_us')),
    ),
    (
        'asdf',
        NameError(
            'asdf',
        ),
    ),
    ('acos(1)', 0.0),
    ('acos(0)', 1.5707963267948966),
    (
        "acox('f')",
        ValueError(
            'Function acox not found',
        ),
    ),
    (
        "acos('f')",
        TypeError(
            'must be real number, not literal',
        ),
    ),
    (
        'acosh(0)',
        ValueError(
            'math domain error',
        ),
    ),
    ('acosh(1)', 0.0),
    ('acosh(2)', 1.3169578969248166),
    (
        "acosh('f')",
        TypeError(
            'must be real number, not literal',
        ),
    ),
    ('asin(0)', 0.0),
    ('asin(1)', 1.5707963267948966),
    (
        "asin('f')",
        TypeError(
            'must be real number, not literal',
        ),
    ),
    (
        'asinh(0))',
        SyntaxError(
            "Unexpected token Token(RPAR, ')') at line 1, column 9.",
        ),
    ),
    ('asinh(0)', 0.0),
    ('asinh(1)', 0.881373587019543),
    ('asinh(pi/2)', 1.233403117511217),
    (
        "asinh('f')",
        TypeError(
            'must be real number, not literal',
        ),
    ),
    ('atan(0)', 0.0),
    ('atan(1)', 0.7853981633974483),
    ('atan(pi)', 1.2626272556789115),
    (
        "atan('f')",
        TypeError(
            'must be real number, not literal',
        ),
    ),
    ('atanh(0)', 0.0),
    (
        'atanh(1)',
        ValueError(
            'math domain error',
        ),
    ),
    (
        "atanh('f')",
        TypeError(
            'must be real number, not literal',
        ),
    ),
    (
        'atanh(pi)',
        ValueError(
            'math domain error',
        ),
    ),
    (
        'b64encode(1)',
        TypeError(
            "a bytes-like object is required, not 'int'",
        ),
    ),
    ("b64encode('foo')", 'Zm9v'),
    ("b64decode('Zm9v')", 'foo'),
    (
        'b64decode()',
        TypeError(
            "f_b64decode() missing 1 required positional argument: 's'",
        ),
    ),
    (
        'b64decode(1)',
        TypeError(
            "argument should be a bytes-like object or ASCII string, not 'int'",
        ),
    ),
    ("bytes('a')", b'a'),
    ("bytes('a','ascii')", b'a'),
    ("center('a', 20)", '         a          '),
    ("choice(False, 'True Choice', 'False Choice')", 'False Choice'),
    ("choice(True, 'True Choice', 'False Choice')", 'True Choice'),
    ("choice(True, 'True Choice')", 'True Choice'),
    ('choice(True)', None),
    (
        'choice()',
        TypeError(
            "f_choice() missing 1 required positional argument: 'condition'",
        ),
    ),
    ('chr(65)', 'A'),
    (
        "chr('x')",
        TypeError(
            'an integer is required (got type literal)',
        ),
    ),
    (
        'chr(-1)',
        ValueError(
            'chr() arg not in range(0x110000)',
        ),
    ),
    ('chr(257)', 'ā'),
    ('cos(0)', 1.0),
    ('cos(1)', 0.5403023058681398),
    ('cos(-1)', 0.5403023058681398),
    (
        "cos('x')",
        TypeError(
            'must be real number, not literal',
        ),
    ),
    ('cosh(0)', 1.0),
    ('cosh(1)', 1.5430806348152437),
    (
        "cosh('x')",
        TypeError(
            'must be real number, not literal',
        ),
    ),
    ("datetime('July 4, 1776')", '1776-07-04T00:00:00'),
    ('datetime(157900000)', '1975-01-02T13:06:40+00:00'),
    (
        "datetime('foo')",
        RuntimeError(
            'Could not format input (foo) to datetime string.',
        ),
    ),
    ('degrees(2*pi)', 360.0),
    (
        "degrees('f')",
        TypeError(
            'must be real number, not literal',
        ),
    ),
    ('erf(1)', 0.842700792949715),
    (
        "erf('x')",
        TypeError(
            'must be real number, not literal',
        ),
    ),
    ('erfc(1)', 0.157299207050285),
    (
        "erfc('x')",
        TypeError(
            'must be real number, not literal',
        ),
    ),
    ('exp(1)', 2.718281828459045),
    ('exp(2)', 7.38905609893065),
    (
        "exp('x')",
        TypeError(
            'must be real number, not literal',
        ),
    ),
    ('expm1(1)', 1.7182818284590453),
    ('expm1(0)', 0.0),
    (
        "expm1('x')",
        TypeError(
            'must be real number, not literal',
        ),
    ),
    (
        'find()',
        TypeError(
            "f_find() missing 2 required positional arguments: 'ob' and 'value'",
        ),
    ),
    ("find('fool', 'foo')", 0),
    ("find('I pity the foo', 'foo')", 11),
    ("find('I pity the foo', 'Foo')", -1),
    (
        "find('I pity the foo', 1)",
        TypeError(
            'must be str, not int',
        ),
    ),
    (
        'find(1, 1)',
        AttributeError(
            "'int' object has no attribute 'index'",
        ),
    ),
    ('flatten({})', {}),
    ("flatten({'a': 1'})", lark.exceptions.UnexpectedCharacters),
    ("flatten({'a': 1})", {'a': '1'}),
    ("flatten({'a': 1, 'b': {'erp': 0, 'ulp': 5}})", {'a': '1', 'b.erp': '0', 'b.ulp': '5'}),
    ('float(1)', 1.0),
    ('float(.1)', 0.1),
    (
        "float('x')",
        ValueError(
            "could not convert string to float: 'x'",
        ),
    ),
    (
        'format()',
        TypeError(
            "f_format() missing 1 required positional argument: 's'",
        ),
    ),
    ("format('a')", 'a'),
    ("format('{pi}')", '3.141592653589793'),
    ("format('{pi} / 2 = {f}', f=pi/2)", '3.141592653589793 / 2 = 1.5707963267948966'),
    (
        'gamma(0)',
        ValueError(
            'math domain error',
        ),
    ),
    ('gamma(1)', 1.0),
    ('gamma(e)', 1.5674682557740531),
    (
        "gamma('x')",
        TypeError(
            'must be real number, not literal',
        ),
    ),
    (
        'hypot(0)',
        TypeError(
            "missing a required argument: 'y'",
        ),
    ),
    ('hypot(0,1)', 1.0),
    ("index('I pity the foo', 'foo')", 11),
    (
        "index('I pity the foo', 'Foo')",
        ValueError(
            'substring not found',
        ),
    ),
    ('index((1,2,3), 2)', 1),
    (
        'index((1,2,3), 2, 4)',
        ValueError(
            'tuple.index(x): x not in tuple',
        ),
    ),
    ('int(1)', 1),
    ('int(1.1)', 1),
    (
        "int('1.1')",
        ValueError(
            "invalid literal for int() with base 10: '1.1'",
        ),
    ),
    ("int('1')", 1),
    (
        "int('foo')",
        ValueError(
            "invalid literal for int() with base 10: 'foo'",
        ),
    ),
    (
        'items()',
        TypeError(
            "f_items() missing 1 required positional argument: 'ob'",
        ),
    ),
    (
        "items('1')",
        AttributeError(
            "'literal' object has no attribute 'items'",
        ),
    ),
    (
        'items([1,2,3])',
        AttributeError(
            "'frozen_list' object has no attribute 'items'",
        ),
    ),
    (
        "items({'a'",
        SyntaxError(
            "Unexpected token Token($END, '') at line 1, column 8.",
        ),
    ),
    ("items({'a': 1, 'b': 1})", [('a', 1), ('b', 1)]),
    (
        "jmespath({ 'a': 1, 'b': [{'i': 0}, {'i': 1}]})",
        TypeError(
            "f_jmespath() missing 1 required positional argument: 'ob'",
        ),
    ),
    ("jmespath('a', { 'a': 1, 'b': [{'i': 0}, {'i': 1}]})", 1),
    ("jmespath('c', { 'a': 1, 'b': [{'i': 0}, {'i': 1}]})", None),
    ("jmespath('b', { 'a': 1, 'b': [{'i': 0}, {'i': 1}]})", [{'i': 0}, {'i': 1}]),
    ("jmespath('*.i', { 'a': 1, 'b': [{'i': 0}, {'i': 1}]})", []),
    ("jmespath('b[].i', { 'a': 1, 'b': [{'i': 0}, {'i': 1}]})", [0, 1]),
    (
        "json({ 'a': 1, 'b': [{'i': 0}, {'i': 1}]})",
        '{\n  "a": 1,\n  "b": [\n    {\n      "i": 0\n    },\n    {\n      "i": 1\n    }\n  ]\n}',
    ),
    (
        'json()',
        TypeError(
            "f_json() missing 1 required positional argument: 'ob'",
        ),
    ),
    ("json('x')", '"x"'),
    (
        "json_dump({ 'a': 1, 'b': [{'i': 0}, {'i': 1}]})",
        '{\n  "a": 1,\n  "b": [\n    {\n      "i": 0\n    },\n    {\n      "i": 1\n    }\n  ]\n}',
    ),
    (
        "json_dump({ 'a': 1, 'b': [{'i': 0}, {'i': 1}]},indent=0)",
        '{\n"a": 1,\n"b": [\n{\n"i": 0\n},\n{\n"i": 1\n}\n]\n}',
    ),
    (
        "json_load({ 'a': 1, 'b': [{'i': 0}, {'i': 1}]})",
        TypeError(
            "the JSON object must be str, bytes or bytearray, not 'dict'",
        ),
    ),
    ('json_load("{ \'a\': 1, \'b\': [{\'i\': 0}, {\'i\': 1}]}")', JSONDecodeError),
    (
        'json_load("{ \'a\': 1, \'b\': [{\'i\': 0}, {\'i\': 1}]})',
        lark.exceptions.UnexpectedCharacters,
    ),
    ('json_load(\'{ "a": 1, "b": [{"i": 0}, {"i": 1}]}\')', {'a': 1, 'b': [{'i': 0}, {'i': 1}]}),
    ("keys({ 'a': 1, 'b': [{'i': 0}, {'i': 1}]})", ['a', 'b']),
    (
        'lgamma(0)',
        ValueError(
            'math domain error',
        ),
    ),
    ('lgamma(1)', 0.0),
    ('lgamma(e)', 0.4494617418200675),
    (
        "locale_format('%5.3f', pi)",
        SkipIf('3.142', lambda: locale.setlocale(locale.LC_ALL, 'EN_us')),
    ),
    (
        "locale_format('%5.3f', pi*1000)",
        SkipIf('3141.593', lambda: locale.setlocale(locale.LC_ALL, 'EN_us')),
    ),
    (
        "locale_format('%5.3f', pi*1000, grouping=True)",
        SkipIf('3,141.593', lambda: locale.setlocale(locale.LC_ALL, 'EN_us')),
    ),
    (
        "locale_format('%5.3f', pi*1000, grouping=True, monetary=True)",
        SkipIf('3,141.593', lambda: locale.setlocale(locale.LC_ALL, 'EN_us')),
    ),
    (
        'locale_currency(pi*1000)',
        SkipIf('$3141.59', lambda: locale.setlocale(locale.LC_ALL, 'EN_us')),
    ),
    (
        'locale_currency(pi*1000, grouping=True)',
        SkipIf('$3,141.59', lambda: locale.setlocale(locale.LC_ALL, 'EN_us')),
    ),
    (
        'locale_currency(pi*1000, symbol=False, grouping=True)',
        SkipIf('3,141.59', lambda: locale.setlocale(locale.LC_ALL, 'EN_us')),
    ),
    (
        'locale_currency(pi*1000, grouping=True, international=True)',
        SkipIf('USD 3,141.59', lambda: locale.setlocale(locale.LC_ALL, 'EN_us')),
    ),
    (
        'locale_currency(pi*1000, grouping=True, locale="ES_es")',
        SkipIf('3.141,59 Eu', lambda: locale.setlocale(locale.LC_ALL, 'ES_es')),
    ),
    (
        'locale_currency(pi*1000, grouping=True, locale="EN_gb")',
        SkipIf('£3,141.59', lambda: locale.setlocale(locale.LC_ALL, 'EN_gb')),
    ),
    ('log(10)', 2.302585092994046),
    ('log(10,2)', 3.3219280948873626),
    ('log(16,2)', 4.0),
    ('log10(100)', 2.0),
    ('log10(1000)', 3.0),
    ('log10(5)', 0.6989700043360189),
    (
        "log10('x')",
        TypeError(
            'must be real number, not literal',
        ),
    ),
    ('log1p(10)', 2.3978952727983707),
    ('log2(16)', 4.0),
    ('log2(10)', 3.321928094887362),
    ("lower('UPPER')", 'upper'),
    ("lstrip('foo')", 'foo'),
    ("lstrip('   foo')", 'foo'),
    ("lstrip('   foo   ')", 'foo   '),
    (
        'namevallist()',
        TypeError(
            "f_namevallist() missing 1 required positional argument: 'ob'",
        ),
    ),
    (
        'namevallist(pi)',
        AttributeError(
            "'float' object has no attribute 'items'",
        ),
    ),
    ("namevallist({'a': 1, 'b': 2})", [{'name': 'a', 'value': 1}, {'name': 'b', 'value': 2}]),
    ("ord('A')", 65),
    (
        'ord()',
        TypeError(
            "f_ord() missing 1 required positional argument: 'char'",
        ),
    ),
    (
        "ord('')",
        TypeError(
            'ord() expected a character, but string of length 0 found',
        ),
    ),
    (
        "ord('AB')",
        TypeError(
            'ord() expected a character, but string of length 2 found',
        ),
    ),
    (
        'pow(0)',
        TypeError(
            "missing a required argument: 'y'",
        ),
    ),
    ('pow(0,1)', 0.0),
    ('radians(360)', 6.283185307179586),
    ('radians(180)', 3.141592653589793),
    (
        "radians('x')",
        TypeError(
            'must be real number, not literal',
        ),
    ),
    ('range(0)', []),
    (
        'range()',
        TypeError(
            "f_range() missing 1 required positional argument: 'start_or_stop'",
        ),
    ),
    ('range(5)', [0, 1, 2, 3, 4]),
    ('range(5,1)', []),
    ('range(1, 5)', [1, 2, 3, 4]),
    ('range(5, 0, -1)', [5, 4, 3, 2, 1]),
    ("replace('foo', 'o', 'e')", 'fee'),
    (
        "replace('foo')",
        TypeError(
            "missing a required argument: 'source'",
        ),
    ),
    ("replace(5, 'o', 'e')", '5'),
    ("rstrip('foo')", 'foo'),
    ("rstrip('   foo   ')", '   foo'),
    ("rstrip('   foo   ')", '   foo'),
    ('sin(0)', 0.0),
    ('sin(1)', 0.8414709848078965),
    ('sin(pi)', 1.2246467991473532e-16),
    ('sinh(0)', 0.0),
    ('sinh(1)', 1.1752011936438014),
    (
        "sinh('x')",
        TypeError(
            'must be real number, not literal',
        ),
    ),
    (
        'sinh(1,2)',
        TypeError(
            'too many positional arguments',
        ),
    ),
    ('sort((1,2,3))', [1, 2, 3]),
    ('sort((3,2,1))', [1, 2, 3]),
    ("sort('abc')", ['abc']),
    ('sort(1,2,3)', [1, 2, 3]),
    ('sort(3,2,1)', [1, 2, 3]),
    ('sqrt(2)', 1.4142135623730951),
    (
        "sqrt('')",
        TypeError(
            'must be real number, not literal',
        ),
    ),
    ('str(pi)', '3.141592653589793'),
    ("strip('  foo    ')", 'foo'),
    ('tan(0)', 0.0),
    ('tan(1)', 1.557407724654902),
    (
        "tan('x')",
        TypeError(
            'must be real number, not literal',
        ),
    ),
    ('tanh(0)', 0.0),
    ('tanh(1)', 0.7615941559557649),
    (
        "tanh('x')",
        TypeError(
            'must be real number, not literal',
        ),
    ),
    (
        "timedelta('July 4, 1776', 'July 4, 2020')",
        {
            'datetime_1': '1776-07-04T00:00:00',
            'datetime_2': '2020-07-04T00:00:00',
            'years': -244,
            'months': 0,
            'weeks': 0,
            'days': 0,
            'hours': 0,
            'minutes': 0,
            'seconds': 0,
            'microseconds': 0,
            'total_months': -2928,
            'total_weeks': -24400,
            'total_days': -89119,
            'total_hours': -2138856,
            'total_minutes': -128331360,
            'total_seconds': -7699881600,
            'total_microseconds': -7699881600000,
        },
    ),
    ("title('foo')", 'Foo'),
    ("title('foo the first')", 'Foo The First'),
    ('trunc(1.1)', 1),
    ("upper('foo')", 'FOO'),
    ("values({'a': 1, 'b': 2})", [1, 2]),
    (
        "values('a')",
        AttributeError(
            "'literal' object has no attribute 'values'",
        ),
    ),
    (
        'values(1)',
        AttributeError(
            "'int' object has no attribute 'values'",
        ),
    ),
    (
        'values([1])',
        AttributeError(
            "'int' object has no attribute 'values'",
        ),
    ),
    ('min(1,2,3)', 1),
    ('min(3,2,1)', 1),
    ('min([3,2,1])', 1),
    (
        'min()3,2,1))',
        SyntaxError(
            "Unexpected token Token(INT, '3') at line 1, column 6.",
        ),
    ),
    ('min((3,2,1))', 1),
    ("min('wxyza')", 'a'),
    ("max('wxyza')", 'z'),
    ('max(1,2,3)', 3),
    ('max(3,2,1)', 3),
    ("min({'a': 'foo', 'b': 'bla'})", 'a'),
    ("max({'a': 'foo', 'b': 'bla'})", 'b'),
    ("pad('foo', 7)", 'foo    '),
    ("pad('foo', 7, '*')", 'foo****'),
    (
        "pad('foo', 7, '**')",
        ValueError(
            'pad value must be string of length one',
        ),
    ),
    ("pad('foofoofoo', 7)", 'foofoofoo'),
    ("pad('foofoof', 7)", 'foofoof'),
    ("pad('foofoo', 7)", 'foofoo '),
    ('pad([1,2,3], 7)', [1, 2, 3, None, None, None, None]),
    ('pad([1,2,3,4,5,6,7], 7)', [1, 2, 3, 4, 5, 6, 7]),
    ('pad([1,2,3,4,5,6,7,8], 7)', [1, 2, 3, 4, 5, 6, 7, 8]),
    (
        "pad([1,2,3,4,5,6,7,8], 'a')",
        TypeError(
            'length must be integer',
        ),
    ),
    ("research('\\d{4}-\\d{2}-\\d{2}', '2017-07-01T16:18:19')", '2017-07-01'),
    ("rematch('\\d{4}-\\d{2}-\\d{2}', '2017-07-01T16:18:19')", '2017-07-01'),
    ('pformat(1)', '1'),
    ("pformat('foo')", "'foo'"),
    ("pformat({'a': 1, 'b': {'c': 2}})", "{'a': 1, 'b': {'c': 2}}"),
    ('csvread("a,b,c,1,2,3.5")', ['a', 'b', 'c', 1, 2, 3.5]),
    (
        'csvread("a,b,c,1,2,3.5\\na,b,c",convert=False)',
        [['a', 'b', 'c', '1', '2', '3.5'], ['a', 'b', 'c']],
    ),
    ('csvread("a,b,c,1,2,3.5\\na,b,c",rows=1)', ['a', 'b', 'c', 1, 2, 3.5]),
    ('csvread("a,b,c,1,2,3.5\\na,b,c",rows=1,columns=3)', ['a', 'b', 'c']),
    ('csvread("a,b,c,1,2,3.5\\nx,y,z",rows=1,columns=3,header=True)', ['x', 'y', 'z']),
    (
        'csvwrite(["Mary had a little lamb, whose fleece was white as snow", 1, 2, 3.5])',
        '"Mary had a little lamb, whose fleece was white as snow",1,2,3.5\r\n',
    ),
    (
        'csvwrite(["Mary had a little lamb, whose fleece was white as snow", 1, 2, 3.5], '
        'delimiter=\'|\')',
        'Mary had a little lamb, whose fleece was white as snow|1|2|3.5\r\n',
    ),
    ("md5('foo')", 'acbd18db4cc2f85cedef654fccc4a4d8'),
    ("md5(bytes('foo', 'utf-8'))", 'acbd18db4cc2f85cedef654fccc4a4d8'),
    ("md5(['foo', 'bla'])", 'fff5d68e6fd4f50ab7d7668481c534aa'),
    ("sha1('foo')", '0beec7b5ea3f0fdbc95d0dd47f3c5bc275da8a33'),
    ("sha256('foo')", '2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae'),
    ('sha256(None)', 'dc937b59892604f5a86ac96936cd7ff09e25f18ae6b758e8014a24c7fa039e91'),
    ("sha256('')", 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'),
    ("fuzzydist(spamsum('foo '*512 + ' bla'), spamsum('foo '*513))", 2),
    ("fuzzyhash('foo bla blerg woot growl bark')", 'NQFu2URFUKSJ9Ee'),
    ("fuzzyhash('foo bla blerg woot Growl bark')", 'NQFu2URF0Ge'),
    ("fuzzydist('NQFu2URFUKSJ9Ee', 'NQFu2URF0Ge')", 8),
    (
        "refindall(urlre, 'this contains www.foo.com https://www.foo.com/bla/oog as a url"
        " and foo.bla.org/path?param=f&z=y and 1.2.3.4 and matt@domain.com')",
        ['www.foo.com', 'https://www.foo.com/bla/oog', 'foo.bla.org/path?param=f&z=y'],
    ),
    (
        "urlparse('https://foo.com/path/to/html?query=None#fragment')",
        ('https', 'foo.com', '/path/to/html', '', 'query=None', 'fragment'),
    ),
    ("urlparse_qs('foo=bla&bla=oog').foo[0]", 'bla'),
    ('unique((1,2,3,4,5,2,1,{"foo": "bla"}))', [1, 2, 3, 4, 5, {'foo': 'bla'}]),
    ("fuzzymatch('bla'+'foo'*63, 'foo'*63+'bla')", 98.17708333333333),
    ("fuzzymatch('foo bla zoid', 'foo bla21 blerg')", 74.07407407407408),
    ("fuzzymatch('foo bla zoid', 'foo bla21 blerg')>75", False),
    ('unnest((1,2,3,(4,5,6,(7,8,9))))', [1, 2, 3, 4, 5, 6, 7, 8, 9]),
    ("unnest((1,2,3,(4,5,6,(7,8,9),{'foo':'bla'})))", [1, 2, 3, 4, 5, 6, 7, 8, 9, {'foo': 'bla'}]),
    ("unnest('abcd')", 'abcd'),
    ('unnest(1)', 1),
    (
        'unnest(1,2,3)',
        TypeError(
            'f_unnest() takes 1 positional argument but 3 were given',
        ),
    ),
    ('twoscompliment(160)', 160),
    ('twoscompliment(-160)', -4294967456),
    ('twoscompliment(-160,64)', -18446744073709551776),
    ('hex(-4294967456)', '-1000000a0'),
    ('hex(-4294967456, False)', '1000000a0'),
    ("int('100000a0', 16)", 268435616),
    ("int('1000000a0', 16)", 4294967456),
    ("int('-1000000a0', 16)", -4294967456),
    ('bin(2)', '10'),
    ('bin(3)', '11'),
    ('bin(-3)', '-11'),
    ('bin(5)', '101'),
    ('bin(-5)', '-101'),
    ("binary('foo')", b'foo'),
    ("bytes('foo')", b'foo'),
    ("str(bytes('foo'))", 'foo'),
    ("conform([{'a': 1}, {'b': 2}])", [{'a': 1, 'b': None}, {'b': 2, 'a': None}]),
    ("conform([{'a': 1}, {'b': 2}], missing_value='')", [{'a': 1, 'b': ''}, {'b': 2, 'a': ''}]),
    ("prune(conform([{'a': 1}, {'b': 2}], missing_value=''))", [{'a': 1}, {'b': 2}]),
    ('structure(12345)', 'int'),
    ("structure('12345')", 'int'),
    ("structure(datetime('now'))", 'iso8601'),
    ("structure(md5('now'))", 'md5'),
    ("structure(sha1('now'))", 'sha1'),
    ("structure(sha256('now'))", 'sha256'),
    ("update({'a': 1}, {'b': 2})", {'a': 1, 'b': 2}),
    (
        'rexxparse(\'Mary had a little lamb\', \'name . "had a" . thing\')',
        {'name': 'Mary', 'thing': 'lamb'},
    ),
    (
        'rexxparse(\'Mary had a little lamb\', \'name . "had a " thing\')',
        {'name': 'Mary', 'thing': 'little lamb'},
    ),
    (
        'rexxparse(\'Mary had a little lamb\', \'name . "had a " size thing\')',
        {'name': 'Mary', 'size': 'little', 'thing': 'lamb'},
    ),
    (
        'rexxparse(\'Mary had a little lamb\', \'name . "had a " size thing 1 phrase\')',
        {'name': 'Mary', 'size': 'little', 'thing': 'lamb', 'phrase': 'Mary had a little lamb'},
    ),
    (
        'rexxparse(\'Mary had a little lamb\', \'name . "had a " size thing 1 phrase 1 name +4\')',
        {'name': 'Mary', 'size': 'little', 'thing': 'lamb', 'phrase': 'Mary had a little lamb'},
    ),
    (
        (
            'rexxparse(\'127.0.0.1 - frank [10/Oct/2000:13:55:36 -0700] '
            '"GET /apache_pb.gif '
            'HTTP/1.0" 200 2326\', "ip id user \' [\' date \'] \\"\'method url '
            'protocol\'\\" \' status size")'
        ),
        {
            'ip': '127.0.0.1',
            'id': '-',
            'user': 'frank',
            'date': '10/Oct/2000:13:55:36 -0700',
            'method': 'GET',
            'url': '/apache_pb.gif',
            'protocol': 'HTTP/1.0',
            'status': '200',
            'size': '2326',
        },
    ),
    (
        'rexxparse(\'Mary had a little lamb\', \'"little " chop +2 -2 animal +3\')',
        {'chop': 'li', 'animal': 'lit'},
    ),
    (
        'rexxparse(\'Mary had a little lamb\', \'"little " chop +2 -2 animal +3 1 phrase\' )',
        {'chop': 'li', 'animal': 'lit', 'phrase': 'Mary had a little lamb'},
    ),
    ("uuid3('dns', 'mtu.edu')", '93ea5ad7-ae2d-3509-bbbc-958b90bfe336'),
    ("uuid5('dns', 'mtu.edu')", 'b796a2f3-fcde-53a1-9123-e11e6c8f3216'),
    ('uuid4()', sametype('b796a2f3-fcde-53a1-9123-e11e6c8f3216')),
    ("structure(uuid4()) == 'guid'", True),
    (
        "xmlread('<people><person><name>Matt</name><job>Developer</job></person></people>',"
        'compact=True)',
        {'people': {'person': {'Matt': 'Developer'}}},
    ),
    (
        "xmlwrite({'people': {'person': {'Matt': 'Developer'}}})",
        '<people><person><Matt>Developer</Matt></person></people>',
    ),
    (
        "xmlread('<people><person><name>Matt</name><job>Developer</job></person></people>', "
        'compact=False)',
        {'people': [{'person': [{'name': 'Matt'}, {'job': 'Developer'}]}]},
    ),
    (
        "xmlwrite({'people': [{'person': [{'name': 'Matt'}, {'job': 'Developer'}]}]})",
        '<people><person><name>Matt</name><job>Developer</job></person></people>',
    ),
    ('chardet(kosme).encoding', 'utf-8'),
    (
        'indicator_patterns()',
        RuntimeError(
            'TCEX not initialized, cannot retrieve patterns',
        ),
    ),
    ("fang('user@threatconnect.com')", 'user@threatconnect.com'),
    ("defang('user@threatconnect.com')", 'user(at)threatconnect[.]com'),
    ("fang('user(at)threatconnect[.]com')", 'user@threatconnect.com'),
    (
        "extract_indicators('ASN1721 is whack but ASN1271 is not')",
        RuntimeError(
            'TCEX not initialized, cannot retrieve patterns',
        ),
    ),
    (
        "fetch_indicators('ASN1271', default_type='ASN')",
        RuntimeError(
            'TCEX not initialized, cannot retrieve indicators',
        ),
    ),
    (
        'indicator_types()',
        RuntimeError(
            'TCEX not initialized, cannot retrieve types',
        ),
    ),
    (
        "pivot(('a', 'b', 'c'), (1,2,3), (1.0, 2.0, 3.0))",
        TypeError(
            'f_pivot() takes from 1 to 2 positional arguments but 3 were given',
        ),
    ),
    (
        "pivot((('a', 'b', 'c'), (1,2,3), (1.0, 2.0, 3.0)))",
        [['a', 1, 1.0], ['b', 2, 2.0], ['c', 3, 3.0]],
    ),
    (
        "pivot((('a', 'b', 'c'), (1,2,3), (1.0, 2.0)))",
        [['a', 1, 1.0], ['b', 2, 2.0], ['c', 3, None]],
    ),
    (
        "pivot((('a', 'b', 'c'), (1,), (1.0, 2.0)))",
        [['a', 1, 1.0], ['b', None, 2.0], ['c', None, None]],
    ),
    (
        "pivot((('a', 'b', 'c'), [], (1.0, 2.0)))",
        [['a', None, 1.0], ['b', None, 2.0], ['c', None, None]],
    ),
    (
        "pivot((('a', 'b', 'c'), [], (1.0, 2.0)), pad='')",
        [['a', '', 1.0], ['b', '', 2.0], ['c', '', '']],
    ),
    (
        "build((1,2,3), ('a', 'b', 'c'), keys=('number', 'letter'))",
        [{'number': 1, 'letter': 'a'}, {'number': 2, 'letter': 'b'}, {'number': 3, 'letter': 'c'}],
    ),
    (
        "build((1,2,3), ('a', 'b', 'c'), keys=('number', 'letter', 'extra'))",
        [{'number': 1, 'letter': 'a'}, {'number': 2, 'letter': 'b'}, {'number': 3, 'letter': 'c'}],
    ),
    (
        "build((1,2,3), ('a', 'b'), keys=('number', 'letter', 'extra'))",
        [{'number': 1, 'letter': 'a'}, {'number': 2, 'letter': 'b'}],
    ),
    (
        "build((1,2,3), ('a', 'b', 'c'), keys=('number',))",
        [{'number': 1}, {'number': 2}, {'number': 3}],
    ),
    (
        "update([{'number': 1}, {'number': 2}, {'number': 3}], {'foo': 'bla'})",
        [{'number': 1, 'foo': 'bla'}, {'number': 2, 'foo': 'bla'}, {'number': 3, 'foo': 'bla'}],
    ),
    (
        "update([{'number': 1}, {'number': 2}, {'number': 3}], {'foo': 'bla', 'number': 0})",
        [{'number': 0, 'foo': 'bla'}, {'number': 0, 'foo': 'bla'}, {'number': 0, 'foo': 'bla'}],
    ),
    (
        "update([{'number': 1}, {'number': 2}, {'number': 3}], {'foo': 'bla', 'number': 0}, "
        'replace=False)',
        [{'number': 1, 'foo': 'bla'}, {'number': 2, 'foo': 'bla'}, {'number': 3, 'foo': 'bla'}],
    ),
    (
        "update([{'number': 1}, {'number': 2}, {'number': 3}, 'foo'], {'foo': 'bla'})",
        TypeError(
            'update must work on dictionaries or lists of dictionaries',
        ),
    ),
    ("merge((1,2,3), ('a','b','c'))", [[1, 'a'], [2, 'b'], [3, 'c']]),
    ("merge((1,2,3), ('a','b','c', 'd'))", [[1, 'a'], [2, 'b'], [3, 'c']]),
    (
        "merge(({'a': 1}, {'a': 2}, {'a': 3}), ({'b': 1}, {'b': 2}, {'b': 3}))",
        [{'a': 1, 'b': 1}, {'a': 2, 'b': 2}, {'a': 3, 'b': 3}],
    ),
    (
        "merge(({'a': 1}, {'a': 2}, {'a': 3}), ({'b': 1}, {'b': 2}, {'b': 3, 'a': 0}))",
        [{'a': 1, 'b': 1}, {'a': 2, 'b': 2}, {'a': 3, 'b': 3}],
    ),
    (
        "merge(({'a': 1}, {'a': 2}, {'a': 3}), ({'b': 1}, {'b': 2}, {'b': 3, 'a': 0}), "
        'replace=True)',
        [{'a': 1, 'b': 1}, {'a': 2, 'b': 2}, {'a': 0, 'b': 3}],
    ),
    ("alter({}, 'a', 1)", 1),
    (
        "report( ( ('a', 'b', 'c'), (1, 'bollux', 3), ('foo', 'bla', 'rumplestiltskin') ), header=True, title='Report', width=20)",
        '\n\n       Report       \n       ------       \n\nA   B      C        \n--- ------ ---------\n1   bollux 3        \nfoo bla    rum-     \n           plestilt-\n           skin     ',
    ),
    (
        "report( ( ('a', 'b', 'c'), (1, 'bollux', 3), ('foo', 'bla', 'rumplestiltskin') ), header=True, title='Report', width=80)",
        '\n\n                                     Report                                     \n                                     ------                                     \n\nA   B      C               \n--- ------ --------------- \n1   bollux 3              \nfoo bla    rumplestiltskin',
    ),
    (
        "report( ( ('a', 'b', 'c'), (1, 'bollux', 3), ('foo', 'bla', 'rumplestiltskin') ), header=True, title='Report', width=80, prolog='Report Prolog', epilog='Report Epilog')",
        '\n\n                                     Report                                     \n                                     ------                                     \n\n\nReport Prolog                                                                   \n\nA   B      C               \n--- ------ --------------- \n1   bollux 3              \nfoo bla    rumplestiltskin\n\nReport Epilog                                                                   \n',
    ),
    ('dict(one=1, two=2)', {'one': 1, 'two': 2}),
    (
        "kvlist( { 'name': 'Foo', 'value': 'Foo Value'}, {'name': 'Bla', 'value': 'Bla Value'})",
        TypeError(
            'dictlist must be a list of dictionaries',
        ),
    ),
    (
        "kvlist(({ 'key': 'Foo', 'value': 'Foo Value'}, {'key': 'Bla', 'value': 'Bla Value'}))",
        {'Foo': 'Foo Value', 'Bla': 'Bla Value'},
    ),
]


class TestFunctions(object):
    """Test atomic values"""

    def setup_class(self):
        """setup"""

        self.expr = Expression()
        self.expr.set('name', 'Matt')
        self.expr.set('one', 1)
        self.expr.set('two', 2.0)
        self.expr.set('self', self)
        self.expr.set('kosme', bytes('κόσμε', 'utf-8'))

    true = True

    @pytest.mark.parametrize('expression,result', FUNCTION_TESTS)
    def test_atom(self, expression, result):
        """test atomic values"""

        if isinstance(result, SkipIf):
            result = result.check_skip()

        if isinstance(result, float):
            result = nearly(result)

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

    @staticmethod
    def test_list_methods():
        """test_list_methods"""

        methods = list_methods()

        tested = {}
        scanning = False
        for method in methods.split('\n'):
            if method:
                method = method.strip()

            if method == '## Functions':
                scanning = True
                continue

            if not scanning:
                continue

            if not method:
                continue

            if method.startswith('#'):
                continue

            if method.startswith('* '):
                method = method[3:-1]
            else:
                continue

            name = method.strip().split('(')[0].strip()

            tested[name] = False

        for test, _ in FUNCTION_TESTS:
            method = test.split('(')[0].strip()

            if method in tested:
                tested[method] = True

        missing = []
        for method, checked in tested.items():
            if checked:
                continue
            missing.append(method)

        missing.sort()
        missing_tests = ', '.join(missing)

        assert not missing, f'Missing tests for {missing_tests}'
