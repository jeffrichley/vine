"""Effect configuration models for Project Vine."""

from typing import Literal, Optional, Union

from pydantic import Field

from vine.models.base import BaseModel


class EffectConfig(BaseModel):
    """Base configuration for video effects."""

    type: str = Field(..., description="Type of effect")
    duration: Optional[float] = Field(
        None, ge=0.0, description="Effect duration in seconds"
    )
    start_time: Optional[float] = Field(0.0, ge=0.0, description="Start time of effect")


class KenBurnsConfig(EffectConfig):
    """Configuration for Ken Burns effect."""

    type: Literal["ken_burns"] = "ken_burns"
    zoom_factor: float = Field(1.2, ge=1.0, le=3.0, description="Zoom factor")
    pan_x: float = Field(0.0, ge=-1.0, le=1.0, description="Horizontal pan (-1 to 1)")
    pan_y: float = Field(0.0, ge=-1.0, le=1.0, description="Vertical pan (-1 to 1)")
    easing: str = Field("ease_in_out", description="Easing function")


class SlideConfig(EffectConfig):
    """Configuration for slide effect."""

    type: Literal["slide"] = "slide"
    direction: Literal["left", "right", "up", "down"] = Field(
        "left", description="Slide direction"
    )
    distance: float = Field(100.0, ge=0.0, description="Slide distance in pixels")
    easing: str = Field("ease_in_out", description="Easing function")


class StaticConfig(EffectConfig):
    """Configuration for static/no effect."""

    type: Literal["static"] = "static"
    # No additional parameters needed for static effect


# Union type for all effect configurations
EffectType = Union[KenBurnsConfig, SlideConfig, StaticConfig]
