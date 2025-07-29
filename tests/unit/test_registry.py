"""Tests for registry system components."""

from typing import Any

import pytest

from vine.models.effects import KenBurnsConfig, SlideConfig, StaticConfig
from vine.models.transition import Transition
from vine.registry import AnimationRegistry, EffectRegistry, TransitionRegistry
from vine.registry.base_registry import BaseRegistry


class ConcreteRegistry(BaseRegistry):
    """Concrete implementation for testing BaseRegistry."""

    def get_default(self) -> str:
        return "default"


class TestBaseRegistry:
    """Test BaseRegistry functionality."""

    def test_init(self) -> None:
        """Test BaseRegistry initialization."""
        registry = ConcreteRegistry()

        assert registry._components == {}
        assert registry._validators == {}

    def test_register_basic(self) -> None:
        """Test basic component registration."""
        registry = ConcreteRegistry()

        component = {"name": "test", "value": 42}
        registry.register("test_component", component)

        assert "test_component" in registry._components
        assert registry._components["test_component"] == component

    def test_register_with_validator(self) -> None:
        """Test component registration with validator."""
        registry = ConcreteRegistry()

        def validator(comp: Any) -> None:
            if not isinstance(comp, dict):
                raise ValueError("Component must be a dict")

        component = {"name": "test", "value": 42}
        registry.register("test_component", component, validator)

        assert "test_component" in registry._components
        assert "test_component" in registry._validators

    def test_register_duplicate(self) -> None:
        """Test that registering duplicate name raises error."""
        registry = ConcreteRegistry()

        registry.register("test", {"value": 1})

        with pytest.raises(ValueError, match="already registered"):
            registry.register("test", {"value": 2})

    def test_register_invalid_component(self) -> None:
        """Test that invalid component raises error with validator."""
        registry = ConcreteRegistry()

        def validator(comp: Any) -> None:
            if not isinstance(comp, dict):
                raise ValueError("Component must be a dict")

        with pytest.raises(ValueError, match="Component must be a dict"):
            registry.register("test", "not_a_dict", validator)

    def test_get_existing(self) -> None:
        """Test getting existing component."""
        registry = ConcreteRegistry()
        component = {"name": "test", "value": 42}

        registry.register("test_component", component)
        retrieved = registry.get("test_component")

        assert retrieved == component

    def test_get_nonexistent(self) -> None:
        """Test that getting nonexistent component raises error."""
        registry = ConcreteRegistry()

        with pytest.raises(KeyError, match="not found"):
            registry.get("nonexistent")

    def test_list(self) -> None:
        """Test listing registered components."""
        registry = ConcreteRegistry()

        registry.register("comp1", {"value": 1})
        registry.register("comp2", {"value": 2})

        components = registry.list()

        assert "comp1" in components
        assert "comp2" in components
        assert len(components) == 2

    def test_exists(self) -> None:
        """Test checking if component exists."""
        registry = ConcreteRegistry()

        assert not registry.exists("test")

        registry.register("test", {"value": 1})
        assert registry.exists("test")

    def test_unregister_existing(self) -> None:
        """Test unregistering existing component."""
        registry = ConcreteRegistry()

        registry.register("test", {"value": 1})
        assert registry.exists("test")

        registry.unregister("test")
        assert not registry.exists("test")

    def test_unregister_with_validator(self) -> None:
        """Test unregistering component with validator."""
        registry = ConcreteRegistry()

        def validator(comp: Any) -> None:
            if not isinstance(comp, dict):
                raise ValueError("Component must be a dict")

        # Register component with validator
        registry.register("test", {"value": 1}, validator)
        assert registry.exists("test")
        assert "test" in registry._validators

        # Unregister should remove both component and validator
        registry.unregister("test")
        assert not registry.exists("test")
        assert "test" not in registry._validators

    def test_unregister_without_validator(self) -> None:
        """Test unregistering component without validator."""
        registry = ConcreteRegistry()

        # Register component without validator
        registry.register("test", {"value": 1})
        assert registry.exists("test")
        assert "test" not in registry._validators

        # Unregister should work fine
        registry.unregister("test")
        assert not registry.exists("test")
        assert "test" not in registry._validators

    def test_unregister_nonexistent(self) -> None:
        """Test that unregistering nonexistent component raises error."""
        registry = ConcreteRegistry()

        with pytest.raises(KeyError, match="not found"):
            registry.unregister("nonexistent")

    def test_clear(self) -> None:
        """Test clearing all components."""
        registry = ConcreteRegistry()

        registry.register("comp1", {"value": 1})
        registry.register("comp2", {"value": 2})

        assert registry.count() == 2

        registry.clear()

        assert registry.count() == 0
        assert len(registry._validators) == 0

    def test_count(self) -> None:
        """Test counting registered components."""
        registry = ConcreteRegistry()

        assert registry.count() == 0

        registry.register("comp1", {"value": 1})
        assert registry.count() == 1

        registry.register("comp2", {"value": 2})
        assert registry.count() == 2


class TestAnimationRegistry:
    """Test AnimationRegistry functionality."""

    def test_init(self) -> None:
        """Test AnimationRegistry initialization."""
        registry = AnimationRegistry()

        assert registry.count() > 0  # Should have default animations

    def test_default_animations(self) -> None:
        """Test that default animations are registered."""
        registry = AnimationRegistry()

        # Check for expected default animations
        assert registry.exists("ken_burns_zoom_in")
        assert registry.exists("ken_burns_zoom_out")
        assert registry.exists("ken_burns_pan_left")
        assert registry.exists("ken_burns_pan_right")
        assert registry.exists("slide_in_left")
        assert registry.exists("slide_in_right")
        assert registry.exists("slide_in_up")
        assert registry.exists("slide_in_down")
        assert registry.exists("static")

    def test_get_default(self) -> None:
        """Test getting default animation name."""
        registry = AnimationRegistry()

        default = registry.get_default()
        assert default == "static"

    def test_create_animation_ken_burns(self) -> None:
        """Test creating Ken Burns animation from registry."""
        registry = AnimationRegistry()

        animation = registry.create_animation("ken_burns_zoom_in", duration=3.0)

        assert isinstance(animation, KenBurnsConfig)
        assert animation.duration == 3.0
        assert animation.zoom_factor == 1.2

    def test_create_animation_slide(self) -> None:
        """Test creating slide animation from registry."""
        registry = AnimationRegistry()

        animation = registry.create_animation("slide_in_left", duration=2.0)

        assert isinstance(animation, SlideConfig)
        assert animation.duration == 2.0
        assert animation.direction == "left"
        assert animation.distance == 100

    def test_create_animation_static(self) -> None:
        """Test creating static animation from registry."""
        registry = AnimationRegistry()

        animation = registry.create_animation("static")

        assert isinstance(animation, StaticConfig)

    def test_create_animation_nonexistent(self) -> None:
        """Test that creating nonexistent animation raises error."""
        registry = AnimationRegistry()

        with pytest.raises(KeyError, match="not found"):
            registry.create_animation("nonexistent")

    def test_create_animation_with_overrides(self) -> None:
        """Test creating animation with parameter overrides."""
        registry = AnimationRegistry()

        animation = registry.create_animation(
            "ken_burns_zoom_in", duration=5.0, zoom_factor=1.5, pan_x=0.1, pan_y=-0.05
        )

        assert animation.duration == 5.0
        assert isinstance(animation, KenBurnsConfig)
        assert animation.zoom_factor == 1.5
        assert animation.pan_x == 0.1
        assert animation.pan_y == -0.05

    def test_create_animation_unknown_type(self) -> None:
        """Test that creating animation from unknown type raises ValueError."""
        registry = AnimationRegistry()

        # Create a mock object that has model_dump() but isn't a known animation type
        class MockAnimationConfig:
            def model_dump(self) -> dict:
                return {"type": "mock", "duration": 1.0}

        # Register the mock object to trigger the unknown type error
        registry.register("unknown_animation", MockAnimationConfig())

        with pytest.raises(ValueError, match="Unknown animation type"):
            registry.create_animation("unknown_animation")


class TestTransitionRegistry:
    """Test TransitionRegistry functionality."""

    def test_init(self) -> None:
        """Test TransitionRegistry initialization."""
        registry = TransitionRegistry()

        assert registry.count() > 0  # Should have default transitions

    def test_default_transitions(self) -> None:
        """Test that default transitions are registered."""
        registry = TransitionRegistry()

        # Check for expected default transitions
        assert registry.exists("fade_in")
        assert registry.exists("fade_out")
        assert registry.exists("fade_in_out")
        assert registry.exists("crossfade")
        assert registry.exists("crossfade_fast")
        assert registry.exists("crossfade_slow")
        assert registry.exists("slide_left")
        assert registry.exists("slide_right")
        assert registry.exists("slide_up")
        assert registry.exists("slide_down")

    def test_get_default(self) -> None:
        """Test getting default transition name."""
        registry = TransitionRegistry()

        default = registry.get_default()
        assert default == "crossfade"

    def test_create_transition_fade(self) -> None:
        """Test creating fade transition from registry."""
        registry = TransitionRegistry()

        transition = registry.create_transition(
            "fade_in",
            start_time=5.0,
            duration=2.0,
            from_tracks=["video_0"],
            to_tracks=["video_1"],
        )

        assert isinstance(transition, Transition)
        assert transition.transition_type == "fade"
        assert transition.duration == 2.0
        assert transition.start_time == 5.0
        assert transition.from_tracks == ["video_0"]
        assert transition.to_tracks == ["video_1"]
        assert transition.direction == "in"

    def test_create_transition_crossfade(self) -> None:
        """Test creating crossfade transition from registry."""
        registry = TransitionRegistry()

        transition = registry.create_transition(
            "crossfade",
            start_time=10.0,
            duration=1.5,
            from_tracks=["video_0"],
            to_tracks=["video_1"],
        )

        assert isinstance(transition, Transition)
        assert transition.transition_type == "crossfade"
        assert transition.duration == 1.5
        assert transition.start_time == 10.0
        assert transition.from_tracks == ["video_0"]
        assert transition.to_tracks == ["video_1"]

    def test_create_transition_slide(self) -> None:
        """Test creating slide transition from registry."""
        registry = TransitionRegistry()

        transition = registry.create_transition(
            "slide_left",
            start_time=15.0,
            duration=1.0,
            from_tracks=["video_0"],
            to_tracks=["video_1"],
        )

        assert isinstance(transition, Transition)
        assert transition.transition_type == "slide"
        assert transition.duration == 1.0
        assert transition.start_time == 15.0
        assert transition.from_tracks == ["video_0"]
        assert transition.to_tracks == ["video_1"]
        assert transition.direction == "left"

    def test_create_transition_nonexistent(self) -> None:
        """Test that creating nonexistent transition raises error."""
        registry = TransitionRegistry()

        with pytest.raises(KeyError, match="not found"):
            registry.create_transition("nonexistent", start_time=0.0, duration=1.0)

    def test_create_transition_with_kwargs_overrides(self) -> None:
        """Test that kwargs properly override template values."""
        registry = TransitionRegistry()

        # Test overriding various fields via kwargs
        transition = registry.create_transition(
            "fade_in",
            start_time=5.0,
            duration=2.0,
            direction="out",  # Override default "in"
            easing="ease_in",  # Override default "ease_in_out"
            from_tracks=["track1", "track2"],
            to_tracks=["track3"],
            metadata={"custom": "data"},
        )

        assert transition.transition_type == "fade"
        assert transition.start_time == 5.0
        assert transition.duration == 2.0
        assert transition.direction == "out"  # Overridden
        assert transition.easing == "ease_in"  # Overridden
        assert transition.from_tracks == ["track1", "track2"]
        assert transition.to_tracks == ["track3"]
        assert transition.metadata == {"custom": "data"}

    def test_create_transition_with_invalid_kwargs(self) -> None:
        """Test that invalid kwargs are ignored (not in template_data)."""
        registry = TransitionRegistry()

        # Add an invalid kwarg that doesn't exist in Transition model
        transition = registry.create_transition(
            "crossfade",
            start_time=1.0,
            invalid_field="should_be_ignored",
            another_invalid="also_ignored",
        )

        # Should still create valid transition
        assert isinstance(transition, Transition)
        assert transition.transition_type == "crossfade"
        assert transition.start_time == 1.0

        # Invalid fields should not be present
        assert not hasattr(transition, "invalid_field")
        assert not hasattr(transition, "another_invalid")

    def test_create_transition_with_partial_kwargs(self) -> None:
        """Test creating transition with only some kwargs overrides."""
        registry = TransitionRegistry()

        # Only override direction, keep other defaults
        transition = registry.create_transition(
            "slide_left", start_time=3.0, direction="right"  # Override default "left"
        )

        assert transition.transition_type == "slide"
        assert transition.start_time == 3.0
        assert transition.duration == 1.0  # Default from template
        assert transition.direction == "right"  # Overridden
        assert transition.easing == "ease_in_out"  # Default from template

    def test_create_transition_with_all_kwargs(self) -> None:
        """Test creating transition with all possible kwargs overrides."""
        registry = TransitionRegistry()

        transition = registry.create_transition(
            "fade_out",
            start_time=10.0,
            duration=3.0,
            from_tracks=["source1", "source2"],
            to_tracks=["target1"],
            direction="in",  # Override default "out"
            easing="linear",  # Override default "ease_in_out"
            metadata={"test": True, "priority": "high"},
        )

        assert transition.transition_type == "fade"
        assert transition.start_time == 10.0
        assert transition.duration == 3.0
        assert transition.from_tracks == ["source1", "source2"]
        assert transition.to_tracks == ["target1"]
        assert transition.direction == "in"
        assert transition.easing == "linear"
        assert transition.metadata == {"test": True, "priority": "high"}

    def test_create_transition_with_empty_kwargs(self) -> None:
        """Test creating transition with empty kwargs dict."""
        registry = TransitionRegistry()

        transition = registry.create_transition(
            "crossfade_fast", start_time=2.0, **{}  # Empty kwargs
        )

        assert isinstance(transition, Transition)
        assert transition.transition_type == "crossfade"
        assert transition.start_time == 2.0
        assert transition.duration == 0.5  # Default from template
        assert transition.easing == "ease_in_out"  # Default from template

    def test_create_transition_kwargs_edge_cases(self) -> None:
        """Test edge cases for kwargs handling."""
        registry = TransitionRegistry()

        # Test with different valid values in kwargs
        transition = registry.create_transition(
            "slide_up",
            start_time=1.0,
            direction="down",  # Override default "up"
            easing="linear",  # Override default "ease_in_out"
        )

        assert transition.direction == "down"
        assert transition.easing == "linear"

        # Test with empty lists/strings
        transition2 = registry.create_transition(
            "fade_in",
            start_time=1.0,
            from_tracks=[],  # Empty list
            to_tracks=[],  # Empty list
            metadata={},  # Empty dict
        )

        assert transition2.from_tracks == []
        assert transition2.to_tracks == []
        assert transition2.metadata == {}


class TestEffectRegistry:
    """Test EffectRegistry functionality."""

    def test_init(self) -> None:
        """Test EffectRegistry initialization."""
        registry = EffectRegistry()

        assert registry.count() > 0  # Should have default effects

    def test_default_effects(self) -> None:
        """Test that default effects are registered."""
        registry = EffectRegistry()

        # Check for expected default effects
        assert registry.exists("ken_burns_zoom_in")
        assert registry.exists("ken_burns_zoom_out")
        assert registry.exists("ken_burns_pan_left")
        assert registry.exists("ken_burns_pan_right")
        assert registry.exists("slide_in_left")
        assert registry.exists("slide_in_right")
        assert registry.exists("slide_in_up")
        assert registry.exists("slide_in_down")
        assert registry.exists("static")

    def test_get_default(self) -> None:
        """Test getting default effect name."""
        registry = EffectRegistry()

        default = registry.get_default()
        assert default == "static"

    def test_create_effect_ken_burns(self) -> None:
        """Test creating Ken Burns effect from registry."""
        registry = EffectRegistry()

        effect = registry.create_effect("ken_burns_zoom_in", duration=3.0)

        assert isinstance(effect, KenBurnsConfig)
        assert effect.duration == 3.0
        assert effect.zoom_factor == 1.2

    def test_create_effect_slide(self) -> None:
        """Test creating slide effect from registry."""
        registry = EffectRegistry()

        effect = registry.create_effect("slide_in_left", duration=2.0)

        assert isinstance(effect, SlideConfig)
        assert effect.duration == 2.0
        assert effect.direction == "left"
        assert effect.distance == 100

    def test_create_effect_static(self) -> None:
        """Test creating static effect from registry."""
        registry = EffectRegistry()

        effect = registry.create_effect("static")

        assert isinstance(effect, StaticConfig)

    def test_create_effect_nonexistent(self) -> None:
        """Test that creating nonexistent effect raises error."""
        registry = EffectRegistry()

        with pytest.raises(KeyError, match="not found"):
            registry.create_effect("nonexistent")

    def test_create_effect_with_overrides(self) -> None:
        """Test creating effect with parameter overrides."""
        registry = EffectRegistry()

        effect = registry.create_effect(
            "ken_burns_zoom_in", duration=5.0, zoom_factor=1.5, pan_x=0.1, pan_y=-0.05
        )

        assert effect.duration == 5.0
        assert isinstance(effect, KenBurnsConfig)
        assert effect.zoom_factor == 1.5
        assert effect.pan_x == 0.1
        assert effect.pan_y == -0.05

    def test_create_effect_unknown_type(self) -> None:
        """Test that creating effect from unknown type raises ValueError."""
        registry = EffectRegistry()

        # Create a mock object that has model_dump() but isn't a known effect type
        class MockEffectConfig:
            def model_dump(self) -> dict:
                return {"type": "mock", "duration": 1.0}

        # Register the mock object to trigger the unknown type error
        registry.register("unknown_effect", MockEffectConfig())

        with pytest.raises(ValueError, match="Unknown effect type"):
            registry.create_effect("unknown_effect")
