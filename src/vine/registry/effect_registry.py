"""Effect registry for managing effect configurations."""

from typing import Optional

from vine.models.effects import EffectConfig, KenBurnsConfig, SlideConfig, StaticConfig
from vine.registry.base_registry import BaseRegistry


class EffectRegistry(BaseRegistry):
    """
    Registry for effect configurations.

    Manages predefined effects that can be applied to timeline blocks
    with consistent parameters and validation.
    """

    def __init__(self):
        """Initialize with default effects."""
        super().__init__()
        self._register_defaults()

    def _register_defaults(self):
        """Register default effect configurations."""
        # Ken Burns effects
        self.register(
            "ken_burns_zoom_in",
            KenBurnsConfig(zoom_factor=1.2, pan_x=0.0, pan_y=0.0, easing="ease_in_out"),
        )

        self.register(
            "ken_burns_zoom_out",
            KenBurnsConfig(zoom_factor=1.0, pan_x=0.0, pan_y=0.0, easing="ease_in_out"),
        )

        self.register(
            "ken_burns_pan_left",
            KenBurnsConfig(
                zoom_factor=1.1, pan_x=-0.1, pan_y=0.0, easing="ease_in_out"
            ),
        )

        self.register(
            "ken_burns_pan_right",
            KenBurnsConfig(zoom_factor=1.1, pan_x=0.1, pan_y=0.0, easing="ease_in_out"),
        )

        # Slide effects
        self.register(
            "slide_in_left",
            SlideConfig(direction="left", distance=100, easing="ease_out"),
        )

        self.register(
            "slide_in_right",
            SlideConfig(direction="right", distance=100, easing="ease_out"),
        )

        self.register(
            "slide_in_up", SlideConfig(direction="up", distance=100, easing="ease_out")
        )

        self.register(
            "slide_in_down",
            SlideConfig(direction="down", distance=100, easing="ease_out"),
        )

        # Static effects
        self.register("static", StaticConfig())

    def get_default(self) -> str:
        """
        Get the default effect name.

        Returns:
            Name of the default effect
        """
        return "static"

    def create_effect(
        self, name: str, duration: Optional[float] = None, **kwargs
    ) -> EffectConfig:
        """
        Create an effect configuration from a registered template.

        Args:
            name: Name of the registered effect
            duration: Optional duration override
            **kwargs: Additional parameters to override

        Returns:
            EffectConfig instance

        Raises:
            KeyError: If effect name is not found
        """
        template = self.get(name)

        # Create a copy with overrides
        template_data = template.model_dump()
        if duration is not None:
            template_data["duration"] = duration

        for key, value in kwargs.items():
            if key in template_data:
                template_data[key] = value

        if isinstance(template, KenBurnsConfig):
            config = KenBurnsConfig(**template_data)
        elif isinstance(template, SlideConfig):
            config = SlideConfig(**template_data)
        elif isinstance(template, StaticConfig):
            config = StaticConfig(**template_data)
        else:
            raise ValueError(f"Unknown effect type: {type(template)}")

        return config
