"""Track-based data models for Project Vine."""

from enum import Enum
from pathlib import Path
from typing import List, Optional, Tuple, Union

from pydantic import Field, ValidationInfo, field_validator

from vine.models.animation_config import AnimationConfig
from vine.models.audio_config import MusicConfig, VoiceConfig
from vine.models.base import BaseModel


class TrackType(str, Enum):
    """Enumeration of supported track types."""

    VIDEO = "video"
    MUSIC = "music"
    VOICE = "voice"
    SFX = "sfx"
    TEXT = "text"


class VideoClip(BaseModel):
    """A video clip within a video track."""

    path: Union[str, Path] = Field(..., description="Path to video file")
    start_time: float = Field(
        0.0, ge=0.0, description="Start time in timeline in seconds"
    )
    duration: Optional[float] = Field(None, ge=0.0, description="Duration in seconds")
    end_time: Optional[float] = Field(
        None, ge=0.0, description="End time in timeline in seconds"
    )

    # Display settings
    width: Optional[int] = Field(None, ge=1, description="Display width in pixels")
    height: Optional[int] = Field(None, ge=1, description="Display height in pixels")
    x_position: float = Field(0.0, description="X position on screen")
    y_position: float = Field(0.0, description="Y position on screen")
    opacity: float = Field(1.0, ge=0.0, le=1.0, description="Opacity (0-1)")

    # Effects and animations
    animations: List[AnimationConfig] = Field(
        default_factory=list, description="List of animations"
    )

    # Metadata
    metadata: dict = Field(
        default_factory=dict, description="Additional metadata for the clip"
    )

    @field_validator("end_time")
    @classmethod
    def validate_end_time(
        cls, v: Optional[float], info: ValidationInfo
    ) -> Optional[float]:
        """Validate end_time is after start_time and not both duration and end_time are set."""
        if v is not None:
            start_time = info.data.get("start_time", 0.0)
            if v <= start_time:
                raise ValueError("End time must be after start time")

            duration = info.data.get("duration")
            if duration is not None:
                raise ValueError("Cannot specify both duration and end_time")

        return v

    def get_end_time(self) -> Optional[float]:
        """Get the end time of the clip."""
        if self.duration is None:
            return self.end_time
        return self.start_time + self.duration

    def is_active_at_time(self, time: float) -> bool:
        """Check if this clip is active at the given time."""
        end_time = self.get_end_time()
        if end_time is None:
            return time >= self.start_time
        return self.start_time <= time < end_time


class ImageClip(BaseModel):
    """An image clip within a video track."""

    path: Union[str, Path] = Field(..., description="Path to image file")
    start_time: float = Field(
        0.0, ge=0.0, description="Start time in timeline in seconds"
    )
    duration: Optional[float] = Field(None, ge=0.0, description="Duration in seconds")
    end_time: Optional[float] = Field(
        None, ge=0.0, description="End time in timeline in seconds"
    )

    # Display settings
    width: Optional[int] = Field(None, ge=1, description="Display width in pixels")
    height: Optional[int] = Field(None, ge=1, description="Display height in pixels")
    x_position: float = Field(0.0, description="X position on screen")
    y_position: float = Field(0.0, description="Y position on screen")
    opacity: float = Field(1.0, ge=0.0, le=1.0, description="Opacity (0-1)")

    # Effects and animations
    animations: List[AnimationConfig] = Field(
        default_factory=list, description="List of animations"
    )

    # Metadata
    metadata: dict = Field(
        default_factory=dict, description="Additional metadata for the clip"
    )

    @field_validator("end_time")
    @classmethod
    def validate_end_time(
        cls, v: Optional[float], info: ValidationInfo
    ) -> Optional[float]:
        """Validate end_time is after start_time and not both duration and end_time are set."""
        if v is not None:
            start_time = info.data.get("start_time", 0.0)
            if v <= start_time:
                raise ValueError("End time must be after start time")

            duration = info.data.get("duration")
            if duration is not None:
                raise ValueError("Cannot specify both duration and end_time")

        return v

    def get_end_time(self) -> Optional[float]:
        """Get the end time of the clip."""
        if self.duration is None:
            return self.end_time
        return self.start_time + self.duration

    def is_active_at_time(self, time: float) -> bool:
        """Check if this clip is active at the given time."""
        end_time = self.get_end_time()
        if end_time is None:
            return time >= self.start_time
        return self.start_time <= time < end_time


class TextClip(BaseModel):
    """A text clip within a text track."""

    content: str = Field(..., description="Text content")
    start_time: float = Field(
        0.0, ge=0.0, description="Start time in timeline in seconds"
    )
    duration: Optional[float] = Field(None, ge=0.0, description="Duration in seconds")
    end_time: Optional[float] = Field(
        None, ge=0.0, description="End time in timeline in seconds"
    )

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
    animations: List[AnimationConfig] = Field(
        default_factory=list, description="List of animations"
    )

    # Metadata
    metadata: dict = Field(
        default_factory=dict, description="Additional metadata for the clip"
    )

    @field_validator("end_time")
    @classmethod
    def validate_end_time(
        cls, v: Optional[float], info: ValidationInfo
    ) -> Optional[float]:
        """Validate end_time is after start_time and not both duration and end_time are set."""
        if v is not None:
            start_time = info.data.get("start_time", 0.0)
            if v <= start_time:
                raise ValueError("End time must be after start time")

            duration = info.data.get("duration")
            if duration is not None:
                raise ValueError("Cannot specify both duration and end_time")

        return v

    def get_end_time(self) -> Optional[float]:
        """Get the end time of the clip."""
        if self.duration is None:
            return self.end_time
        return self.start_time + self.duration

    def is_active_at_time(self, time: float) -> bool:
        """Check if this clip is active at the given time."""
        end_time = self.get_end_time()
        if end_time is None:
            return time >= self.start_time
        return self.start_time <= time < end_time


class AudioClip(BaseModel):
    """An audio clip within an audio track."""

    path: Union[str, Path] = Field(..., description="Path to audio file")
    start_time: float = Field(
        0.0, ge=0.0, description="Start time in timeline in seconds"
    )
    duration: Optional[float] = Field(None, ge=0.0, description="Duration in seconds")
    end_time: Optional[float] = Field(
        None, ge=0.0, description="End time in timeline in seconds"
    )

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
    volume_curve: Optional[List[Tuple[float, float]]] = Field(
        None, description="Custom volume envelope as list of (time, volume) tuples"
    )

    # Audio configuration
    voice_config: Optional[VoiceConfig] = Field(None, description="Voice configuration")
    music_config: Optional[MusicConfig] = Field(None, description="Music configuration")

    # Metadata
    metadata: dict = Field(
        default_factory=dict, description="Additional metadata for the clip"
    )

    @field_validator("end_time")
    @classmethod
    def validate_end_time(
        cls, v: Optional[float], info: ValidationInfo
    ) -> Optional[float]:
        """Validate end_time is after start_time and not both duration and end_time are set."""
        if v is not None:
            start_time = info.data.get("start_time", 0.0)
            if v <= start_time:
                raise ValueError("End time must be after start time")

            duration = info.data.get("duration")
            if duration is not None:
                raise ValueError("Cannot specify both duration and end_time")

        return v

    def get_end_time(self) -> Optional[float]:
        """Get the end time of the clip."""
        if self.duration is None:
            return self.end_time
        return self.start_time + self.duration

    def is_active_at_time(self, time: float) -> bool:
        """Check if this clip is active at the given time."""
        end_time = self.get_end_time()
        if end_time is None:
            return time >= self.start_time
        return self.start_time <= time < end_time


class VideoTrack(BaseModel):
    """A video track containing video and image clips."""

    name: str = Field(..., description="Track name")
    clips: List[Union[VideoClip, ImageClip]] = Field(
        default_factory=list, description="List of video/image clips"
    )
    z_order: int = Field(0, description="Rendering order (lower = background)")
    visible: bool = Field(True, description="Whether the track is visible")

    def add_clip(self, clip: Union[VideoClip, ImageClip]) -> None:
        """Add a clip to this track."""
        self.clips.append(clip)

    def get_active_clips_at_time(
        self, time: float
    ) -> List[Union[VideoClip, ImageClip]]:
        """Get all clips active at the given time."""
        return [clip for clip in self.clips if clip.is_active_at_time(time)]

    def has_overlapping_clips(self) -> bool:
        """Check if this track has overlapping clips."""
        if len(self.clips) < 2:
            return False

        # Sort clips by start time
        sorted_clips = sorted(self.clips, key=lambda c: c.start_time)

        for i in range(len(sorted_clips) - 1):
            current_clip = sorted_clips[i]
            next_clip = sorted_clips[i + 1]

            current_end = current_clip.get_end_time()
            if current_end is None:
                return True  # Infinite duration clips overlap with everything

            if current_end > next_clip.start_time:
                return True

        return False


class AudioTrack(BaseModel):
    """An audio track containing audio clips."""

    name: str = Field(..., description="Track name")
    clips: List[AudioClip] = Field(
        default_factory=list, description="List of audio clips"
    )
    volume: float = Field(1.0, ge=0.0, le=2.0, description="Track volume level")
    muted: bool = Field(False, description="Whether the track is muted")

    def add_clip(self, clip: AudioClip) -> None:
        """Add a clip to this track."""
        self.clips.append(clip)

    def get_active_clips_at_time(self, time: float) -> List[AudioClip]:
        """Get all clips active at the given time."""
        return [clip for clip in self.clips if clip.is_active_at_time(time)]

    def has_overlapping_clips(self) -> bool:
        """Check if this track has overlapping clips."""
        if len(self.clips) < 2:
            return False

        # Sort clips by start time
        sorted_clips = sorted(self.clips, key=lambda c: c.start_time)

        for i in range(len(sorted_clips) - 1):
            current_clip = sorted_clips[i]
            next_clip = sorted_clips[i + 1]

            current_end = current_clip.get_end_time()
            if current_end is None:
                return True  # Infinite duration clips overlap with everything

            if current_end > next_clip.start_time:
                return True

        return False


class TextTrack(BaseModel):
    """A text track containing text clips."""

    name: str = Field(..., description="Track name")
    clips: List[TextClip] = Field(
        default_factory=list, description="List of text clips"
    )
    z_order: int = Field(0, description="Rendering order (lower = background)")
    visible: bool = Field(True, description="Whether the track is visible")

    def add_clip(self, clip: TextClip) -> None:
        """Add a clip to this track."""
        self.clips.append(clip)

    def get_active_clips_at_time(self, time: float) -> List[TextClip]:
        """Get all clips active at the given time."""
        return [clip for clip in self.clips if clip.is_active_at_time(time)]

    def has_overlapping_clips(self) -> bool:
        """Check if this track has overlapping clips."""
        if len(self.clips) < 2:
            return False

        # Sort clips by start time
        sorted_clips = sorted(self.clips, key=lambda c: c.start_time)

        for i in range(len(sorted_clips) - 1):
            current_clip = sorted_clips[i]
            next_clip = sorted_clips[i + 1]

            current_end = current_clip.get_end_time()
            if current_end is None:
                return True  # Infinite duration clips overlap with everything

            if current_end > next_clip.start_time:
                return True

        return False
