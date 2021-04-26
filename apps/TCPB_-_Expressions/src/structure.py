# -*- coding: utf-8 -*-
"""Structure Comparision Tool"""
# standard library
import ipaddress
import re


class When:
    """Class to have conditional regexes"""

    def __init__(self, regex, *args, **kwargs):
        """Initialize the When construct"""

        self.regex = regex
        self.args = args
        self.kwargs = kwargs


DEBUG = False

RULES = {
    'int': re.compile(r'(?:(?<=\s)|^)[+-]?[0-9]+\b(?!\.[0-9]|\S)'),
    'float': re.compile(r'(?:(?<=\s)|\b)[+-]?(?:\d*\.\d+|\d+\.\d*)(?=\s|$)'),
    'epoch': When(
        re.compile(r'\b\d+(?:\.\d+)?\b'), lambda x: float(x) > 900000000 and float(x) < 900000000000
    ),
    'epochms': When(re.compile(r'\b\d+(?:\.\d+)?\b'), lambda x: float(x) > 900000000000),
    'guid': re.compile(r'\b[{]?[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}[}]?\b', re.I),
    'iso8601': re.compile(
        r'\d{4}-?\d{2}-?\d{2}T\d{2}:?\d{2}:?\d{2}(?:\.\d{0,3})?(?:[+-]\d{2}:\d{2}|Z)?'
    ),
    'date': (
        re.compile(
            r'\d{1,2} (?:Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?'
            r'|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?) \d{2,4}',
            re.I,
        ),
        re.compile(
            r'(?:Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?'
            r'|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?) \d{1,2}, \d{2,4}',
            re.I,
        ),
        re.compile(r'\d{2}/\d{2}/\d{2,4}'),
        re.compile(r'\d{2,4}-\d{2}-\d{2}'),
    ),
    'time': (
        re.compile(
            r'\d{1,2}:\d{2}(?::\d{2}(?:\.\d+)?)?(?: ?AM| ?PM|Z|[+-]\d{2}:?(?:\d{2})?)?', re.I
        )
    ),
    'url': (
        re.compile(
            r'(?:(?:https?|ftp):\/\/)(?:\S+(?::\S*)?@)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})'
            r'(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])'
            r'(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])'
            r'(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}'
            r'(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*'
            r'[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*'
            r'[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,}))\.?)'
            r'(?::\d{2,5})?(?:[/?#]\S*)?',
            re.I,
        )
    ),
    'ip': (
        When(
            re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', re.I),
            ipaddress.ip_address,
        ),
        When(re.compile(r'\b([a-f0-9:]+:+)+[a-f0-9]+\b', re.I), ipaddress.ip_address),
    ),
    'md5': re.compile(r'\b[0-9a-f]{32}\b', re.I),
    'sha1': re.compile(r'\b[0-9a-f]{40}\b', re.I),
    'sha256': re.compile(r'\b[0-9a-f]{64}\b', re.I),
}


def reduce_value(value):
    """Reduce the value to a string for typing"""

    result = None

    if isinstance(value, bool):
        result = 'bool'
    elif isinstance(value, float):
        result = 'float'
    elif isinstance(value, int):
        result = 'int'
    elif isinstance(value, bytes):
        result = 'binary'
    elif isinstance(value, str):
        result = describe_string(value)
    elif value is None:
        result = 'null'
    elif isinstance(value, dict):
        result = 'dict'
    elif isinstance(value, (list, tuple)):
        result = 'list'

    return result


def reduce_structure(value):
    """Reduce a structure to a prototypical form"""

    if isinstance(value, dict):
        result = {}
        for key in value:
            result[key] = reduce_structure(value[key])
    elif isinstance(value, (list, tuple)):
        result = [reduce_structure(x) for x in value]
        if len(result) > 1:
            result = result[:1]  # TODO try to handle lists of *different* things
        if isinstance(value, tuple):
            result = tuple(result)
    else:
        result = reduce_value(value)

    return result


def sort_possibles(x):
    """Sort Key For Possibles"""

    # pylint: disable=unused-variable
    name, regex, search, match, conditions = x

    lc = len(conditions)
    if search:
        span = search.span()
        ls = span[1] - span[0]
    else:
        ls = 0
    if match:
        span = match.span()
        lm = span[1] - span[0]
    else:
        lm = 0

    # Return a negative sort key based on
    # ls - the length of the matching string
    # lm - the length of the full match * 100
    # lc - the number of matching conditions * 10000
    return -(lc * 10000 + lm * 100 + ls)


def describe_string(value):
    """Transform the string value to one or more rule names"""

    if DEBUG:
        print(f'Examining {value!r}')

    if not isinstance(value, str):
        return ''

    value = value.strip()
    if not value:
        return ''

    possibles = []

    # pylint: disable=too-many-nested-blocks
    for name, rules in RULES.items():
        if not isinstance(rules, (list, tuple)):
            rules = [rules]
        for rule in rules:
            conditions = []
            if isinstance(rule, When):
                regex = rule.regex
                conditions = rule.args
            else:
                regex = rule

            match = None
            search = None
            if regex:
                try:
                    match = regex.fullmatch(value)
                    # print(f'\tfullmatch matched {match}')
                except Exception:
                    match = None

                try:
                    search = regex.search(value)
                    # print(f'\tsearch matched {search}')
                except Exception:
                    search = None

                if not search:
                    continue

            all_conditions = True
            for condition in conditions:
                if all_conditions and callable(condition):
                    # print(f'Trying condition {condition}')
                    try:
                        mv = value
                        if search:
                            mv = search.group()
                        if not condition(mv):
                            # print(f'\t{name} condition failed {condition}')
                            all_conditions = False
                        else:
                            # print(f'\t{name} condition passed {condition}')
                            pass
                    except Exception:
                        all_conditions = False
                        # print(f'\t{name} condition raised exception {condition}')
                if not all_conditions:
                    break

            if all_conditions:
                possibles.append((name, regex, search, match, conditions))

    # now, for each possible match, sort the possibles based on

    possibles.sort(key=sort_possibles)

    if DEBUG:
        for possible in possibles:
            print(possible)

    if not possibles:
        return 'string'

    name, regex, search, match, conditions = possibles[0]
    #
    # TODO -- apply as many of the non-overlapping possibles in one
    # pass
    #

    if search:
        left = search.string[: search.start()]
        right = search.string[search.end() :]  # noqa: E203

        r = []
        if left:
            left = describe_string(left)
            if left:
                r.append(left)
        r.append(name)

        if right:
            right = describe_string(right)
            if right:
                r.append(right)

        result = ' '.join(r)
    else:
        result = name

    return result
