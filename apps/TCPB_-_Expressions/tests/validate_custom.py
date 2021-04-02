# -*- coding: utf-8 -*-
"""Validate custom test case class."""
from .validate import Validate


class ValidateCustom(Validate):
    """Validate for Feature Foo

    This file will only be auto-generated once to ensure any changes are not overwritten.
    """

    def __init__(self, validator):  # pylint: disable=useless-super-delegation
        """Initialize class properties."""
        super(ValidateCustom, self).__init__(validator)

    def expression_expression_string(self, variable, data):
        """Assert for #App:9876:expression.expression!String."""

        app_data = self.validator.tcex.playbook.read(variable, embedded=False)
        expected_output = data.pop('expected_output')

        # assert variable data
        assert app_data == expected_output, 'Expression does not match'
