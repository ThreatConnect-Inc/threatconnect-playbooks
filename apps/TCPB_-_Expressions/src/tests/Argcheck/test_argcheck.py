# -*- coding: utf-8 -*-
"""Test Argcheck"""

from argcheck import argcheck, tc_argcheck
import pytest


class tcex_dummy:
    """tcex_dummy"""

    def __init__(self):
        """__init__"""
        self.exitrc = None
        self.exitmsg = None
        self.playbook = self

    def exit(self, exitcode, exitmessage):
        """exit"""
        self.exitrc = exitcode
        self.exitmsg = exitmessage


class TestArgcheck:
    """Test Argcheck Code"""

    foo = 'bla'  # pylint: disable=blacklisted-name
    one = 1
    twelve = '12'
    camel_case = 'Camel Case'
    blank = ''
    null = None
    d = {'foo': 'bla'}

    def test_required(self):
        """test_required"""

        assert argcheck(self, 'foo', required=True) == 'bla'

    def test_required_missing(self):
        """test_required_missing"""
        with pytest.raises(AttributeError):
            assert argcheck(self, 'bla', required=True) == 'bla'

        with pytest.raises(AttributeError):
            assert argcheck(self, 'blank', required=True) == 'bla'

        with pytest.raises(AttributeError):
            assert argcheck(self, 'null', required=True) is None

    def test_notrequired_missing(self):
        """test_notrequired_missing"""
        assert argcheck(self, 'bla') is None
        assert argcheck(self.d, 'bla') is None

    def test_required_dict(self):
        """test_required_dict"""

        assert argcheck(self.d, 'foo', required=True) == 'bla'

    def test_required_missing_dict(self):
        """test_required_missing_dict"""
        with pytest.raises(KeyError):
            assert argcheck(self.d, 'bla', required=True) == 'bla'

    def test_label_conversion(self):
        """test_label_conversion"""
        try:
            argcheck(self, 'camel_case', types=int)
        except ValueError as e:
            assert e.args[0] == self.camel_case

    def test_default(self):
        """test_default"""

        assert argcheck(self, 'bla', default='default') == 'default'
        assert argcheck(self.d, 'bla', default='default') == 'default'
        assert argcheck(self, 'blank', default='default') == 'default'
        assert argcheck(self, 'blank') is None
        assert argcheck(self, 'blank', allow_empty=True) == ''
        assert argcheck(self, 'null', allow_empty=True) is None

    def test_typecheck(self):
        """test_typecheck"""

        assert argcheck(self, 'foo', types=str) == 'bla'
        assert argcheck(self, 'foo', types=(str,)) == 'bla'
        assert argcheck(self, 'twelve', types=int) == 12
        assert argcheck(self, 'twelve', types=float) == 12.0

        with pytest.raises(ValueError):
            assert argcheck(self, 'foo', types=int) == 12

        with pytest.raises(ValueError):
            assert argcheck(self, 'foo', types=(int, float)) == 12

    def test_range_callable(self):
        """test_range_callable"""
        # pylint: disable=chained-comparison

        assert argcheck(self, 'twelve', types=int, range=lambda x: (x > 1) and (x < 100))

        with pytest.raises(ValueError):
            assert argcheck(self, 'twelve', types=int, range=lambda x: (x > 1) and (x < 10))

    def test_range_single(self):
        """test_range_single"""

        assert argcheck(self, 'twelve', types=int, range=1)

        with pytest.raises(ValueError):
            assert argcheck(self, 'twelve', types=int, range=100)

    def test_range_double(self):
        """test_range_double"""

        assert argcheck(self, 'twelve', types=int, range=(1, 100))

        with pytest.raises(ValueError):
            assert argcheck(self, 'twelve', types=int, range=(1, 10))

        with pytest.raises(ValueError):
            assert argcheck(self, 'twelve', types=int, range=(100, 1000))

    def test_tc_argcheck(self):
        """test_tc_argcheck"""
        tcex = tcex_dummy()

        assert tc_argcheck(self, 'b', required=False) is None
        assert tc_argcheck(self, 'foo', required=True, tcex=tcex) == 'bla'
        tc_argcheck(self, 'b', required=True, tcex=tcex)

        assert tcex.exitrc == 1
        assert tcex.exitmsg == 'Invalid value for B. Value is required.'
