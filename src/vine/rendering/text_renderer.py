"""Text-specific renderer implementation."""

from moviepy import ColorClip, CompositeVideoClip, VideoClip

from vine.models.video_spec import VideoSpec
from vine.rendering.base_renderer import BaseRenderer


class TextRenderer(BaseRenderer[VideoClip]):
    """Text-specific renderer implementation.

    Implements the BaseRenderer template method for text rendering,
    focusing on text overlays and typography.
    """

    def create_clips(self, video_spec: VideoSpec) -> list[VideoClip]:
        """Create text clips from the video spec.

        Args:
            video_spec: Project Vine VideoSpec model

        Returns:
            List of MoviePy VideoClip objects
        """
        clips = []

        # Create clips from text tracks
        for track in video_spec.text_tracks:
            if track.visible:
                track_clips = self.adapter.adapt_text_track(track)
                clips.extend(track_clips)

        return clips

    def compose_clips(self, clips: list[VideoClip], video_spec: VideoSpec) -> VideoClip:
        """Compose text clips into a composite video.

        Args:
            clips: List of MoviePy TextClip objects
            video_spec: Project Vine VideoSpec model

        Returns:
            MoviePy VideoClip object
        """
        # Create composite from all text clips or empty video
        if clips:
            result: VideoClip = CompositeVideoClip(
                clips, size=(video_spec.width, video_spec.height)
            )
        else:
            result = ColorClip(
                size=(video_spec.width, video_spec.height), color=(0, 0, 0)
            )

        return result

    def finalize(self, composite: VideoClip, video_spec: VideoSpec) -> VideoClip:
        """Finalize the text video with additional processing.

        Args:
            composite: MoviePy VideoClip object
            video_spec: Project Vine VideoSpec model

        Returns:
            Finalized MoviePy VideoClip object
        """
        # Call parent finalize method
        final_result = super().finalize(composite, video_spec)

        # Set background color for text-only videos
        if video_spec.background_color != "#000000":
            # This would require additional processing to set background color
            # For now, we'll use the default black background
            raise NotImplementedError("Background color setting not yet implemented")

        return final_result

    def render_text_overlay(self, video_spec: VideoSpec) -> list[VideoClip]:
        """Render text clips as overlays (without background).

        Args:
            video_spec: Project Vine VideoSpec model

        Returns:
            List of MoviePy TextClip objects
        """
        return self.create_clips(video_spec)
