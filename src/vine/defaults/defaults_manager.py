"""Defaults manager for Project Vine."""

from vine.models.yaml_models import DefaultsData


class DefaultsManager:
    """Manages hierarchical defaults for video composition."""

    _defaults: dict[str, str | int | float | bool]

    def __init__(
        self, defaults: dict[str, str | int | float | bool] | DefaultsData | None = None
    ) -> None:
        """Initialize the defaults manager.

        Args:
            defaults: Initial defaults dictionary or typed DefaultsData
        """
        if isinstance(defaults, DefaultsData):
            self._defaults = defaults.model_dump()
        else:
            self._defaults = defaults or {}

    def get(
        self, key: str, default: str | int | float | bool | None = None
    ) -> str | int | float | bool | None:
        """Get a default value.

        Args:
            key: The key to look up
            default: Default value if key not found

        Returns:
            The default value or the provided default
        """
        return self._defaults.get(key, default)

    def set(self, key: str, value: str | int | float | bool) -> None:
        """Set a default value.

        Args:
            key: The key to set
            value: The value to set
        """
        self._defaults[key] = value

    def update(
        self, defaults: dict[str, str | int | float | bool] | DefaultsData
    ) -> None:
        """Update defaults with a dictionary.

        Args:
            defaults: Dictionary of defaults to add/update or typed DefaultsData
        """
        if isinstance(defaults, DefaultsData):
            # Type ignore for model_dump() which returns Dict[str, Any]
            self._defaults.update(defaults.model_dump())  # type: ignore[misc]
        else:
            self._defaults.update(defaults)

    def clear(self) -> None:
        """Clear all defaults."""
        self._defaults.clear()

    @property
    def all(self) -> dict[str, str | int | float | bool]:
        """Get all current defaults.

        Returns:
            Dictionary of all current defaults
        """
        return self._defaults.copy()

    # Audio defaults
    DEFAULT_MUSIC_VOLUME = 0.3  # Background music should be subtle
    DEFAULT_VOICE_VOLUME = 0.8  # Voice should be prominent
    DEFAULT_SFX_VOLUME = 0.5  # SFX should be noticeable but not overwhelming

    def get_audio_defaults(self) -> dict[str, float]:
        """Get all audio default settings.

        Returns:
            Dictionary with all audio defaults
        """
        return {
            "music_volume": self.DEFAULT_MUSIC_VOLUME,
            "voice_volume": self.DEFAULT_VOICE_VOLUME,
            "sfx_volume": self.DEFAULT_SFX_VOLUME,
        }

    def get_music_volume(self) -> float:
        """Get default music volume.

        Returns:
            Default music volume (0.3)
        """
        return self.DEFAULT_MUSIC_VOLUME

    def get_voice_volume(self) -> float:
        """Get default voice volume.

        Returns:
            Default voice volume (0.8)
        """
        return self.DEFAULT_VOICE_VOLUME

    def get_sfx_volume(self) -> float:
        """Get default SFX volume.

        Returns:
            Default SFX volume (0.5)
        """
        return self.DEFAULT_SFX_VOLUME
