"""Timeline block models for Project Vine."""

from typing import List, Literal, Optional

from pydantic import Field, model_validator

from vine.models.animation_config import AnimationConfig
from vine.models.audio_config import MusicConfig, VoiceConfig
from vine.models.base import BaseModel


class TimelineBlock(BaseModel):
    """A block in the video timeline representing a video/audio segment."""

    block_type: Literal["video", "audio", "image", "text"] = Field(
        ..., description="Type of timeline block"
    )
    start_time: float = Field(
        0.0, ge=0.0, description="Start time in timeline in seconds"
    )
    duration: Optional[float] = Field(None, ge=0.0, description="Duration in seconds")

    # Media sources
    video_path: Optional[str] = Field(None, description="Path to video file")
    image_path: Optional[str] = Field(None, description="Path to image file")
    audio_path: Optional[str] = Field(None, description="Path to audio file")
    text_content: Optional[str] = Field(
        None, description="Text content for text blocks"
    )

    # Configuration
    animations: List[AnimationConfig] = Field(
        default_factory=list, description="List of animations"
    )
    voice_config: Optional[VoiceConfig] = Field(
        None, description="Voice audio configuration"
    )
    music_config: Optional[MusicConfig] = Field(
        None, description="Music audio configuration"
    )

    # Display settings
    width: Optional[int] = Field(None, ge=1, description="Display width in pixels")
    height: Optional[int] = Field(None, ge=1, description="Display height in pixels")
    x_position: float = Field(0.0, description="X position on screen")
    y_position: float = Field(0.0, description="Y position on screen")
    opacity: float = Field(1.0, ge=0.0, le=1.0, description="Opacity (0-1)")

    @model_validator(mode="after")
    def validate_block_configuration(self) -> "TimelineBlock":
        """Validate block configuration based on type."""
        block_type = self.block_type

        if block_type == "video" and not self.video_path:
            raise ValueError("Video blocks must have a video_path")
        elif block_type == "image" and not self.image_path:
            raise ValueError("Image blocks must have an image_path")
        elif block_type == "audio" and not self.audio_path:
            raise ValueError("Audio blocks must have an audio_path")
        elif block_type == "text" and not self.text_content:
            raise ValueError("Text blocks must have text_content")

        return self

    def get_end_time(self) -> Optional[float]:
        """Get the end time of the block."""
        if self.duration is None:
            return None
        return self.start_time + self.duration

    def overlaps_with(self, other: "TimelineBlock") -> bool:
        """Check if this block overlaps with another."""
        if self.duration is None or other.duration is None:
            return False

        self_end = self.start_time + self.duration
        other_end = other.start_time + other.duration

        return not (self_end <= other.start_time or other_end <= self.start_time)

    def add_animation(self, animation: AnimationConfig) -> None:
        """Add an animation to this block."""
        self.animations.append(animation)

    def get_animations_at_time(self, time: float) -> List[AnimationConfig]:
        """Get animations active at the given time."""
        return [
            anim
            for anim in self.animations
            if anim.start_time <= time <= anim.get_end_time()
        ]

    def is_active_at_time(self, time: float) -> bool:
        """Check if this block is active at the given time."""
        if self.duration is None:
            return time >= self.start_time
        return self.start_time <= time <= self.start_time + self.duration
