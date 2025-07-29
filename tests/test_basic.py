"""Basic tests for the vine package."""

import pytest

from vine.defaults import DefaultsManager


def test_defaults_manager_import() -> None:
    """Test that DefaultsManager can be imported."""
    assert DefaultsManager is not None


def test_basic_math() -> None:
    """A simple test to verify pytest is working."""
    assert 2 + 2 == 4


@pytest.mark.asyncio
async def test_async_test() -> None:
    """Test that async tests work."""
    result = await async_function()
    assert result == "async_works"


async def async_function() -> str:
    """Simple async function for testing."""
    return "async_works"


class TestDefaultsManager:
    """Test the DefaultsManager class."""

    def test_init_empty(self) -> None:
        """Test initialization with no defaults."""
        dm = DefaultsManager()
        assert dm.all == {}

    def test_init_with_defaults(self) -> None:
        """Test initialization with defaults."""
        defaults = {"width": 1920, "height": 1080}
        dm = DefaultsManager(defaults)
        assert dm.all == defaults

    def test_get_existing(self) -> None:
        """Test getting an existing default."""
        dm = DefaultsManager({"width": 1920})
        assert dm.get("width") == 1920

    def test_get_missing(self) -> None:
        """Test getting a missing default."""
        dm = DefaultsManager()
        assert dm.get("width") is None
        assert dm.get("width", 1920) == 1920

    def test_set(self) -> None:
        """Test setting a default."""
        dm = DefaultsManager()
        dm.set("width", 1920)
        assert dm.get("width") == 1920

    def test_update(self) -> None:
        """Test updating defaults."""
        dm = DefaultsManager({"width": 1920})
        dm.update({"height": 1080, "fps": 30})
        assert dm.get("width") == 1920
        assert dm.get("height") == 1080
        assert dm.get("fps") == 30

    def test_clear(self) -> None:
        """Test clearing all defaults."""
        dm = DefaultsManager({"width": 1920, "height": 1080})
        dm.clear()
        assert dm.all == {}

    def test_all_property(self) -> None:
        """Test the all property returns a copy."""
        defaults = {"width": 1920, "height": 1080}
        dm = DefaultsManager(defaults)
        all_defaults = dm.all
        assert all_defaults == defaults
        assert all_defaults is not dm._defaults  # Should be a copy
