"""Custom test method feature class."""
# standard library
from typing import Optional

from ..custom import Custom  # pylint: disable=relative-beyond-top-level


# pylint: disable=no-self-use,unused-argument,useless-super-delegation
class CustomFeature(Custom):
    """Custom test method class Apps."""

    def __init__(self, **kwargs):
        """Initialize class properties."""
        super().__init__(**kwargs)

    def setup_class(self, test_feature: object) -> None:
        """Run setup class code."""
        super().setup_class(test_feature)

    def setup_method(self, test_feature: object) -> None:
        """Run setup method code."""
        super().setup_method(test_feature)

    def teardown_class(self, test_feature: object) -> None:
        """Run teardown class code."""
        super().teardown_class(test_feature)

    def teardown_method(self, test_feature: object) -> None:
        """Run teardown method code."""
        super().teardown_method(test_feature)

    def test_pre_run(
        self, test_feature: object, profile_data: dict, monkeypatch: Optional[object]
    ) -> None:
        """Run test method code before App run method.

        Args:
            test_feature: test_feature object for this test run.
            profile_data: Data loaded from the test profile json file.
            monkeypatch: if run_method is 'inline', then a monkeypatch object, else None
        """
        super().test_pre_run(test_feature, profile_data, monkeypatch)

    def test_pre_validate(self, test_feature: object, profile_data: dict) -> None:
        """Run test method code before test validation."""
        super().test_pre_validate(test_feature, profile_data)
