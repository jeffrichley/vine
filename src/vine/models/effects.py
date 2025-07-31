"""Effect models for Project Vine."""

from typing import Literal

from pydantic import Field

from vine.models.base import BaseModel
from vine.models.transition import TransitionDirection


class BaseEffect(BaseModel):
    """Base class for all effects."""

    type: str = Field(..., description="Type of effect")
    duration: float | None = Field(
        None, ge=0.0, description="Effect duration in seconds"
    )
    start_time: float | None = Field(0.0, ge=0.0, description="Start time of effect")

    def get_type(self) -> str:
        """Get the effect type."""
        return self.type

    def get_duration(self) -> float | None:
        """Get the effect duration."""
        return self.duration

    def get_start_time(self) -> float:
        """Get the effect start time."""
        return self.start_time or 0.0


class KenBurnsEffect(BaseEffect):
    """Ken Burns effect for zooming and panning."""

    type: Literal["ken_burns"] = "ken_burns"
    zoom_factor: float = Field(1.2, ge=1.0, le=3.0, description="Zoom factor")
    pan_x: float = Field(0.0, ge=-1.0, le=1.0, description="Horizontal pan (-1 to 1)")
    pan_y: float = Field(0.0, ge=-1.0, le=1.0, description="Vertical pan (-1 to 1)")
    easing: str = Field("ease_in_out", description="Easing function")


class SlideEffect(BaseEffect):
    """Slide effect for directional movement."""

    type: Literal["slide"] = "slide"
    direction: TransitionDirection = Field(
        TransitionDirection.LEFT, description="Slide direction"
    )
    distance: float = Field(100.0, ge=0.0, description="Slide distance in pixels")
    easing: str = Field("ease_in_out", description="Easing function")


class StaticEffect(BaseEffect):
    """Static/no effect."""

    type: Literal["static"] = "static"
    # No additional parameters needed for static effect
