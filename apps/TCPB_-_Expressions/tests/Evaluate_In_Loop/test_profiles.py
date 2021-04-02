# -*- coding: utf-8 -*-
"""Test case template for App testing."""
# flake8: noqa: F401
import os

from tcex.testing import TestCasePlaybook

from .custom_feature import CustomFeature  # pylint: disable=relative-beyond-top-level
from .validate_feature import ValidateFeature  # pylint: disable=relative-beyond-top-level


# pylint: disable=useless-super-delegation,too-many-function-args
class TestProfiles(TestCasePlaybook):
    """TcEx App Testing Template."""

    def setup_class(self):
        """Run setup logic before all test cases in this module."""
        super(TestProfiles, self).setup_class()
        self.custom = CustomFeature()  # pylint: disable=attribute-defined-outside-init
        if os.getenv('SETUP_CLASS') is None:
            self.custom.setup_class(self)
        # enable auto-update of profile data
        self.enable_update_profile = True  # pylint: disable=attribute-defined-outside-init

    def setup_method(self):
        """Run setup logic before test method runs."""
        super(TestProfiles, self).setup_method()
        if os.getenv('SETUP_METHOD') is None:
            self.custom.setup_method(self)

    def teardown_class(self):
        """Run setup logic after all test cases in this module."""
        if os.getenv('TEARDOWN_CLASS') is None:
            self.custom.teardown_class(self)
        super(TestProfiles, self).teardown_class()
        # disable auto-update of profile data
        self.enable_update_profile = False  # pylint: disable=attribute-defined-outside-init

    def teardown_method(self):
        """Run teardown logic after test method completes."""
        if os.getenv('TEARDOWN_METHOD') is None:
            self.custom.teardown_method(self)
        super(TestProfiles, self).teardown_method()

    def test_profiles(
        self, profile_name, pytestconfig, monkeypatch, options
    ):  # pylint: disable=unused-argument
        """Run pre-created testing profiles."""

        # initialize profile
        valid, message = self.init_profile(
            profile_name, pytestconfig=pytestconfig, monkeypatch=monkeypatch, options=options
        )
        assert valid, message

        # run custom test method before run method
        self.custom.test_pre_run(self, self.profile.data, monkeypatch)

        assert self.run_profile() in self.profile.exit_codes

        # run custom test method before validation
        self.custom.test_pre_validate(self, self.profile.data)

        # get Validation instance
        validation = ValidateFeature(self.validator)

        # validate App outputs and Profile outputs are consistent
        validation.validate_outputs(self.profile.tc_playbook_out_variables, self.profile.outputs)

        # validate App outputs with Profile outputs
        validation.validate(self.profile.outputs)

        # validate exit message
        exit_message_data = self.profile.exit_message
        if exit_message_data:
            self.validate_exit_message(
                exit_message_data.pop('expected_output'),
                exit_message_data.pop('op'),
                **exit_message_data
            )
