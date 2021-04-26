# -*- coding: utf-8 -*-
"""REXX Style Parsing

Derived from https://www.ibm.com/docs/en/zos/2.3.0?topic=parsing-details-steps-in

"""

from collections import deque
import re

tokenize_re = re.compile(
    r"""
    \s*
    (
          \.        # dot
        | ,         # source change
        | \+        # Relative length prefix
        | -         # Relative length prefix
        | =         # absolute length prefix
        | \(        # Indirect target start
        | \)        # Indirect target end
        | \d+       # Column Position
        | \w+       # Pattern
        | '(?:[^'\\]|\\.)*'   # String
        | "(?:[^"\\]|\\.)*"   # String
    )
    \s*
""",
    re.VERBOSE,
)


class literal(str):
    """Literal Strings"""

    def __repr__(self):
        """__repr__"""

        return f'<literal {str(self)!r}>'


class variable(str):
    """Variable names"""

    def __repr__(self):
        """__repr__"""

        return f'<variable "{self}">'


class reference(str):
    """Reference to Variable"""

    def __repr__(self):
        """__repr__"""

        return f'<reference "{self}">'


class RexxParser:
    """Rexx Parser Object"""

    def __init__(self, pattern=None, context=None):
        """Initializer"""

        self.source = None
        self.pattern = None

        if pattern:
            self.pattern = self.tokenize(pattern)

        self.start = None
        self.end = None
        self.length = None
        self.match_start = None
        self.match_end = None
        self.match_position = None
        self.context = context
        self.variables = None

    def tokenize(self, pattern):
        """Return a list of pattern tokens"""

        intermediate = deque()

        while pattern:
            match = tokenize_re.match(pattern)
            if match:
                token = match.groups()[0]
                intermediate.append(self.encode_token(token))
                pattern = pattern[match.end() :]

        result = []
        # Now go through and collapse any '(' variable ')' to reference

        state = None
        while intermediate:
            token = intermediate.popleft()
            if state is None:
                if token == '(':
                    state = 'paren'
                    continue
                result.append(token)

            if state == 'paren':
                if not isinstance(token, variable):
                    raise ValueError(
                        f'Expecting variable name for indirect reference instead of {token}'
                    )
                token = reference(token)
                if not intermediate or intermediate[0] != ')':
                    raise ValueError('Expecting ) after indirect reference')
                intermediate.popleft()
                state = None
                result.append(token)

        return result

    @staticmethod
    def encode_token(string):
        """Encode a token into a class instance"""

        if string and string.startswith("'"):
            if not string.endswith("'"):
                raise ValueError(f'No matching end quote on string {string}')
            return literal(string[1:-1])

        if string and string.startswith('"'):
            if not string.endswith('"'):
                raise ValueError(f'No matching end quote on string {string}')
            return literal(string[1:-1])

        if string in ('-', '+', '(', ')', '.', ',', '='):
            return string

        try:
            i = int(string)
            return i
        except (TypeError, ValueError):
            pass

        return variable(string)

    def parse(self, source, pattern=None, context=None):
        """Parse a source string with a pattern"""

        if pattern:
            self.pattern = self.tokenize(pattern)

        self.source = source
        self.start = 1
        self.end = len(source) + 1
        self.length = len(source)
        self.match_start = 1
        self.match_end = 1
        self.match_position = 0
        if context is not None:
            self.context = context

        self.variables = {}

        tokens = deque(self.pattern)
        while tokens:
            pattern = self.next_pattern(tokens)
            self.word_parse(pattern)

        return self.variables

    def next_pattern(self, tokens):
        """Get the next pattern"""

        # pylint: disable=too-many-return-statements

        pattern = deque()

        if not tokens:
            self.start = self.match_end
            self.match_start = self.length + 1
            self.match_end = self.length + 1
            return pattern

        while tokens:
            token = tokens.popleft()
            if token == '.' or isinstance(token, variable):
                pattern.append(token)
                continue

            if token == '+' and not isinstance(token, literal):
                token = tokens.popleft()
                if not isinstance(token, (int, reference)):
                    raise ValueError(
                        '+ in pattern must be followed by an integer or indirect variable reference'
                    )
                if isinstance(token, reference):
                    token = self.dereference(token, types=int)

                # print(f'?+ start={self.start}, match_start={self.match_start}, '
                # f'match_end={self.match_end}, '
                # f'match={self.source[self.match_start-1:self.match_end-1]}')
                self.start = self.match_end
                self.match_start = min(self.length + 1, self.match_end + token)
                self.match_end = self.match_start
                # print(f'+ start={self.start}, match_start={self.match_start}, '
                # f'match_end={self.match_end}')
                return pattern
            if token == '-' and not isinstance(token, literal):
                token = tokens.popleft()
                if not isinstance(token, (int, reference)):
                    raise ValueError(
                        '- in pattern must be followed by an integer or indirect variable reference'
                    )
                if isinstance(token, reference):
                    token = self.dereference(token, types=int)

                self.start = self.match_start
                self.match_start = max(1, self.match_start - token)
                self.match_end = self.match_start
                return pattern
            if token == '=' and not isinstance(token, literal):
                token = tokens.popleft()
                if not isinstance(token, (int, reference)):
                    raise ValueError(
                        '= in pattern must be followed by an integer or indirect variable reference'
                    )
                if isinstance(token, reference):
                    token = self.dereference(token, types=int)

                self.start = self.match_end
                self.match_start = min(self.length + 1, token)
                self.match_end = self.match_start
                return pattern
            if isinstance(token, int):
                self.start = self.match_end
                self.match_start = min(self.length + 1, token)
                self.match_end = self.match_start
                return pattern
            if isinstance(token, (literal, reference)):
                if isinstance(token, reference):
                    token = self.dereference(token, types=str)

                if self.start < self.match_end:
                    self.start = self.match_end

                idx = self.source.find(str(token), self.start - 1) + 1

                # print(f'# find {token} at {idx}, start={self.start}')

                if idx > 0:
                    # self.start = self.match_start
                    self.start = self.match_end
                    self.match_start = idx
                    self.match_end = idx + len(token)
                    return pattern
                self.start = self.match_end
                self.match_start = self.length + 1
                self.match_end = self.length + 1
                return pattern
            if token == ',':
                self.match_start = self.length + 1
                self.match_end = self.length + 1
                return pattern

            raise RuntimeError(f'Unexpected token {token}')

        self.start = self.match_end
        self.match_start = self.length + 1
        self.match_end = self.length + 1

        return pattern

    def word_parse(self, tokens):
        """Parse pattern word"""

        if self.match_end <= self.start:
            self.end = self.length + 1
        else:
            self.end = self.match_start

        substring = self.source[self.start - 1 : self.end - 1]
        # print(f'{tokens} of {substring}')
        while tokens:
            token = tokens.popleft()
            if not (token == '.' or isinstance(token, variable)):
                return

            if not tokens:
                self.assign(token, substring)
                continue

            if not (tokens[0] == '.' or isinstance(tokens[0], variable)):
                self.assign(token, substring)
                continue

            if not substring:
                self.assign(token, None)
                continue

            substring = substring.lstrip()

            if not substring:
                self.assign(token, None)
                continue

            if ' ' not in substring:
                self.assign(token, substring)
                continue

            idx = substring.find(' ')
            word = substring[:idx]
            substring = substring[idx + 1 :]
            self.assign(token, word)

    def dereference(self, name, types=None):
        """Look up name in the context, assert it is one of types if possible"""

        name = str(name)
        result = None
        if self.context is None:
            raise TypeError(f'Context required to resolve variable reference {name}')

        if isinstance(self.context, dict):
            if name not in self.context:
                raise KeyError(name)
            result = self.context[name]
        else:
            if not hasattr(self.context, name):
                raise AttributeError(name)

            result = getattr(self.context, name)

        if types:
            if not isinstance(types, list):
                types = [
                    types,
                ]

            if isinstance(result, tuple(types)):
                return result

            for t in types:
                try:
                    result = t(result)
                    return result
                except Exception:
                    pass

            raise TypeError(f'{name} must be one of {types}')

        return result

    def assign(self, name, value):
        """Assign name = value"""

        name = str(name)
        if name == '.':
            return
        self.variables[name] = value
