# -*- coding: utf-8 -*-
"""Reporting class to handle various reporting types"""

from collections import OrderedDict
import math
import re

from operator import itemgetter
from report import Report
from smartdict import smart_format


formatRE = re.compile(r'([^{]*) (?: { ((?:[^}\\] | \\.)*) } (.*))?', re.VERBOSE)


class Reporting:
    """Reporting class to handle various reporting types"""

    def __init__(self, context):
        """__init__"""

        self.context = context
        self.data = None

    def count_depth(self, thing, depth=0):
        """Count how deep the thing is"""

        if isinstance(thing, (list, tuple)):
            if (
                isinstance(thing, tuple)
                and len(thing) == 2
                and not isinstance(thing[0], (tuple, list, dict))
                and thing[1] not in self.headings
            ):
                return depth  # this is a (heading, specifier) tuple
            return min([self.count_depth(x, depth + 1) for x in thing])
        if isinstance(thing, dict):
            return 3
        return depth

    # pylint: disable=redefined-builtin

    def create_report(
        self,
        data: list,
        columns: list = None,
        title=None,
        header=True,
        width=None,
        prolog=None,
        epilog=None,
        sort=None,
        filter=None,
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
        widths will be automatically calculated.  If the width parameter is not specified,
        a default width of 80 will be used to size the report.

        Options:    align=left|right|center
                    value=format    - format for values e.g. {lineno}.
                                      to add a . after lineno
                    notrim          - Don't trim leading/trailing space
                    hang=n          - Hanging paragraph by N spaces
                    indent=n        - Indent paragraph by N spaces
                    split=n         - split at n% through the column (default 80)
                                      if necessary
                    label=string    - heading label
                    doublenl        - Double newlines (ie, add line after paragraph)
                    nohyphenate     - Don't hyphenate value

        If sort is specified, it is a column or list of columns to sort by, with the column
        name optionally prefixed with a '-' to do a descending sort.

        If filter is specified, it is an expression that must be true for that record to appear
        in the result, e.g. filter="salary>70000".
        """

        data = self.data_to_dict(data)
        if not data:
            raise ValueError('No data provided.')

        original_columns = list(data[0].keys())

        data = self.sort_and_filter(data, sort=sort, filter=filter)

        nodata = False
        if not data:
            # All data is filtered, so add a null row
            d = OrderedDict()
            for name in original_columns:
                d[name] = ''
            data = [d]
            nodata = True

        self.data = data

        if not columns:
            columns = self.report_autowidth(data, line_width=width or 0)
        else:
            auto_columns = self.report_autowidth(data, line_width=width or 0, headers=columns)
            columns = self.normalize_columns(columns, auto_columns)

        rpt = Report(
            columns,
            title=title,
            headers=header,
            width=width,
            prolog=prolog,
            epilog=epilog,
            formatter=self.formatter,
        )

        if not nodata:
            for row in data:
                rpt.add(**row)

        return str(rpt)

    @staticmethod
    def data_to_dict(data):
        """Turn data into a list of dictionaries, one per row"""

        if not isinstance(data, (list, tuple)):
            data = [data]  # wrap dictionaries as a list if they weren't wrapped

        if not isinstance(data[0], (list, tuple, dict)):
            raise TypeError('data must be a list of lists or list of dictionaries')

        if isinstance(data[0], dict):
            return data  #  N.B. This doesn't force all rows to be dicts, but presumes it

        # Now the rows are rows of columns

        result = []

        headers = data[0]
        data = data[1:]

        for row in data:
            rowdict = OrderedDict()
            for colno, name in enumerate(headers):
                # N.B. rows wider than row 0 are silently trimmed here
                if colno >= len(row):
                    value = ''
                else:
                    value = row[colno]
                if name in rowdict:
                    raise ValueError('Duplicate column name {name!r}')
                rowdict[name] = value
            result.append(rowdict)

        return result

    def formatter(self, value: str, data: dict):
        """Called by the reporting engine to format a value"""

        result = ''
        if self.context and hasattr(self.context, 'eval'):
            while value:
                prefix, expr, suffix = formatRE.match(value).groups()

                result += prefix

                if expr is None:
                    break

                representation = None
                format = None

                if ':' in expr:
                    colon = expr.rindex(':')
                    format = expr[colon:]
                    expr = expr[:colon]

                if '!' in expr:
                    bang = expr.rindex('!')
                    representation = expr[bang:]
                    expr = expr[:bang]

                try:
                    expr = self.context.eval(expr, data)
                except Exception as e:
                    result = f'#Error {e!r}'
                    break

                fmt = '{0'
                if representation:
                    fmt += representation
                if format:
                    fmt += format
                fmt += '}'

                try:
                    result += fmt.format(expr)
                except Exception as e:
                    result = f'#Error: {e}'

                value = suffix

        if result is None:
            result = smart_format(value, **data, default='', _context=self.context)
        return result

    @property
    def headings(self):
        """Return the keys of row 0 of the data"""

        if self.data:
            return list(self.data[0].keys())

        return []

    def normalize_columns(self, columns, auto_columns):
        """Turn a list of columns into a list of column dictionaries"""

        if not isinstance(columns, (list, tuple)):
            columns = [columns]

        if isinstance(columns[0][0], dict):
            return columns

        depth = self.count_depth(columns)

        while depth < 2:
            columns = [columns]
            depth += 1

        # At this point, columns is nominally [['name', 'name', ('name', 'specifier'), ...]]

        result = []
        for row in columns:
            rowdict = {}

            for name in row:
                if isinstance(name, tuple):
                    if len(name) != 2:
                        raise ValueError(
                            'Expecting column description tuple to be (name, specifier)'
                        )
                    specifier = name[1]
                    name = name[0]
                else:
                    specifier = None

                if specifier is None:
                    if name not in self.headings:
                        raise ValueError(f'Column name {name!r} not in first data row')

                    specifier = auto_columns[0][name]

                if name in rowdict:
                    raise ValueError(f'Duplicate column name {name} in row')

                rowdict[name] = specifier
            result.append(rowdict)
        return result

    @staticmethod
    def report_autowidth(data, line_width, headers=None):
        """Generate the width of the report columns by looking at the data"""

        column_length = {}
        max_width = {}
        average_width = {}
        rows = {}

        for row in data:
            if isinstance(row, dict):
                for name in row:
                    name = str(name)
                    max_width[name] = max(max_width.get(name, 0), len(name))

                for name, value in row.items():
                    value = str(value)
                    name = str(name)
                    for v in value.split('\n'):
                        column_length[name] = column_length.get(name, 0) + len(v)
                        rows[name] = rows.get(name, 0) + 1
                        max_width[name] = max(max_width.get(name, 0), len(v))
            else:
                columnno = 0
                for value in row:
                    name = data[0][columnno]
                    name = str(name)
                    columnno += 1

                    value = str(value)

                    for v in value.split('\n'):
                        column_length[name] = column_length.get(name, 0) + len(v)
                        rows[name] = rows.get(name, 0) + 1
                        max_width[name] = max(max_width.get(name, 0), len(v))

        column_names = list(max_width.keys())
        if headers:
            colno = 0
            for name in headers:
                while isinstance(name, (list, tuple)):
                    name = name[0]
                if name in max_width:
                    column_name = name
                else:
                    column_name = column_names[colno]
                colno += 1
                max_width[column_name] = max(max_width.get(column_name, 0), len(name))

        # let's see if we can fit all the desired widths

        desired_width = 0
        avg_desired = 0

        scale = 1.0

        for column, width in max_width.items():
            desired_width += width
            avg = math.ceil(column_length[column] / rows[column])
            average_width[column] = avg
            avg_desired += avg

        desired_width += len(max_width) - 1
        avg_desired += len(max_width) - 1

        columns = {}

        if not line_width:
            line_width = desired_width

        # If the average desired is too wide, we scale down
        # the outputs evenly.  This isn't great, since narrow
        # columns should not be shrunk much
        if avg_desired > line_width:
            scale = line_width / avg_desired

        residual = line_width - avg_desired

        for column, awidth in average_width.items():
            w = max(int(awidth * scale), 1)
            columns[column] = w

        while residual > 0:
            closest_column = None
            closest_ratio = 0
            for column, maxw in max_width.items():
                ratio = columns[column] / maxw
                if ratio < 1.0 and ratio > closest_ratio:
                    closest_ratio = ratio
                    closest_column = column
            if not closest_column:
                break
            columns[closest_column] += 1
            residual -= 1

        return [columns]

    def sort_and_filter(self, data, sort=None, filter=None):
        """Filter and sort the data dictionaries"""

        if filter and hasattr(self.context, 'eval'):
            result = []
            for record in data:
                try:
                    if self.context.eval(filter, record):
                        result.append(record)
                except Exception:
                    # Bad filters don't halt report generation, they just exclude records
                    pass
            data = result

        if sort:
            if not isinstance(sort, (list, tuple)):
                sort = [sort]
            sort = list(sort)
            sort.reverse()  # process sort in reverse column order

            for sortcolumn in sort:
                reverse = False
                if sortcolumn.startswith('-'):
                    sortcolumn = sortcolumn[1:]
                    reverse = True
                data.sort(key=itemgetter(sortcolumn), reverse=reverse)

        return data
