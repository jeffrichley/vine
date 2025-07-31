"""Adapter pattern for bridging Project Vine models with MoviePy API."""

from moviepy import (
    AudioClip,
    AudioFileClip,
    ColorClip,
    CompositeAudioClip,
    CompositeVideoClip,
    ImageClip,
    TextClip,
    VideoClip,
)

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
    """Adapter for converting Project Vine models to MoviePy clips.

    Implements the Adapter pattern to provide a clean interface between
    our Pydantic models and MoviePy's API, handling the conversion
    and composition logic.
    """

    def __init__(self) -> None:
        """Initialize the adapter with a clip factory."""
        self.clip_factory = ClipFactory()

    def adapt_image_clip(self, image_clip: VineImageClip) -> ImageClip:
        """Adapt a Project Vine ImageClip to a MoviePy ImageClip.

        Args:
            image_clip: Project Vine ImageClip model

        Returns:
            MoviePy ImageClip object
        """
        return self.clip_factory.create_image_clip(image_clip)

    def adapt_audio_clip(self, audio_clip: VineAudioClip) -> AudioFileClip:
        """Adapt a Project Vine AudioClip to a MoviePy AudioFileClip.

        Args:
            audio_clip: Project Vine AudioClip model

        Returns:
            MoviePy AudioFileClip object
        """
        return self.clip_factory.create_audio_clip(audio_clip)

    def adapt_text_clip(self, text_clip: VineTextClip) -> TextClip:
        """Adapt a Project Vine TextClip to a MoviePy TextClip.

        Args:
            text_clip: Project Vine TextClip model

        Returns:
            MoviePy TextClip object
        """
        return self.clip_factory.create_text_clip(text_clip)

    def adapt_video_track(self, video_track: VideoTrack) -> list[VideoClip]:
        """Adapt a Project Vine VideoTrack to a list of MoviePy clips.

        Args:
            video_track: Project Vine VideoTrack model

        Returns:
            List of MoviePy VideoClip objects
        """
        moviepy_clips: list[VideoClip] = []

        for clip in video_track.clips:
            # MoviePy types have Any in their inheritance chain, causing isinstance issues
            if isinstance(clip, VineImageClip):  # type: ignore[misc]
                moviepy_clip = self.adapt_image_clip(clip)
                moviepy_clips.append(moviepy_clip)
            # Add support for VideoClip when implemented
            # elif isinstance(clip, VineVideoClip):
            #     moviepy_clip = self.adapt_video_clip(clip)
            #     moviepy_clips.append(moviepy_clip)

        return moviepy_clips

    def adapt_audio_track(self, audio_track: AudioTrack) -> list[AudioClip]:
        """Adapt a Project Vine AudioTrack to a list of MoviePy clips.

        Args:
            audio_track: Project Vine AudioTrack model

        Returns:
            List of MoviePy AudioClip objects
        """
        moviepy_clips: list[AudioClip] = []

        for clip in audio_track.clips:
            # MoviePy types have Any in their inheritance chain, causing isinstance issues
            if isinstance(clip, VineAudioClip):  # type: ignore[misc]
                moviepy_clip = self.adapt_audio_clip(clip)
                moviepy_clips.append(moviepy_clip)

        return moviepy_clips

    def adapt_text_track(self, text_track: TextTrack) -> list[VideoClip]:
        """Adapt a Project Vine TextTrack to a list of MoviePy clips.

        Args:
            text_track: Project Vine TextTrack model

        Returns:
            List of MoviePy VideoClip objects
        """
        moviepy_clips: list[VideoClip] = []

        for clip in text_track.clips:
            # MoviePy types have Any in their inheritance chain, causing isinstance issues
            if isinstance(clip, VineTextClip):  # type: ignore[misc]
                moviepy_clip = self.adapt_text_clip(clip)
                moviepy_clips.append(moviepy_clip)

        return moviepy_clips

    def adapt_timeline(self, video_spec: VideoSpec) -> VideoClip:
        """Adapt a Project Vine VideoSpec to a MoviePy CompositeVideoClip.

        Args:
            video_spec: Project Vine VideoSpec model

        Returns:
            MoviePy CompositeVideoClip object
        """
        all_clips = []

        # Convert video tracks
        for video_track in video_spec.video_tracks:
            if video_track.visible:
                track_clips = self.adapt_video_track(video_track)
                all_clips.extend(track_clips)

        # Convert text tracks (overlays)
        for text_track in video_spec.text_tracks:
            if text_track.visible:
                track_clips = self.adapt_text_track(text_track)
                all_clips.extend(track_clips)

        # Create composite video clip
        if all_clips:
            return CompositeVideoClip(
                all_clips, size=(video_spec.width, video_spec.height)
            )
        else:
            # Create empty clip if no video content
            return ColorClip(
                size=(video_spec.width, video_spec.height), color=(0, 0, 0)
            )

    def adapt_audio_timeline(self, video_spec: VideoSpec) -> AudioClip | None:
        """Adapt audio tracks to a composite audio clip.

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
            return CompositeAudioClip(audio_clips)

        return None
