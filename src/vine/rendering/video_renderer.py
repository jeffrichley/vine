"""Video-specific renderer implementation."""

from typing import List

from moviepy import CompositeVideoClip, ImageClip

from vine.models.video_spec import VideoSpec
from vine.rendering.base_renderer import BaseRenderer


class VideoRenderer(BaseRenderer):
    """
    Video-specific renderer implementation.

    Implements the BaseRenderer template method for video rendering,
    focusing on image clips and text overlays.
    """

    def create_clips(self, video_spec: VideoSpec) -> List[ImageClip]:
        """
        Create video clips from the video spec.

        Args:
            video_spec: Project Vine VideoSpec model

        Returns:
            List of MoviePy ImageClip objects
        """
        clips = []

        # Create clips from video tracks
        for track in video_spec.video_tracks:
            if track.visible:
                track_clips = self.adapter.adapt_video_track(track)
                clips.extend(track_clips)

        # Create clips from text tracks (overlays)
        for track in video_spec.text_tracks:
            if track.visible:
                track_clips = self.adapter.adapt_text_track(track)
                clips.extend(track_clips)

        return clips

    def compose_clips(
        self, clips: List[ImageClip], video_spec: VideoSpec
    ) -> CompositeVideoClip:
        """
        Compose video clips into a composite video.

        Args:
            clips: List of MoviePy ImageClip objects
            video_spec: Project Vine VideoSpec model

        Returns:
            MoviePy CompositeVideoClip object
        """
        if clips:
            # Create composite from all clips
            composite = CompositeVideoClip(
                clips, size=(video_spec.width, video_spec.height)
            )
        else:
            # Create empty black video if no clips
            from moviepy import ColorClip

            composite = ColorClip(
                size=(video_spec.width, video_spec.height), color=(0, 0, 0)
            )

        return composite

    def finalize(
        self, composite: CompositeVideoClip, video_spec: VideoSpec
    ) -> CompositeVideoClip:
        """
        Finalize the video with additional processing.

        Args:
            composite: MoviePy CompositeVideoClip object
            video_spec: Project Vine VideoSpec model

        Returns:
            Finalized MoviePy CompositeVideoClip object
        """
        # Call parent finalize method
        composite = super().finalize(composite, video_spec)

        # Set background color if specified
        if video_spec.background_color != "#000000":
            # This would require additional processing to set background color
            # For now, we'll use the default black background
            pass

        return composite
