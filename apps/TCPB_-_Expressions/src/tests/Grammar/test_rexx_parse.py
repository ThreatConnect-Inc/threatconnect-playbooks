# -*- coding: utf-8 -*-
"""Test Rexx Parsing"""

from inspect import isclass

import pytest
from rexxparse import RexxParser

PARSE_TESTS = (
    (
        'astronomers',
        '2 var1 +2 -3 var2 +1 +2 var3 +1 +6 var4',
        {'var1': 'st', 'var2': 'a', 'var3': 'r', 'var4': 's'},
    ),
    ('Old-English', 'left . "-" right .', {'left': 'Old', 'right': 'English'}),
    (
        'REstructured eXtended eXecutor',
        'var1 3 . "X" var2 +1 . "X" var3 +1 .',
        {'var1': 'RE', 'var2': 'X', 'var3': 'X'},
    ),
)


class Test_RexxParse:
    """Test Rexx Parse"""

    def setup_class(self):
        """setup"""

    @pytest.mark.parametrize('source,template,result', PARSE_TESTS)
    def test_parse(self, source, template, result):
        """Test Parse"""

        rp = RexxParser(pattern=template, context=self)

        if isclass(result) and issubclass(result, Exception):
            with pytest.raises(result):
                value = rp.parse(source)
        elif isinstance(result, Exception):
            with pytest.raises(result.__class__):
                value = rp.parse(source)
                result = result.args[0]
                assert value == result, f'{template} == {result}'
        else:
            value = rp.parse(source)
            assert value == result, f'{template} == {result}'
