"""Text-specific renderer implementation."""

from typing import List

from moviepy import CompositeVideoClip, TextClip

from vine.models.video_spec import VideoSpec
from vine.rendering.base_renderer import BaseRenderer


class TextRenderer(BaseRenderer):
    """
    Text-specific renderer implementation.

    Implements the BaseRenderer template method for text rendering,
    focusing on text overlays and typography.
    """

    def create_clips(self, video_spec: VideoSpec) -> List[TextClip]:
        """
        Create text clips from the video spec.

        Args:
            video_spec: Project Vine VideoSpec model

        Returns:
            List of MoviePy TextClip objects
        """
        clips = []

        # Create clips from text tracks
        for track in video_spec.text_tracks:
            if track.visible:
                track_clips = self.adapter.adapt_text_track(track)
                clips.extend(track_clips)

        return clips

    def compose_clips(
        self, clips: List[TextClip], video_spec: VideoSpec
    ) -> CompositeVideoClip:
        """
        Compose text clips into a composite video.

        Args:
            clips: List of MoviePy TextClip objects
            video_spec: Project Vine VideoSpec model

        Returns:
            MoviePy CompositeVideoClip object
        """
        if clips:
            # Create composite from all text clips
            composite = CompositeVideoClip(
                clips, size=(video_spec.width, video_spec.height)
            )
        else:
            # Create empty video if no text clips
            from moviepy import ColorClip

            composite = ColorClip(
                size=(video_spec.width, video_spec.height), color=(0, 0, 0)
            )

        return composite

    def finalize(
        self, composite: CompositeVideoClip, video_spec: VideoSpec
    ) -> CompositeVideoClip:
        """
        Finalize the text video with additional processing.

        Args:
            composite: MoviePy CompositeVideoClip object
            video_spec: Project Vine VideoSpec model

        Returns:
            Finalized MoviePy CompositeVideoClip object
        """
        # Call parent finalize method
        composite = super().finalize(composite, video_spec)

        # Set background color for text-only videos
        if video_spec.background_color != "#000000":
            # This would require additional processing to set background color
            # For now, we'll use the default black background
            pass

        return composite

    def render_text_overlay(self, video_spec: VideoSpec) -> List[TextClip]:
        """
        Render text clips as overlays (without background).

        Args:
            video_spec: Project Vine VideoSpec model

        Returns:
            List of MoviePy TextClip objects
        """
        return self.create_clips(video_spec)
