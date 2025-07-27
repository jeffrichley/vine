"""Unit tests for transition configurations."""

import pytest

from vine.models import CrossfadeConfig, FadeConfig, SlideTransitionConfig


class TestTransitionConfigs:
    """Test all transition configurations."""

    def test_fade_config(self):
        """Test fade configuration."""
        fade = FadeConfig()
        assert fade.type == "fade"
        assert fade.duration == 1.0
        assert fade.fade_type == "cross"
        assert fade.easing == "ease_in_out"

    def test_crossfade_config(self):
        """Test crossfade configuration."""
        crossfade = CrossfadeConfig()
        assert crossfade.type == "crossfade"
        assert crossfade.duration == 1.0
        assert crossfade.overlap == 0.5
        assert crossfade.easing == "ease_in_out"

    def test_slide_transition_config(self):
        """Test slide transition configuration."""
        slide_trans = SlideTransitionConfig()
        assert slide_trans.type == "slide"
        assert slide_trans.duration == 1.0
        assert slide_trans.direction == "left"
        assert slide_trans.distance == 100.0
        assert slide_trans.easing == "ease_in_out"

    def test_transition_duration_validation(self):
        """Test transition duration validation."""
        # Test duration too short
        with pytest.raises(
            ValueError, match="Input should be greater than or equal to 0.1"
        ):
            FadeConfig(duration=0.05)

        # Test duration too long
        with pytest.raises(
            ValueError, match="Input should be less than or equal to 10"
        ):
            FadeConfig(duration=15.0)
