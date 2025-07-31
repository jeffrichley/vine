"""Shared pytest fixtures and configuration."""

from typing import Any, Optional, Protocol
from unittest.mock import MagicMock

import pytest

from vine.rendering.moviepy_adapter import MoviePyAdapter


# Phase 2.1: Advanced Mock Types for MoviePy and Vine objects
class MockVideoClip(Protocol):
    duration: float
    fps: float
    size: tuple[int, int]
    layer_index: int
    end: float
    audio: Optional["MockAudioClip"]

    def with_duration(self, duration: float) -> "MockVideoClip": ...
    def with_position(self, position: tuple[float, float]) -> "MockVideoClip": ...
    def with_opacity(self, opacity: float) -> "MockVideoClip": ...
    def with_volume_scaled(self, volume: float) -> "MockVideoClip": ...
    def with_volume_function(self, func: Any) -> "MockVideoClip": ...
    def with_effects(self, effects: Any) -> "MockVideoClip": ...
    def resize(self, size: tuple[int, int]) -> "MockVideoClip": ...
    def close(self) -> None: ...


class MockAudioClip(Protocol):
    nchannels: int
    ends: list[float]

    def with_volume_scaled(self, volume: float) -> "MockAudioClip": ...
    def with_volume_function(self, func: Any) -> "MockAudioClip": ...
    def close(self) -> None: ...


class MockImageClip(MockVideoClip):
    pass


class MockTextClip(MockVideoClip):
    pass


class MockAudioFileClip(MockAudioClip):
    pass


# Mock Protocols for Vine objects
class MockVideoRenderer(Protocol):
    def render(self) -> MockVideoClip: ...
    def render_with_audio(self) -> tuple[MockVideoClip, MockAudioClip | None]: ...


class MockClipFactory(Protocol):
    def create_image_clip(self, clip_params: Any) -> MockImageClip: ...
    def create_text_clip(self, clip_params: Any) -> MockTextClip: ...
    def create_audio_clip(self, clip_params: Any) -> MockAudioFileClip: ...


# Mock factory functions
def create_mock_video_clip() -> MockVideoClip:
    """Create a properly typed mock MoviePy video clip."""
    mock_clip: MockVideoClip = MagicMock(spec=MockVideoClip)
    mock_clip.duration = 5.0
    mock_clip.fps = 30.0
    mock_clip.size = (1920, 1080)
    mock_clip.layer_index = 0
    mock_clip.end = 5.0

    # Mock audio properties
    mock_audio: MockAudioClip = MagicMock(spec=MockAudioClip)
    mock_audio.nchannels = 2
    # Use type ignore for property assignment to mock
    type(mock_audio).ends = property(lambda _: [5.0])  # type: ignore[assignment]
    mock_clip.audio = mock_audio

    # Mock method chaining - each method returns the same mock object
    mock_clip.with_duration.return_value = mock_clip
    mock_clip.with_position.return_value = mock_clip
    mock_clip.with_opacity.return_value = mock_clip
    mock_clip.with_volume_scaled.return_value = mock_clip
    mock_clip.with_volume_function.return_value = mock_clip
    mock_clip.with_effects.return_value = mock_clip
    mock_clip.resize.return_value = mock_clip

    return mock_clip


def create_mock_audio_clip() -> MockAudioClip:
    """Create a properly typed mock MoviePy audio clip."""
    mock_audio: MockAudioClip = MagicMock(spec=MockAudioClip)
    mock_audio.nchannels = 2
    # Use type ignore for property assignment to mock
    type(mock_audio).ends = property(lambda _: [5.0])  # type: ignore[assignment]

    # Mock method chaining
    mock_audio.with_volume_scaled.return_value = mock_audio
    mock_audio.with_volume_function.return_value = mock_audio

    return mock_audio


def create_mock_video_renderer() -> MockVideoRenderer:
    """Create a properly typed mock VideoRenderer."""
    mock_renderer: MockVideoRenderer = MagicMock(spec=MockVideoRenderer)

    # Mock render methods
    video_clip = create_mock_video_clip()
    audio_clip = create_mock_audio_clip()

    mock_renderer.render.return_value = video_clip
    mock_renderer.render_with_audio.return_value = (video_clip, audio_clip)

    return mock_renderer


def create_mock_clip_factory() -> MockClipFactory:
    """Create a properly typed mock ClipFactory."""
    mock_factory: MockClipFactory = MagicMock(spec=MockClipFactory)

    # Create mock clips
    image_clip = create_mock_video_clip()
    text_clip = create_mock_video_clip()
    audio_clip = create_mock_audio_clip()

    # Set return values
    mock_factory.create_image_clip.return_value = image_clip
    mock_factory.create_text_clip.return_value = text_clip
    mock_factory.create_audio_clip.return_value = audio_clip

    return mock_factory


def safe_assert(condition: Any, message: str = "") -> None:
    """Assert that helps mypy understand control flow.

    This function is used in tests to help mypy understand that certain
    conditions are guaranteed to be true, especially when dealing with
    optional types or complex control flow.

    Args:
        condition: The condition to assert
        message: Optional error message if assertion fails
    """
    assert condition, message


@pytest.fixture(scope="function")
def moviepy_adapter() -> Any:
    """Create a MoviePyAdapter instance for testing.

    Scope: function - Each test gets a fresh adapter instance
    """
    return MoviePyAdapter()


@pytest.fixture(scope="function")
def mock_clip_factory() -> MockClipFactory:
    """Create a mock ClipFactory for testing.

    Scope: function - Each test gets a fresh mock factory
    """
    return create_mock_clip_factory()


@pytest.fixture(scope="function")
def mock_video_renderer() -> MockVideoRenderer:
    """Create a mock VideoRenderer for testing.

    Scope: function - Each test gets a fresh mock renderer
    """
    return create_mock_video_renderer()


# Note: The mocker fixture below is provided by pytest-mock plugin
# It's automatically available when pytest-mock is installed
# We don't need to define it here, so removing the unused fixture
