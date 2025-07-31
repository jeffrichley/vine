"""Unit tests for transition configurations."""

import pytest

from vine.models import CrossfadeTransition, FadeTransition, SlideTransition
from vine.models.transition import (
    Transition,
    TransitionDirection,
    TransitionEasing,
    TransitionType,
)


class TestTransitionConfigs:
    """Test all transition configurations."""

    def test_fade_config(self) -> None:
        """Test fade configuration."""
        fade = FadeTransition()
        assert fade.type == TransitionType.FADE
        assert fade.duration == 1.0
        assert fade.fade_type == TransitionDirection.IN
        assert fade.easing == TransitionEasing.EASE_IN_OUT

    def test_crossfade_config(self) -> None:
        """Test crossfade configuration."""
        crossfade = CrossfadeTransition()
        assert crossfade.type == TransitionType.CROSSFADE
        assert crossfade.duration == 1.0
        assert crossfade.overlap == 0.5
        assert crossfade.easing == TransitionEasing.EASE_IN_OUT

    def test_slide_transition_config(self) -> None:
        """Test slide transition configuration."""
        slide_trans = SlideTransition()
        assert slide_trans.type == TransitionType.SLIDE
        assert slide_trans.duration == 1.0
        assert slide_trans.direction == TransitionDirection.LEFT
        assert slide_trans.distance == 100.0
        assert slide_trans.easing == TransitionEasing.EASE_IN_OUT

    def test_transition_duration_validation(self) -> None:
        """Test transition duration validation."""
        # Test duration too short
        with pytest.raises(
            ValueError, match="Input should be greater than or equal to 0.1"
        ):
            FadeTransition(duration=0.05)
        # Test duration too long
        with pytest.raises(
            ValueError, match="Input should be less than or equal to 10"
        ):
            FadeTransition(duration=15.0)


class TestBaseTransitionGetters:
    """Test the getter methods in BaseTransition class."""

    def test_get_type_method(self) -> None:
        """Test get_type() method returns the correct type."""
        fade = FadeTransition()
        assert fade.get_type() == TransitionType.FADE
        crossfade = CrossfadeTransition()
        assert crossfade.get_type() == TransitionType.CROSSFADE
        slide = SlideTransition()
        assert slide.get_type() == TransitionType.SLIDE

    def test_get_duration_method(self) -> None:
        """Test get_duration() method returns the correct duration."""
        # Test default duration
        fade = FadeTransition()
        assert fade.get_duration() == 1.0
        # Test custom duration
        custom_fade = FadeTransition(duration=2.5)
        assert custom_fade.get_duration() == 2.5
        crossfade = CrossfadeTransition(duration=0.5)
        assert crossfade.get_duration() == 0.5

    def test_get_easing_method(self) -> None:
        """Test get_easing() method returns the correct easing."""
        # Test default easing
        fade = FadeTransition()
        assert fade.get_easing() == TransitionEasing.EASE_IN_OUT
        # Test custom easing
        custom_fade = FadeTransition(easing=TransitionEasing.EASE_IN)
        assert custom_fade.get_easing() == TransitionEasing.EASE_IN
        slide = SlideTransition(easing=TransitionEasing.EASE_OUT)
        assert slide.get_easing() == TransitionEasing.EASE_OUT

    def test_getter_methods_with_custom_values(self) -> None:
        """Test all getter methods with custom values."""
        custom_transition = FadeTransition(
            type=TransitionType.FADE, duration=3.0, easing=TransitionEasing.LINEAR
        )
        assert custom_transition.get_type() == TransitionType.FADE
        assert custom_transition.get_duration() == 3.0
        assert custom_transition.get_easing() == TransitionEasing.LINEAR

    def test_getter_methods_inheritance(self) -> None:
        """Test that getter methods work correctly with inheritance."""
        # Test FadeTransition
        fade = FadeTransition(fade_type=TransitionDirection.OUT)
        assert fade.get_type() == TransitionType.FADE
        assert fade.get_duration() == 1.0
        assert fade.get_easing() == TransitionEasing.EASE_IN_OUT
        # Test CrossfadeTransition
        crossfade = CrossfadeTransition(overlap=0.8)
        assert crossfade.get_type() == TransitionType.CROSSFADE
        assert crossfade.get_duration() == 1.0
        assert crossfade.get_easing() == TransitionEasing.EASE_IN_OUT
        # Test SlideTransition
        slide = SlideTransition(direction=TransitionDirection.RIGHT, distance=200.0)
        assert slide.get_type() == TransitionType.SLIDE
        assert slide.get_duration() == 1.0
        assert slide.get_easing() == TransitionEasing.EASE_IN_OUT


class TestTransitionProgress:
    """Test the Transition model's get_progress_at_time method."""

    def test_basic_progress_calculation(self) -> None:
        """Test basic progress calculation during transition."""
        transition = Transition(
            transition_type=TransitionType.FADE, start_time=5.0, duration=2.0
        )
        # Before transition starts
        assert transition.get_progress_at_time(4.0) == 0.0
        assert transition.get_progress_at_time(4.9) == 0.0
        # At transition start
        assert transition.get_progress_at_time(5.0) == 0.0
        # During transition
        assert transition.get_progress_at_time(5.5) == 0.25  # 0.5/2.0
        assert transition.get_progress_at_time(6.0) == 0.5  # 1.0/2.0
        assert transition.get_progress_at_time(6.5) == 0.75  # 1.5/2.0
        # At transition end
        assert transition.get_progress_at_time(7.0) == 1.0
        # After transition ends
        assert transition.get_progress_at_time(7.1) == 1.0
        assert transition.get_progress_at_time(10.0) == 1.0

    def test_zero_duration_transition(self) -> None:
        """Test transition with zero duration."""
        transition = Transition(
            transition_type=TransitionType.FADE, start_time=5.0, duration=0.0
        )
        # Before transition
        assert transition.get_progress_at_time(4.0) == 0.0
        # At transition time
        assert transition.get_progress_at_time(5.0) == 1.0
        # After transition
        assert transition.get_progress_at_time(6.0) == 1.0

    def test_instantaneous_transition(self) -> None:
        """Test transition with very small duration."""
        transition = Transition(
            transition_type=TransitionType.FADE, start_time=5.0, duration=0.001
        )
        # Before transition
        assert transition.get_progress_at_time(4.999) == 0.0
        # At transition start
        assert transition.get_progress_at_time(5.0) == 0.0
        # During transition (very brief)
        assert transition.get_progress_at_time(5.0005) == pytest.approx(0.5, rel=1e-10)
        # At transition end
        assert transition.get_progress_at_time(5.001) == 1.0
        # After transition
        assert transition.get_progress_at_time(5.002) == 1.0

    def test_long_duration_transition(self) -> None:
        """Test transition with long duration."""
        transition = Transition(
            transition_type=TransitionType.CROSSFADE, start_time=10.0, duration=30.0
        )
        # Before transition
        assert transition.get_progress_at_time(9.0) == 0.0
        # At transition start
        assert transition.get_progress_at_time(10.0) == 0.0
        # During transition
        assert transition.get_progress_at_time(15.0) == 0.16666666666666666  # 5/30
        assert transition.get_progress_at_time(20.0) == 0.3333333333333333  # 10/30
        assert transition.get_progress_at_time(25.0) == 0.5  # 15/30
        assert transition.get_progress_at_time(30.0) == 0.6666666666666666  # 20/30
        assert transition.get_progress_at_time(35.0) == 0.8333333333333334  # 25/30
        # At transition end
        assert transition.get_progress_at_time(40.0) == 1.0
        # After transition
        assert transition.get_progress_at_time(50.0) == 1.0

    def test_transition_at_zero_time(self) -> None:
        """Test transition starting at time zero."""
        transition = Transition(
            transition_type=TransitionType.SLIDE, start_time=0.0, duration=1.0
        )
        # At transition start
        assert transition.get_progress_at_time(0.0) == 0.0
        # During transition
        assert transition.get_progress_at_time(0.25) == 0.25
        assert transition.get_progress_at_time(0.5) == 0.5
        assert transition.get_progress_at_time(0.75) == 0.75
        # At transition end
        assert transition.get_progress_at_time(1.0) == 1.0
        # After transition
        assert transition.get_progress_at_time(2.0) == 1.0

    def test_negative_time_handling(self) -> None:
        """Test handling of negative time values."""
        transition = Transition(
            transition_type=TransitionType.WIPE, start_time=5.0, duration=2.0
        )
        # Negative times should return 0.0
        assert transition.get_progress_at_time(-1.0) == 0.0
        assert transition.get_progress_at_time(-10.0) == 0.0
        assert transition.get_progress_at_time(-0.1) == 0.0

    def test_floating_point_precision(self) -> None:
        """Test floating point precision in progress calculation."""
        transition = Transition(
            transition_type=TransitionType.DISSOLVE, start_time=1.0, duration=1.0
        )
        # Test with floating point precision
        assert transition.get_progress_at_time(1.0) == 0.0
        assert transition.get_progress_at_time(1.1) == pytest.approx(0.1, rel=1e-10)
        assert transition.get_progress_at_time(1.5) == 0.5
        assert transition.get_progress_at_time(1.9) == pytest.approx(0.9, rel=1e-10)
        assert transition.get_progress_at_time(2.0) == 1.0

    def test_edge_case_timing(self) -> None:
        """Test edge cases around transition timing."""
        transition = Transition(
            transition_type=TransitionType.FADE, start_time=10.0, duration=5.0
        )
        # Just before transition
        assert transition.get_progress_at_time(9.999999) == 0.0
        # Exactly at start
        assert transition.get_progress_at_time(10.0) == 0.0
        # Just after start
        assert transition.get_progress_at_time(10.000001) == pytest.approx(
            0.0000002, rel=1e-10
        )
        # Just before end
        assert transition.get_progress_at_time(14.999999) == pytest.approx(
            0.9999998, rel=1e-10
        )
        # Exactly at end
        assert transition.get_progress_at_time(15.0) == 1.0
        # Just after end
        assert transition.get_progress_at_time(15.000001) == 1.0

    def test_multiple_transitions_same_time(self) -> None:
        """Test multiple transitions with different configurations."""
        transition1 = Transition(
            transition_type=TransitionType.FADE, start_time=0.0, duration=1.0
        )
        transition2 = Transition(
            transition_type=TransitionType.CROSSFADE, start_time=5.0, duration=2.0
        )
        transition3 = Transition(
            transition_type=TransitionType.SLIDE, start_time=10.0, duration=0.5
        )
        # Test transition1
        assert transition1.get_progress_at_time(0.5) == 0.5
        assert transition1.get_progress_at_time(1.0) == 1.0
        assert transition1.get_progress_at_time(2.0) == 1.0
        # Test transition2
        assert transition2.get_progress_at_time(4.0) == 0.0
        assert transition2.get_progress_at_time(6.0) == 0.5
        assert transition2.get_progress_at_time(7.0) == 1.0
        assert transition2.get_progress_at_time(8.0) == 1.0
        # Test transition3
        assert transition3.get_progress_at_time(9.0) == 0.0
        assert transition3.get_progress_at_time(10.25) == 0.5
        assert transition3.get_progress_at_time(10.5) == 1.0
        assert transition3.get_progress_at_time(11.0) == 1.0

    def test_transition_with_metadata(self) -> None:
        """Test that metadata doesn't affect progress calculation."""
        transition = Transition(
            transition_type=TransitionType.FADE,
            start_time=5.0,
            duration=2.0,
            metadata={"custom_param": "value", "intensity": 0.8},
        )
        # Progress calculation should be identical regardless of metadata
        assert transition.get_progress_at_time(4.0) == 0.0
        assert transition.get_progress_at_time(6.0) == 0.5
        assert transition.get_progress_at_time(7.0) == 1.0

    def test_transition_with_track_targeting(self) -> None:
        """Test that track targeting doesn't affect progress calculation."""
        transition = Transition(
            transition_type=TransitionType.CROSSFADE,
            start_time=3.0,
            duration=1.5,
            from_tracks=["track1", "track2"],
            to_tracks=["track3", "track4"],
        )
        # Progress calculation should be identical regardless of track targeting
        assert transition.get_progress_at_time(2.0) == 0.0
        assert transition.get_progress_at_time(3.75) == 0.5
        assert transition.get_progress_at_time(4.5) == 1.0

    def test_all_transition_types(self) -> None:
        """Test progress calculation for all transition types."""
        transition_types = [
            TransitionType.FADE,
            TransitionType.CROSSFADE,
            TransitionType.SLIDE,
            TransitionType.WIPE,
            TransitionType.DISSOLVE,
        ]
        for transition_type in transition_types:
            transition = Transition(
                transition_type=transition_type, start_time=10.0, duration=2.0
            )
            # All transition types should have identical progress calculation
            assert transition.get_progress_at_time(9.0) == 0.0
            assert transition.get_progress_at_time(11.0) == 0.5
            assert transition.get_progress_at_time(12.0) == 1.0
