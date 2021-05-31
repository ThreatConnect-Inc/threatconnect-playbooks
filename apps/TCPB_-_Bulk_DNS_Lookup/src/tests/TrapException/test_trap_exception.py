#!/usr/bin/env python
"""Trap tests"""

# third-party
import pytest

# first-party
from trap_exception import trap

# pylint: disable=attribute-defined-outside-init

SAVE = []


def custom_handle_exception(exception):
    """Custom exception handler"""
    SAVE.append(exception)


class TestTrapException:
    """Test Trap Exception"""

    def setup_method(self):
        """setup"""
        self.exception = None
        self.error = None
        while SAVE:
            SAVE.pop()

    def handle_exception(self, exception):
        """handle_exception"""
        self.exception = exception

    @trap
    def value_exception(self):
        """raise a Value Error"""
        self.error = ValueError('foo')
        raise self.error

    @trap(classes=KeyError)
    def not_a_key_error(self):
        """raise a Value Error"""
        self.error = ValueError('foo')
        raise self.error

    @trap(classes=KeyError)
    def key_error(self):
        """raise a Value Error"""
        self.error = KeyError('foo')
        raise self.error

    @trap(custom_handle_exception)
    def method_handler(self):
        """raise an error"""
        self.error = ValueError('foo')
        raise self.error

    @trap(custom_handle_exception, classes=ValueError)
    @trap(classes=KeyError)
    def double_trap(self):
        """raise an error"""
        self.error = ValueError('foo')
        raise self.error

    def test_exception(self):
        """normal test"""

        self.value_exception()
        assert self.exception is self.error

    def test_not_a_key_error(self):
        """test specific trap"""

        with pytest.raises(ValueError):
            self.not_a_key_error()

    def test_method_handler(self):
        """method handler test"""
        self.method_handler()
        assert SAVE[0] is self.error

    def test_double_trap(self):
        """method handler test"""
        self.double_trap()
        assert SAVE[0] is self.error
