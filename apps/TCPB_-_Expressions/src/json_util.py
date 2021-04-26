#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Read a JSON document and kick out the equivalent output section of install.json"""

# standard library
from warnings import warn


def camel2snake(s):
    """Convert a camelCase name to snake_case"""
    o = ''
    lastcap = False
    for letter in s:
        lc = letter.lower()
        if not lc.isalpha():
            lastcap = True
        if lc == '-':
            lc = '_'
            lastcap = True
        elif not lc.isalpha():
            lastcap = True
        elif lc != letter:
            if not lastcap:
                o += '_'
            lastcap = True
        else:
            lastcap = False
        o += lc
    return o


def identify(v, prefix, depth=0, strikeout=False):
    """Identify all output variables, assigning them a given prefix"""

    outputVariables = []

    if depth == 0:
        out = {'name': camel2snake(prefix), 'type': 'String'}
    else:
        out = {'name': camel2snake(prefix), 'type': 'StringArray'}
    if depth > 1:
        warn(f'List depth exceeds 1, Arrays of Arrays detected with {prefix}')
        if strikeout:
            out = {'name': '~' + camel2snake(prefix), 'type': 'StringArray'}
        else:
            return []

    if isinstance(v, (str, int)) or v is None:
        outputVariables.append(out)
    elif isinstance(v, list):
        if v:
            v = v[0]
            outputVariables.extend(identify(v, prefix, depth + 1, strikeout=strikeout))
        else:
            v = ''
            outputVariables.extend(identify(v, prefix, depth + 1, strikeout=strikeout))
    elif isinstance(v, dict):
        keys = list(v.keys())
        keys.sort()
        for key in keys:
            s = v[key]
            outputVariables.extend(identify(s, f'{prefix}.{key}', depth, strikeout=strikeout))

    return outputVariables


def refold(v, prefix, depth=0, collection=None):
    """Refold a dictionary-ish object into a new dictionary, prefixing key
    names with a prefix"""

    if collection is None:
        collection = {}

    prefix = camel2snake(prefix)

    if depth > 1:
        return collection

    # if the key already exists, and isn't a list, promote it to a list
    if prefix in collection:
        data = collection.get(prefix)
        if not isinstance(data, list):
            collection[prefix] = [data]

    if v is None:
        if prefix not in collection:
            collection[prefix] = None
        else:
            collection[prefix].append(None)
    elif isinstance(v, (str, int, float)):
        if isinstance(v, bool):
            v = str(v).lower()
        if depth == 0:
            collection[prefix] = str(v)
        else:
            ls = collection.get(prefix, [])
            ls.append(str(v))
            collection[prefix] = ls
    elif isinstance(v, list):
        for s in v:
            refold(s, prefix, depth + 1, collection)
    elif isinstance(v, dict) or hasattr(v, 'keys'):
        keys = list(v.keys())
        keys.sort()
        if prefix:
            prefix = prefix + '.'
        for key in keys:
            s = v[key]
            refold(s, f'{prefix}{key}', depth, collection)

    return collection


def conform_objects(object_list, _path=None, _mapping=None, add_missing=False, missing_value=None):
    """Conform objects to a common structure.

    Any simple field which is discovered is remembered, then a second pass through
    the objects will add any *missing* fields.

    Returns the conformed object list.
    """

    if _mapping is None:
        mapping = set()
    else:
        mapping = _mapping

    if _path is None:
        path = []
    else:
        path = _path

    path = path.copy()

    if isinstance(object_list, list):
        result = []
        for obj in object_list:
            result.append(
                conform_objects(
                    obj, path, mapping, add_missing=add_missing, missing_value=missing_value
                )
            )

        if _mapping is None:
            result = conform_objects(
                result, path, mapping, add_missing=True, missing_value=missing_value
            )

        return result

    if isinstance(object_list, dict):
        for key, value in object_list.items():
            path.append(key)
            if not isinstance(value, (list, dict)):
                mk = ':'.join(path)
                if mk not in mapping:
                    mapping.add(mk)
            else:
                object_list[key] = conform_objects(
                    value, path, mapping, add_missing=add_missing, missing_value=missing_value
                )

            path.pop()

        if add_missing:
            add_missing_keys(object_list, path, mapping, missing_value)

        if _mapping is None:
            object_list = conform_objects(
                object_list, path, mapping, add_missing=True, missing_value=missing_value
            )

    return object_list


def add_missing_keys(obj: dict, path: list, mapping: set, missing_value=None):
    """Add missing keys to a dictionary-like obj"""

    lp = len(path) + 1

    for key in mapping:
        key_parts = key.split(':')

        if len(key_parts) == lp and key_parts[:-1] == path:
            mk = key_parts[-1]
            value = obj.get(mk, None)
            if value is None:
                value = missing_value
                obj[mk] = value
