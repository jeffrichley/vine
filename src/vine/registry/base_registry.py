"""Base registry class for extensible component registration."""

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Optional


class BaseRegistry(ABC):
    """
    Base class for component registries.

    Provides common functionality for registering and retrieving
    components by name with validation and error handling.
    """

    def __init__(self) -> None:
        """Initialize an empty registry."""
        self._components: Dict[str, Any] = {}
        self._validators: Dict[str, Callable] = {}

    def register(
        self, name: str, component: Any, validator: Optional[Callable] = None
    ) -> None:
        """
        Register a component with the given name.

        Args:
            name: Unique name for the component
            component: Component to register
            validator: Optional validation function

        Raises:
            ValueError: If name is already registered
        """
        if name in self._components:
            raise ValueError(f"Component '{name}' is already registered")

        # Validate component if validator provided
        if validator:
            validator(component)

        self._components[name] = component
        if validator:
            self._validators[name] = validator

    def get(self, name: str) -> Any:
        """
        Get a component by name.

        Args:
            name: Name of the component to retrieve

        Returns:
            The registered component

        Raises:
            KeyError: If component is not found
        """
        if name not in self._components:
            raise KeyError(f"Component '{name}' not found in registry")
        return self._components[name]

    def list(self) -> list[str]:
        """
        Get list of all registered component names.

        Returns:
            List of registered component names
        """
        return list(self._components.keys())

    def exists(self, name: str) -> bool:
        """
        Check if a component is registered.

        Args:
            name: Name to check

        Returns:
            True if component exists, False otherwise
        """
        return name in self._components

    def unregister(self, name: str) -> None:
        """
        Remove a component from the registry.

        Args:
            name: Name of the component to remove

        Raises:
            KeyError: If component is not found
        """
        if name not in self._components:
            raise KeyError(f"Component '{name}' not found in registry")

        del self._components[name]
        if name in self._validators:
            del self._validators[name]

    def clear(self) -> None:
        """Clear all registered components."""
        self._components.clear()
        self._validators.clear()

    def count(self) -> int:
        """
        Get the number of registered components.

        Returns:
            Number of registered components
        """
        return len(self._components)

    @abstractmethod
    def get_default(self) -> str:
        """
        Get the name of the default component.

        Returns:
            Name of the default component
        """
