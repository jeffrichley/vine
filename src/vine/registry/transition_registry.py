"""Transition registry for managing transition configurations."""

from typing import Any, Optional

from vine.models.transition import (
    Transition,
    TransitionDirection,
    TransitionEasing,
    TransitionType,
)
from vine.registry.base_registry import BaseRegistry


class TransitionRegistry(BaseRegistry):
    """
    Registry for transition configurations.

    Manages predefined transition effects that can be applied between
    tracks with consistent parameters.
    """

    def __init__(self) -> None:
        """Initialize with default transitions."""
        super().__init__()
        self._register_defaults()

    def _register_defaults(self) -> None:
        """Register default transition configurations."""
        # Fade transitions
        self.register(
            "fade_in",
            Transition(
                transition_type=TransitionType.FADE,
                start_time=0.0,
                duration=1.0,
                direction=TransitionDirection.IN,
                easing=TransitionEasing.EASE_IN_OUT,
            ),
        )

        self.register(
            "fade_out",
            Transition(
                transition_type=TransitionType.FADE,
                start_time=0.0,
                duration=1.0,
                direction=TransitionDirection.OUT,
                easing=TransitionEasing.EASE_IN_OUT,
            ),
        )

        self.register(
            "fade_in_out",
            Transition(
                transition_type=TransitionType.FADE,
                start_time=0.0,
                duration=1.0,
                direction=TransitionDirection.IN,
                easing=TransitionEasing.EASE_IN_OUT,
            ),
        )

        # Crossfade transitions
        self.register(
            "crossfade",
            Transition(
                transition_type=TransitionType.CROSSFADE,
                start_time=0.0,
                duration=1.0,
                easing=TransitionEasing.EASE_IN_OUT,
            ),
        )

        self.register(
            "crossfade_fast",
            Transition(
                transition_type=TransitionType.CROSSFADE,
                start_time=0.0,
                duration=0.5,
                easing=TransitionEasing.EASE_IN_OUT,
            ),
        )

        self.register(
            "crossfade_slow",
            Transition(
                transition_type=TransitionType.CROSSFADE,
                start_time=0.0,
                duration=2.0,
                easing=TransitionEasing.EASE_IN_OUT,
            ),
        )

        # Slide transitions
        self.register(
            "slide_left",
            Transition(
                transition_type=TransitionType.SLIDE,
                start_time=0.0,
                duration=1.0,
                direction=TransitionDirection.LEFT,
                easing=TransitionEasing.EASE_IN_OUT,
            ),
        )

        self.register(
            "slide_right",
            Transition(
                transition_type=TransitionType.SLIDE,
                start_time=0.0,
                duration=1.0,
                direction=TransitionDirection.RIGHT,
                easing=TransitionEasing.EASE_IN_OUT,
            ),
        )

        self.register(
            "slide_up",
            Transition(
                transition_type=TransitionType.SLIDE,
                start_time=0.0,
                duration=1.0,
                direction=TransitionDirection.UP,
                easing=TransitionEasing.EASE_IN_OUT,
            ),
        )

        self.register(
            "slide_down",
            Transition(
                transition_type=TransitionType.SLIDE,
                start_time=0.0,
                duration=1.0,
                direction=TransitionDirection.DOWN,
                easing=TransitionEasing.EASE_IN_OUT,
            ),
        )

    def get_default(self) -> str:
        """
        Get the default transition name.

        Returns:
            Name of the default transition
        """
        return "crossfade"

    def create_transition(
        self,
        name: str,
        start_time: float = 0.0,
        duration: Optional[float] = None,
        from_tracks: Optional[list] = None,
        to_tracks: Optional[list] = None,
        **kwargs: Any,
    ) -> Transition:
        """
        Create a transition configuration from a registered template.

        Args:
            name: Name of the registered transition
            start_time: Start time in timeline in seconds
            duration: Optional duration override
            from_tracks: Optional list of source track names
            to_tracks: Optional list of target track names
            **kwargs: Additional parameters to override

        Returns:
            Transition instance

        Raises:
            KeyError: If transition name is not found
        """
        template = self.get(name)

        # Create a copy with overrides
        template_data = template.model_dump()
        template_data["start_time"] = start_time

        if duration is not None:
            template_data["duration"] = duration

        if from_tracks is not None:
            template_data["from_tracks"] = from_tracks

        if to_tracks is not None:
            template_data["to_tracks"] = to_tracks

        for key, value in kwargs.items():
            if key in template_data:
                template_data[key] = value

        return Transition(**template_data)
