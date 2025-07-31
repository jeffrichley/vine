"""Animation configuration models for Project Vine."""

from pydantic import Field, field_validator

from vine.models.base import BaseModel
from vine.models.effects import BaseEffect


class AnimationConfig(BaseModel):
    """Configuration for video animations."""

    effect: BaseEffect = Field(..., description="Animation effect configuration")
    start_time: float = Field(
        0.0, ge=0.0, description="Animation start time in seconds"
    )
    duration: float | None = Field(
        None, ge=0.0, description="Animation duration in seconds"
    )
    easing: str = Field("ease_in_out", description="Easing function for animation")

    @field_validator("easing")
    @classmethod
    def validate_easing(cls, v: str) -> str:
        """Validate easing function is supported."""
        valid_easings = [
            "linear",
            "ease_in",
            "ease_out",
            "ease_in_out",
            "ease_in_quad",
            "ease_out_quad",
            "ease_in_out_quad",
            "ease_in_cubic",
            "ease_out_cubic",
            "ease_in_out_cubic",
        ]
        if v not in valid_easings:
            raise ValueError(f"Unsupported easing function: {v}")
        return v

    def get_end_time(self) -> float | None:
        """Get the end time of the animation."""
        if self.duration is None:
            return None
        return self.start_time + self.duration

    def overlaps_with(self, other: "AnimationConfig") -> bool:
        """Check if this animation overlaps with another."""
        if self.duration is None or other.duration is None:
            return False

        self_end = self.start_time + self.duration
        other_end = other.start_time + other.duration

        return not (self_end <= other.start_time or other_end <= self.start_time)
