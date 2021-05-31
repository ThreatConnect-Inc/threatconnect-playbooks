"""Custom test method Class for runtime_level -> playbook."""
# standard library
from typing import Optional


# pylint: disable=no-self-use,unused-argument
class Custom:
    """Custom test method class Apps."""

    def __init__(self):
        """Initialize class properties."""

    def setup_class(self, test_feature: object) -> None:
        """Run setup class code."""
        # set the App run method (inline (default), subprocess)
        # Note: using inline forces the App to use the tcex version
        # from site-packages and not the lib_ directory.
        # test_feature.run_method = 'inline'

    def setup_method(self, test_feature: object) -> None:
        """Run setup method code."""

    def teardown_class(self, test_feature: object) -> None:
        """Run teardown class code."""

    def teardown_method(self, test_feature: object) -> None:
        """Run teardown method code."""

    def test_pre_run(
        self, test_feature: object, profile_data: dict, monkeypatch: Optional[object]
    ) -> None:  # pylint: disable=useless-super-delegation
        """Run test method code before App run method."""
        if test_feature.run_method != 'inline':
            test_feature.log.warning('run_method is not inline, monkeypatch will not work!')

    def test_pre_validate(
        self, test_feature: object, profile_data: dict
    ) -> None:  # pylint: disable=useless-super-delegation
        """Run test method code before test validation."""
