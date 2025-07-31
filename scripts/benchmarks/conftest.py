"""Benchmark test fixtures and utilities."""

from pathlib import Path

import pytest

from vine.builder.timeline_builder import TimelineBuilder
from vine.models import ImageClip, VideoSpec, VideoTrack
from vine.models.transition import TransitionDirection
from vine.models.transitions import FadeTransition, SlideTransition


@pytest.fixture
def sample_images() -> list[Path]:
    """Provide sample image paths for benchmarking."""
    # Use existing images from examples
    image_dir = Path("examples/assets")
    return [
        image_dir / "image1.jpg",
        image_dir / "image2.jpg",
        image_dir / "background.jpg",
    ]


@pytest.fixture
def sample_audio() -> Path:
    """Provide sample audio path for benchmarking."""
    # Use existing audio from examples
    return Path("examples/assets/shorts/chrona_voice/music")


@pytest.fixture
def basic_image_clip() -> ImageClip:
    """Provide basic image clip for benchmarking."""
    return ImageClip(path="examples/assets/image1.jpg", duration=3.0, start_time=0.0)


@pytest.fixture
def complex_image_clip() -> ImageClip:
    """Provide complex image clip for benchmarking."""
    return ImageClip(
        path="examples/assets/image1.jpg", duration=5.0, start_time=1.0, opacity=0.8
    )


@pytest.fixture
def small_timeline_builder() -> TimelineBuilder:
    """Provide a small timeline builder for basic benchmarks."""
    return TimelineBuilder()


@pytest.fixture
def medium_timeline_builder() -> TimelineBuilder:
    """Provide a medium-sized timeline builder for scaling benchmarks."""
    builder = TimelineBuilder()

    # Add some basic content
    for i in range(5):
        builder.add_image_at(
            image_path=f"examples/assets/image{i % 2 + 1}.jpg",
            start_time=i * 2.0,
            duration=2.0,
        )

    return builder


@pytest.fixture
def large_timeline_builder() -> TimelineBuilder:
    """Provide a large timeline builder for stress testing."""
    builder = TimelineBuilder()

    # Add many clips
    for i in range(20):
        for j in range(3):
            builder.add_image_at(
                image_path=f"examples/assets/image{j % 2 + 1}.jpg",
                start_time=i * 3.0 + j * 1.0,
                duration=1.0,
            )

    return builder


@pytest.fixture
def complex_video_spec() -> VideoSpec:
    """Provide a complex video specification for benchmarking."""
    # Create multiple tracks with various effects
    video_tracks = []

    for i in range(10):
        video_track = VideoTrack(
            name=f"video_track_{i}",
            clips=[
                ImageClip(
                    path=f"examples/assets/image{i % 2 + 1}.jpg",
                    start_time=i * 2.0,
                    duration=2.0,
                )
            ],
        )
        video_tracks.append(video_track)

    return VideoSpec(
        width=1920,
        height=1080,
        fps=30,
        duration=20.0,
        title="Benchmark Test",
        video_tracks=video_tracks,
    )


@pytest.fixture
def transition_effects():
    """Provide various transition effects for benchmarking."""
    return {
        "fade": FadeTransition(duration=0.5),
        "slide": SlideTransition(duration=0.5, direction=TransitionDirection.LEFT),
        "none": None,
    }
