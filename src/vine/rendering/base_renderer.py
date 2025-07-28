"""Template Method pattern for rendering algorithms."""

from abc import ABC, abstractmethod
from typing import Optional

from moviepy import AudioFileClip, CompositeVideoClip

from vine.models.video_spec import VideoSpec
from vine.rendering.moviepy_adapter import MoviePyAdapter


class BaseRenderer(ABC):
    """
    Abstract base class for rendering algorithms.

    Implements the Template Method pattern to define the skeleton
    of the rendering algorithm while allowing subclasses to
    implement specific parts.
    """

    def __init__(self):
        """Initialize the renderer with an adapter."""
        self.adapter = MoviePyAdapter()

    def render(self, video_spec: VideoSpec) -> CompositeVideoClip:
        """
        Template method for rendering a video spec.

        This method defines the algorithm structure:
        1. Create clips from the video spec
        2. Compose clips into a final video
        3. Finalize the video (optional hook)

        Args:
            video_spec: Project Vine VideoSpec model

        Returns:
            MoviePy CompositeVideoClip object
        """
        # Step 1: Create clips (implemented by subclasses)
        clips = self.create_clips(video_spec)

        # Step 2: Compose clips (implemented by subclasses)
        composite = self.compose_clips(clips, video_spec)

        # Step 3: Finalize (optional hook)
        composite = self.finalize(composite, video_spec)

        return composite

    @abstractmethod
    def create_clips(self, video_spec: VideoSpec) -> list:
        """
        Create clips from the video spec.

        Args:
            video_spec: Project Vine VideoSpec model

        Returns:
            List of MoviePy clip objects
        """
        pass

    @abstractmethod
    def compose_clips(self, clips: list, video_spec: VideoSpec) -> CompositeVideoClip:
        """
        Compose clips into a final video.

        Args:
            clips: List of MoviePy clip objects
            video_spec: Project Vine VideoSpec model

        Returns:
            MoviePy CompositeVideoClip object
        """
        pass

    def finalize(
        self, composite: CompositeVideoClip, video_spec: VideoSpec
    ) -> CompositeVideoClip:
        """Finalize the composite clip with video spec settings."""
        # Set FPS if not already set
        if not hasattr(composite, "fps") or composite.fps is None:
            composite = composite.with_fps(video_spec.fps)

        return composite

    def render_with_audio(
        self, video_spec: VideoSpec
    ) -> tuple[CompositeVideoClip, Optional[AudioFileClip]]:
        """
        Render video with audio.

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
