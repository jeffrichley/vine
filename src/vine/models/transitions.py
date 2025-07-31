"""Transition configuration models for Project Vine."""

from pydantic import Field

from vine.models.base import BaseModel
from vine.models.transition import TransitionDirection, TransitionEasing, TransitionType


class BaseTransition(BaseModel):
    """Base class for all transitions."""

    type: TransitionType = Field(..., description="Type of transition")
    duration: float = Field(
        1.0, ge=0.1, le=10.0, description="Transition duration in seconds"
    )
    easing: TransitionEasing = Field(
        TransitionEasing.EASE_IN_OUT, description="Easing function"
    )

    def get_type(self) -> TransitionType:
        """Get the transition type."""
        return self.type

    def get_duration(self) -> float:
        """Get the transition duration."""
        return self.duration

    def get_easing(self) -> TransitionEasing:
        """Get the transition easing function."""
        return self.easing


class FadeTransition(BaseTransition):
    """Fade transition for smooth opacity changes."""

    type: TransitionType = TransitionType.FADE
    fade_type: TransitionDirection = Field(
        TransitionDirection.IN, description="Type of fade"
    )


class CrossfadeTransition(BaseTransition):
    """Crossfade transition for overlapping content."""

    type: TransitionType = TransitionType.CROSSFADE
    overlap: float = Field(0.5, ge=0.0, le=1.0, description="Overlap ratio (0-1)")


class SlideTransition(BaseTransition):
    """Slide transition for directional movement."""

    type: TransitionType = TransitionType.SLIDE
    direction: TransitionDirection = Field(
        TransitionDirection.LEFT, description="Slide direction"
    )
    distance: float = Field(100.0, ge=0.0, description="Slide distance in pixels")
