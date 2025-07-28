"""Audio-specific renderer implementation."""

from typing import List, Optional

from moviepy import AudioFileClip, CompositeAudioClip

from vine.models.video_spec import VideoSpec
from vine.rendering.base_renderer import BaseRenderer


class AudioRenderer(BaseRenderer):
    """
    Audio-specific renderer implementation.

    Implements the BaseRenderer template method for audio rendering,
    focusing on audio clips and mixing.
    """

    def create_clips(self, video_spec: VideoSpec) -> List[AudioFileClip]:
        """
        Create audio clips from the video spec.

        Args:
            video_spec: Project Vine VideoSpec model

        Returns:
            List of MoviePy AudioFileClip objects
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

    def compose_clips(
        self, clips: List[AudioFileClip], video_spec: VideoSpec
    ) -> CompositeAudioClip:
        """
        Compose audio clips into a composite audio.

        Args:
            clips: List of MoviePy AudioFileClip objects
            video_spec: Project Vine VideoSpec model

        Returns:
            MoviePy CompositeAudioClip object
        """
        if clips:
            # Create composite from all audio clips
            composite = CompositeAudioClip(clips)
        else:
            # Create silent audio clip if no clips
            from moviepy import AudioClip

            composite = AudioClip(lambda _: 0, duration=video_spec.get_total_duration())

        return composite

    def finalize(
        self, composite: CompositeAudioClip, video_spec: VideoSpec
    ) -> CompositeAudioClip:
        """
        Finalize the audio with additional processing.

        Args:
            composite: MoviePy CompositeAudioClip object
            video_spec: Project Vine VideoSpec model

        Returns:
            Finalized MoviePy CompositeAudioClip object
        """
        # Set duration if specified
        if video_spec.duration is not None:
            composite = composite.set_duration(video_spec.duration)

        return composite

    def render_audio_only(self, video_spec: VideoSpec) -> Optional[AudioFileClip]:
        """
        Render audio only from the video spec.

        Args:
            video_spec: Project Vine VideoSpec model

        Returns:
            MoviePy AudioFileClip object or None if no audio
        """
        clips = self.create_clips(video_spec)

        if not clips:
            return None

        composite = self.compose_clips(clips, video_spec)
        return self.finalize(composite, video_spec)
