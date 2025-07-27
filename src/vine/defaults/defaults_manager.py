"""Defaults manager for Project Vine."""

from typing import Any, Dict, Optional


class DefaultsManager:
    """Manages hierarchical defaults for video composition."""

    def __init__(self, defaults: Optional[Dict[str, Any]] = None):
        """Initialize the defaults manager.

        Args:
            defaults: Initial defaults dictionary
        """
        self._defaults = defaults or {}

    def get(self, key: str, default: Any = None) -> Any:
        """Get a default value.

        Args:
            key: The key to look up
            default: Default value if key not found

        Returns:
            The default value or the provided default
        """
        return self._defaults.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set a default value.

        Args:
            key: The key to set
            value: The value to set
        """
        self._defaults[key] = value

    def update(self, defaults: Dict[str, Any]) -> None:
        """Update defaults with a dictionary.

        Args:
            defaults: Dictionary of defaults to add/update
        """
        self._defaults.update(defaults)

    def clear(self) -> None:
        """Clear all defaults."""
        self._defaults.clear()

    @property
    def all(self) -> Dict[str, Any]:
        """Get all current defaults.

        Returns:
            Dictionary of all current defaults
        """
        return self._defaults.copy()
