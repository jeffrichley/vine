"""Basic tests for the vine package."""

import pytest

from vine.defaults import DefaultsManager
from vine.models.yaml_models import DefaultsData


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
        defaults: dict[str, str | int | float | bool] = {
            "width": 1920,
            "height": 1080,
        }
        dm = DefaultsManager(defaults)
        assert dm.all == defaults

    def test_init_with_defaults_data(self) -> None:
        """Test initialization with DefaultsData."""
        defaults_data = DefaultsData(width=1920, height=1080, volume=0.5)
        dm = DefaultsManager(defaults_data)
        assert dm.get("width") == 1920
        assert dm.get("height") == 1080
        assert dm.get("volume") == 0.5

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

    def test_update_with_defaults_data(self) -> None:
        """Test updating defaults with DefaultsData."""
        dm = DefaultsManager({"width": 1920})
        defaults_data = DefaultsData(width=1920, height=1080, volume=0.5)
        dm.update(defaults_data)
        assert dm.get("width") == 1920
        assert dm.get("height") == 1080
        assert dm.get("volume") == 0.5

    def test_clear(self) -> None:
        """Test clearing all defaults."""
        dm = DefaultsManager({"width": 1920, "height": 1080})
        dm.clear()
        assert dm.all == {}

    def test_all_property(self) -> None:
        """Test the all property returns a copy."""
        defaults: dict[str, str | int | float | bool] = {
            "width": 1920,
            "height": 1080,
        }
        dm = DefaultsManager(defaults)
        all_defaults = dm.all
        assert all_defaults == defaults
        assert all_defaults is not dm._defaults  # Should be a copy

    def test_audio_defaults(self) -> None:
        """Test audio default methods."""
        dm = DefaultsManager()
        audio_defaults = dm.get_audio_defaults()
        assert audio_defaults["music_volume"] == 0.3
        assert audio_defaults["voice_volume"] == 0.8
        assert audio_defaults["sfx_volume"] == 0.5
        assert dm.get_music_volume() == 0.3
        assert dm.get_voice_volume() == 0.8
        assert dm.get_sfx_volume() == 0.5
