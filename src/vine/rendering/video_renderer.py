"""Video-specific renderer implementation."""

from typing import List

from moviepy import CompositeVideoClip, ImageClip, VideoClip

from vine.models.video_spec import VideoSpec
from vine.rendering.base_renderer import BaseRenderer


class VideoRenderer(BaseRenderer[VideoClip]):
    """
    Video-specific renderer implementation.

    Implements the BaseRenderer template method for video rendering,
    focusing on image clips and text overlays.
    """

    def create_clips(self, video_spec: VideoSpec) -> List[VideoClip]:
        """
        Create video clips from the video spec.

        Args:
            video_spec: Project Vine VideoSpec model

        Returns:
            List of MoviePy VideoClip objects
        """
        clips = []

        # Create clips from video tracks
        for video_track in video_spec.video_tracks:
            if video_track.visible:
                track_clips = self.adapter.adapt_video_track(video_track)
                clips.extend(track_clips)

        # Create clips from text tracks (overlays)
        for text_track in video_spec.text_tracks:
            if text_track.visible:
                track_clips = self.adapter.adapt_text_track(text_track)
                clips.extend(track_clips)

        return clips

    def compose_clips(self, clips: List[ImageClip], video_spec: VideoSpec) -> VideoClip:
        """
        Compose video clips into a composite video.

        Args:
            clips: List of MoviePy ImageClip objects
            video_spec: Project Vine VideoSpec model

        Returns:
            MoviePy CompositeVideoClip object
        """
        # Create composite from all clips or empty video
        if clips:
            result: VideoClip = CompositeVideoClip(
                clips, size=(video_spec.width, video_spec.height)
            )
        else:
            from moviepy import ColorClip

            result = ColorClip(
                size=(video_spec.width, video_spec.height), color=(0, 0, 0)
            )

        return result

    def finalize(self, composite: VideoClip, video_spec: VideoSpec) -> VideoClip:
        """
        Finalize the video with additional processing.

        Args:
            composite: MoviePy VideoClip object
            video_spec: Project Vine VideoSpec model

        Returns:
            Finalized MoviePy VideoClip object
        """
        # Call parent finalize method
        final_result = super().finalize(composite, video_spec)

        # Set background color if specified
        if video_spec.background_color != "#000000":
            # This would require additional processing to set background color
            # For now, we'll use the default black background
            raise NotImplementedError("Background color setting not yet implemented")

        return final_result
