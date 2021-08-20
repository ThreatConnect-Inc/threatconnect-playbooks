# -*- coding: utf-8 -*-
"""Attribute Dictionary"""

# standard library
from collections import OrderedDict

__notfound__ = object()

# pylint: disable=inconsistent-return-statements


class literal(str):
    """Literal string"""


class AttrDict(OrderedDict):
    """Dictionary which allows attribute access"""

    def __init__(self, *args, **kwargs):
        """Initializer with promotion"""

        super().__init__(*args, **kwargs)
        for key, value in self.items():
            self[key] = self._promote(value)

    def __getattr__(self, attr, deflt=__notfound__):
        """Get attribute -- converts attribute to key"""

        value = self.get(attr, deflt)
        if value is __notfound__:
            return Phantom(attr, self)
        return value

    def __setattr__(self, attr, value):
        """Set attribute -- converts attribute to key"""

        self[attr] = value

    def __setitem__(self, key, value):
        """Set item"""

        super().__setitem__(key, self._promote(value))

    def _promote(self, value):
        """Promote value to AttrDict, if it can be promoted.  Returns
        promoted value."""

        if isinstance(value, (list, tuple)):
            result = [self._promote(x) for x in value]
            if isinstance(value, tuple):
                result = tuple(result)
            return result

        if isinstance(value, dict) and not isinstance(value, AttrDict):
            result = AttrDict(value)
            for key, nvalue in result.items():
                newvalue = self._promote(nvalue)
                if nvalue is not newvalue:
                    result[key] = newvalue
            return result

        return value

    def _dict(self):
        """Return dictionary representation of self"""
        return self._demote(self)

    def _demote(self, value):
        """Reverse a promotion of values"""

        if isinstance(value, literal):
            return str(value)

        if isinstance(value, (list, tuple)):
            result = [self._demote(x) for x in value]
            if isinstance(value, tuple):
                result = tuple(result)
            return result

        if isinstance(value, AttrDict):
            result = dict(value)
            for key, nvalue in list(result.items()):
                newvalue = self._demote(nvalue)
                if nvalue is not newvalue:
                    result[key] = newvalue
                if not result[key]:
                    del result[key]

            return result

        return value


class PhantomObjectError(RuntimeError):
    """Phantom object error"""


class Phantom:
    """Phantom object returned by AttrDict on an attribute access
    to an undefined object"""

    def __init__(self, name, parent):
        """Stand up a new phantom"""
        d = self.__dict__  # can't use self.attrs YET
        d['_name'] = name
        d['_parent'] = parent
        d['_realized'] = False
        # print(f'Created new Phantom {name} of {parent!r}')

    @property
    def _check_realized(self):
        """Check to see if this object has been realized"""

        if self._realized:
            return True

        if self._name in self._parent:
            d = self.__dict__
            d['_realized'] = True
            return True

        return False

    def _proxy(self, method, *args, **kwargs):
        """If self._realized, call whatever the proxy method is
        on the realized object"""

        # print(f'Proxying {method} on {self!r}')
        if self._check_realized:
            ob = self._parent
            if isinstance(ob, dict):
                ob = ob.get(self._name)
            else:
                ob = getattr(ob, self._name)

            # print(f'... resolved {self._name} of parent to {ob!r}')
            meth = getattr(ob, method)
            # print(f'... method is {meth!r}')
            return meth(*args, **kwargs)

        raise PhantomObjectError(method)

    def __setattr__(self, attr, value):
        """If realized, call setattr on the realized object"""

        if self._check_realized:
            return self._proxy('__setattr__', attr, value)

        ob = AttrDict()
        ob[attr] = value
        self._parent[self._name] = ob
        d = self.__dict__
        d['_realized'] = True

    def __setitem__(self, attr, value):
        """If realized, call setattr on the realized object"""

        if self._check_realized:
            return self._proxy('__setitem__', attr, value)

        ob = AttrDict()
        ob[attr] = value
        self._parent[self._name] = ob
        d = self.__dict__
        d['_realized'] = True

    def __getitem__(self, item, default=__notfound__):
        """Proxy getitem"""

        # print(f'Phantom getitem {item}')
        if self._check_realized:
            result = self._proxy('__getitem__', item, default)
        else:
            result = __notfound__

        if result is __notfound__:
            result = Phantom(item, self)

        return result

    def __getattr__(self, item, default=__notfound__):
        """Proxy getattr"""

        # print(f'Phantom getattr {item}')
        if self._check_realized:
            result = self._proxy('__getattr__', item, default)
        else:
            result = __notfound__

        if result is __notfound__:
            result = Phantom(item, self)

        return result

    def __repr__(self):
        """Repr of self"""

        if self._check_realized:
            return f'<Phantom (lingering) {self._name} of {self._parent}>'
        return f'<Phantom {self._name} of {self._parent}>'

    def __str__(self):
        """Str of phantom is either None or ''"""

        return ''  # lets give back a str

    def __iter__(self):
        """Return ourself as an iterator"""

        # print(f'__iter__ on {self!r}')

        if self._check_realized:
            return self._proxy('__iter__')

        return self

    def __next__(self):
        """Phantoms can be iterated over, but they stop immediately"""

        if self._check_realized:
            return self._proxy('__next__')

        raise StopIteration

    def __len__(self):
        """Phantoms have no length"""

        if self._check_realized:
            return self._proxy('__len__')

        return 0
