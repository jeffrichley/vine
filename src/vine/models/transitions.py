"""Transition configuration models for Project Vine."""

from typing import Literal, Union

from pydantic import Field

from vine.models.base import BaseModel


class TransitionType(BaseModel):
    """Base configuration for video transitions."""

    type: str = Field(..., description="Type of transition")
    duration: float = Field(
        1.0, ge=0.1, le=10.0, description="Transition duration in seconds"
    )
    easing: str = Field("ease_in_out", description="Easing function")


class FadeConfig(TransitionType):
    """Configuration for fade transition."""

    type: Literal["fade"] = "fade"
    fade_type: Literal["in", "out", "cross"] = Field(
        "cross", description="Type of fade"
    )


class CrossfadeConfig(TransitionType):
    """Configuration for crossfade transition."""

    type: Literal["crossfade"] = "crossfade"
    overlap: float = Field(0.5, ge=0.0, le=1.0, description="Overlap ratio (0-1)")


class SlideTransitionConfig(TransitionType):
    """Configuration for slide transition."""

    type: Literal["slide"] = "slide"
    direction: Literal["left", "right", "up", "down"] = Field(
        "left", description="Slide direction"
    )
    distance: float = Field(100.0, ge=0.0, description="Slide distance in pixels")


# Union type for all transition configurations
TransitionTypeUnion = Union[FadeConfig, CrossfadeConfig, SlideTransitionConfig]
