# -*- coding: utf-8 -*-
"""Custom test method Class for runtime_level -> playbook."""


# pylint: disable=no-self-use,unused-argument
class Custom(object):
    """Custom test method class Apps."""

    def __init__(self):
        """Initialize class properties."""

    def setup_class(self, test_feature):
        """Run setup class code."""
        # set the App run method (inline (default), subprocess)
        # Note: using inline forces the App to use the tcex version
        # from site-packages and not the lib_ directory.
        # test_feature.run_method = 'inline'

    def setup_method(self, test_feature):
        """Run setup method code."""

    def teardown_class(self, test_feature):
        """Run teardown class code."""

    def teardown_method(self, test_feature):
        """Run teardown method code."""

    def test_pre_run(
        self, test_feature, profile_data, monkeypatch
    ):  # pylint: disable=useless-super-delegation
        """Run test method code before App run method."""

    def test_pre_validate(
        self, test_feature, profile_data
    ):  # pylint: disable=useless-super-delegation
        """Run test method code before test validation."""
