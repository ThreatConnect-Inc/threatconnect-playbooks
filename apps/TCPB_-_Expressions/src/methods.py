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

# pylint: disable=no-member

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
import urllib.parse
import uuid
import typing
from typing import Union, List

import chardet
import ioc_fanger
import jmespath
import requests

from tcex.utils.date_utils import DatetimeUtils

import json_util
import structure
from literal import literal

from spamspy.spamsum import spamsum
from spamspy.edit_dist import edit_dist

from mergearray import mergearray
from reporting import Reporting
from rexxparse import RexxParser
from smartdict import SmartDict, smart_format
from throttle import Throttle
from xml_util import xml_to_dict, dict_to_xml

tzutil = DatetimeUtils()

NoneType = type(None)

aliases = ('spammatch', 'spamsum', 'spamdist', 'json')
THROTTLE_SEC = 3


def strbytes(value, annotation):
    """Convert value between str and bytes depending on annotation"""

    if not isinstance(value, (bytes, str)):
        return value

    if isinstance(value, str) and bytes in annotation and str not in annotation:
        return bytes(str(value), 'utf-8')

    if isinstance(value, bytes) and str in annotation and bytes not in annotation:
        return value.decode('utf-8')

    return value


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

            if hasattr(annotation, '_subs_tree'):
                annotation = annotation._subs_tree()[1:]  # this is a Union
            elif hasattr(typing, 'get_args'):
                union_args = typing.get_args(annotation)  # pylint: disable=E1101
                if union_args:
                    annotation = union_args

            if not isinstance(annotation, tuple):
                annotation = (annotation,)

            # print(f'Annotation is {annotation!r}')

            if kind is inspect.Parameter.VAR_POSITIONAL:
                # *args
                result = []
                for v in value:
                    # print(f'>?>{v} -> {annotation}')
                    # special case to deal with bytes inputs with no bytes but str in annotations
                    v = strbytes(v, annotation)
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
                    v = strbytes(v, annotation)
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
                value = strbytes(value, annotation)
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
    def f_acos(x: Union[int, float]):
        """Arc Cosine of X"""

        return math.acos(x)

    @coerce
    @staticmethod
    def f_acosh(x: Union[int, float]):
        """Inverse Hyperbolic Cosine"""

        return math.acosh(x)

    @staticmethod
    def f_alter(dictionary, key, value):
        """Set a specific key in a dictionary.  Returns the value."""

        if not isinstance(dictionary, dict):
            raise TypeError('First argument to alter must be a dictionary')

        dictionary[key] = value
        return value

    @coerce
    @staticmethod
    def f_asin(x: Union[int, float]):
        """Arc Sine of X"""

        return math.asin(x)

    @coerce
    @staticmethod
    def f_asinh(x: Union[int, float]):
        """Inverse Hyperbolic Sine"""

        return math.asinh(x)

    @coerce
    @staticmethod
    def f_atan(x: Union[int, float]):
        """Arc Tangent of X"""

        return math.atan(x)

    @coerce
    @staticmethod
    def f_atanh(x: Union[int, float]):
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
    def f_build(*lists, keys=()):
        """Constructs a sequence of dictionaries based on the lists, such
        that each dictionary contains the corresponding key for each list
        from the keys value, and value from each list, respectively.
        Columns without a key are ignored.  Columns that are longer than
        the shortest column are truncated."""

        result = []

        numkeys = len(keys)

        if len(lists) == 1 and isinstance(lists[0], (list, tuple)):
            lists = lists[0]

        for row in zip(*lists):
            rowdict = {}
            for column in range(min(numkeys, len(row))):
                rowdict[keys[column]] = row[column]
            result.append(rowdict)

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
    def f_ceil(x: Union[int, float]):
        """Ceiling of X"""

        return math.ceil(x)

    @coerce
    @staticmethod
    def f_center(s: str, width: int, fillchar=' '):
        """Center string in width columns"""

        return s.center(width, fillchar)

    @coerce
    @staticmethod
    def f_chardet(byteseq: bytes) -> dict:
        """Return a dictionary with the guessed character encoding
        of byteseq, the confidence of the encoding, and the estimated
        language."""

        return chardet.detect(byteseq)

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
    def f_cos(x: Union[int, float]):
        """Cosine of X"""

        return math.cos(x)

    @coerce
    @staticmethod
    def f_cosh(x: Union[int, float]):
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

    @staticmethod
    def f_defang(s: str):
        """Return a defanged representation of string, ie, one with
        textual indicators of compromise converted to the defanged state"""

        return ioc_fanger.defang(s)

    @coerce
    @staticmethod
    def f_degrees(x: Union[int, float]):
        """Convert X to degrees"""

        return math.degrees(x)

    @staticmethod
    def f_dict(**kwargs):
        """Return a dictionary of arguments"""
        d = OrderedDict()
        # kwarg keys can be tokens from the lexer
        for key, value in kwargs.items():
            d[str(key)] = value

        return d

    @coerce
    @staticmethod
    def f_erf(x: Union[int, float]):
        """Error Function of X"""

        return math.erf(x)

    @coerce
    @staticmethod
    def f_erfc(x: Union[int, float]):
        """Complimentary Error Function of X"""

        return math.erfc(x)

    @coerce
    @staticmethod
    def f_exp(x: Union[int, float]):
        """Math Exp of X"""

        return math.exp(x)

    @coerce
    @staticmethod
    def f_expm1(x: Union[int, float]):
        """Math Expm1 of X"""

        return math.expm1(x)

    @coerce
    def f_extract_indicators(
        self, data: Union[bytes, str], ignore=None, dedup=True, fang=False, convert=True
    ):
        """Extract IOCs from data, which may be bytes or string.
        If fang is true, data is re-fanged before processing. This option is
        ignored if the input is binary.
        Any entity match on the ignore list will be ignored.
        If convert is true, bytesmode matches will be converted to utf-8, or
        the specified conversion e.g. convert='latin-1'.
        Returns a list of (indicator, value) tuples.  If dedup is True,
        duplicate results are not returned."""

        results = []
        result_set = set()

        if ignore is None:
            ignore = []

        if not isinstance(ignore, list):
            ignore = [ignore]

        regexes = self.f_indicator_patterns()

        bytesmode = isinstance(data, bytes)
        if bytesmode:
            flags = re.MULTILINE | re.DOTALL
        else:
            flags = re.MULTILINE

        encoding = convert if isinstance(convert, str) else 'utf-8'

        extra_ignore = []
        for ignorable in ignore:
            if isinstance(ignorable, bytes):
                extra_ignore.append(ignorable.decode(encoding))

        ignore.extend(extra_ignore)

        if fang and not bytesmode:
            data = ioc_fanger.fang(data)

        for key, value in regexes.items():
            if value in ignore:
                continue
            if bytesmode:
                value = bytes(value, 'utf-8')
                if value in ignore:
                    continue
            all_hits = re.finditer(value, data, flags)
            for match in all_hits:
                hit = data[match.start() : match.end()]
                if bytesmode and convert:
                    hit = hit.decode(encoding)
                v = (key, hit)
                if dedup and v in result_set:
                    continue
                results.append(v)
                result_set.add(v)
        return results

    @coerce
    @staticmethod
    def f_factorial(x: float):
        """Factorial of X"""

        return math.factorial(x)

    @staticmethod
    def f_fang(s: str):
        """Return a fanged representation of string, ie, one with
        textual indicators of compromise reverted from the defanged state"""

        return ioc_fanger.fang(s)

    @functools.lru_cache(32)
    def indicator_name_to_branch(self, name):
        """Convert the indicator name to the API branch"""

        if '.' in name:
            name = name.split('.', 1)[0]

        indicator_types = self.f_indicator_types()

        for indicator_type in indicator_types:
            if indicator_type.get('name') == name:
                return indicator_type.get('apiBranch')

        return None

    def f_fetch_indicators(
        self, *search_values: Union[list, tuple], default_type=None
    ) -> List[dict]:
        """Fetches available indicators from ThreatConnect based on
        search_values.  A search value is either an indicator value (which uses
        the default_type as the indicator type) or a (type, value) pair.  If
        only one search_value is passed in, it may be a list of search_values.

        Returns a list of [(indicator_type, indicator_value, api_entity, indicator), ...],
        but the api_entity, result, and owners will be None if that
        indicator was not found.
        """

        # pylint: disable=no-member

        if not self.tcex:
            raise RuntimeError('TCEX not initialized, cannot retrieve indicators')

        result = []

        if len(search_values) == 1:  # did we get passed in a nested list?
            if isinstance(search_values[0], (list, tuple)):
                if len(search_values[0]) > 0:
                    if isinstance(search_values[0][0], (list, tuple)):
                        search_values = search_values[0]  # un-nest
                    elif not self.indicator_name_to_branch(search_values[0][0]):
                        # if the first word in the tuple isn't a type, un-nest it
                        search_values = search_values[0]  # un-nest

        for search_value in search_values:
            source = search_value

            if not isinstance(source, (list, tuple)):
                source = [default_type, source]

            self.tcex.log.debug(f'Looking up indicator {source!r}')

            indicator_name = source[0]
            indicator_value = source[1]
            api_branch = self.indicator_name_to_branch(indicator_name)
            if not api_branch:
                raise ValueError(f'{indicator_name} is not a known indicator type')

            path = (
                f'/v2/indicators/{urllib.parse.quote_plus(api_branch)}/'
                f'{urllib.parse.quote_plus(indicator_value)}'
            )
            indicator = self.tcex.session.get(path, params={'includeAdditional': 'true'}).json()
            if indicator['status'] != 'Success':
                api_entity = None
                answer = None
                self.tcex.log.debug(f'Failed fetching {path}: {indicator}')
            else:
                answer = indicator.get('data')
                api_entity = list(answer.keys())[0]
                answer = answer.get(api_entity)

            if answer:
                owners = self.tcex.session.get(
                    path + '/owners',
                ).json()
                if owners.get('status') != 'Success':
                    owners = None
                else:
                    owners = owners.get('data', {}).get('owner', None)

                answer['owners'] = owners

                observationCount = self.tcex.session.get(
                    path + '/observationCount',
                ).json()
                if observationCount.get('status') != 'Success':
                    observationCount = None
                else:
                    observationCount = observationCount.get('data', {}).get(
                        'observationCount', None
                    )

                answer['observationCount'] = observationCount

                attributes = self.tcex.session.get(
                    path + '/attributes',
                ).json()
                if attributes.get('status') != 'Success':
                    attributes = None
                else:
                    attributes = attributes.get('data', {}).get('attribute', None)

                answer['attribute'] = attributes

                securitylabels = self.tcex.session.get(
                    path + '/securityLabels',
                ).json()
                if securitylabels.get('status') != 'Success':
                    securitylabels = None
                else:
                    securitylabels = securitylabels.get('data', {}).get('securityLabel', None)

                answer['securityLabel'] = securitylabels

                groups = self.tcex.session.get(
                    path + '/groups',
                ).json()
                if groups.get('status') != 'Success':
                    groups = None
                else:
                    groups = groups.get('data', {}).get('group', [])

                answer['associations'] = groups

                tags = self.tcex.session.get(
                    path + '/tags',
                ).json()
                if tags.get('status') != 'Success':
                    tags = None
                else:
                    tags = tags.get('data', {}).get('tag', None)

                answer['tag'] = tags

            result.append((indicator_name, indicator_value, api_entity, answer))

        return result

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

    def f_format(self, s: str, *args, default=__notfound__, **kwargs):
        """Format string S according to Python string formatting rules.  Compound
        structure elements may be accessed with dot or bracket notation and without quotes
        around key names, e.g. `blob[0][events][0][source][device][ipAddress]`
        or `blob[0].events[0].source.device.ipAddress`.  If default is set,
        that value will be used for any missing value."""

        return smart_format(s, *args, _default=default, _context=self, **kwargs)

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
    def f_gamma(x: Union[int, float]):
        """Return the gamma function at X"""

        return math.gamma(x)

    @coerce
    @staticmethod
    def f_gcd(a: Union[int, float], b: Union[int, float]):
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
    def f_hypot(x: Union[int, float], y: Union[int, float]):
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

    @functools.lru_cache(maxsize=1)
    def f_indicator_patterns(self):
        """Returns a dictionary of regular expression patterns for indicators
        of compromise, based on ThreatConnect Data."""

        # pylint: disable=no-member

        if not self.tcex:
            raise RuntimeError('TCEX not initialized, cannot retrieve patterns')

        result = {}

        types = self.f_indicator_types()

        for ioc_type in types:
            entityName = ioc_type.get('apiEntity')
            self.tcex.log.debug(f'IndicatorType {entityName} = {ioc_type}')
            if ioc_type.get('parsable', 'false') != 'true':
                continue
            ioc_data = self.tcex.session.get(
                f'/v2/types/indicatorTypes/{entityName}', params={'includeAdditional': 'true'}
            ).json()
            self.tcex.log.debug(f'Indicator Data: {ioc_data}')
            if ioc_data['status'] != 'Success':
                continue
            type_keys = ioc_type.get('keys', {})
            ioc_name = ioc_type.get('name')
            key_names = [ioc_name + '.' + type_keys[x] for x in sorted(type_keys)]
            if len(key_names) == 1:
                key_names = [ioc_name]
            regexes = ioc_data.get('data', {}).get('indicatorType', {}).get('regexes', [])
            self.tcex.log.debug(f'Key Names: {key_names}, Regexes: {regexes}')
            pairs = zip(key_names, regexes)
            for kv in pairs:
                key, value = kv
                self.tcex.log.debug(f'regex {key} = {value}')
                result[key] = value
        self.tcex.log.debug(f'IOC Regexes: {result}')

        return result

    @functools.lru_cache(maxsize=1)
    def f_indicator_types(self):
        """Return the ThreatConnect Indicator Types"""
        # pylint: disable=no-member

        if not self.tcex:
            raise RuntimeError('TCEX not initialized, cannot retrieve types')

        types = self.tcex.session.get(
            '/v2/types/indicatorTypes', params={'includeAdditional': 'true'}
        ).json()
        if types['status'] != 'Success':
            raise RuntimeError('Failed to retrieve indicator types')

        return types.get('data', {}).get('indicatorType', [])

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
    def f_kvlist(dictlist: List[dict], key='key', value='value'):
        """Return a list of dictionaries as a single dictionary with the list
        item's key value as the key, and the list item's value value as the value.
        Duplicate keys will promote the value to a list of values."""

        result = {}
        duplicates = set()

        if not dictlist:
            return result

        if not isinstance(dictlist, (list, tuple)):
            raise TypeError('dictlist must be a list or tuple of dictionaries')

        for item in dictlist:
            if not isinstance(item, dict):
                raise TypeError('dictlist must only contain dictionaries')

            key_value = item.get(key, None)
            value_value = item.get(value, None)

            if key_value not in result:
                result[key_value] = value_value
            else:
                if key_value not in duplicates:
                    existing_value = [result[key_value]]
                    duplicates.add(key_value)
                else:
                    existing_value = result[key_value]
                existing_value.append(value_value)
                result[key_value] = existing_value

        return result

    @staticmethod
    def f_len(container):
        """Length of an iterable"""

        return len(container)

    @coerce
    @staticmethod
    def f_lgamma(x: Union[int, float]):
        """Return the natural logarithm of the absolute value of the gamma function at X"""

        return math.lgamma(x)

    @coerce
    @staticmethod
    def f_locale_currency(
        val: Union[int, float], symbol=True, grouping=False, international=False, locale='EN_us'
    ):
        """Format a currency value according to locale settings"""
        if locale:
            locale_.setlocale(locale_.LC_ALL, locale)
        else:
            locale_.setlocale(locale_.LC_ALL, '')

        return locale_.currency(val, symbol=symbol, grouping=grouping, international=international)

    @coerce
    @staticmethod
    def f_locale_format(
        fmt, val: Union[int, float], grouping=False, monetary=False, locale='EN_us'
    ):
        """Format a number according to locale settings"""
        if locale:
            locale_.setlocale(locale_.LC_ALL, locale)
        else:
            locale_.setlocale(locale_.LC_ALL, '')

        return locale_.format(fmt, val, grouping=grouping, monetary=monetary)

    @coerce
    @staticmethod
    def f_log(x: Union[int, float], base: Union[int, float, NoneType] = None):
        """Math Logarithm of X to base"""

        args = [x]
        if base:
            args.append(base)

        return math.log(*args)

    @coerce
    @staticmethod
    def f_log10(x: Union[int, float]):
        """Math log base 10 of X"""

        return math.log10(x)

    @coerce
    @staticmethod
    def f_log1p(x: Union[int, float]):
        """Math log1p of x"""

        return math.log1p(x)

    @coerce
    @staticmethod
    def f_log2(x: Union[int, float]):
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
    def f_merge(*iterables, replace=False):
        """Merges a list of iterables into a single list.
        If the iterables are dictionaries, they are updated into a
        single dictionary per row.  If replace is true, subsequent
        columns overwrite the original values.  The result length
        is constrained to the shortest column."""

        result = []
        for row in zip(*iterables):
            alldicts = True
            rowdict = {}
            rowarray = []
            for column in row:
                if not isinstance(column, dict):
                    alldicts = False
                    break
            for column in row:
                if alldicts:
                    if replace:
                        rowdict.update(column)
                    else:
                        for key, value in column.items():
                            if key not in rowdict:
                                rowdict[key] = value
                else:
                    rowarray.append(column)
            if alldicts:
                result.append(rowdict)
            else:
                result.append(rowarray)

        return result

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
    def f_pad(iterable, length: Union[int, literal], padvalue=None):
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
    def f_partitionedmerge(array1, array2):
        """Merges two arrays of strings to a single array with ordering
        preserved between partitions in the arrays.  Common lines are partitions
        subject to the ordering of the partitions being the same in each array.

        For example partitionedmerge(['A', 'a1', 'a2', 'B', 'b1', 'b2', 'D'],
        ['A', 'a3', 'a4', 'B', 'b3', 'b4', 'C', 'c1', 'c2', 'D'])

        is

        ['A', 'a1', 'a2', 'a3', 'a4', 'B', 'b1', 'b2', 'b3', 'b4', 'C', 'c1', 'c2', 'D']

        The values 'A', 'B', and 'D' act as partition lines for the merge.
        """

        return mergearray(array1, array2)

    @staticmethod
    def f_pivot(list_of_lists, pad=None):
        """Pivots a list of lists, such that item[x][y] becomes item[y][x].
        If the inner lists are not of even length, they will be padded with
        the pad value."""

        result = []
        width = 0

        if not isinstance(list_of_lists, (list, tuple)):
            raise TypeError('list_of_lists must be a list or a tuple')

        for row in list_of_lists:
            if not isinstance(row, (list, tuple)):
                raise TypeError('list_of_lists must contain lists or tuples')
            rowlen = len(row)
            if rowlen > width:
                width = rowlen

        for column in range(width):
            result.append([])  # initialize the pivot

        for row in list_of_lists:
            for column in range(width):
                value = row[column] if column < len(row) else pad
                result[column].append(value)

        return result

    @staticmethod
    def f_pformat(ob, indent: int = 1, width: int = 80, *, compact: bool = False):
        """Pretty formatter for displaying hierarchial data"""

        return pformat(ob, indent=indent, width=width, compact=compact)

    @coerce
    @staticmethod
    def f_pow(x: Union[int, float], y: Union[int, float]):
        """Math X ** Y"""

        return math.pow(x, y)

    @staticmethod
    def f_printf(fmt, *args):
        """Format arguments according to format"""

        return fmt % args

    def f_prune(self, ob, depth=None, prune=(None, '', [], {}), keys=()):
        """Recursively Prunes entries from the object,
        with an optional depth limit.  The pruned values, and
        optionally prune keys may be specified.  If any dictionary
        has a key in keys, that dictionary element will be removed.
        """

        if depth is not None:
            if depth <= 0:
                return ob
            depth -= 1

        if not isinstance(ob, (list, tuple, dict)):
            return ob

        if isinstance(keys, str):
            keys = (keys,)

        if isinstance(ob, (list, tuple)):
            result = []
            for value in ob:
                value = self.f_prune(value, depth, prune=prune)
                if value not in prune:
                    result.append(value)
            return result

        result = {}
        for key, value in ob.items():
            if key not in keys:
                value = self.f_prune(value, depth, prune=prune)
                if value not in prune:
                    result[key] = value
        return result

    @coerce
    @staticmethod
    def f_radians(x: Union[int, float]):
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

    def f_report(
        self,
        data: list,
        columns: list = None,
        title=None,
        header=True,
        width=None,
        prolog=None,
        epilog=None,
        sort=None,
        filter=None,  # pylint: disable=redefined-builtin
    ):
        """Generates a text report of data in columnar format.  Data is either a list of
        dictionaries, or a list of lists of columnar data.  If a list of lists,
        then the first row is the header row of the data.

        Columns is a list of row specifiers or a single row specifier, which is a list of
        column definitions.  If there are multiple row specifiers, each record takes up
        multiple output rows.

        A row specifier is either an ordered dictionary of name: column specifier or
        a list of (name, column specifier) tuples.

        A column specifier is width[:height][/option[=value]][/option[=value]]...
        If rows are lists of lists (e.g. CSV data) and no column specifiers are used, the
        widths will be automatically calculated.

        Options:

            - align=left|right|center

            - value=format    - format for values e.g. {lineno}.
                                to add a . after lineno

            - error=value     - value to use if the value= format causes an error

            - notrim          - Don't trim leading/trailing space

            - hang=n          - Hanging paragraph by N spaces

            - indent=n        - Indent paragraph by N spaces

            - split=n         - split at n% through the column (default 80)
                                if necessary

            - label=string    - heading label

            - doublenl        - Double newlines (ie, add line after paragraph)

            - nohyphenate     - Don't hyphenate value

        If sort is specified, it is a column or list of columns to sort by, with the column
        name optionally prefixed with a '-' to do a descending sort.

        If filter is specified, it is an expression that must be true for that record to appear
        in the result, e.g. filter="salary>70000".
        """

        reporting = Reporting(self)
        return reporting.create_report(
            data,
            columns=columns,
            title=title,
            header=header,
            width=width,
            prolog=prolog,
            epilog=epilog,
            sort=sort,
            filter=filter,
        )

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
    def f_round(number: Union[int, float], digits: int = 0):
        """Round number to digits decimal places"""

        return round(number, digits)

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
    def f_sin(x: Union[int, float]):
        """Sine of X"""

        return math.sin(x)

    @coerce
    @staticmethod
    def f_sinh(x: Union[int, float]):
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
    def f_sqrt(x: Union[int, float]):
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
    def f_sum(*elements: Union[int, float]):
        """Sum a list of elements"""

        if len(elements) == 1 and isinstance(elements, (tuple, list)):
            elements = elements[0]

        return math.fsum(elements)

    @coerce
    @staticmethod
    def f_tan(x: Union[int, float]):
        """Tangent of X"""

        return math.tan(x)

    @coerce
    @staticmethod
    def f_tanh(x: Union[int, float]):
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
    def f_trunc(x: Union[int, float]):
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
    def f_update(target: Union[dict, list, tuple], source: dict, replace=True):
        """Updates one dictionary with keys from the other. If the target is
        a list of dictionaries, each dictionary will be updated.  If replace
        is false, existing values will not be replaced."""

        if isinstance(target, dict):
            result = target.copy()
            if replace:
                result.update(source)
            else:
                for key, value in source.items():
                    if key not in result:
                        result[key] = value
            return result

        result = []
        for item in target:
            if not isinstance(item, dict):
                raise TypeError('update must work on dictionaries or lists of dictionaries')
            replacement = item.copy()
            if replace:
                replacement.update(source)
            else:
                for key, value in source.items():
                    if key not in replacement:
                        replacement[key] = value
            result.append(replacement)
        return result

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

    def f_url(self, method, url=None, **kwargs):
        """A direct dispatch of requests.request with an external session.  See
        https://docs.python-requests.org/en/latest/api for full API details.
        Returns a Response object, but callable methods on the response are
        not callable; retrieve the status via the .status_code attribute, or the content
        via the .content or .text attribute.

        If the URL is not specified, the first argument is assumed to be the URL
        and the method will default to 'GET'.

        If not specified, a timeout parameter of 30 seconds will be applied.
        The stream argument will *always* be set to True.
        The proxies argument will default to the system specified proxies.

        URL requests are throttled to one request every 3 seconds.

        If there is a json result, the json method on the result will
        be replaced with a json attribute that is the result of the json
        method, otherwise the json attribute will be set to None.

        Expressions-specific kwargs:
            rate=request rate per period  (default: 20)
            period=number of seconds in a period (default: 60)
            burst=number of requests to burst before throttling (default: 0)

        Only one rate throttle is maintained; switching throttles with multiple
        url function expressions will not yield intended results.
        """

        if url is None:
            url = method
            method = 'GET'

        if self.tcex:
            session = self.tcex.session_external
        else:
            session = getattr(self, 'session', None)

        if session is None:
            session = requests.Session()
            setattr(self, 'session', session)

        if 'timeout' not in kwargs:
            kwargs['timeout'] = 30

        kwargs['stream'] = False

        rate = kwargs.pop('rate', 20)
        period = kwargs.pop('period', 60)
        burst = kwargs.pop('burst', 0)
        throttle = getattr(self, 'throttle', None)

        if throttle is None:
            throttle = Throttle(rate, period, burst)
            setattr(self, 'throttle', throttle)

        if throttle.rate != rate or throttle.period != period or throttle.burst != burst:
            throttle()  # run the old throttle to run it out
            throttle = Throttle(rate, period, burst)
            setattr(self, 'throttle', throttle)

        throttle()

        if self.tcex:
            self.tcex.log.debug(f'URL: {method} {url} {kwargs}')
        result = session.request(method, url, **kwargs)
        if self.tcex:
            self.tcex.log.debug(f'URL result: {result}')

        try:
            json_data = result.json()
            setattr(result, 'json', json_data)
        except Exception:
            setattr(result, 'json', None)

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

    @staticmethod
    def f_uuid3(namespace, name):
        """Generate a UUID based on the MD5 hash of a namespace and a name.
        The namespace may be a UUID or one of 'dns', 'url', 'oid', or 'x500'.
        """

        namespace = namespace_to_uuid(namespace)

        return str(uuid.uuid3(namespace, name))

    @staticmethod
    def f_uuid4():
        """Generate a random UUID"""

        return str(uuid.uuid4())

    @staticmethod
    def f_uuid5(namespace, name):
        """Generate a UUID based on the SHA-1 hash of a namespace and a name.
        The namespace may be a UUID or one of 'dns', 'url', 'oid', or 'x500'.
        """

        namespace = namespace_to_uuid(namespace)

        return str(uuid.uuid5(namespace, name))

    @coerce
    @staticmethod
    def f_xmlread(xmldata: str, namespace=False, strip=True, convert=True, compact=False):
        """Constructs an object from XML data.  The XML data should have
        a single root node.  If namespace is True, the resolved namespace will
        be prefixed to tag names in braces, i.e. {namespace}tag.  If strip
        is True, values will be stripped of leading and trailing whitespace.
        If convert is True, numeric values will be converted to their numeric
        equivalents.  If compact is true, the object will be compacted to
        a more condensed form if possible.  Attribute names will be prefixed
        with @ in the corresponding output.
        """

        return xml_to_dict(
            xmldata,
            namespace=namespace,
            strip=strip,
            convert=convert,
            compact=compact,
        )

    @staticmethod
    def f_xmlwrite(obj, namespace=False, indent=0):
        """Converts an object to XML.  If namespace is True or a dictionary,
        namespace prefixed values will be converted to a derived or specified
        namespace value.  The namespace dictionary should be in the form
        {key: namespace} and will be used to turn the namespace back into the
        key. If indent is nonzero, an indented XML tree with newlines will
        be generated.  If namespaces are used, the caller must add the
        `xmlns` attributes to an enclosing scope.
        """

        return dict_to_xml(obj, namespace=namespace, indent=indent)


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
            if params and params[0] == 'self':
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


def namespace_to_uuid(namespace):
    """Convert a namespace into a UUID by lookup"""

    namespace = {
        'dns': uuid.NAMESPACE_DNS,
        'url': uuid.NAMESPACE_URL,
        'oid': uuid.NAMESPACE_OID,
        'x500': uuid.NAMESPACE_X500,
    }.get(namespace, namespace)

    if not isinstance(namespace, uuid.UUID):
        namespace = uuid.UUID(namespace)

    return namespace


if __name__ == '__main__':
    print(list_methods())
