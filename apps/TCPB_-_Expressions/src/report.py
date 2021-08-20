# -*- coding: utf-8 -*-
"""Report Class for Scanner Output"""

# standard library
from collections import OrderedDict
from functools import lru_cache
import re
from typing import List

# third-party
from attrdict import AttrDict
from hyphenate import hyphenate_word


optionsRE = re.compile(r'((?:[^/\\]|\\.)+)')

DECODE = {'n': '\n', 'r': '\r', 't': '\t', 'b': '\b', 'f': '\f'}


class Report:
    """Report Class"""

    def __init__(
        self,
        fields: List[OrderedDict],
        title=None,
        headers=True,
        prolog=None,
        epilog=None,
        width=None,
        formatter=None,
    ):
        """Defines the report.  The fields are a list of ordered dictionary of the
        field name, and field specifier.  Each dictionary represents one line of a report.
        If there are multiple dictionaries, each report item spans multiple lines.

        The format of the *value* of each key is
            width[:height][/option[=value]]...[/option[=value]]
        e.g.
            40:2/align=center
        The default height is 0.  Values with a height of 0 may have unlimited height.
        The output for that format will be formatted to fit the space available.
        """

        if isinstance(fields, dict):
            fields = [fields]

        self.fields = fields
        self.formatter = formatter
        self.data = []
        self.title = self.format(title)
        self.headers = headers
        self.lineno = 0
        self.record = {}
        if width:
            self.fixedwidth = width
        else:
            self.fixedwidth = 0
        self.width = width or self.auto_width()
        self.prolog = self.format(prolog)
        self.epilog = self.format(epilog)

        self.all_fields = []
        for row in fields:
            for key in row:
                if key not in self.all_fields:
                    self.all_fields.append(key)

    def __str__(self):
        """__str__"""

        return self.render()

    def add(self, **kwargs):
        """Add a new result row to this report"""

        row = {}

        for key in self.all_fields:
            if key in kwargs:
                row[key] = kwargs.pop(key)
            else:
                row[key] = ''

        # any unconsumed kwargs *could* be checked here
        for key, value in kwargs.items():
            row[key] = value

        self.data.append(row)

    def auto_width(self):
        """Calculate the report width based on the specifiers"""

        maxwidth = 0
        for row in self.fields:
            width = 0
            for specifier in row.values():
                spec = self.parse_specifier(specifier)
                width += spec.width

            width += len(row) - 1
            maxwidth = max(width, maxwidth)

        return maxwidth

    @staticmethod
    def deescape(value):
        """De-Escape any string value"""

        if '\\' not in value:
            return value

        parts = value.split('\\')
        result = parts[0]
        for part in parts[1:]:
            if part:
                escchar = part[0]
                rest = part[1:]
                result += DECODE.get(escchar, escchar) + rest
        return result

    def format(self, value: str, data: dict = None):
        """Format value"""

        if value is None:
            return None

        if data is None:
            data = {}

        if self.formatter and callable(self.formatter):
            value = self.formatter(value, data)
        else:
            value = value.format(**data)

        return value

    @staticmethod
    def format_heading(value):
        """Transform value into a column heading"""

        value = str(value)

        value = value.replace('_', ' ')
        value = value.title()

        return value

    def format_value(self, value, specifier):
        """Formats a value according to any options in the specifier"""

        spec = self.parse_specifier(specifier)

        pad = spec.pad or ' '

        if spec.align == 'center':
            return value.center(spec.width, pad)

        if spec.align == 'right' or spec.numeric:
            return value.rjust(spec.width, pad)

        return value.ljust(spec.width, pad)

    def hyphenate(self, value, width) -> List[str]:
        """Split a word into a hyphenated section under a specific width,
        returns both sections"""

        if '-' not in value:
            parts = hyphenate_word(value)
        else:
            return self.split_at_hyphen(value, width)

        word = ''
        while parts:
            part = parts.pop(0)
            if len(part) + len(word) + 1 <= width:
                word += part
            else:
                parts.insert(0, part)
                break

        remainder = ''.join(parts)
        if word and remainder:
            word += '-'

        if not word:
            word = value[:width]
            remainder = value[width:]

        # print(f'hyphenate({value!r}) = {word!r}, {remainder!r}')
        return word, remainder

    def pad_block(self, value, specifier):
        """Pad this value to the width of the field"""

        if not value:
            value = ''
        value = str(value)
        # ovalue = value

        width = self.parse_specifier(specifier).width

        value += ' ' * width
        value = value[:width]

        # print(f'pad_block({ovalue!r}, {specifier!r}) = {value!r}')
        return value

    @lru_cache(50)
    def parse_specifier(self, specifier):  # pylint: disable=no-self-use
        """Parse a Specifier"""

        result = AttrDict()

        if not isinstance(specifier, str):
            specifier = str(specifier)

        parts = [self.deescape(x) for x in optionsRE.findall(specifier)]
        specifier = parts[0]
        if len(parts) > 1:
            options = parts[1:]
        else:
            options = []

        if ':' not in specifier:
            specifier += ':0'

        width, height = specifier.split(':', 1)

        result.width = int(width)
        result.height = int(height)
        for option in options:
            if '=' in option:
                name, value = option.split('=', 1)
            else:
                name = option
                value = True
            result[name] = value
        return result

    def render(self) -> str:
        """Render this report"""

        if not self.data:
            return ''

        result = []
        if self.title:
            title_row = self.title.center(self.width)
            result.append('')
            result.append('')
            result.append(title_row)
            underscores = ''.join(['-' if c != ' ' else ' ' for c in title_row])
            result.append(underscores)
            result.append('')

        if self.prolog:
            result.append('')
            result.extend(self.render_data(self.prolog, str(self.width)))
            result.append('')

        if self.headers:
            line = ''
            for name, specification in self.fields[0].items():
                spec = self.parse_specifier(specification)
                title = spec.label or self.format_heading(name)
                line += title.ljust(spec.width)[: spec.width] + ' '
            result.append(line)

            line = ''
            for name, specification in self.fields[0].items():
                spec = self.parse_specifier(specification)
                line += ''.ljust(spec.width, '-')[: spec.width] + ' '
            result.append(line)

        self.lineno = 1
        for item in self.data:
            self.record = item
            result.extend(self.render_row(item))
            self.lineno += 1

        if self.epilog:
            result.append('')
            result.extend(self.render_data(self.epilog, str(self.width)))
            result.append('')

        if self.fixedwidth:
            result = [x[: self.fixedwidth] for x in result]

        # print(f'render: {result!r}')
        return '\n'.join(result)

    def render_data(self, value, specifier) -> List[str]:
        """Render a specific value to a block (list) of strings"""

        # N.B. the phantoms in attrdict take care of missing
        # values

        result = []
        spec = self.parse_specifier(specifier)

        if spec.value and isinstance(spec.value, str):
            # TODO -- add other values here for the format
            data = self.record.copy()
            if 'lineno' not in data:
                data['lineno'] = self.lineno
            value = self.format(spec.value, data)
            value = str(value)
            if value and value.startswith('#Error') and 'error' in spec:
                value = spec.error

        value = str(value)

        postnewline = False
        while value:
            if value.replace(' ', '').replace('\n', '') == '' and not spec.notrim:
                break  # stop if its only whitespace remaining

            postnewline = False
            line = None

            if value.startswith('\n'):
                postnewline = True
                value = value[1:]

            if '\n' in value:
                line, value = value.split('\n')
                value = '\n' + value
            else:
                line = value
                value = ''

            if not postnewline and not spec.notrim:
                line = line.lstrip()

            if spec.hang and result and not postnewline:
                line = ' ' * int(spec.hang) + line

            if spec.indent and (not result or postnewline):
                line = ' ' * int(spec.indent) + line

            if len(line) > spec.width:
                line, extra = self.wrap_value(line, specifier)
                value = extra + ('\n' if postnewline else '') + value

            result.append(self.format_value(line, specifier))
            if spec.height and len(result) >= spec.height:
                break
            if postnewline and spec.doublenl:
                result.append('')

        # print(f'render_data({ovalue!r}) = {result!r}')
        return result

    def render_fields(self, item: dict, fields: dict) -> List[str]:
        """Render one line of fields (which may really be multiline)"""

        result = []

        line_blocks = []

        for name, specifier in fields.items():
            value = self.render_data(item.get(name, ''), specifier)
            line_blocks.append((value, specifier))

        row = 0
        while True:
            line = ''
            found = False
            for block, specifier in line_blocks:
                # print(f'block: {block}, {len(block)}')
                if len(block) > row:
                    line += self.pad_block(block[row], specifier) + ' '
                    found = True
                else:
                    line += self.pad_block('', specifier) + ' '
            row += 1

            if found:
                result.append(line[:-1])
            else:
                break

        # print(f'render_fields({item!r}): {result!r}')
        return result

    def render_row(self, item: dict) -> List[str]:
        """Render one row of the report"""

        result = []

        for fields in self.fields:
            result.extend(self.render_fields(item, fields))

        # print(f'render_row: {result!r}')
        return result

    @staticmethod
    def split_at_hyphen(value, width) -> List[str]:
        """Split at the hyphen in the word, if there's one before the width"""

        hp = value.find('-')
        if hp > -1 and hp < width - 1:  # pylint: disable=R1716
            hp += 1
        else:
            hp = width

        word = value[:hp]
        remainder = value[hp:]
        return word, remainder

    def wrap_value(self, value, specifier) -> List[str]:
        """Returns the first portion of value (because its too long),
        and the residual value"""

        spec = self.parse_specifier(specifier)

        splitwidth = max(1, int(int(spec.split or 80) * spec.width / 100))
        # print(f'splitwidth: {splitwidth}, spec: {spec!r}')

        parts = value.split(' ')
        line = ''

        while parts:
            part = parts.pop(0)

            lp = len(part)
            ll = len(line.split('\n')[-1])

            if ll + lp < spec.width:
                line += part + ' '
            elif ll >= splitwidth:
                parts.insert(0, part)
                break
            else:
                # need to break the word or hyphenate
                splitat = spec.width - ll
                if not spec.nohyphenate:
                    part, remainder = self.hyphenate(part, splitat)
                else:
                    remainder = part[splitat:]
                    part = part[:splitat]

                line += part
                if remainder:
                    parts.insert(0, remainder)
                break

        remainder = ' '.join(parts)
        return line, remainder
