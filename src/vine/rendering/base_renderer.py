"""Base renderer implementation."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, cast

from moviepy import AudioClip, VideoClip

from vine.models.video_spec import VideoSpec
from vine.rendering.moviepy_adapter import MoviePyAdapter

T = TypeVar("T", bound=VideoClip)


class BaseRenderer(ABC, Generic[T]):
    """Abstract base class for rendering algorithms.

    Implements the Template Method pattern to define the skeleton
    of the rendering algorithm while allowing subclasses to
    implement specific parts.
    """

    def __init__(self) -> None:
        """Initialize the renderer with an adapter."""
        self.adapter = MoviePyAdapter()

    def render(self, video_spec: VideoSpec) -> T:
        """Template method for rendering a video spec.

        This method defines the algorithm structure:
        1. Create clips from the video spec
        2. Compose clips into a final video
        3. Finalize the video (optional hook)

        Args:
            video_spec: Project Vine VideoSpec model

        Returns:
            MoviePy clip object
        """
        # Step 1: Create clips (implemented by subclasses)
        clips = self.create_clips(video_spec)

        # Step 2: Compose clips (implemented by subclasses)
        result: T = self.compose_clips(clips, video_spec)

        # Step 3: Finalize (optional hook)
        final_result: T = self.finalize(result, video_spec)

        return final_result

    @abstractmethod
    def create_clips(self, video_spec: VideoSpec) -> list[VideoClip]:
        """Create clips from the video spec.

        Args:
            video_spec: Project Vine VideoSpec model

        Returns:
            List of MoviePy clip objects
        """

    @abstractmethod
    def compose_clips(self, clips: list[VideoClip], video_spec: VideoSpec) -> T:
        """Compose clips into a final video.

        Args:
            clips: List of MoviePy clip objects
            video_spec: Project Vine VideoSpec model

        Returns:
            MoviePy clip object
        """

    def finalize(self, composite: T, video_spec: VideoSpec) -> T:
        """Finalize the composite clip with video spec settings."""
        # Set FPS if not already set
        # getattr returns Any | None due to Python typing limitations with dynamic attributes
        if not hasattr(composite, "fps") or getattr(composite, "fps", None) is None:  # type: ignore[misc]
            return cast(T, composite.with_fps(video_spec.fps))

        return composite

    def render_with_audio(
        self, video_spec: VideoSpec
    ) -> tuple[VideoClip, AudioClip | None]:
        """Render video with audio.

        Args:
            video_spec: Project Vine VideoSpec model

        Returns:
            Tuple of (video_clip, audio_clip)
        """
        # Render video
        video_clip = self.render(video_spec)

        # Render audio
        audio_clip = self.adapter.adapt_audio_timeline(video_spec)

        return video_clip, audio_clip
