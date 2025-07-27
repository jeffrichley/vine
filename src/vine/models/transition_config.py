"""Transition configuration models for Project Vine."""

from typing import Optional

from pydantic import Field, field_validator

from vine.models.base import BaseModel
from vine.models.transitions import TransitionTypeUnion


class TransitionConfig(BaseModel):
    """Configuration for transitions between timeline blocks."""

    transition: TransitionTypeUnion = Field(
        ..., description="Transition effect configuration"
    )
    start_time: float = Field(
        0.0, ge=0.0, description="Transition start time in seconds"
    )
    from_block_id: Optional[str] = Field(None, description="Source block ID")
    to_block_id: Optional[str] = Field(None, description="Target block ID")

    @field_validator("from_block_id", "to_block_id")
    @classmethod
    def validate_block_ids(cls, v: Optional[str]) -> Optional[str]:
        """Validate block IDs are not empty strings."""
        if v == "":
            return None
        return v

    def get_end_time(self) -> float:
        """Get the end time of the transition."""
        return self.start_time + self.transition.duration

    def overlaps_with(self, other: "TransitionConfig") -> bool:
        """Check if this transition overlaps with another."""
        self_end = self.start_time + self.transition.duration
        other_end = other.start_time + other.transition.duration

        return not (self_end <= other.start_time or other_end <= self.start_time)

    def is_valid_for_blocks(self, from_block_id: str, to_block_id: str) -> bool:
        """Check if transition is valid for the given blocks."""
        if self.from_block_id and self.from_block_id != from_block_id:
            return False
        if self.to_block_id and self.to_block_id != to_block_id:
            return False
        return True
