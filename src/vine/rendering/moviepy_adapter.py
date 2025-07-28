"""Adapter pattern for bridging Project Vine models with MoviePy API."""

from typing import List, Optional

from moviepy import AudioFileClip, CompositeVideoClip, ImageClip, TextClip

from vine.models.tracks import AudioClip as VineAudioClip
from vine.models.tracks import (
    AudioTrack,
    TextTrack,
    VideoTrack,
)
from vine.models.tracks import (
    ImageClip as VineImageClip,
)
from vine.models.tracks import (
    TextClip as VineTextClip,
)
from vine.models.video_spec import VideoSpec
from vine.rendering.clip_factory import ClipFactory


class MoviePyAdapter:
    """
    Adapter for converting Project Vine models to MoviePy clips.

    Implements the Adapter pattern to provide a clean interface between
    our Pydantic models and MoviePy's API, handling the conversion
    and composition logic.
    """

    def __init__(self):
        """Initialize the adapter with a clip factory."""
        self.clip_factory = ClipFactory()

    def adapt_image_clip(self, image_clip: VineImageClip) -> ImageClip:
        """
        Adapt a Project Vine ImageClip to a MoviePy ImageClip.

        Args:
            image_clip: Project Vine ImageClip model

        Returns:
            MoviePy ImageClip object
        """
        return self.clip_factory.create_image_clip(image_clip)

    def adapt_audio_clip(self, audio_clip: VineAudioClip) -> AudioFileClip:
        """
        Adapt a Project Vine AudioClip to a MoviePy AudioFileClip.

        Args:
            audio_clip: Project Vine AudioClip model

        Returns:
            MoviePy AudioFileClip object
        """
        return self.clip_factory.create_audio_clip(audio_clip)

    def adapt_text_clip(self, text_clip: VineTextClip) -> TextClip:
        """
        Adapt a Project Vine TextClip to a MoviePy TextClip.

        Args:
            text_clip: Project Vine TextClip model

        Returns:
            MoviePy TextClip object
        """
        return self.clip_factory.create_text_clip(text_clip)

    def adapt_video_track(self, video_track: VideoTrack) -> List[ImageClip]:
        """
        Adapt a Project Vine VideoTrack to a list of MoviePy clips.

        Args:
            video_track: Project Vine VideoTrack model

        Returns:
            List of MoviePy ImageClip objects
        """
        moviepy_clips = []

        for clip in video_track.clips:
            if isinstance(clip, VineImageClip):
                moviepy_clip = self.adapt_image_clip(clip)
                moviepy_clips.append(moviepy_clip)
            # Add support for VideoClip when implemented
            # elif isinstance(clip, VineVideoClip):
            #     moviepy_clip = self.adapt_video_clip(clip)
            #     moviepy_clips.append(moviepy_clip)

        return moviepy_clips

    def adapt_audio_track(self, audio_track: AudioTrack) -> List[AudioFileClip]:
        """
        Adapt a Project Vine AudioTrack to a list of MoviePy clips.

        Args:
            audio_track: Project Vine AudioTrack model

        Returns:
            List of MoviePy AudioFileClip objects
        """
        moviepy_clips = []

        for clip in audio_track.clips:
            moviepy_clip = self.adapt_audio_clip(clip)
            moviepy_clips.append(moviepy_clip)

        return moviepy_clips

    def adapt_text_track(self, text_track: TextTrack) -> List[TextClip]:
        """
        Adapt a Project Vine TextTrack to a list of MoviePy clips.

        Args:
            text_track: Project Vine TextTrack model

        Returns:
            List of MoviePy TextClip objects
        """
        moviepy_clips = []

        for clip in text_track.clips:
            moviepy_clip = self.adapt_text_clip(clip)
            moviepy_clips.append(moviepy_clip)

        return moviepy_clips

    def adapt_timeline(self, video_spec: VideoSpec) -> CompositeVideoClip:
        """
        Adapt a Project Vine VideoSpec to a MoviePy CompositeVideoClip.

        Args:
            video_spec: Project Vine VideoSpec model

        Returns:
            MoviePy CompositeVideoClip object
        """
        all_clips = []

        # Convert video tracks
        for track in video_spec.video_tracks:
            if track.visible:
                track_clips = self.adapt_video_track(track)
                all_clips.extend(track_clips)

        # Convert text tracks (overlays)
        for track in video_spec.text_tracks:
            if track.visible:
                track_clips = self.adapt_text_track(track)
                all_clips.extend(track_clips)

        # Create composite video clip
        if all_clips:
            composite = CompositeVideoClip(
                all_clips, size=(video_spec.width, video_spec.height)
            )
        else:
            # Create empty clip if no video content
            from moviepy import ColorClip

            composite = ColorClip(
                size=(video_spec.width, video_spec.height), color=(0, 0, 0)
            )

        return composite

    def adapt_audio_timeline(self, video_spec: VideoSpec) -> Optional[AudioFileClip]:
        """
        Adapt audio tracks to a composite audio clip.

        Args:
            video_spec: Project Vine VideoSpec model

        Returns:
            MoviePy AudioFileClip object or None if no audio
        """
        audio_clips = []

        # Convert music tracks
        for track in video_spec.music_tracks:
            if not track.muted:
                track_clips = self.adapt_audio_track(track)
                audio_clips.extend(track_clips)

        # Convert voice tracks
        for track in video_spec.voice_tracks:
            if not track.muted:
                track_clips = self.adapt_audio_track(track)
                audio_clips.extend(track_clips)

        # Convert SFX tracks
        for track in video_spec.sfx_tracks:
            if not track.muted:
                track_clips = self.adapt_audio_track(track)
                audio_clips.extend(track_clips)

        # Combine audio clips if any exist
        if audio_clips:
            from moviepy import CompositeAudioClip

            return CompositeAudioClip(audio_clips)

        return None
