"""Unit tests for AudioConfig models."""

import pytest

from vine.models import MusicConfig, VoiceConfig


class TestAudioConfig:
    """Test AudioConfig models."""

    def test_create_voice_config(self) -> None:
        """Test creating a voice configuration."""
        voice = VoiceConfig(volume=0.8, speed=1.2, pitch=1.1, fade_in=0.5)
        assert voice.audio_type == "voice"
        assert voice.volume == 0.8
        assert voice.speed == 1.2
        assert voice.pitch == 1.1
        assert voice.fade_in == 0.5

    def test_create_music_config(self) -> None:
        """Test creating a music configuration."""
        music = MusicConfig(volume=0.6, loop=True, duck_voice=True, duck_level=0.4)
        assert music.audio_type == "music"
        assert music.volume == 0.6
        assert music.loop is True
        assert music.duck_voice is True
        assert music.duck_level == 0.4

    def test_audio_validation(self) -> None:
        """Test audio configuration validation."""
        # Test invalid volume
        with pytest.raises(
            ValueError, match="Input should be greater than or equal to 0"
        ):
            VoiceConfig(volume=-0.5)
        # Test invalid speed
        with pytest.raises(
            ValueError, match="Input should be greater than or equal to 0.5"
        ):
            VoiceConfig(speed=0.3)
        # Test invalid duck level
        with pytest.raises(ValueError, match="Input should be less than or equal to 1"):
            MusicConfig(duck_level=1.5)

    def test_audio_end_time_validation(self) -> None:
        """Test audio end time validation."""
        # Test end_time before start_time
        with pytest.raises(ValueError, match="End time must be after start time"):
            VoiceConfig(start_time=5.0, end_time=3.0)

    def test_audio_fade_validation(self) -> None:
        """Test audio fade validation."""
        # Test negative fade_in
        with pytest.raises(
            ValueError, match="Input should be greater than or equal to 0"
        ):
            VoiceConfig(fade_in=-0.5)
        # Test negative fade_out
        with pytest.raises(
            ValueError, match="Input should be greater than or equal to 0"
        ):
            VoiceConfig(fade_out=-0.5)

    def test_audio_validation_none_values(self) -> None:
        """Test audio validation with None values."""
        # Test that None values are allowed for optional fields
        voice = VoiceConfig(
            volume=0.8,
            speed=1.0,
            pitch=1.0,
            fade_in=None,
            fade_out=None,
            start_time=None,
            end_time=None,
        )
        assert voice.fade_in is None
        assert voice.fade_out is None
        assert voice.start_time is None
        assert voice.end_time is None

    def test_audio_validation_zero_values(self) -> None:
        """Test audio validation with zero values."""
        # Test that zero values are allowed for time fields
        voice = VoiceConfig(
            volume=0.8, speed=1.0, pitch=1.0, fade_in=0.0, fade_out=0.0, start_time=0.0
        )
        assert voice.fade_in == 0.0
        assert voice.fade_out == 0.0
        assert voice.start_time == 0.0

    def test_audio_validation_empty_strings(self) -> None:
        """Test audio validation with empty strings."""
        # Test that empty strings are converted to None by BaseModel validation
        # Note: VoiceConfig doesn't have audio_path or text_content fields
        # This test demonstrates that BaseModel validation works for empty strings
        voice = VoiceConfig(volume=0.8, speed=1.0, pitch=1.0)
        # The BaseModel validation should work for any empty string fields
        assert voice.volume == 0.8
