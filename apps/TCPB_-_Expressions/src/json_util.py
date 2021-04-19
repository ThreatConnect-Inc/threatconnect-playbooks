#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Read a JSON document and kick out the equivalent output section of install.json """

import json
import sys
from warnings import warn


def camel2snake(s):
    """ Convert a MS Graph camelCase name to snake_case """
    o = ''
    if s.upper() == s:
        s = s.lower()
    for letter in s:
        lc = letter.lower()
        if lc != letter:
            o += '_'
        o += lc
    if o.startswith('_'):
        o = o[1:]
    return o


def identify(v, prefix, depth=0):
    """ Identify all output variables, assigning them a given prefix """

    outputVariables = []

    if depth == 0:
        out = {'name': camel2snake(prefix), 'type': 'String'}
    else:
        out = {'name': camel2snake(prefix), 'type': 'StringArray'}
    if depth > 1:
        warn('List depth exceeds 1, Arrays of Arrays detected with {}'.format(prefix))
        return []

    if isinstance(v, (str, int, float)):
        outputVariables.append(out)
    elif isinstance(v, list):
        v = v[0]
        outputVariables.extend(identify(v, prefix, depth + 1))
    elif isinstance(v, dict):
        keys = list(v.keys())
        keys.sort()
        for key in keys:
            s = v[key]
            outputVariables.extend(identify(s, '{}.{}'.format(prefix, key), depth))

    return outputVariables


def refold(v, prefix, depth=0, collection=None):
    """ Refold a dictionary-ish object into a new dictionary, prefixing key
        names with a prefix """

    if collection is None:
        collection = {}

    prefix = camel2snake(prefix)

    if depth > 1:
        return collection

    if v is None:
        collection[prefix] = None
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
        collection[prefix] = []
        for s in v:
            refold(s, prefix, depth + 1, collection)
    elif isinstance(v, dict) or hasattr(v, 'keys'):
        keys = list(v.keys())
        keys.sort()
        for key in keys:
            s = v[key]
            if prefix:
                newprefix = f'{prefix}.{key}'
            else:
                newprefix = key
            refold(s, newprefix, depth, collection)

    return collection


if __name__ == '__main__':

    def cmdline():
        """ Put all the variables into a local function so pylint
            doesn't complain """
        args = sys.argv[1:]
        filename = args[0]
        prefix = args[1]

        f = open(filename, 'r')
        data = json.load(f)

        keys = list(data.keys())
        keys.sort()

        outputVariables = []

        collection = {}
        # for key in keys:
        #    v = data[key]
        #    outputVariables.extend(identify(v, '{}.{}'.format(prefix, key)))
        #    refold(v, '{}.{}'.format(prefix, key), 0, collection)

        outputVariables = identify(data, prefix)
        collection = refold(data, prefix)

        print(json.dumps(outputVariables, indent=3, ensure_ascii=False))

        print(json.dumps(collection, sort_keys=True, indent=3, ensure_ascii=False))

    cmdline()
