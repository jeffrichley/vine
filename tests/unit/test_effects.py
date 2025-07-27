"""Unit tests for effect configurations."""

import pytest

from vine.models import KenBurnsConfig, SlideConfig, StaticConfig


class TestEffectConfigs:
    """Test all effect configurations."""

    def test_ken_burns_config(self):
        """Test Ken Burns configuration."""
        ken_burns = KenBurnsConfig()
        assert ken_burns.type == "ken_burns"
        assert ken_burns.zoom_factor == 1.2
        assert ken_burns.pan_x == 0.0
        assert ken_burns.pan_y == 0.0
        assert ken_burns.easing == "ease_in_out"

    def test_slide_config(self):
        """Test slide configuration."""
        slide = SlideConfig()
        assert slide.type == "slide"
        assert slide.direction == "left"
        assert slide.distance == 100.0
        assert slide.easing == "ease_in_out"

    def test_static_config(self):
        """Test static configuration."""
        static = StaticConfig()
        assert static.type == "static"

    def test_effect_time_validation(self):
        """Test effect time validation."""
        # Test negative duration
        with pytest.raises(
            ValueError, match="Input should be greater than or equal to 0"
        ):
            KenBurnsConfig(duration=-1.0)

        # Test negative start_time
        with pytest.raises(
            ValueError, match="Input should be greater than or equal to 0"
        ):
            KenBurnsConfig(start_time=-1.0)

    def test_effect_time_validation_none_values(self):
        """Test effect time validation with None values."""
        # Test that None values are allowed
        ken_burns = KenBurnsConfig(duration=None, start_time=None)
        assert ken_burns.duration is None
        assert ken_burns.start_time is None  # None is allowed

    def test_effect_time_validation_zero_values(self):
        """Test effect time validation with zero values."""
        # Test that zero values are allowed
        ken_burns = KenBurnsConfig(duration=0.0, start_time=0.0)
        assert ken_burns.duration == 0.0
        assert ken_burns.start_time == 0.0
