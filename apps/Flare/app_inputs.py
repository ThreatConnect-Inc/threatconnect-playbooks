"""App Inputs"""
# standard library
from typing import List, Union

# third-party
from pydantic import BaseModel
from tcex.input.field_types import KeyValue, TCEntity


class AppBaseModel(BaseModel):
    """Base model for the App containing any common inputs."""

    indent: int = 4
    # install.json defines the following playbook data types:
    # KeyValue      - KeyValueModel
    # KeyValueArray - List[KeyValueModel]
    # String        - str
    # StringArray   - List[str]
    # TCEntity      - TCEntityModel
    # TCEntityArray - List[TCEntityModel]
    json_data: Union[KeyValue, List[KeyValue], str, List[str], TCEntity, List[TCEntity]]
    sort_keys: bool = False


class AppInputs:
    """App Inputs"""

    def __init__(self, inputs: 'BaseModel') -> None:
        """Initialize class properties."""
        self.inputs = inputs

    def update_inputs(self) -> None:
        """Add custom App models to inputs. Validation will run at the same time."""
        self.inputs.add_model(AppBaseModel)
