"""Tests for effect models."""

import pytest

from vine.models.effects import KenBurnsEffect, SlideEffect, StaticEffect
from vine.models.transition import TransitionDirection


class TestEffectConfigs:
    """Test effect configurations."""

    @pytest.mark.unit
    def test_ken_burns_config(self) -> None:
        """Test Ken Burns effect configuration."""
        ken_burns = KenBurnsEffect()
        assert ken_burns.type == "ken_burns"
        assert ken_burns.zoom_factor == 1.2
        assert ken_burns.pan_x == 0.0
        assert ken_burns.pan_y == 0.0

    @pytest.mark.unit
    def test_slide_config(self) -> None:
        """Test slide effect configuration."""
        slide = SlideEffect()
        assert slide.type == "slide"
        assert slide.direction == TransitionDirection.LEFT
        assert slide.distance == 100.0

    @pytest.mark.unit
    def test_static_config(self) -> None:
        """Test static effect configuration."""
        static = StaticEffect()
        assert static.type == "static"


class TestEffectTimeValidation:
    """Test effect time validation."""

    @pytest.mark.unit
    def test_effect_time_validation(self) -> None:
        """Test effect time validation with valid values."""
        # Test with valid values
        ken_burns = KenBurnsEffect(duration=2.0, start_time=1.0)
        assert ken_burns.duration == 2.0
        assert ken_burns.start_time == 1.0

    @pytest.mark.unit
    def test_effect_time_validation_none_values(self) -> None:
        """Test effect time validation with None values."""
        # Test that None values are allowed
        ken_burns = KenBurnsEffect(duration=None, start_time=None)
        assert ken_burns.duration is None
        assert ken_burns.start_time is None  # None is allowed

    @pytest.mark.unit
    def test_effect_time_validation_zero_values(self) -> None:
        """Test effect time validation with zero values."""
        # Test that zero values are allowed
        ken_burns = KenBurnsEffect(duration=0.0, start_time=0.0)
        assert ken_burns.duration == 0.0
        assert ken_burns.start_time == 0.0


class TestBaseEffectGetters:
    """Test BaseEffect getter methods."""

    @pytest.mark.unit
    def test_get_type_method(self) -> None:
        """Test get_type() method returns the correct type."""
        ken_burns = KenBurnsEffect()
        slide = SlideEffect()
        static = StaticEffect()
        assert ken_burns.get_type() == "ken_burns"
        assert slide.get_type() == "slide"
        assert static.get_type() == "static"

    @pytest.mark.unit
    def test_get_duration_method(self) -> None:
        """Test get_duration() method returns the correct duration."""
        # Test with None duration
        ken_burns_none = KenBurnsEffect(duration=None)
        assert ken_burns_none.get_duration() is None
        # Test with specific duration
        ken_burns_duration = KenBurnsEffect(duration=2.5)
        assert ken_burns_duration.get_duration() == 2.5
        # Test with zero duration
        ken_burns_zero = KenBurnsEffect(duration=0.0)
        assert ken_burns_zero.get_duration() == 0.0

    @pytest.mark.unit
    def test_get_start_time_method(self) -> None:
        """Test get_start_time() method returns the correct start time."""
        # Test with None start_time (should return 0.0)
        ken_burns_none = KenBurnsEffect(start_time=None)
        assert ken_burns_none.get_start_time() == 0.0
        # Test with specific start_time
        ken_burns_start = KenBurnsEffect(start_time=1.5)
        assert ken_burns_start.get_start_time() == 1.5
        # Test with zero start_time
        ken_burns_zero = KenBurnsEffect(start_time=0.0)
        assert ken_burns_zero.get_start_time() == 0.0


class TestEffectValidation:
    """Test effect validation rules."""

    @pytest.mark.unit
    def test_ken_burns_zoom_factor_validation(self) -> None:
        """Test Ken Burns zoom factor validation."""
        # Test valid zoom factors
        KenBurnsEffect(zoom_factor=1.0)  # Should work
        KenBurnsEffect(zoom_factor=2.0)  # Should work
        KenBurnsEffect(zoom_factor=1.5)  # Should work
        # Test invalid zoom factors
        with pytest.raises(
            ValueError, match="Input should be greater than or equal to 1"
        ):
            KenBurnsEffect(zoom_factor=0.0)
        with pytest.raises(
            ValueError, match="Input should be greater than or equal to 1"
        ):
            KenBurnsEffect(zoom_factor=-1.0)
        with pytest.raises(
            ValueError, match="Input should be greater than or equal to 1"
        ):
            KenBurnsEffect(zoom_factor=0.5)

    @pytest.mark.unit
    def test_ken_burns_pan_validation(self) -> None:
        """Test Ken Burns pan validation."""
        # Test valid pan values
        KenBurnsEffect(pan_x=-1.0, pan_y=-1.0)  # Should work
        KenBurnsEffect(pan_x=0.0, pan_y=0.0)  # Should work
        KenBurnsEffect(pan_x=1.0, pan_y=1.0)  # Should work
        # Test invalid pan values
        with pytest.raises(
            ValueError, match="Input should be greater than or equal to -1"
        ):
            KenBurnsEffect(pan_x=-1.1)
        with pytest.raises(ValueError, match="Input should be less than or equal to 1"):
            KenBurnsEffect(pan_x=1.1)
        with pytest.raises(
            ValueError, match="Input should be greater than or equal to -1"
        ):
            KenBurnsEffect(pan_y=-1.1)
        with pytest.raises(ValueError, match="Input should be less than or equal to 1"):
            KenBurnsEffect(pan_y=1.1)

    @pytest.mark.unit
    def test_slide_direction_validation(self) -> None:
        """Test slide direction validation."""
        # Test valid directions
        SlideEffect(direction=TransitionDirection.LEFT)  # Should work
        SlideEffect(direction=TransitionDirection.RIGHT)  # Should work
        SlideEffect(direction=TransitionDirection.UP)  # Should work
        SlideEffect(direction=TransitionDirection.DOWN)  # Should work
        # Test invalid direction - this should raise a ValueError from Pydantic
        with pytest.raises(ValueError):
            SlideEffect(direction="invalid")

    @pytest.mark.unit
    def test_slide_distance_validation(self) -> None:
        """Test slide distance validation."""
        # Test valid distances
        SlideEffect(distance=0.0)  # Should work
        SlideEffect(distance=100.0)  # Should work
        SlideEffect(distance=500.0)  # Should work
        # Test invalid distance
        with pytest.raises(
            ValueError, match="Input should be greater than or equal to 0"
        ):
            SlideEffect(distance=-1.0)
