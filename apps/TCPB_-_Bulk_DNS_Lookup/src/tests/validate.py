"""Validate App outputs Class."""
# flake8: noqa
# pylint: disable=line-too-long
# standard library
import inspect


class Validate:
    """Validate base class for App output validation."""

    def __init__(self, validator: object):
        """Initialize class properties."""
        self.validator = validator

    @staticmethod
    def validate_outputs(app_outputs: list, profile_outputs: dict) -> None:
        """Assert outputs match."""
        if not isinstance(app_outputs, list) or not isinstance(profile_outputs, dict):
            assertion_error = (
                'Invalid value provided for App or profile outputs.\n'
                f'App Output     : {app_outputs}\n'
                f'Profile Output : {profile_outputs}\n'
            )
            assert False, assertion_error

        diff_1 = list(set(app_outputs).difference(set(profile_outputs)))
        diff_2 = list(set(profile_outputs).difference(set(app_outputs)))
        if diff_1 or diff_2:
            assertion_error = (
                f'Profile outputs are not consistent with App outputs.\n'
                f'App Output difference    : {diff_1}\n'
                f'Profile Output difference: {list(diff_2)}\n'
            )
            assert False, assertion_error

    def validate(self, output_variables: dict) -> None:
        """Validate Redis output data."""
        if output_variables is None:
            return

        for k, v in output_variables.items():
            # get method name from variable name
            method_name = self.validator.utils.variable_method_name(k)
            if hasattr(self, method_name):
                method = getattr(self, method_name)  # get the validation method by name
                if 'variable' in [p.name for p in inspect.signature(method).parameters.values()]:
                    method(k, dict(v))  # methods with new signature
                else:
                    method(dict(v))  # methods with old signature
            else:
                self.dynamic_output_variable(k, dict(v))

    def dynamic_output_variable(self, variable: str, data: dict) -> None:
        """Assert for dynamic output variables."""
        expected_output = data.pop('expected_output')
        op = data.pop('op', '=')

        # assert variable data
        passed, assert_error = self.validator.redis.data(variable, expected_output, op, **data)
        assert passed, assert_error

    def dns_action_string(self, variable: str, data: dict) -> None:
        """Assert for #App:9876:dns.action!String."""
        expected_output = data.pop('expected_output')
        op = data.pop('op', '=')

        # assert variable data
        passed, assert_error = self.validator.redis.data(variable, expected_output, op, **data)
        assert passed, assert_error

    def dns_invalid_stringarray(self, variable: str, data: dict) -> None:
        """Assert for #App:9876:dns.invalid!StringArray."""
        expected_output = data.pop('expected_output')
        op = data.pop('op', '=')

        # assert variable data
        passed, assert_error = self.validator.redis.data(variable, expected_output, op, **data)
        assert passed, assert_error

    def dns_result_json_string(self, variable: str, data: dict) -> None:
        """Assert for #App:9876:dns.result.json!String."""
        expected_output = data.pop('expected_output')
        op = data.pop('op', '=')

        # assert variable data
        passed, assert_error = self.validator.redis.data(variable, expected_output, op, **data)
        assert passed, assert_error

    def dns_valid_stringarray(self, variable: str, data: dict) -> None:
        """Assert for #App:9876:dns.valid!StringArray."""
        expected_output = data.pop('expected_output')
        op = data.pop('op', '=')

        # assert variable data
        passed, assert_error = self.validator.redis.data(variable, expected_output, op, **data)
        assert passed, assert_error
