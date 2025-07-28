"""Base model for Project Vine."""

import uuid

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field


class BaseModel(PydanticBaseModel):
    """Base model with common functionality for Project Vine."""

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), description="Unique identifier"
    )

    model_config = ConfigDict(
        extra="forbid",  # Reject extra fields
        validate_assignment=True,  # Validate on assignment
        use_enum_values=True,  # Use enum values instead of enum objects
    )
