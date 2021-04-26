# -*- coding: utf-8 -*-
"""Validate feature test case class."""
from ..validate_custom import ValidateCustom


class ValidateFeature(ValidateCustom):
    """Validate for Feature Expression

    This file will only be auto-generated once to ensure any changes are not overwritten.
    """

    def __init__(self, validator):  # pylint: disable=useless-super-delegation
        """Initialize class properties."""
        super(ValidateFeature, self).__init__(validator)
