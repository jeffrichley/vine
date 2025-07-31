"""Context classes for fluent API styling in Project Vine."""

from dataclasses import dataclass
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Protocol,
    TypeVar,
    cast,
    runtime_checkable,
)

if TYPE_CHECKING:
    from vine.builder.timeline_builder import TimelineBuilder
from vine.models.animation_config import AnimationConfig
from vine.models.effects import BaseEffect
from vine.models.tracks import (
    AudioClip,
    BaseClip,
    ImageClip,
    TextClip,
)
from vine.models.transitions import BaseTransition


@dataclass
class AudioConfig:
    """Configuration for audio settings."""

    volume: float = 1.0
    fade_in: float = 0.0
    fade_out: float = 0.0
    crossfade_duration: float = 0.5
    auto_crossfade: bool = True
    normalize_audio: bool = False


# Type variables for generic return types
class HasClip(Protocol):
    """Protocol for classes that have a clip attribute."""

    clip: BaseClip


class HasBuilder(Protocol):
    """Protocol for classes that have a builder attribute."""

    builder: "TimelineBuilder"


class HasVisualClip(Protocol):
    """Protocol for clips that have visual properties."""

    x_position: float
    y_position: float
    opacity: float


class HasAudioClip(Protocol):
    """Protocol for clips that have audio properties."""

    volume: float
    fade_in: float
    fade_out: float
    crossfade_duration: float
    auto_crossfade: bool


@runtime_checkable
class HasAnimations(Protocol):
    """Protocol for clips that have animations."""

    animations: list[object]


T = TypeVar("T", bound=HasClip)
B = TypeVar("B", bound=HasBuilder)


class BuilderProtocol(Protocol):
    """Protocol that defines all builder methods that must be implemented."""

    def add_image(
        self, image_path: str | Path, duration: float | None = None
    ) -> "ImageContext":
        """Add image and return context for styling."""
        ...

    def add_image_at(
        self,
        image_path: str | Path,
        start_time: float,
        duration: float | None = None,
        end_time: float | None = None,
    ) -> "ImageContext":
        """Add image at specific time and return context for styling."""
        ...

    def add_text(self, text: str, duration: float | None = None) -> "TextContext":
        """Add text and return context for styling."""
        ...

    def add_text_at(
        self,
        text: str,
        start_time: float,
        duration: float | None = None,
        end_time: float | None = None,
    ) -> "TextContext":
        """Add text at specific time and return context for styling."""
        ...

    def add_voice(
        self, voice_path: str | Path, duration: float | None = None
    ) -> "VoiceContext":
        """Add voice and return context for styling."""
        ...

    def add_voice_at(
        self,
        voice_path: str | Path,
        start_time: float,
        duration: float | None = None,
        end_time: float | None = None,
    ) -> "VoiceContext":
        """Add voice at specific time and return context for styling."""
        ...

    def add_music(
        self, music_path: str | Path, duration: float | None = None
    ) -> "VoiceContext":
        """Add background music and return context for styling."""
        ...

    def add_music_at(
        self,
        music_path: str | Path,
        start_time: float,
        duration: float | None = None,
        end_time: float | None = None,
    ) -> "VoiceContext":
        """Add background music at specific time and return context for styling."""
        ...

    def add_sfx(
        self, sfx_path: str | Path, duration: float | None = None
    ) -> "SfxContext":
        """Add sound effect and return context for styling."""
        ...

    def add_sfx_at(
        self,
        sfx_path: str | Path,
        start_time: float,
        duration: float | None = None,
        end_time: float | None = None,
    ) -> "SfxContext":
        """Add sound effect at specific time and return context for styling."""
        ...


class BuilderMethodsMixin:
    """Mixin that provides all builder delegation methods with proper type annotations."""

    def add_image(
        self: B, image_path: str | Path, duration: float | None = None
    ) -> "ImageContext":
        """Add image and return context for styling."""
        return self.builder.add_image(image_path, duration)

    def add_image_at(
        self: B,
        image_path: str | Path,
        start_time: float,
        duration: float | None = None,
        end_time: float | None = None,
    ) -> "ImageContext":
        """Add image at specific time and return context for styling."""
        return self.builder.add_image_at(image_path, start_time, duration, end_time)

    def add_text(self: B, text: str, duration: float | None = None) -> "TextContext":
        """Add text and return context for styling."""
        return self.builder.add_text(text, duration)

    def add_text_at(
        self: B,
        text: str,
        start_time: float,
        duration: float | None = None,
        end_time: float | None = None,
    ) -> "TextContext":
        """Add text at specific time and return context for styling."""
        return self.builder.add_text_at(text, start_time, duration, end_time)

    def add_voice(
        self: B, voice_path: str | Path, duration: float | None = None
    ) -> "VoiceContext":
        """Add voice and return context for styling."""
        return self.builder.add_voice(voice_path, duration)

    def add_voice_at(
        self: B,
        voice_path: str | Path,
        start_time: float,
        duration: float | None = None,
        end_time: float | None = None,
    ) -> "VoiceContext":
        """Add voice at specific time and return context for styling."""
        return self.builder.add_voice_at(voice_path, start_time, duration, end_time)

    def add_music(
        self: B, music_path: str | Path, duration: float | None = None
    ) -> "VoiceContext":
        """Add background music and return context for styling."""
        return self.builder.add_music(music_path, duration)

    def add_music_at(
        self: B,
        music_path: str | Path,
        start_time: float,
        duration: float | None = None,
        end_time: float | None = None,
    ) -> "VoiceContext":
        """Add background music at specific time and return context for styling."""
        return self.builder.add_music_at(music_path, start_time, duration, end_time)

    def add_sfx(
        self: B, sfx_path: str | Path, duration: float | None = None
    ) -> "SfxContext":
        """Add sound effect and return context for styling."""
        return self.builder.add_sfx(sfx_path, duration)

    def add_sfx_at(
        self: B,
        sfx_path: str | Path,
        start_time: float,
        duration: float | None = None,
        end_time: float | None = None,
    ) -> "SfxContext":
        """Add sound effect at specific time and return context for styling."""
        return self.builder.add_sfx_at(sfx_path, start_time, duration, end_time)


class VisualStylingMixin:
    """Mixin for visual properties (position, opacity, effects, transitions)."""

    def with_position(self: T, x_position: float = 0.0, y_position: float = 0.0) -> T:
        """Set position on screen."""
        clip = cast(HasVisualClip, self.clip)
        clip.x_position = x_position
        clip.y_position = y_position
        return self

    def with_opacity(self: T, opacity: float = 1.0) -> T:
        """Set opacity (0-1)."""
        clip = cast(HasVisualClip, self.clip)
        clip.opacity = opacity
        return self

    def with_effect(self: T, effect: BaseEffect) -> T:
        """Apply an effect to this visual clip."""
        # Create animation config
        animation = AnimationConfig(
            effect=effect,
            start_time=self.clip.start_time,
            duration=self.clip.duration,
            easing="ease_in_out",
        )

        # Add animation to the clip
        if isinstance(self.clip, HasAnimations):
            self.clip.animations.append(animation)
        else:
            raise ValueError(
                f"Clip type {type(self.clip).__name__} does not support visual effects"
            )

        return self

    def with_transitions(
        self: T,
        transition_in: BaseTransition | None = None,
        transition_out: BaseTransition | None = None,
    ) -> T:
        """Apply transitions to this visual clip."""
        if transition_in is not None:
            self.clip.transition_in = transition_in

        if transition_out is not None:
            self.clip.transition_out = transition_out

        return self


class AudioStylingMixin:
    """Mixin for audio properties."""

    def with_volume(self: T, volume: float = 1.0) -> T:
        """Set volume level (0-2)."""
        clip = cast(HasAudioClip, self.clip)
        clip.volume = volume
        return self

    def with_fade(self: T, fade_in: float = 0.0, fade_out: float = 0.0) -> T:
        """Set fade in/out durations."""
        clip = cast(HasAudioClip, self.clip)
        clip.fade_in = fade_in
        clip.fade_out = fade_out
        return self

    def with_crossfade(
        self: T, crossfade_duration: float = 0.5, auto_crossfade: bool = True
    ) -> T:
        """Set crossfade settings."""
        clip = cast(HasAudioClip, self.clip)
        clip.crossfade_duration = crossfade_duration
        clip.auto_crossfade = auto_crossfade
        return self


class ImageContext(BuilderMethodsMixin, VisualStylingMixin):
    """Context for styling image clips."""

    def __init__(self, builder: "TimelineBuilder", clip: ImageClip) -> None:
        """Initialize the image context."""
        self.builder = builder
        self.clip = clip

    def with_styling(
        self, width: int | None = None, height: int | None = None
    ) -> "ImageContext":
        """Style the image clip with size."""
        if width is not None:
            self.clip.width = width
        if height is not None:
            self.clip.height = height
        return self


class TextContext(BuilderMethodsMixin, VisualStylingMixin):
    """Context for styling text clips."""

    def __init__(self, builder: "TimelineBuilder", clip: TextClip) -> None:
        """Initialize the text context."""
        self.builder = builder
        self.clip = clip

    def with_text_styling(
        self,
        font_size: int = 48,
        font_color: str = "#FFFFFF",
        font_family: str = "Arial",
        font_weight: str = "normal",
    ) -> "TextContext":
        """Style the text clip with font properties."""
        self.clip.font_size = font_size
        self.clip.font_color = font_color
        self.clip.font_family = font_family
        self.clip.font_weight = font_weight
        return self

    def with_alignment(self, alignment: str = "center") -> "TextContext":
        """Set text alignment."""
        self.clip.alignment = alignment
        return self


class VoiceContext(BuilderMethodsMixin, AudioStylingMixin):
    """Context for styling voice clips."""

    def __init__(self, builder: "TimelineBuilder", clip: AudioClip) -> None:
        """Initialize the voice context."""
        self.builder = builder
        self.clip = clip

    def with_audio_config(self, config: AudioConfig | None = None) -> "VoiceContext":
        """Configure the audio clip with all audio settings."""
        if config is None:
            config = AudioConfig()

        self.clip.volume = config.volume
        self.clip.fade_in = config.fade_in
        self.clip.fade_out = config.fade_out
        self.clip.crossfade_duration = config.crossfade_duration
        self.clip.auto_crossfade = config.auto_crossfade
        self.clip.normalize_audio = config.normalize_audio
        return self


class SfxContext(BuilderMethodsMixin, AudioStylingMixin):
    """Context for styling sound effect clips."""

    def __init__(self, builder: "TimelineBuilder", clip: AudioClip) -> None:
        """Initialize the sound effect context."""
        self.builder = builder
        self.clip = clip

    def with_audio_config(self, config: AudioConfig | None = None) -> "SfxContext":
        """Configure the audio clip with all audio settings."""
        if config is None:
            config = AudioConfig()

        self.clip.volume = config.volume
        self.clip.fade_in = config.fade_in
        self.clip.fade_out = config.fade_out
        self.clip.crossfade_duration = config.crossfade_duration
        self.clip.auto_crossfade = config.auto_crossfade
        self.clip.normalize_audio = config.normalize_audio
        return self


# Validation has been moved to vine.validation.protocol_validator
# to avoid circular import issues
