""" Custom validation logic """
# standard library
import json
from fnmatch import fnmatch

# third-party
from deepdiff import DeepDiff

from .structure import compare_structure, reduce_structure
from .validate import Validate

NOTFOUND = object()

# To make this validator work, we strip out the builtin validations

PRESERVE = ['validate', 'validate_outputs', 'dynamic_output_variable', '*status_code*']


class ValidateCustom(Validate):
    """Validate for Feature add_signature

    This file will only be auto-generated once to ensure any changes are not overwritten.
    """

    def __init__(self, validator):  # pylint: disable=useless-super-delegation
        """Initialize class properties."""
        super().__init__(validator)

        # now *undo* all of the tests that are in Validate, and replace them with
        # compare structure tests

        for name in dir(Validate):
            self.replace_method(name, self.compare_structure)

    def replace_method(self, name, replacement):
        """Replace the method if it isn't a preserved one"""

        if name.startswith('__'):
            return

        if '_' not in name:
            return

        for preserve in PRESERVE:
            if fnmatch(name, preserve):
                return

        setattr(self, name, replacement)  # whomp!

    def read_data(self, variable):
        """Read the original value from the provider"""
        provider = self.validator.redis.provider
        if variable.endswith('Binary'):
            app_data = provider.tcex.playbook.read_binary(variable, False, False)
        elif variable.endswith('BinaryArray'):
            app_data = provider.tcex.playbook.read_binary_array(variable, False, False)
        elif variable.endswith('TCEnhancedEntity') or variable.endswith('TCEntity'):
            app_data = provider.tcex.playbook.read(variable)
            try:
                app_data = json.loads(app_data)
            except Exception:
                provider.log.warning(f'Could not convert {app_data} to json.')
        else:
            app_data = provider.tcex.playbook.read(variable)
        return app_data

    def compare_structure(self, variable: str, data: dict) -> None:
        """Compare the structure of the variable, NOT the values"""

        expected_output = data.pop('expected_output')
        # op = data.pop('op', '=')

        redis_value = self.read_data(variable)
        r_value = redis_value
        r_expectation = expected_output

        if (
            isinstance(r_value, str)
            and isinstance(r_expectation, str)
            and (r_value and r_expectation)
        ):

            if r_value[0] == r_expectation[0] and r_value[0] in ('[', '{'):
                try:
                    rj = json.loads(r_value)
                    re = json.loads(r_expectation)
                    r_value = rj
                    r_expectation = re
                except Exception:  # nosec  it it cant load as json, oh well
                    pass

        r_value = reduce_structure(r_value)
        r_expectation = reduce_structure(r_expectation)

        # assert variable data
        passed, assert_error = (
            compare_structure(r_value, r_expectation),
            f'Structural differences in {variable} output: {r_value!r} vs {r_expectation!r}',
        )

        if (
            not passed
            and isinstance(r_value, (dict, list))
            and isinstance(r_expectation, (dict, list))
        ):
            dd = DeepDiff(r_value, r_expectation, ignore_order=True)
            if not dd:
                passed = True
            else:
                assert_error = f'Structural differences in {variable} output: {dd}'

        assert passed, assert_error
