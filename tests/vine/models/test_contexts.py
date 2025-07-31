"""Tests for vine.models.contexts module."""

from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from vine.models.contexts import (
    BuilderMethodsMixin,
    ImageContext,
    SfxContext,
    TextContext,
    VoiceContext,
)
from vine.models.effects import BaseEffect
from vine.models.tracks import AudioClip, ImageClip, TextClip
from vine.models.transitions import BaseTransition
from vine.validation.protocol_validator import validate_builder_implementation


class TestVisualStylingMixin:
    """Test VisualStylingMixin through concrete context classes."""

    @pytest.fixture
    def mock_builder(self) -> Any:
        """Create a mock TimelineBuilder."""
        return MagicMock()

    @pytest.fixture
    def mock_image_clip(self) -> Any:
        """Create a mock ImageClip with visual properties."""
        clip = MagicMock(spec=ImageClip)
        clip.x_position = 0.0
        clip.y_position = 0.0
        clip.opacity = 1.0
        clip.transition_in = None
        clip.transition_out = None
        return clip

    @pytest.fixture
    def image_context(self, mock_builder, mock_image_clip) -> Any:
        """Create an ImageContext for testing."""
        return ImageContext(mock_builder, mock_image_clip)

    def test_with_position_sets_coordinates(
        self, image_context, mock_image_clip
    ) -> None:
        """Test that with_position sets x and y coordinates correctly."""
        result = image_context.with_position(x_position=100.0, y_position=200.0)
        assert mock_image_clip.x_position == 100.0
        assert mock_image_clip.y_position == 200.0
        assert result is image_context  # Method chaining

    def test_with_position_uses_defaults(self, image_context, mock_image_clip) -> None:
        """Test that with_position uses default values when not specified."""
        image_context.with_position()
        assert mock_image_clip.x_position == 0.0
        assert mock_image_clip.y_position == 0.0

    def test_with_opacity_sets_opacity(self, image_context, mock_image_clip) -> None:
        """Test that with_opacity sets opacity correctly."""
        result = image_context.with_opacity(0.5)
        assert mock_image_clip.opacity == 0.5
        assert result is image_context  # Method chaining

    def test_with_opacity_uses_default(self, image_context, mock_image_clip) -> None:
        """Test that with_opacity uses default value when not specified."""
        image_context.with_opacity()
        assert mock_image_clip.opacity == 1.0

    def test_with_effect_adds_animation_to_supported_clip(
        self, image_context, mock_image_clip
    ) -> None:
        """Test that with_effect adds animation to clips that support it."""
        mock_effect = MagicMock(spec=BaseEffect)
        mock_image_clip.animations = []
        mock_image_clip.start_time = 0.0
        mock_image_clip.duration = 5.0
        with patch("vine.models.contexts.AnimationConfig") as mock_animation_config:
            mock_animation: MagicMock = MagicMock()
            mock_animation_config.return_value = mock_animation
            result = image_context.with_effect(mock_effect)
            mock_animation_config.assert_called_once_with(
                effect=mock_effect, start_time=0.0, duration=5.0, easing="ease_in_out"
            )
            assert mock_image_clip.animations == [mock_animation]
            assert result is image_context

    def test_with_effect_raises_on_unsupported_clip(
        self, image_context, mock_image_clip
    ) -> None:
        """Test that with_effect raises ValueError for unsupported clip types."""
        mock_effect = MagicMock(spec=BaseEffect)
        # Set up mock clip with required attributes but no animations
        mock_image_clip.start_time = 0.0
        mock_image_clip.duration = 5.0
        # Remove animations attribute to simulate unsupported clip
        delattr(mock_image_clip, "animations")
        with pytest.raises(ValueError, match="does not support visual effects"):
            image_context.with_effect(mock_effect)

    def test_with_transitions_sets_both_transitions(
        self, image_context, mock_image_clip
    ) -> None:
        """Test that with_transitions sets both transition_in and transition_out."""
        mock_transition_in = MagicMock(spec=BaseTransition)
        mock_transition_out = MagicMock(spec=BaseTransition)
        result = image_context.with_transitions(
            transition_in=mock_transition_in, transition_out=mock_transition_out
        )
        assert mock_image_clip.transition_in == mock_transition_in
        assert mock_image_clip.transition_out == mock_transition_out
        assert result is image_context

    def test_with_transitions_handles_none_values(
        self, image_context, mock_image_clip
    ) -> None:
        """Test that with_transitions handles None values correctly."""
        mock_transition_in = MagicMock(spec=BaseTransition)
        image_context.with_transitions(transition_in=mock_transition_in)
        assert mock_image_clip.transition_in == mock_transition_in
        assert mock_image_clip.transition_out is None


class TestAudioStylingMixin:
    """Test AudioStylingMixin through concrete context classes."""

    @pytest.fixture
    def mock_builder(self) -> Any:
        """Create a mock TimelineBuilder."""
        return MagicMock()

    @pytest.fixture
    def mock_audio_clip(self) -> Any:
        """Create a mock AudioClip with audio properties."""
        clip = MagicMock(spec=AudioClip)
        clip.volume = 1.0
        clip.fade_in = 0.0
        clip.fade_out = 0.0
        clip.crossfade_duration = 0.5
        clip.auto_crossfade = True
        return clip

    @pytest.fixture
    def voice_context(self, mock_builder, mock_audio_clip) -> Any:
        """Create a VoiceContext for testing."""
        return VoiceContext(mock_builder, mock_audio_clip)

    def test_with_volume_sets_volume(self, voice_context, mock_audio_clip) -> None:
        """Test that with_volume sets volume correctly."""
        result = voice_context.with_volume(0.8)
        assert mock_audio_clip.volume == 0.8
        assert result is voice_context  # Method chaining

    def test_with_volume_uses_default(self, voice_context, mock_audio_clip) -> None:
        """Test that with_volume uses default value when not specified."""
        voice_context.with_volume()
        assert mock_audio_clip.volume == 1.0

    def test_with_fade_sets_fade_durations(
        self, voice_context, mock_audio_clip
    ) -> None:
        """Test that with_fade sets fade_in and fade_out durations."""
        result = voice_context.with_fade(fade_in=1.0, fade_out=2.0)
        assert mock_audio_clip.fade_in == 1.0
        assert mock_audio_clip.fade_out == 2.0
        assert result is voice_context

    def test_with_fade_uses_defaults(self, voice_context, mock_audio_clip) -> None:
        """Test that with_fade uses default values when not specified."""
        voice_context.with_fade()
        assert mock_audio_clip.fade_in == 0.0
        assert mock_audio_clip.fade_out == 0.0

    def test_with_crossfade_sets_crossfade_settings(
        self, voice_context, mock_audio_clip
    ) -> None:
        """Test that with_crossfade sets crossfade duration and auto flag."""
        result = voice_context.with_crossfade(
            crossfade_duration=1.5, auto_crossfade=False
        )
        assert mock_audio_clip.crossfade_duration == 1.5
        assert mock_audio_clip.auto_crossfade is False
        assert result is voice_context

    def test_with_crossfade_uses_defaults(self, voice_context, mock_audio_clip) -> None:
        """Test that with_crossfade uses default values when not specified."""
        voice_context.with_crossfade()
        assert mock_audio_clip.crossfade_duration == 0.5
        assert mock_audio_clip.auto_crossfade is True


class TestBuilderMethodsMixin:
    """Test BuilderMethodsMixin through concrete context classes."""

    @pytest.fixture
    def mock_builder(self) -> Any:
        """Create a mock TimelineBuilder."""
        return MagicMock()

    @pytest.fixture
    def mock_clip(self) -> Any:
        """Create a mock clip."""
        return MagicMock()

    @pytest.fixture
    def context_with_mixin(self, mock_builder, mock_clip) -> Any:
        """Create a context class that uses BuilderMethodsMixin."""

        class TestContext(BuilderMethodsMixin):
            def __init__(self, builder, clip):
                self.builder = builder
                self.clip = clip

        return TestContext(mock_builder, mock_clip)

    def test_add_image_delegates_to_builder(
        self, context_with_mixin, mock_builder
    ) -> None:
        """Test that add_image delegates to the builder."""
        mock_context: MagicMock = MagicMock()
        mock_builder.add_image.return_value = mock_context
        result = context_with_mixin.add_image("test.jpg", 5.0)
        mock_builder.add_image.assert_called_once_with("test.jpg", 5.0)
        assert result is mock_context

    def test_add_image_at_delegates_to_builder(
        self, context_with_mixin, mock_builder
    ) -> None:
        """Test that add_image_at delegates to the builder."""
        mock_context: MagicMock = MagicMock()
        mock_builder.add_image_at.return_value = mock_context
        result = context_with_mixin.add_image_at("test.jpg", 2.0, 3.0, 5.0)
        mock_builder.add_image_at.assert_called_once_with("test.jpg", 2.0, 3.0, 5.0)
        assert result is mock_context

    def test_add_text_delegates_to_builder(
        self, context_with_mixin, mock_builder
    ) -> None:
        """Test that add_text delegates to the builder."""
        mock_context: MagicMock = MagicMock()
        mock_builder.add_text.return_value = mock_context
        result = context_with_mixin.add_text("Hello World", 3.0)
        mock_builder.add_text.assert_called_once_with("Hello World", 3.0)
        assert result is mock_context

    def test_add_text_at_delegates_to_builder(
        self, context_with_mixin, mock_builder
    ) -> None:
        """Test that add_text_at delegates to the builder."""
        mock_context: MagicMock = MagicMock()
        mock_builder.add_text_at.return_value = mock_context
        result = context_with_mixin.add_text_at("Hello World", 1.0, 2.0, 3.0)
        mock_builder.add_text_at.assert_called_once_with("Hello World", 1.0, 2.0, 3.0)
        assert result is mock_context

    def test_add_voice_delegates_to_builder(
        self, context_with_mixin, mock_builder
    ) -> None:
        """Test that add_voice delegates to the builder."""
        mock_context: MagicMock = MagicMock()
        mock_builder.add_voice.return_value = mock_context
        result = context_with_mixin.add_voice("voice.mp3", 4.0)
        mock_builder.add_voice.assert_called_once_with("voice.mp3", 4.0)
        assert result is mock_context

    def test_add_voice_at_delegates_to_builder(
        self, context_with_mixin, mock_builder
    ) -> None:
        """Test that add_voice_at delegates to the builder."""
        mock_context: MagicMock = MagicMock()
        mock_builder.add_voice_at.return_value = mock_context
        result = context_with_mixin.add_voice_at("voice.mp3", 0.5, 3.5, 4.0)
        mock_builder.add_voice_at.assert_called_once_with("voice.mp3", 0.5, 3.5, 4.0)
        assert result is mock_context

    def test_add_music_delegates_to_builder(
        self, context_with_mixin, mock_builder
    ) -> None:
        """Test that add_music delegates to the builder."""
        mock_context: MagicMock = MagicMock()
        mock_builder.add_music.return_value = mock_context
        result = context_with_mixin.add_music("music.mp3", 10.0)
        mock_builder.add_music.assert_called_once_with("music.mp3", 10.0)
        assert result is mock_context

    def test_add_music_at_delegates_to_builder(
        self, context_with_mixin, mock_builder
    ) -> None:
        """Test that add_music_at delegates to the builder."""
        mock_context: MagicMock = MagicMock()
        mock_builder.add_music_at.return_value = mock_context
        result = context_with_mixin.add_music_at("music.mp3", 0.0, 10.0, 10.0)
        mock_builder.add_music_at.assert_called_once_with("music.mp3", 0.0, 10.0, 10.0)
        assert result is mock_context

    def test_add_sfx_delegates_to_builder(
        self, context_with_mixin, mock_builder
    ) -> None:
        """Test that add_sfx delegates to the builder."""
        mock_context: MagicMock = MagicMock()
        mock_builder.add_sfx.return_value = mock_context
        result = context_with_mixin.add_sfx("sfx.wav", 1.0)
        mock_builder.add_sfx.assert_called_once_with("sfx.wav", 1.0)
        assert result is mock_context

    def test_add_sfx_at_delegates_to_builder(
        self, context_with_mixin, mock_builder
    ) -> None:
        """Test that add_sfx_at delegates to the builder."""
        mock_context: MagicMock = MagicMock()
        mock_builder.add_sfx_at.return_value = mock_context
        result = context_with_mixin.add_sfx_at("sfx.wav", 2.0, 0.5, 2.5)
        mock_builder.add_sfx_at.assert_called_once_with("sfx.wav", 2.0, 0.5, 2.5)
        assert result is mock_context


class TestImageContext:
    """Test ImageContext class."""

    @pytest.fixture
    def mock_builder(self) -> Any:
        """Create a mock TimelineBuilder."""
        return MagicMock()

    @pytest.fixture
    def mock_image_clip(self) -> Any:
        """Create a mock ImageClip."""
        clip = MagicMock(spec=ImageClip)
        clip.width = None
        clip.height = None
        return clip

    @pytest.fixture
    def image_context(self, mock_builder, mock_image_clip) -> Any:
        """Create an ImageContext for testing."""
        return ImageContext(mock_builder, mock_image_clip)

    def test_init_sets_builder_and_clip(self, mock_builder, mock_image_clip) -> None:
        """Test that __init__ sets builder and clip correctly."""
        context = ImageContext(mock_builder, mock_image_clip)
        assert context.builder is mock_builder
        assert context.clip is mock_image_clip

    def test_with_styling_sets_width_and_height(
        self, image_context, mock_image_clip
    ) -> None:
        """Test that with_styling sets width and height correctly."""
        result = image_context.with_styling(width=800, height=600)
        assert mock_image_clip.width == 800
        assert mock_image_clip.height == 600
        assert result is image_context

    def test_with_styling_handles_none_values(
        self, image_context, mock_image_clip
    ) -> None:
        """Test that with_styling handles None values correctly."""
        mock_image_clip.width = 100
        mock_image_clip.height = 100
        image_context.with_styling(width=None, height=None)
        assert mock_image_clip.width == 100  # Unchanged
        assert mock_image_clip.height == 100  # Unchanged

    def test_with_styling_sets_only_width(self, image_context, mock_image_clip) -> None:
        """Test that with_styling sets only width when height is None."""
        image_context.with_styling(width=800)
        assert mock_image_clip.width == 800
        assert mock_image_clip.height is None

    def test_with_styling_sets_only_height(
        self, image_context, mock_image_clip
    ) -> None:
        """Test that with_styling sets only height when width is None."""
        image_context.with_styling(height=600)
        assert mock_image_clip.width is None
        assert mock_image_clip.height == 600


class TestTextContext:
    """Test TextContext class."""

    @pytest.fixture
    def mock_builder(self) -> Any:
        """Create a mock TimelineBuilder."""
        return MagicMock()

    @pytest.fixture
    def mock_text_clip(self) -> Any:
        """Create a mock TextClip."""
        clip = MagicMock(spec=TextClip)
        clip.font_size = 48
        clip.font_color = "#FFFFFF"
        clip.font_family = "Arial"
        clip.font_weight = "normal"
        clip.alignment = "center"
        return clip

    @pytest.fixture
    def text_context(self, mock_builder, mock_text_clip) -> Any:
        """Create a TextContext for testing."""
        return TextContext(mock_builder, mock_text_clip)

    def test_init_sets_builder_and_clip(self, mock_builder, mock_text_clip) -> None:
        """Test that __init__ sets builder and clip correctly."""
        context = TextContext(mock_builder, mock_text_clip)
        assert context.builder is mock_builder
        assert context.clip is mock_text_clip

    def test_with_text_styling_sets_font_properties(
        self, text_context, mock_text_clip
    ) -> None:
        """Test that with_text_styling sets font properties correctly."""
        result = text_context.with_text_styling(
            font_size=24,
            font_color="#FF0000",
            font_family="Helvetica",
            font_weight="bold",
        )
        assert mock_text_clip.font_size == 24
        assert mock_text_clip.font_color == "#FF0000"
        assert mock_text_clip.font_family == "Helvetica"
        assert mock_text_clip.font_weight == "bold"
        assert result is text_context

    def test_with_text_styling_uses_defaults(
        self, text_context, mock_text_clip
    ) -> None:
        """Test that with_text_styling uses default values when not specified."""
        text_context.with_text_styling()
        assert mock_text_clip.font_size == 48
        assert mock_text_clip.font_color == "#FFFFFF"
        assert mock_text_clip.font_family == "Arial"
        assert mock_text_clip.font_weight == "normal"

    def test_with_alignment_sets_alignment(self, text_context, mock_text_clip) -> None:
        """Test that with_alignment sets text alignment correctly."""
        result = text_context.with_alignment("left")
        assert mock_text_clip.alignment == "left"
        assert result is text_context

    def test_with_alignment_uses_default(self, text_context, mock_text_clip) -> None:
        """Test that with_alignment uses default value when not specified."""
        text_context.with_alignment()
        assert mock_text_clip.alignment == "center"


class TestVoiceContext:
    """Test VoiceContext class."""

    @pytest.fixture
    def mock_builder(self) -> Any:
        """Create a mock TimelineBuilder."""
        return MagicMock()

    @pytest.fixture
    def mock_audio_clip(self) -> Any:
        """Create a mock AudioClip."""
        clip = MagicMock(spec=AudioClip)
        clip.volume = 1.0
        clip.fade_in = 0.0
        clip.fade_out = 0.0
        clip.crossfade_duration = 0.5
        clip.auto_crossfade = True
        clip.normalize_audio = False
        return clip

    @pytest.fixture
    def voice_context(self, mock_builder, mock_audio_clip) -> Any:
        """Create a VoiceContext for testing."""
        return VoiceContext(mock_builder, mock_audio_clip)

    def test_init_sets_builder_and_clip(self, mock_builder, mock_audio_clip) -> None:
        """Test that __init__ sets builder and clip correctly."""
        context = VoiceContext(mock_builder, mock_audio_clip)
        assert context.builder is mock_builder
        assert context.clip is mock_audio_clip

    def test_with_audio_config_sets_all_audio_properties(
        self, voice_context, mock_audio_clip
    ) -> None:
        """Test that with_audio_config sets all audio properties correctly."""
        from vine.models.contexts import AudioConfig

        audio_config = AudioConfig(
            volume=0.8,
            fade_in=1.0,
            fade_out=2.0,
            crossfade_duration=1.5,
            auto_crossfade=False,
            normalize_audio=True,
        )
        result = voice_context.with_audio_config(audio_config)
        assert mock_audio_clip.volume == 0.8
        assert mock_audio_clip.fade_in == 1.0
        assert mock_audio_clip.fade_out == 2.0
        assert mock_audio_clip.crossfade_duration == 1.5
        assert mock_audio_clip.auto_crossfade is False
        assert mock_audio_clip.normalize_audio is True
        assert result is voice_context

    def test_with_audio_config_uses_defaults(
        self, voice_context, mock_audio_clip
    ) -> None:
        """Test that with_audio_config uses default values when not specified."""
        voice_context.with_audio_config()
        assert mock_audio_clip.volume == 1.0
        assert mock_audio_clip.fade_in == 0.0
        assert mock_audio_clip.fade_out == 0.0
        assert mock_audio_clip.crossfade_duration == 0.5
        assert mock_audio_clip.auto_crossfade is True
        assert mock_audio_clip.normalize_audio is False


class TestSfxContext:
    """Test SfxContext class."""

    @pytest.fixture
    def mock_builder(self) -> Any:
        """Create a mock TimelineBuilder."""
        return MagicMock()

    @pytest.fixture
    def mock_audio_clip(self) -> Any:
        """Create a mock AudioClip."""
        clip = MagicMock(spec=AudioClip)
        clip.volume = 1.0
        clip.fade_in = 0.0
        clip.fade_out = 0.0
        clip.crossfade_duration = 0.5
        clip.auto_crossfade = True
        clip.normalize_audio = False
        return clip

    @pytest.fixture
    def sfx_context(self, mock_builder, mock_audio_clip) -> Any:
        """Create an SfxContext for testing."""
        return SfxContext(mock_builder, mock_audio_clip)

    def test_init_sets_builder_and_clip(self, mock_builder, mock_audio_clip) -> None:
        """Test that __init__ sets builder and clip correctly."""
        context = SfxContext(mock_builder, mock_audio_clip)
        assert context.builder is mock_builder
        assert context.clip is mock_audio_clip

    def test_with_audio_config_sets_all_audio_properties(
        self, sfx_context, mock_audio_clip
    ) -> None:
        """Test that with_audio_config sets all audio properties correctly."""
        from vine.models.contexts import AudioConfig

        audio_config = AudioConfig(
            volume=0.8,
            fade_in=1.0,
            fade_out=2.0,
            crossfade_duration=1.5,
            auto_crossfade=False,
            normalize_audio=True,
        )
        result = sfx_context.with_audio_config(audio_config)
        assert mock_audio_clip.volume == 0.8
        assert mock_audio_clip.fade_in == 1.0
        assert mock_audio_clip.fade_out == 2.0
        assert mock_audio_clip.crossfade_duration == 1.5
        assert mock_audio_clip.auto_crossfade is False
        assert mock_audio_clip.normalize_audio is True
        assert result is sfx_context

    def test_with_audio_config_uses_defaults(
        self, sfx_context, mock_audio_clip
    ) -> None:
        """Test that with_audio_config uses default values when not specified."""
        sfx_context.with_audio_config()
        assert mock_audio_clip.volume == 1.0
        assert mock_audio_clip.fade_in == 0.0
        assert mock_audio_clip.fade_out == 0.0
        assert mock_audio_clip.crossfade_duration == 0.5
        assert mock_audio_clip.auto_crossfade is True
        assert mock_audio_clip.normalize_audio is False


class TestValidationFunction:
    """Test the validate_builder_implementation function."""

    def test_validation_passes_when_all_methods_implemented(self) -> None:
        """Test that validation passes when all protocol methods are implemented."""
        # Use context manager to isolate the patch
        with patch(
            "vine.builder.timeline_builder.TimelineBuilder"
        ) as mock_timeline_builder:
            # Mock TimelineBuilder to have all required methods
            mock_timeline_builder.add_image = MagicMock()
            mock_timeline_builder.add_image_at = MagicMock()
            mock_timeline_builder.add_text = MagicMock()
            mock_timeline_builder.add_text_at = MagicMock()
            mock_timeline_builder.add_voice = MagicMock()
            mock_timeline_builder.add_voice_at = MagicMock()
            mock_timeline_builder.add_music = MagicMock()
            mock_timeline_builder.add_music_at = MagicMock()
            mock_timeline_builder.add_sfx = MagicMock()
            mock_timeline_builder.add_sfx_at = MagicMock()
            # Mock the inspect.getmembers to return our mocked methods
            with patch("inspect.getmembers") as mock_getmembers:
                mock_getmembers.return_value = [
                    ("add_image", mock_timeline_builder.add_image),
                    ("add_image_at", mock_timeline_builder.add_image_at),
                    ("add_text", mock_timeline_builder.add_text),
                    ("add_text_at", mock_timeline_builder.add_text_at),
                    ("add_voice", mock_timeline_builder.add_voice),
                    ("add_voice_at", mock_timeline_builder.add_voice_at),
                    ("add_music", mock_timeline_builder.add_music),
                    ("add_music_at", mock_timeline_builder.add_music_at),
                    ("add_sfx", mock_timeline_builder.add_sfx),
                    ("add_sfx_at", mock_timeline_builder.add_sfx_at),
                ]
                # This should not raise an exception
                validate_builder_implementation()

    def test_validation_fails_when_timeline_builder_methods_missing(self) -> None:
        """Test that validation fails when TimelineBuilder is missing required methods."""
        # Use context manager to isolate the patch
        with patch(
            "vine.builder.timeline_builder.TimelineBuilder"
        ) as mock_timeline_builder:
            # Mock TimelineBuilder to be missing some methods
            mock_timeline_builder.add_image = MagicMock()
            # Missing add_image_at, add_text, etc.
            with pytest.raises(
                RuntimeError, match="TimelineBuilder is missing protocol methods"
            ):
                validate_builder_implementation()

    def test_validation_fails_when_builder_methods_mixin_missing(self) -> None:
        """Test that validation fails when BuilderMethodsMixin is missing required methods."""

        # Create a mock BuilderMethodsMixin class that's missing methods
        class MockBuilderMethodsMixin:
            def add_image(self):
                pass

            # Missing other methods

        # Patch the actual BuilderMethodsMixin class temporarily
        with (
            patch("vine.models.contexts.BuilderMethodsMixin", MockBuilderMethodsMixin),
            pytest.raises(
                RuntimeError, match="BuilderMethodsMixin is missing protocol methods"
            ),
        ):
            validate_builder_implementation()


class TestMethodChaining:
    """Test method chaining behavior across all context classes."""

    @pytest.fixture
    def mock_builder(self) -> Any:
        """Create a mock TimelineBuilder."""
        return MagicMock()

    @pytest.fixture
    def mock_image_clip(self) -> Any:
        """Create a mock ImageClip."""
        clip = MagicMock(spec=ImageClip)
        clip.x_position = 0.0
        clip.y_position = 0.0
        clip.opacity = 1.0
        clip.width = None
        clip.height = None
        return clip

    def test_image_context_method_chaining(self, mock_builder, mock_image_clip) -> None:
        """Test that ImageContext methods support chaining."""
        context = ImageContext(mock_builder, mock_image_clip)
        result = (
            context.with_position(100, 200)
            .with_opacity(0.8)
            .with_styling(width=800, height=600)
        )
        assert result is context
        assert mock_image_clip.x_position == 100
        assert mock_image_clip.y_position == 200
        assert mock_image_clip.opacity == 0.8
        assert mock_image_clip.width == 800
        assert mock_image_clip.height == 600

    @pytest.fixture
    def mock_text_clip(self) -> Any:
        """Create a mock TextClip."""
        clip = MagicMock(spec=TextClip)
        clip.x_position = 0.0
        clip.y_position = 0.0
        clip.opacity = 1.0
        clip.font_size = 48
        clip.font_color = "#FFFFFF"
        clip.font_family = "Arial"
        clip.font_weight = "normal"
        clip.alignment = "center"
        return clip

    def test_text_context_method_chaining(self, mock_builder, mock_text_clip) -> None:
        """Test that TextContext methods support chaining."""
        context = TextContext(mock_builder, mock_text_clip)
        result = (
            context.with_position(50, 100)
            .with_opacity(0.9)
            .with_text_styling(font_size=24, font_color="#FF0000")
            .with_alignment("left")
        )
        assert result is context
        assert mock_text_clip.x_position == 50
        assert mock_text_clip.y_position == 100
        assert mock_text_clip.opacity == 0.9
        assert mock_text_clip.font_size == 24
        assert mock_text_clip.font_color == "#FF0000"
        assert mock_text_clip.alignment == "left"

    @pytest.fixture
    def mock_audio_clip(self) -> Any:
        """Create a mock AudioClip."""
        clip = MagicMock(spec=AudioClip)
        clip.volume = 1.0
        clip.fade_in = 0.0
        clip.fade_out = 0.0
        clip.crossfade_duration = 0.5
        clip.auto_crossfade = True
        clip.normalize_audio = False
        return clip

    def test_voice_context_method_chaining(self, mock_builder, mock_audio_clip) -> None:
        """Test that VoiceContext methods support chaining."""
        context = VoiceContext(mock_builder, mock_audio_clip)
        from vine.models.contexts import AudioConfig

        audio_config = AudioConfig(
            volume=0.8,
            fade_in=1.0,
            fade_out=2.0,
            crossfade_duration=1.5,
            auto_crossfade=False,
            normalize_audio=True,
        )
        result = (
            context.with_volume(0.8)
            .with_fade(fade_in=1.0, fade_out=2.0)
            .with_crossfade(crossfade_duration=1.5, auto_crossfade=False)
            .with_audio_config(audio_config)
        )
        # Verify method chaining works (each method returns self)
        assert result is context

    def test_sfx_context_method_chaining(self, mock_builder, mock_audio_clip) -> None:
        """Test that SfxContext methods support chaining."""
        context = SfxContext(mock_builder, mock_audio_clip)
        from vine.models.contexts import AudioConfig

        audio_config = AudioConfig(
            volume=0.6,
            fade_in=0.5,
            fade_out=1.0,
            crossfade_duration=0.3,
            auto_crossfade=True,
            normalize_audio=True,
        )
        result = (
            context.with_volume(0.6)
            .with_fade(fade_in=0.5, fade_out=1.0)
            .with_crossfade(crossfade_duration=0.3, auto_crossfade=True)
            .with_audio_config(audio_config)
        )
        # Verify method chaining works (each method returns self)
        assert result is context
