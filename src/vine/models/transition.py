"""Global transition model for Project Vine."""

from enum import Enum
from typing import Any

from pydantic import Field

from vine.models.base import BaseModel


class TransitionType(str, Enum):
    """Enumeration of supported transition types."""

    FADE = "fade"
    CROSSFADE = "crossfade"
    SLIDE = "slide"
    WIPE = "wipe"
    DISSOLVE = "dissolve"


class TransitionDirection(str, Enum):
    """Enumeration of transition directions."""

    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"
    IN = "in"
    OUT = "out"


class TransitionEasing(str, Enum):
    """Enumeration of transition easing functions."""

    LINEAR = "linear"
    EASE_IN = "ease_in"
    EASE_OUT = "ease_out"
    EASE_IN_OUT = "ease_in_out"


class Transition(BaseModel):
    """A global transition that affects multiple tracks."""

    transition_type: TransitionType = Field(..., description="Type of transition")
    start_time: float = Field(
        0.0, ge=0.0, description="Start time in timeline in seconds"
    )
    duration: float = Field(1.0, ge=0.0, description="Duration in seconds")

    # Track targeting
    from_tracks: list[str] = Field(
        default_factory=list, description="Source track names"
    )
    to_tracks: list[str] = Field(default_factory=list, description="Target track names")

    # Transition parameters
    direction: TransitionDirection = Field(
        TransitionDirection.IN, description="Transition direction"
    )
    easing: TransitionEasing = Field(
        TransitionEasing.LINEAR, description="Easing function"
    )

    # Metadata
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata for the transition"
    )

    def get_end_time(self) -> float:
        """Get the end time of the transition."""
        return self.start_time + self.duration

    def is_active_at_time(self, time: float) -> bool:
        """Check if this transition is active at the given time."""
        return self.start_time <= time <= self.get_end_time()

    def get_progress_at_time(self, time: float) -> float:
        """Get the transition progress (0.0 to 1.0) at the given time."""
        if not self.is_active_at_time(time):
            return 0.0 if time < self.start_time else 1.0

        # Handle zero duration case
        if self.duration == 0.0:
            return 1.0 if time >= self.start_time else 0.0

        elapsed = time - self.start_time
        return min(elapsed / self.duration, 1.0)
