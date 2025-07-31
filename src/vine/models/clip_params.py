"""Clip parameter models for Project Vine."""

from dataclasses import dataclass

from pydantic import Field, model_validator

from vine.models.audio_config import MusicConfig, VoiceConfig
from vine.models.base import BaseModel


class ImageClipParams(BaseModel):
    """Parameters for ImageClip configuration."""

    # Display settings
    width: int | None = Field(None, ge=1, description="Display width in pixels")
    height: int | None = Field(None, ge=1, description="Display height in pixels")
    x_position: float = Field(0.0, description="X position on screen")
    y_position: float = Field(0.0, description="Y position on screen")
    opacity: float = Field(1.0, ge=0.0, le=1.0, description="Opacity (0-1)")


class TextClipParams(BaseModel):
    """Parameters for TextClip configuration."""

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


class AudioClipParams(BaseModel):
    """Parameters for AudioClip configuration."""

    # Audio settings
    volume: float = Field(1.0, ge=0.0, le=2.0, description="Volume level (0-2)")
    fade_in: float = Field(0.0, ge=0.0, description="Fade in duration in seconds")
    fade_out: float = Field(0.0, ge=0.0, description="Fade out duration in seconds")

    # Professional audio controls
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


class VideoClipParams(BaseModel):
    """Parameters for VideoClip configuration."""

    # Display settings
    width: int | None = Field(None, ge=1, description="Display width in pixels")
    height: int | None = Field(None, ge=1, description="Display height in pixels")
    x_position: float = Field(0.0, description="X position on screen")
    y_position: float = Field(0.0, description="Y position on screen")
    opacity: float = Field(1.0, ge=0.0, le=1.0, description="Opacity (0-1)")


class TransitionParams(BaseModel):
    """Parameters for Transition configuration."""

    # Transition-specific parameters can be added here as needed
    pass


class ExportParams(BaseModel):
    """Parameters for video export configuration."""

    codec: str = Field("libx264", description="Video codec")
    bitrate: str | None = Field(None, description="Video bitrate")
    audio_codec: str = Field("aac", description="Audio codec")
    audio_bitrate: str | None = Field(None, description="Audio bitrate")
    preset: str = Field("medium", description="Encoding preset")
    threads: int = Field(0, description="Number of threads (0 = auto)")
    verbose: bool = Field(False, description="Verbose output")
    logger: str | None = Field(None, description="Logger configuration")


class VideoExportOptions(BaseModel):
    """Options for video export with MoviePy write_videofile."""

    codec: str | None = Field(None, description="Video codec (e.g., 'libx264')")
    bitrate: str | None = Field(None, description="Video bitrate (e.g., '5000k')")
    fps: float | None = Field(None, ge=1.0, le=120.0, description="Output FPS")
    audio_codec: str | None = Field(None, description="Audio codec (e.g., 'aac')")
    preset: str | None = Field(None, description="Encoding preset (e.g., 'medium')")
    threads: int | None = Field(
        None, ge=1, le=32, description="Number of encoding threads"
    )
    audio: bool | None = Field(None, description="Include audio in output")
    verbose: bool | None = Field(None, description="Verbose output during encoding")

    @model_validator(mode="after")
    def validate_bitrate_format(self) -> "VideoExportOptions":
        """Validate bitrate format if provided."""
        if self.bitrate and not self.bitrate.endswith(("k", "M")):
            raise ValueError("Bitrate must end with 'k' or 'M' (e.g., '5000k', '5M')")
        return self


@dataclass
class ExportResult:
    """Result of a video export operation."""

    success: bool
    output_path: str
    duration: float
    file_size: int | None = None
    error_message: str | None = None
