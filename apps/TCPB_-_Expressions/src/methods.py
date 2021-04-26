# -*- coding: utf-8 -*-

"""Methods for expression module

The expression parser will look up functions on the
ExpressionMethods class here so long as the function name is prefixed
with f_, e.g. f_ceil for the ceil() function.

Use the @coerce decorator to cause type coercion based on the
signature to take place.  If the type is a tuple of types, any one
of the allowed types will qualify.  The coercion is necessary
for conversion of string equivalents to their float or int
counterparts.  The coercion is attempted left-to-right, so
if there are multiple allowed types, the second will be attempted
if the first fails, and so on.

Note that the parser has a string subclass named 'literal' which
it uses to denote a quoted literal value, which will NOT be coerced.

Attributes defined on the ExpressionMethod class are available
as constants to the expression handler, *without* the f_ prefix.
"""

import base64
from collections import OrderedDict, deque
import csv
import functools
import hashlib
import inspect
from io import StringIO
import json
import locale as locale_
import math
from pprint import pformat
import re
from string import Formatter
import urllib.parse
import jmespath

from tcex.utils.date_utils import DatetimeUtils

import json_util
import structure
from literal import literal

from spamspy.spamsum import spamsum
from spamspy.edit_dist import edit_dist

from attrdict import AttrDict
from rexxparse import RexxParser


tzutil = DatetimeUtils()

NoneType = type(None)

aliases = ('spammatch', 'spamsum', 'spamdist', 'json')


def coerce(f):
    """Coerce the arguments of f to the signatures in inspect.signatures"""

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        """argument coercion wrapper"""
        func = f
        # staticmethods ... argh
        if isinstance(f, staticmethod):
            func = f.__func__
            args = tuple(args[1:])
        sig = inspect.signature(func, follow_wrapped=True)
        bindings = sig.bind(*args, **kwargs)
        bindings.apply_defaults()

        # print(f'\n>>>Coercing for {func}')
        for param in bindings.arguments:
            value = bindings.arguments[param]

            annotation = sig.parameters[param].annotation
            kind = sig.parameters[param].kind

            # print(f'>>>Inspecting {param} with value {value}, type {kind}, '
            #      f'annotations {annotation}')
            if not annotation:
                continue

            if not isinstance(annotation, tuple):
                annotation = (annotation,)

            if kind is inspect.Parameter.VAR_POSITIONAL:
                # *args
                result = []
                for v in value:
                    # print(f'>?>{v} -> {annotation}')
                    # special case to deal with bytes inputs with no bytes but str in annotations
                    if isinstance(v, bytes) and bytes not in annotation and str in annotation:
                        v = v.decode('utf-8')
                    if not isinstance(v, annotation):
                        for constructor in annotation:
                            try:
                                v = constructor(v)
                                # print(f'>!>{v}')
                                break
                            except Exception:
                                pass
                    result.append(v)
                bindings.arguments[param] = result
            elif kind is inspect.Parameter.VAR_KEYWORD:
                # **kwargs
                for k, v in value.items():
                    # special case to deal with bytes inputs with no bytes but str in annotations
                    if isinstance(v, bytes) and bytes not in annotation and str in annotation:
                        v = v.decode('utf-8')
                    if not isinstance(v, annotation):
                        for constructor in annotation:
                            try:
                                v = constructor(v)
                                break
                            except Exception:
                                pass
                        value[k] = v
            else:
                # special case to deal with bytes inputs with no bytes but str in annotations
                if isinstance(value, bytes) and bytes not in annotation and str in annotation:
                    value = value.decode('utf-8')
                if not isinstance(value, annotation):
                    for constructor in annotation:
                        try:
                            value = constructor(value)
                            break
                        except Exception:
                            pass

                    bindings.arguments[param] = value

        return func(*bindings.args, **bindings.kwargs)

    return wrapper


__notfound__ = object()


class SmartDict:
    """Smart dictionary object"""

    def __init__(self, namespace, d=None):
        """init"""
        self.namespace = namespace
        if not d:
            d = {}
        self.values = d

    def __getitem__(self, name, default=__notfound__):
        """ get item from values *or* namespace """

        if name in self.values:
            value = self.values[name]
        else:
            value = self.namespace.get(name, __notfound__)

        if value is __notfound__:
            value = getattr(self.namespace, name, __notfound__)

        if value is __notfound__:
            value = default

        if value is __notfound__:
            raise KeyError(name)

        return self.encapsulate(value)

    get = __getitem__
    __getattr__ = __getitem__

    def encapsulate(self, value):
        """Encapsulate dicts into AttrDicts"""

        if not isinstance(value, (list, tuple, dict)):
            return value

        if isinstance(value, (list, tuple)):
            result = [self.encapsulate(x) for x in value]
            if isinstance(value, tuple):
                result = tuple(result)
            return result

        return AttrDict(value)


class ExpressionMethods:
    """Expression methods"""

    pi = math.pi
    e = math.e
    tau = math.tau
    urlre = re.compile(
        r"""\b
  # Word cannot begin with special characters
  (?<![@.,%&#-])
  # Protocols are optional, but take them with us if they are present
  (?P<protocol>\w{2,10}:\/\/)?
  # Domains have to be of a length of 1 chars or greater
  ((?:\w|\&\#\d{1,5};)[.-]?)+
  # The domain ending has to be between 2 to 15 characters
  (\.([a-z]{2,15})
       # If no domain ending we want a port, only if a protocol is specified
       |(?(protocol)(?:\:\d{1,6})|(?!)))
\b
# Word cannot end with @ (made to catch emails)
(?![@])
# We accept any number of slugs, given we have a char after the slash
(\/)?
# If we have endings like ?=fds include the ending
(?:([\w\d\?\-=#:%@&.;])+(?:\/(?:([\w\d\?\-=#:%@&;.])+))*)?
# The last char cannot be one of these symbols .,?!,- exclude these
(?<![.,?!-])""",
        re.VERBOSE,
    )

    @coerce
    @staticmethod
    def f_abs(x: float):
        """Absolute value of X"""

        return math.fabs(x)

    @coerce
    @staticmethod
    def f_acos(x: (int, float)):
        """Arc Cosine of X"""

        return math.acos(x)

    @coerce
    @staticmethod
    def f_acosh(x: (int, float)):
        """Inverse Hyperbolic Cosine"""

        return math.acosh(x)

    @coerce
    @staticmethod
    def f_asin(x: (int, float)):
        """Arc Sine of X"""

        return math.asin(x)

    @coerce
    @staticmethod
    def f_asinh(x: (int, float)):
        """Inverse Hyperbolic Sine"""

        return math.asinh(x)

    @coerce
    @staticmethod
    def f_atan(x: (int, float)):
        """Arc Tangent of X"""

        return math.atan(x)

    @coerce
    @staticmethod
    def f_atanh(x: (int, float)):
        """Inverse Hyperbolic Tangent"""

        return math.atanh(x)

    @staticmethod
    def f_b64decode(s: str, altchars=None, validate=False, encoding='utf-8'):
        """Base 64 decode of string"""

        result = base64.b64decode(s, altchars=altchars, validate=validate)
        if encoding:
            result = result.decode(encoding=encoding)
        return result

    @staticmethod
    def f_b64encode(s: str, altchars=None, encoding='utf-8'):
        """Base 64 encode of string"""

        if isinstance(s, str):
            s = bytes(s, encoding=encoding)

        result = base64.b64encode(s, altchars=altchars)
        if encoding:
            result = result.decode('utf-8')
        return result

    @coerce
    @staticmethod
    def f_bin(n: int, sign=True):
        """Return the binary value of int"""
        result = bin(n)
        if result.startswith('-'):
            if sign:
                result = '-' + result[3:]
            else:
                result = result[3:]
        else:
            result = result[2:]
        return result

    @staticmethod
    def f_bytes(s: str, encoding='utf-8', errors=None):
        """Convert object to binary string (bytes)"""
        arg = [s]
        if encoding:
            arg.append(encoding)
            if errors:
                arg.append(errors)

        return bytes(*arg)

    @coerce
    @staticmethod
    def f_ceil(x: (int, float)):
        """Ceiling of X"""

        return math.ceil(x)

    @coerce
    @staticmethod
    def f_center(s: str, width: int, fillchar=' '):
        """Center string in width columns"""

        return s.center(width, fillchar)

    @staticmethod
    def f_choice(condition, true_result=None, false_result=None):
        """Choice of true_result or false_result based on condition"""

        if condition:
            return true_result
        return false_result

    @coerce
    @staticmethod
    def f_chr(x: int):
        """Return character value of x"""

        return chr(x)

    @staticmethod
    def f_conform(object_list, missing_value=None):
        """Conform objects in a list to have the same structure,
        using missing_value as the value of any missing key
        """

        return json_util.conform_objects(object_list, missing_value=missing_value)

    @coerce
    @staticmethod
    def f_copysign(x: float, y: float):
        """Copy sign of X to Y"""

        return math.copysign(x, y)

    @coerce
    @staticmethod
    def f_cos(x: (int, float)):
        """Cosine of X"""

        return math.cos(x)

    @coerce
    @staticmethod
    def f_cosh(x: (int, float)):
        """Hyperbolic Cosine"""

        return math.cosh(x)

    @staticmethod
    def f_csvread(data, header=False, convert=True, delimiter=',', quote='"', rows=0, columns=0):
        """Process data as a CSV File.  Return the data as a list of rows of columns,
        or if rows=1, return a list of columns).  If header is true, the first record
        is discarded.  If rows or columns is nonzero, the row or column count will
        be truncated to that number of rows or columns. If convert is True, numeric
        values will be returned as numbers, not strings"""

        if isinstance(data, bytes):
            data = data.decode('utf-8')

        buffer = StringIO(data)

        result = []

        reader = csv.reader(buffer, delimiter=delimiter, quotechar=quote)
        for rowdata in reader:
            if columns and len(rowdata) > columns:
                rowdata = rowdata[:columns]

            if convert:
                rd = []
                for value in rowdata:
                    i = None
                    f = None
                    try:
                        f = float(value)
                        i = int(value)
                    except ValueError:
                        pass
                    if i is not None or f is not None:
                        if f and i != f:
                            value = f
                        else:
                            value = i
                    rd.append(value)
                rowdata = rd

            result.append(rowdata)

        if header and result:
            result.pop(0)

        if rows and len(result) > rows:
            result = result[:rows]

        if rows == 1 or rows == 0 and len(result) == 1:
            return result[0]

        return result

    @staticmethod
    def f_csvwrite(data, delimiter=',', quote='"'):
        """Write data in CSV format.  Returns a string"""

        buffer = StringIO()

        writer = csv.writer(buffer, delimiter=delimiter, quotechar=quote)

        writer.writerow(data)

        return buffer.getvalue()

    @staticmethod
    def f_datetime(datetime, date_format=None, tz=None):
        """Format a datetime object according to a format string"""

        return tzutil.format_datetime(datetime, tz=tz, date_format=date_format)

    @coerce
    @staticmethod
    def f_degrees(x: (int, float)):
        """Convert X to degrees"""

        return math.degrees(x)

    @coerce
    @staticmethod
    def f_erf(x: (int, float)):
        """Error Function of X"""

        return math.erf(x)

    @coerce
    @staticmethod
    def f_erfc(x: (int, float)):
        """Complimentary Error Function of X"""

        return math.erfc(x)

    @coerce
    @staticmethod
    def f_exp(x: (int, float)):
        """Math Exp of X """

        return math.exp(x)

    @coerce
    @staticmethod
    def f_expm1(x: (int, float)):
        """Math Expm1 of X"""

        return math.expm1(x)

    @coerce
    @staticmethod
    def f_factorial(x: float):
        """Factorial of X"""

        return math.factorial(x)

    def f_find(self, ob, value, start=None, stop=None):
        """Find index value in ob or return -1"""

        try:
            return self.f_index(ob, value, start, stop)
        except ValueError:
            return -1

    @staticmethod
    def f_flatten(ob, prefix=''):
        """Flatten a possibly nested list of dictionaries to a list, prefixing keys with prefix"""

        return json_util.refold(ob, prefix)

    @staticmethod
    def f_float(s):
        """Return floating point value of object"""

        return float(s)

    def f_format(self, s: str, *args, **kwargs):
        """Format string S according to Python string formatting rules.  Compound
        structure elements may be accessed with dot or bracket notation and without quotes
        around key names, e.g. `blob[0][events][0][source][device][ipAddress]`
        or `blob[0].events[0].source.device.ipAddress`"""

        kws = SmartDict(self, kwargs)
        fmt = Formatter()

        return fmt.vformat(s, args, kws)

    @staticmethod
    def f_fuzzydist(hash1, hash2):
        """Return the edit distance between two fuzzy hashes"""

        return edit_dist(hash1, hash2)

    @staticmethod
    def f_fuzzyhash(data):
        """Return the fuzzy hash of data"""

        return spamsum(data)

    @staticmethod
    def f_fuzzymatch(input1, input2):
        """Return a score from 0..100 representing a poor match (0) or
        a strong match(100) between the two inputs"""

        sum1 = spamsum(input1)
        sum2 = spamsum(input2)

        score = edit_dist(sum1, sum2) * 64 / (len(input1) + len(input2))

        score = (score * 100.0) / 64
        if score >= 100:
            return 0

        return 100.0 - score

    @coerce
    @staticmethod
    def f_gamma(x: (int, float)):
        """Return the gamma function at X"""

        return math.gamma(x)

    @coerce
    @staticmethod
    def f_gcd(a: (int, float), b: (int, float)):
        """Greatest Common Denominator of A and B"""
        return math.gcd(a, b)

    @coerce
    @staticmethod
    def f_hex(n: int, sign=True):
        """Return the hexadecimal value of int"""
        result = hex(n)
        if result.startswith('-'):
            if sign:
                result = '-' + result[3:]
            else:
                result = result[3:]
        else:
            result = result[2:]
        return result

    @coerce
    @staticmethod
    def f_hypot(x: (int, float), y: (int, float)):
        """Hypotenuse of X,Y"""

        return math.hypot(x, y)

    @staticmethod
    def f_index(ob, value, start=None, stop=None):
        """Index of value in ob"""

        args = [value]
        if start:
            args.append(start)
            if stop:
                args.append(stop)

        return ob.index(*args)

    @staticmethod
    def f_int(s, radix=None):
        """Return integer value of object"""

        if radix:
            return int(s, radix)
        return int(s)

    @staticmethod
    def f_items(ob: dict):
        """Items (key, value pairs) of dictionary"""

        return list(ob.items())

    @staticmethod
    def f_jmespath(path, ob):
        """JMESPath search"""

        if isinstance(ob, str):
            ob = json.loads(ob)

        return jmespath.search(path, ob)

    @staticmethod
    def f_join(separator, *elements):
        """Join a list with separator"""

        if len(elements) == 1 and isinstance(elements[0], (list, tuple)):
            elements = elements[0]

        return separator.join(elements)

    @staticmethod
    def f_json(ob, sort_keys=True, indent=2):
        """Dump an object to a JSON string"""

        return json.dumps(ob, sort_keys=sort_keys, indent=indent, ensure_ascii=False)

    @staticmethod
    def f_json_load(ob):
        """Load an object from a JSON string"""

        return json.loads(ob)

    @staticmethod
    def f_keys(ob: dict):
        """Keys of dictionary"""

        return list(ob.keys())

    @staticmethod
    def f_len(container):
        """Length of an iterable"""

        return len(container)

    @coerce
    @staticmethod
    def f_lgamma(x: (int, float)):
        """Return the natural logarithm of the absolute value of the gamma function at X"""

        return math.lgamma(x)

    @coerce
    @staticmethod
    def f_locale_currency(
        val: (int, float), symbol=True, grouping=False, international=False, locale='EN_us'
    ):
        """Format a currency value according to locale settings"""
        if locale:
            locale_.setlocale(locale_.LC_ALL, locale)
        else:
            locale_.setlocale(locale_.LC_ALL, '')

        return locale_.currency(val, symbol=symbol, grouping=grouping, international=international)

    @coerce
    @staticmethod
    def f_locale_format(fmt, val: (int, float), grouping=False, monetary=False, locale='EN_us'):
        """Format a nubmer according to locale settings"""
        if locale:
            locale_.setlocale(locale_.LC_ALL, locale)
        else:
            locale_.setlocale(locale_.LC_ALL, '')

        return locale_.format(fmt, val, grouping=grouping, monetary=monetary)

    @coerce
    @staticmethod
    def f_log(x: (int, float), base: (int, float, NoneType) = None):
        """Math Logarithm of X to base"""

        args = [x]
        if base:
            args.append(base)

        return math.log(*args)

    @coerce
    @staticmethod
    def f_log10(x: (int, float)):
        """Math log base 10 of X"""

        return math.log10(x)

    @coerce
    @staticmethod
    def f_log1p(x: (int, float)):
        """Math log1p of x"""

        return math.log1p(x)

    @coerce
    @staticmethod
    def f_log2(x: (int, float)):
        """Math log base 2 of X"""

        return math.log2(x)

    @coerce
    @staticmethod
    def f_lower(s: str):
        """Lowercase string"""

        return s.lower()

    @coerce
    @staticmethod
    def f_lstrip(s: str, chars=None):
        """Strip chars from left of string"""

        return s.lstrip(chars)

    @coerce
    @staticmethod
    def f_max(*items):
        """Return the greatest value of the list"""

        return max(*items)

    @staticmethod
    def f_md5(data):
        """Return MD5 hash of data"""

        h = hashlib.md5()
        if not isinstance(data, bytes):
            data = bytes(str(data), 'utf-8')
        h.update(data)
        return h.hexdigest()

    @coerce
    @staticmethod
    def f_min(*items):
        """Return the least value of the list"""

        return min(*items)

    @staticmethod
    def f_namevallist(ob: dict, namekey='name', valuekey='value'):
        """Return a dictionary formatted as a list of name=name, value=value dictionaries"""

        result = []
        for key, value in ob.items():
            result.append({namekey: key, valuekey: value})
        return result

    @staticmethod
    def f_ord(char):
        """Return ordinal value of char"""

        return ord(char)

    @coerce
    @staticmethod
    def f_pad(iterable, length: (int, literal), padvalue=None):
        """Pad iterable to length"""

        if not isinstance(length, int):
            raise TypeError('length must be integer')

        if len(iterable) >= length:
            return iterable

        if isinstance(iterable, str):
            if padvalue is None:
                padvalue = ' '
            if not isinstance(padvalue, str) or len(padvalue) != 1:
                raise ValueError('pad value must be string of length one')
            return iterable + padvalue * (length - len(iterable))

        result = list(iterable)
        while len(result) < length:
            result.append(padvalue)

        return result

    @staticmethod
    def f_pformat(ob, indent: int = 1, width: int = 80, *, compact: bool = False):
        """Pretty formatter for displaying hierarchial data"""

        return pformat(ob, indent=indent, width=width, compact=compact)

    @coerce
    @staticmethod
    def f_pow(x: (int, float), y: (int, float)):
        """Math X ** Y"""

        return math.pow(x, y)

    @staticmethod
    def f_printf(fmt, *args):
        """Format arguments according to format"""

        return fmt % args

    def f_prune(self, ob, depth=None, prune=(None, '', [], {})):
        """Recursively Prunes entries from the object,
        with an optional depth limit
        """

        if depth is not None:
            if depth <= 0:
                return ob
            depth -= 1

        if not isinstance(ob, (list, tuple, dict)):
            return ob

        if isinstance(ob, (list, tuple)):
            result = []
            for value in ob:
                value = self.f_prune(value, depth, prune=prune)
                if value not in prune:
                    result.append(value)
            return result

        result = {}
        for key, value in ob.items():
            value = self.f_prune(value, depth, prune=prune)
            if value not in prune:
                result[key] = value
        return result

    @coerce
    @staticmethod
    def f_radians(x: (int, float)):
        """Convert X to radians"""

        return math.radians(x)

    @staticmethod
    def f_range(start_or_stop, stop=None, step=None):
        """Return range of values"""

        args = [start_or_stop]
        if stop is not None:
            args.append(stop)
            if step is not None:
                args.append(step)

        return list(range(*args))

    @staticmethod
    def f_refindall(pattern, string, flags=''):
        """Find all instances of the regular expression in source"""

        f = 0
        if isinstance(flags, int):
            f = flags
        elif isinstance(flags, str):
            for c in flags:
                c = c.upper()
                i = getattr(re, c, None)
                if i:
                    f += i

        result = []
        match_iter = re.finditer(pattern, string, flags=f)
        for m in match_iter:
            result.append(m.group())

        if result:
            return result

        return None

    @staticmethod
    def f_rematch(pattern, string, flags=''):
        """Regular expression match pattern to source"""

        f = 0
        if isinstance(flags, int):
            f = flags
        elif isinstance(flags, str):
            for c in flags:
                c = c.upper()
                i = getattr(re, c, None)
                if i:
                    f += i

        m = re.match(pattern, string, flags=f)
        if m:
            return m.group()
        return None

    @coerce
    @staticmethod
    def f_replace(s: str, source: str, target: str):
        """Replace chars on S"""

        return s.replace(source, target)

    @staticmethod
    def f_research(pattern, string, flags=''):
        """Regular expression search pattern to source"""

        f = 0
        if isinstance(flags, int):
            f = flags
        elif isinstance(flags, str):
            for c in flags:
                c = c.upper()
                i = getattr(re, c, None)
                if i:
                    f += i

        m = re.search(pattern, string, flags=f)
        if m:
            return m.group()
        return None

    @coerce
    def f_rexxparse(self, source: str, template: str, strip=False, convert=False, **kwargs):
        """REXX parse of source using template.  If strip is True, values are stripped,
        if convert is True, values are converted to float or int if possible.  Any other
        keyword arguments are made available for indirect pattern substitution, in
        addition to the standard variables."""

        rp = RexxParser(template)

        context = SmartDict(self, kwargs)
        result = rp.parse(source, context=context)
        if strip or convert:
            for key, value in result.items():
                if strip:
                    value = value.strip()
                if convert:
                    try:
                        ov = value
                        value = float(value)
                        if int(value) == value and '.' not in ov:
                            value = int(value)
                    except (TypeError, ValueError):
                        pass

                result[key] = value
        return result

    @coerce
    @staticmethod
    def f_rstrip(s: str, chars=None):
        """Strip chars from right of string"""

        return s.rstrip(chars)

    @staticmethod
    def f_sha1(data):
        """Return SHA1 hash of data"""

        h = hashlib.sha1()
        if not isinstance(data, bytes):
            data = bytes(str(data), 'utf-8')
        h.update(data)
        return h.hexdigest()

    @staticmethod
    def f_sha256(data):
        """Return SHA256 hash of data"""

        h = hashlib.sha256()
        if not isinstance(data, bytes):
            data = bytes(str(data), 'utf-8')
        h.update(data)
        return h.hexdigest()

    @coerce
    @staticmethod
    def f_sin(x: (int, float)):
        """Sine of X"""

        return math.sin(x)

    @coerce
    @staticmethod
    def f_sinh(x: (int, float)):
        """Hyperbolic Sine"""

        return math.sinh(x)

    @staticmethod
    def f_sort(*elements):
        """Sort array"""

        elements = list(elements)

        if len(elements) == 1 and isinstance(elements[0], (tuple, list)):
            elements = list(elements[0])

        elements.sort()
        return elements

    @staticmethod
    def f_split(string, separator=None, maxsplit=-1):
        """Split a string into elements"""

        return string.split(separator, maxsplit)

    @coerce
    @staticmethod
    def f_sqrt(x: (int, float)):
        """Square root of X"""

        return math.sqrt(x)

    @staticmethod
    def f_str(s, encoding='utf-8'):
        """Return string representation of object"""

        if hasattr(s, 'decode'):
            s = s.decode(encoding)

        # return a literal so it wont generally be re-decoded
        return literal(s)

    @coerce
    @staticmethod
    def f_strip(s: str, chars=None):
        """Strip chars from ends of string"""

        return s.strip(chars)

    @staticmethod
    def f_structure(ob):
        """Return a reduced structure of the object, useful for comparisons"""

        return structure.reduce_structure(ob)

    @coerce
    @staticmethod
    def f_sum(*elements: (int, float)):
        """Sum a list of elements"""

        if len(elements) == 1 and isinstance(elements, (tuple, list)):
            elements = elements[0]

        return math.fsum(elements)

    @coerce
    @staticmethod
    def f_tan(x: (int, float)):
        """Tangent of X"""

        return math.tan(x)

    @coerce
    @staticmethod
    def f_tanh(x: (int, float)):
        """Hyperbolic Tangent"""

        return math.tanh(x)

    @staticmethod
    def f_timedelta(datetime_1, datetime_2):
        """Return the delta between time 1 and time 2"""

        return tzutil.timedelta(datetime_1, datetime_2)

    @coerce
    @staticmethod
    def f_title(s: str):
        """Title of string"""

        return s.title()

    @coerce
    @staticmethod
    def f_trunc(x: (int, float)):
        """Math Truncate X"""

        return math.trunc(x)

    @coerce
    @staticmethod
    def f_twoscompliment(n: int, bits=32):
        """Return the twos compliment of N with the desired word width"""
        if (n & (1 << (bits - 1))) != 0:
            n = n - (1 << bits)
        return n

    @coerce
    @staticmethod
    def f_update(target: dict, source: dict):
        """Updates one dictionary with keys from the other"""

        target = target.copy()
        target.update(source)
        return target

    @coerce
    @staticmethod
    def f_upper(s: str):
        """Uppercase string"""

        return s.upper()

    @staticmethod
    def f_values(ob: dict):
        """Values of dictionary"""

        return list(ob.values())

    f_spammatch = f_fuzzymatch

    @staticmethod
    def f_unique(*args):
        """Return the list of unique elements of arguments, which may be a list of arguments, or a
        single argument that is a list.  Inputs are compared by converting them to
        sorted JSON objects, so dictionaries with the same keys and values but different
        order will count as duplicates."""

        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            args = args[0]

        seen = set()
        result = []
        for element in args:
            key = json.dumps(element, sort_keys=True, ensure_ascii=False)
            if key in seen:
                continue
            result.append(element)
            seen.add(key)

        return result

    @staticmethod
    def f_unnest(iterable):
        """Reduces nested list to a single flattened list.  [A, B, [C, D, [E, F]]
        turns into [A, B, C, D, E, F]."""

        result = []
        if isinstance(iterable, (str, literal)):
            return iterable

        try:
            queue = deque(iterable)
        except TypeError:
            return iterable

        while queue:
            item = queue.popleft()
            if isinstance(item, (list, tuple)):
                insertions = deque(item)
                insertions.reverse()
                queue.extendleft(insertions)
            else:
                result.append(item)

        return result

    @staticmethod
    def f_urlparse(urlstring, scheme='', allow_fragments=True):
        """Parse a URL into a six component named tuple"""

        return urllib.parse.urlparse(urlstring, scheme=scheme, allow_fragments=allow_fragments)

    @staticmethod
    def f_urlparse_qs(
        qs,
        keep_blank_values=False,
        strict_parsing=False,
        encoding='utf-8',
        errors='replace',
        max_num_fields=None,
    ):
        """Parse a URL query string into a dictionary.  Each value is a list."""

        return urllib.parse.parse_qs(
            qs,
            keep_blank_values=keep_blank_values,
            strict_parsing=strict_parsing,
            encoding=encoding,
            errors=errors,
            max_num_fields=max_num_fields,
        )

    f_binary = f_bytes
    f_json_dump = f_json
    f_spamsum = f_fuzzyhash
    f_spamdist = f_fuzzydist


def list_methods():
    """List expression methods"""

    constants = OrderedDict()
    methods = OrderedDict()
    docstr = OrderedDict()

    e = ExpressionMethods()

    for key in sorted(dir(e)):
        if key.startswith('_'):
            continue
        value = getattr(e, key, None)

        if not callable(value):
            try:
                if value.__class__.__name__ == 'SRE_Pattern':
                    # pylint: disable=unnecessary-comprehension
                    pat = '\n        '.join([x for x in value.pattern.split('\n')])
                    value = f'Regular Expression\n\n        {pat}'
            except Exception:
                pass
            constants[key] = value
        elif key.startswith('f_'):
            func = key[2:]

            if func in aliases:
                continue

            # unwrap value
            while hasattr(value, '__wrapped__'):
                value = value.__wrapped__

            if hasattr(value, '__func__'):
                value = value.__func__
            sig = inspect.signature(value)
            doc = value.__doc__

            params = []
            for param in sig.parameters.values():
                name = param.name
                if param.kind == inspect.Parameter.VAR_POSITIONAL:
                    name = '*' + name
                elif param.kind == inspect.Parameter.VAR_KEYWORD:
                    name = '**' + name
                if param.default is not inspect.Parameter.empty:
                    params.append(f'{name}={param.default!r}')
                else:
                    params.append(name)
            if params[0] == 'self':
                del params[0]

            methods[func] = ', '.join(params)
            docstr[func] = '\n    '.join([x.strip() for x in doc.split('\n')])

    result = []
    result.append('\n# Builtins\n')
    result.append('\n## Constants\n')
    for key, value in constants.items():
        result.append(f'  * {key} = {value}')
    result.append('\n## Functions\n')
    for key, value in methods.items():
        result.append(f'  * `{key}({value})`')
        result.append('')
        result.append(f'    {docstr[key]}')
        result.append('')

    return '\n'.join(result)


if __name__ == '__main__':
    print(list_methods())
