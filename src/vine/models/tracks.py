"""Track-based data models for Project Vine."""

from enum import Enum
from pathlib import Path
from typing import Any, Generic, Self, TypeVar

from pydantic import Field, model_validator

from vine.models.animation_config import AnimationConfig
from vine.models.audio_config import MusicConfig, VoiceConfig
from vine.models.base import BaseModel
from vine.models.transitions import BaseTransition


# Track types
class TrackType(str, Enum):
    """Enumeration of supported track types."""

    VIDEO = "video"
    MUSIC = "music"
    VOICE = "voice"
    SFX = "sfx"
    TEXT = "text"


class BaseClip(BaseModel):
    """Base class for all clips with common timing functionality."""

    start_time: float = Field(
        0.0, ge=0.0, description="Start time in timeline in seconds"
    )
    duration: float | None = Field(None, ge=0.0, description="Duration in seconds")
    end_time: float | None = Field(
        None, ge=0.0, description="End time in timeline in seconds"
    )

    # Transitions
    transition_in: BaseTransition | None = Field(
        None, description="Transition when this clip starts"
    )
    transition_out: BaseTransition | None = Field(
        None, description="Transition when this clip ends"
    )

    @model_validator(mode="after")
    def validate_timing(self) -> Self:
        """Validate timing relationships."""
        if self.end_time is not None:
            if self.end_time <= self.start_time:
                raise ValueError("End time must be after start time")

            if self.duration is not None:
                raise ValueError("Cannot specify both duration and end_time")
        return self

    def get_end_time(self) -> float | None:
        """Get the end time of this clip."""
        if self.end_time is not None:
            return self.end_time
        if self.duration is not None:
            return self.start_time + self.duration
        return None

    def is_active_at_time(self, time: float) -> bool:
        """Check if this clip is active at the given time."""
        if time < self.start_time:
            return False
        end_time = self.get_end_time()
        if end_time is None:
            return True  # Infinite duration
        return time < end_time  # End time is exclusive


# Type variable for clip types
ClipT = TypeVar("ClipT", bound=BaseClip)


class BaseTrack(BaseModel, Generic[ClipT]):
    """Base class for all track types."""

    name: str = Field(..., description="Track name")
    clips: list[ClipT] = Field(default_factory=list, description="List of clips")

    def add_clip(self, clip: ClipT) -> None:
        """Add a clip to this track."""
        self.clips.append(clip)

    def remove_clip(self, clip: ClipT) -> None:
        """Remove a clip from this track."""
        if clip in self.clips:
            self.clips.remove(clip)

    def remove_clip_at_index(self, index: int) -> None:
        """Remove a clip at the specified index."""
        if 0 <= index < len(self.clips):
            del self.clips[index]

    def get_active_clips_at_time(self, time: float) -> list[ClipT]:
        """Get all clips active at the given time."""
        return [clip for clip in self.clips if clip.is_active_at_time(time)]

    def has_overlapping_clips(self) -> bool:
        """Check if this track has overlapping clips."""
        if len(self.clips) < 2:
            return False

        # Sort clips by start time
        def get_start_time(clip: ClipT) -> float:
            return clip.start_time

        sorted_clips = sorted(self.clips, key=get_start_time)

        for i in range(len(sorted_clips) - 1):
            current_clip = sorted_clips[i]
            next_clip = sorted_clips[i + 1]

            current_end = current_clip.get_end_time()
            if current_end is None:
                return True  # Infinite duration clips overlap with everything

            if current_end > next_clip.start_time:
                return True

        return False


class VideoClip(BaseClip):
    """A video clip within a video track."""

    path: str | Path = Field(..., description="Path to video file")

    # Display settings
    width: int | None = Field(None, ge=1, description="Display width in pixels")
    height: int | None = Field(None, ge=1, description="Display height in pixels")
    x_position: float = Field(0.0, description="X position on screen")
    y_position: float = Field(0.0, description="Y position on screen")
    opacity: float = Field(1.0, ge=0.0, le=1.0, description="Opacity (0-1)")

    # Effects and animations
    animations: list[AnimationConfig] = Field(
        default_factory=list, description="List of animations"
    )

    # Metadata
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata for the clip"
    )


class ImageClip(BaseClip):
    """An image clip within a video track."""

    path: str | Path = Field(..., description="Path to image file")

    # Display settings
    width: int | None = Field(None, ge=1, description="Display width in pixels")
    height: int | None = Field(None, ge=1, description="Display height in pixels")
    x_position: float = Field(0.0, description="X position on screen")
    y_position: float = Field(0.0, description="Y position on screen")
    opacity: float = Field(1.0, ge=0.0, le=1.0, description="Opacity (0-1)")

    # Effects and animations
    animations: list[AnimationConfig] = Field(
        default_factory=list, description="List of animations"
    )

    # Metadata
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata for the clip"
    )


class TextClip(BaseClip):
    """A text clip within a text track."""

    content: str = Field(..., description="Text content")

    # Text styling
    font_size: int = Field(48, ge=1, description="Font size in pixels")
    font_color: str = Field("#FFFFFF", description="Font color (hex)")
    font_family: str = Field("Arial", description="Font family")
    font_weight: str = Field("normal", description="Font weight")

    # Position and layout
    x_position: float = Field(0.0, description="X position on screen")
    y_position: float = Field(0.0, description="Y position on screen")
    alignment: str = Field("center", description="Text alignment (left, center, right)")
    opacity: float = Field(1.0, ge=0.0, le=1.0, description="Opacity (0-1)")

    # Effects and animations
    animations: list[AnimationConfig] = Field(
        default_factory=list, description="List of animations"
    )

    # Metadata
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata for the clip"
    )


class AudioClip(BaseClip):
    """An audio clip within an audio track."""

    path: str | Path = Field(..., description="Path to audio file")

    # Audio settings
    volume: float = Field(1.0, ge=0.0, le=2.0, description="Volume level (0-2)")
    fade_in: float = Field(0.0, ge=0.0, description="Fade in duration in seconds")
    fade_out: float = Field(0.0, ge=0.0, description="Fade out duration in seconds")

    # Professional audio controls (leveraging MoviePy effects)
    crossfade_duration: float = Field(
        0.5, ge=0.0, description="Crossfade duration with adjacent clips"
    )
    auto_crossfade: bool = Field(
        True, description="Enable automatic crossfades with adjacent clips"
    )
    normalize_audio: bool = Field(False, description="Apply audio normalization")
    volume_curve: list[tuple[float, float]] | None = Field(
        None, description="Custom volume envelope as list of (time, volume) tuples"
    )

    # Audio configuration
    voice_config: VoiceConfig | None = Field(None, description="Voice configuration")
    music_config: MusicConfig | None = Field(None, description="Music configuration")

    # Metadata
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata for the clip"
    )


class VideoTrack(BaseTrack[VideoClip | ImageClip]):
    """A video track containing video and image clips."""

    z_order: int = Field(0, description="Rendering order (lower = background)")
    visible: bool = Field(True, description="Whether the track is visible")


class AudioTrack(BaseTrack[AudioClip]):
    """An audio track containing audio clips."""

    volume: float = Field(1.0, ge=0.0, le=2.0, description="Track volume level")
    muted: bool = Field(False, description="Whether the track is muted")


class TextTrack(BaseTrack[TextClip]):
    """A text track containing text clips."""

    z_order: int = Field(0, description="Rendering order (lower = background)")
    visible: bool = Field(True, description="Whether the track is visible")
