"""Audio configuration models for Project Vine."""

from typing import Literal, Self

from pydantic import Field, model_validator

from vine.models.base import BaseModel


class AudioConfig(BaseModel):
    """Configuration for audio settings."""

    volume: float = Field(1.0, ge=0.0, le=2.0, description="Audio volume (0-2)")
    fade_in: float | None = Field(
        None, ge=0.0, description="Fade in duration in seconds"
    )
    fade_out: float | None = Field(
        None, ge=0.0, description="Fade out duration in seconds"
    )
    start_time: float | None = Field(
        None, ge=0.0, description="Start time offset in seconds"
    )
    end_time: float | None = Field(None, ge=0.0, description="End time in seconds")

    @model_validator(mode="after")
    def validate_timing(self) -> Self:
        """Validate timing relationships."""
        if (
            self.end_time is not None
            and self.start_time is not None
            and self.end_time <= self.start_time
        ):
            raise ValueError("End time must be after start time")
        return self


class VoiceConfig(AudioConfig):
    """Configuration for voice audio."""

    audio_type: Literal["voice"] = "voice"
    speed: float = Field(1.0, ge=0.5, le=2.0, description="Playback speed")
    pitch: float = Field(1.0, ge=0.5, le=2.0, description="Pitch adjustment")


class MusicConfig(AudioConfig):
    """Configuration for background music."""

    audio_type: Literal["music"] = "music"
    loop: bool = Field(False, description="Whether to loop the music")
    duck_voice: bool = Field(True, description="Whether to duck music during voice")
    duck_level: float = Field(0.3, ge=0.0, le=1.0, description="Ducking level (0-1)")
