# -*- coding: utf-8 -*-
"""Smartdict -- smart dictionary for formatting strings"""

from string import Formatter
from attrdict import AttrDict

__notfound__ = object()


class SmartDict:
    """Smart dictionary object"""

    def __init__(self, namespace: object, valuedict: dict = None, default=__notfound__):
        """init"""
        if namespace is None:
            namespace = {}
        self.namespace = namespace
        if not valuedict:
            valuedict = {}
        self.values = valuedict
        self.default = default

    def __getitem__(self, name, default=__notfound__):
        """get item from values *or* namespace"""

        if default is __notfound__:
            default = self.default

        if name in self.values:
            value = self.values[name]
        else:
            try:
                value = self.namespace.get(name, __notfound__)
            except (AttributeError, TypeError):
                value = __notfound__

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


def smart_format(s: str, *args, _default=__notfound__, _context=None, **kwargs):
    """Format string S according to Python string formatting rules.  Compound
    structure elements may be accessed with dot or bracket notation and without quotes
    around key names, e.g. `blob[0][events][0][source][device][ipAddress]`
    or `blob[0].events[0].source.device.ipAddress`.  If default is set,
    that value will be used for any missing value."""

    kws = SmartDict(_context, kwargs, default=_default)
    fmt = Formatter()

    return fmt.vformat(s, args, kws)
