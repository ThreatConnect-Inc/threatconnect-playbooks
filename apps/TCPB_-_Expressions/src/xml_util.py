# -*- coding: utf-8 -*-
"""XML Parsing Utilities"""


# standard library
from collections import OrderedDict
from io import StringIO
from xml.sax.saxutils import escape, quoteattr  # nosec

# third-party
from defusedxml import ElementTree


class Tag(str):
    """Tag class to distinguish text from tags"""


def name_val_transform(obj: dict):
    """Transform a dictionary in the form {"name": name, "value": value} into {name: value}"""

    if not isinstance(obj, (dict, OrderedDict)):
        return obj

    namekey = None
    valuekey = None

    keys = list(obj.keys())

    for key in keys:
        if 'name' in key.lower():
            namekey = key
            break

    if not namekey:
        return obj

    for key in keys:
        if key != namekey:
            valuekey = key
            break

    return OrderedDict({obj[namekey]: obj[valuekey]})


def compact_dict(obj, name=None):
    """Compacts a list or dictionary, if possible"""

    # look at the children; if they are each a dictionary with one element,

    children = obj
    if isinstance(children, list):
        conforming = True
        extended = False
        child_dict = OrderedDict()
        for child in children:
            if not isinstance(child, (dict, OrderedDict)):
                conforming = False
                break
            if len(child) == 2:
                child = name_val_transform(child)
            if len(child) != 1:
                conforming = False
                break
            key = list(child.keys())[0]
            value = compact_dict(child[key])
            if key not in child_dict:
                child_dict[key] = value
            else:
                v = child_dict.get(key)
                if not isinstance(v, list):
                    v = [v]
                v.append(value)
                extended = True
                child_dict[key] = v

        if conforming and child_dict != children:
            # print(f'Compacting\n{pformat(children)}\nto\n{pformat(child_dict)}\n')
            if extended:
                child_dict = compact_dict([child_dict], name=name)
            children = child_dict

        if isinstance(children, OrderedDict) and len(children) == 2:
            children = name_val_transform(children)

    return children


def convert_value(value):
    """Convert a value"""

    if isinstance(value, bool):
        return value

    try:
        ov = value
        value = float(value)
        if int(value) == value and '.' not in ov:
            value = int(value)
    except (TypeError, ValueError):
        pass

    return value


def walk_xml(
    element,
    namespace=False,
    strip=False,
    convert=False,
    compact=False,
    transform=None,
):
    """Walk down an XML element"""

    result = {}

    tag = element.tag
    if not namespace and tag.startswith('{'):
        tag = tag.split('}', 1)[1]

    value = element.text
    if strip:
        if isinstance(value, str):
            value = value.strip()

    if transform and callable(transform):
        value = transform(value)

    if convert:
        value = convert_value(value)

    children = []
    for sub in element:
        children.append(
            walk_xml(
                sub,
                namespace=namespace,
                strip=strip,
                convert=convert,
                compact=compact,
                transform=transform,
            )
        )

    if compact and children:
        children = compact_dict(children, name=tag)

    result = OrderedDict({tag: children or value})
    if element.attrib:
        for key, value in element.attrib.items():
            if convert:
                value = convert_value(value)
            result[f'@{key}'] = value

    return result


def xml_to_dict(
    xmldata,
    namespace=False,
    strip=True,
    convert=True,
    compact=True,
    transform=None,
):
    """Convert the XML data to a dictionary structure"""

    wrap = False

    while True:
        try:
            etree = ElementTree.parse(StringIO(xmldata))
            break
        except Exception as e:
            if 'junk after document element' in str(e) and not wrap:
                xmldata = '<X_PARSE_ROOT>\n' + xmldata + '\n</X_PARSE_ROOT>'
                wrap = True
            else:
                raise

    result = walk_xml(
        etree.getroot(),
        namespace=namespace,
        strip=strip,
        convert=convert,
        compact=compact,
        transform=transform,
    )

    if wrap:
        result = result['X_PARSE_ROOT']

    return result


def tag_for(name, attributes=None, close=False, prefix='', namespace=None):
    """Returns an opening or closing tag with attributes"""

    if namespace is None:
        namespace = {}

    if attributes is None:
        attributes = {}

    if '}' in name:
        nsprefix, tag = name.split('}', 1)
        nsprefix = nsprefix[1:]
        ns = None
        for key, value in namespace.items():
            if value == nsprefix:
                ns = key
                break
        if ns:
            name = f'{ns}:{tag}'
        else:
            i = 1
            while True:
                ns = f'ns{i}'
                if ns not in namespace:
                    namespace[ns] = prefix
                    break
                i += 1
            name = f'{ns}:{tag}'

    attr = []
    if not close:
        for key, value in attributes.items():
            value = quoteattr(value)
            attr.append(f'{key}={value}')
        attrs = ' '.join(attr)
    else:
        attrs = ''

    if close:
        closetag = '/'
    else:
        closetag = ''

    parts = [name]
    if attrs:
        parts.append(attrs)

    return Tag(f'{prefix}<{closetag}{" ".join(parts)}>')


def dict_to_xml(ob: dict, namespace=False, indent=0, _depth=0):
    """Convert a dictionary back to XML"""

    if indent:
        prefix = ' ' * indent * _depth
    else:
        prefix = ''

    parts = []
    attrs = {}

    if isinstance(ob, (list, tuple)):
        for value in ob:
            result = dict_to_xml(value, namespace=namespace, indent=indent, _depth=_depth + 1)
            if isinstance(result, list):
                parts.extend(result)
            else:
                parts.append(result)

    elif isinstance(ob, (dict, OrderedDict)):
        # Pass 1, collect attributes
        attrs = {}
        for name, value in ob.items():
            if name.startswith('@'):
                attrs[name[1:]] = value

        # Pass 2, resolve voaluesresolve voaluesresolve voalues
        for name, value in ob.items():
            if name.startswith('@'):
                continue

            value = dict_to_xml(value, namespace=namespace, indent=indent, _depth=_depth + 1)

            if isinstance(value, list) and len(value) == 1:
                value = value[0]
            if isinstance(value, str):
                opentag = tag_for(name, attributes=attrs)
                closetag = tag_for(name, close=True)
                parts.append(f'{prefix}{opentag}{value.lstrip()}{closetag}')
            else:
                opentag = tag_for(name, prefix=prefix, attributes=attrs)
                closetag = tag_for(name, prefix=prefix, close=True)
                parts.append(opentag)
                parts.extend(value)
                parts.append(closetag)
    else:
        parts.append(escape(str(ob)))

    if _depth > 0:
        # print(f'toXML: {parts}')
        return parts

    if indent:
        return '\n'.join(parts)
    return ''.join(parts)
