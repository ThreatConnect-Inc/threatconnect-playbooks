#!/usr/bin/env python
"""Argument Checking Utility"""

notfound = object()


def argcheck(
    base,
    name,
    *,
    default=notfound,
    types=None,
    range=None,  # pylint: disable=redefined-builtin
    required=False,
    label=None,
    allow_empty=False,
    encoding=None,
    strip=True,
):
    """Gets an argument named 'name' from the base object, which
    may support either getattr or getitem.  Validates the type and
    ranges of the result object, if types or range is specified.

    Types is a list of class constructors, to be tried in order with the
    value.  Range can either be a callable, a single value, or a
    (low, high) tuple.

    If encoding is specified, the value must be *able* to be encoded
    using that encoding.  The value is not re-encoded.

    If strip is True (the default), the value is stripped of leading
    and trailing whitespace.
    """

    if label is None:
        label = name.replace('_', ' ').title()

    if isinstance(base, dict):
        value = base.get(name, default)
        if value is notfound:
            if not required:
                return None
            raise KeyError(label, 'Value is required')
    else:
        value = getattr(base, name, default)
        if value is notfound:
            if not required:
                return None
            raise AttributeError(label, 'Value is required')

    if isinstance(value, str) and strip:
        value = value.strip()

    if value in (None, ''):
        if allow_empty:
            return value

        if required and not allow_empty:
            if isinstance(base, dict):
                raise KeyError(label, 'Value is required')  # pragma: no cover
            raise AttributeError(label, 'Value is required')

        if default is not notfound:
            return default

        return None

    ovalue = value

    if types:
        if not isinstance(types, (list, tuple)):
            types = (types,)

        # First a special case when the value is bytes and we want str
        if isinstance(value, bytes) and bytes not in types and str in types:
            try:
                value = value.decode('utf-8')
            except UnicodeDecodeError:
                pass

        # Second special case, if its a bool, and str is not allowed,
        # treat "true" and "false" specially
        if isinstance(value, str) and str not in types and bool in types:
            if value.lower() == 'true':
                value = True
            elif value.lower() == 'false':
                value = False

        # first pass, if not a direct instance, try the class constructors
        if not isinstance(value, types):
            for t in types:
                try:
                    value = t(value)
                    break
                except Exception:  # nosec
                    pass

        if not isinstance(value, types):
            allowed = ', '.join(x.__name__ for x in types)
            if len(types) > 1:
                raise ValueError(
                    label, f'{ovalue} is not an acceptable type, must be one of {allowed}'
                )
            raise ValueError(label, f'{ovalue} is not an acceptable type, must be {allowed}')

    if range is not None:
        if callable(range):
            if not range(value):
                raise ValueError(label, f'{ovalue} is did not validate successfully')
        elif not isinstance(range, tuple):
            if value < range:
                raise ValueError(label, f'{ovalue} is below minimum value {range}')
        else:
            low, high = range
            if value < low:
                raise ValueError(label, f'{ovalue} is below minimum value {low}')
            if value > high:
                raise ValueError(label, f'{ovalue} is above maximum value {high}')

    if encoding is not None and isinstance(value, str):
        try:
            _ = value.encode(encoding)
        except UnicodeError as e:
            raise ValueError(
                label, f'{ovalue} cannot be encoded with the {encoding} encoding'
            ) from e

    return value


def tc_argcheck(base, name, **kwargs):
    """Playbook friendly version of argcheck"""
    tcex = kwargs.pop('tcex', None)
    if not tcex:
        return argcheck(base, name, **kwargs)
    try:
        value = argcheck(base, name, **kwargs)
    except (KeyError, AttributeError, ValueError) as e:
        name, message = e.args  # pylint: disable=unbalanced-tuple-unpacking
        tcex.playbook.exit(1, f'Invalid value for {name}. {message}.')
        return None

    return value
