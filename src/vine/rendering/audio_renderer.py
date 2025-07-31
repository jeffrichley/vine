"""Audio-specific renderer implementation."""

from abc import ABC, abstractmethod

from moviepy import AudioClip, CompositeAudioClip

from vine.models.video_spec import VideoSpec
from vine.rendering.moviepy_adapter import MoviePyAdapter


class AudioRendererBase(ABC):
    """
    Abstract base class for audio rendering algorithms.
    """

    def __init__(self) -> None:
        """Initialize the renderer with an adapter."""
        self.adapter = MoviePyAdapter()

    @abstractmethod
    def create_clips(self, video_spec: VideoSpec) -> list[AudioClip]:
        """Create audio clips from the video spec."""
        pass

    @abstractmethod
    def compose_clips(self, clips: list[AudioClip], video_spec: VideoSpec) -> AudioClip:
        """Compose audio clips into a final audio."""
        pass

    def finalize(self, composite: AudioClip, video_spec: VideoSpec) -> AudioClip:
        """Finalize the audio with additional processing."""
        # Set duration if specified
        if video_spec.duration is not None:
            return composite.set_duration(video_spec.duration)

        # Audio clips don't have FPS like video clips
        # If we need to set FPS for audio, we'll need to implement this
        # For now, we'll just return the composite as-is
        return composite


class AudioRenderer(AudioRendererBase):
    """
    Audio-specific renderer implementation.

    Implements the BaseRenderer template method for audio rendering,
    focusing on audio clips and mixing.
    """

    def create_clips(self, video_spec: VideoSpec) -> list[AudioClip]:
        """
        Create audio clips from the video spec.

        Args:
            video_spec: Project Vine VideoSpec model

        Returns:
            List of MoviePy AudioClip objects
        """
        clips = []

        # Create clips from music tracks
        for track in video_spec.music_tracks:
            if not track.muted:
                track_clips = self.adapter.adapt_audio_track(track)
                clips.extend(track_clips)

        # Create clips from voice tracks
        for track in video_spec.voice_tracks:
            if not track.muted:
                track_clips = self.adapter.adapt_audio_track(track)
                clips.extend(track_clips)

        # Create clips from SFX tracks
        for track in video_spec.sfx_tracks:
            if not track.muted:
                track_clips = self.adapter.adapt_audio_track(track)
                clips.extend(track_clips)

        return clips

    def compose_clips(self, clips: list[AudioClip], video_spec: VideoSpec) -> AudioClip:
        """
        Compose audio clips into a composite audio.

        Args:
            clips: List of MoviePy AudioClip objects
            video_spec: Project Vine VideoSpec model

        Returns:
            MoviePy AudioClip object
        """
        # Create composite from all audio clips or silent clip
        if clips:
            composite_result: AudioClip = CompositeAudioClip(clips)
        else:
            # MoviePy AudioClip constructor expects a callable with Any type due to library typing
            composite_result = AudioClip(
                lambda _: 0, duration=video_spec.get_total_duration()  # type: ignore[misc]
            )

        return composite_result

    def finalize(self, composite: AudioClip, video_spec: VideoSpec) -> AudioClip:
        """
        Finalize the audio with additional processing.

        Args:
            composite: MoviePy CompositeAudioClip object
            video_spec: Project Vine VideoSpec model

        Returns:
            Finalized MoviePy AudioClip object
        """
        # Set duration if specified
        if video_spec.duration is not None:
            final_composite: AudioClip = composite.set_duration(video_spec.duration)
        else:
            final_composite = composite

        return final_composite

    def render_audio_only(self, video_spec: VideoSpec) -> AudioClip | None:
        """
        Render audio only from the video spec.

        Args:
            video_spec: Project Vine VideoSpec model

        Returns:
            MoviePy AudioClip object or None if no audio
        """
        clips = self.create_clips(video_spec)

        if not clips:
            return None

        result = self.compose_clips(clips, video_spec)
        return self.finalize(result, video_spec)
