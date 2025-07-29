"""Video specification models for Project Vine."""

from typing import List, Literal, Optional, Sequence

from pydantic import Field, model_validator

from vine.models.audio_config import MusicConfig, VoiceConfig
from vine.models.base import BaseModel
from vine.models.tracks import AudioTrack, TextTrack, TrackType, VideoTrack
from vine.models.transition import Transition


class VideoSpec(BaseModel):
    """Complete video specification for Project Vine."""

    # Basic metadata
    title: str = Field(..., description="Video title")
    description: Optional[str] = Field(None, description="Video description")
    author: Optional[str] = Field(None, description="Video author")

    # Video settings
    width: int = Field(1920, ge=1, le=7680, description="Video width in pixels")
    height: int = Field(1080, ge=1, le=7680, description="Video height in pixels")
    fps: float = Field(30.0, ge=1.0, le=120.0, description="Frames per second")
    duration: Optional[float] = Field(
        None, ge=0.0, description="Total video duration in seconds"
    )

    # Track-based timeline configuration
    video_tracks: List[VideoTrack] = Field(
        default_factory=lambda: [VideoTrack(name="video_0")], description="Video tracks"
    )
    music_tracks: List[AudioTrack] = Field(
        default_factory=lambda: [AudioTrack(name="music_0")], description="Music tracks"
    )
    voice_tracks: List[AudioTrack] = Field(
        default_factory=lambda: [AudioTrack(name="voice_0")], description="Voice tracks"
    )
    sfx_tracks: List[AudioTrack] = Field(
        default_factory=lambda: [AudioTrack(name="sfx_0")], description="SFX tracks"
    )
    text_tracks: List[TextTrack] = Field(
        default_factory=lambda: [TextTrack(name="text_0")], description="Text tracks"
    )
    transitions: List[Transition] = Field(
        default_factory=list, description="Global transitions"
    )

    # Audio configuration
    voice_config: Optional[VoiceConfig] = Field(
        None, description="Global voice configuration"
    )
    music_config: Optional[MusicConfig] = Field(
        None, description="Global music configuration"
    )

    # Export settings
    output_path: Optional[str] = Field(None, description="Output video file path")
    output_format: Literal["mp4", "avi", "mov", "mkv"] = Field(
        "mp4", description="Output video format"
    )
    quality: Literal["low", "medium", "high", "ultra"] = Field(
        "high", description="Output quality"
    )

    # Advanced settings
    background_color: str = Field(
        "#000000", pattern=r"^#[0-9A-Fa-f]{6}$", description="Background color (hex)"
    )

    @model_validator(mode="after")
    def validate_video_configuration(self) -> "VideoSpec":
        """Sort tracks by z_order for consistent rendering."""
        # Sort tracks by z_order for consistent rendering
        self.video_tracks.sort(key=lambda t: t.z_order)
        self.text_tracks.sort(key=lambda t: t.z_order)

        return self

    def _get_max_end_time_from_clips(self, clips: List) -> float:
        """Get the maximum end time from a list of clips."""
        max_end_time = 0.0
        for clip in clips:
            end_time = clip.get_end_time()
            if end_time is not None:
                max_end_time = max(max_end_time, end_time)
        return max_end_time

    def _get_max_end_time_from_tracks(self, tracks: List) -> float:
        """Get the maximum end time from a list of tracks."""
        max_end_time = 0.0
        for track in tracks:
            track_max = self._get_max_end_time_from_clips(track.clips)
            max_end_time = max(max_end_time, track_max)
        return max_end_time

    def get_total_duration(self) -> float:
        """Calculate total duration from all tracks."""
        max_end_time = 0.0

        # Check video tracks
        video_max = self._get_max_end_time_from_tracks(self.video_tracks)
        max_end_time = max(max_end_time, video_max)

        # Check music tracks
        music_max = self._get_max_end_time_from_tracks(self.music_tracks)
        max_end_time = max(max_end_time, music_max)

        # Check voice tracks
        voice_max = self._get_max_end_time_from_tracks(self.voice_tracks)
        max_end_time = max(max_end_time, voice_max)

        # Check SFX tracks
        sfx_max = self._get_max_end_time_from_tracks(self.sfx_tracks)
        max_end_time = max(max_end_time, sfx_max)

        # Check text tracks
        text_max = self._get_max_end_time_from_tracks(self.text_tracks)
        max_end_time = max(max_end_time, text_max)

        # Check transitions
        transition_max = self._get_max_end_time_from_clips(self.transitions)
        max_end_time = max(max_end_time, transition_max)

        return max_end_time

    def get_active_clips_at_time(self, time: float) -> dict:
        """Get all active clips at the given time, organized by track type."""
        return {
            "video": [
                clip
                for track in self.video_tracks
                for clip in track.get_active_clips_at_time(time)
            ],
            "music": [
                clip
                for track in self.music_tracks
                for clip in track.get_active_clips_at_time(time)
            ],
            "voice": [
                clip
                for track in self.voice_tracks
                for clip in track.get_active_clips_at_time(time)
            ],
            "sfx": [
                clip
                for track in self.sfx_tracks
                for clip in track.get_active_clips_at_time(time)
            ],
            "text": [
                clip
                for track in self.text_tracks
                for clip in track.get_active_clips_at_time(time)
            ],
        }

    def get_transitions_at_time(self, time: float) -> List[Transition]:
        """Get transitions active at the given time."""
        return [trans for trans in self.transitions if trans.is_active_at_time(time)]

    def _get_tracks_by_type(
        self, track_type: TrackType
    ) -> Sequence[VideoTrack | AudioTrack | TextTrack]:
        """Get tracks list by type."""
        if track_type == TrackType.VIDEO:
            return self.video_tracks
        elif track_type == TrackType.MUSIC:
            return self.music_tracks
        elif track_type == TrackType.VOICE:
            return self.voice_tracks
        elif track_type == TrackType.SFX:
            return self.sfx_tracks
        elif track_type == TrackType.TEXT:
            return self.text_tracks
        else:
            raise ValueError(f"Unknown track type: {track_type}")

    def _get_track_list_by_type(
        self, track_type: TrackType
    ) -> List[VideoTrack | AudioTrack | TextTrack]:
        """Get track list by type for modification."""
        if track_type == TrackType.VIDEO:
            return self.video_tracks  # type: ignore[return-value]
        elif track_type == TrackType.MUSIC:
            return self.music_tracks  # type: ignore[return-value]
        elif track_type == TrackType.VOICE:
            return self.voice_tracks  # type: ignore[return-value]
        elif track_type == TrackType.SFX:
            return self.sfx_tracks  # type: ignore[return-value]
        elif track_type == TrackType.TEXT:
            return self.text_tracks  # type: ignore[return-value]
        else:
            raise ValueError(f"Unknown track type: {track_type}")

    def get_track_by_name(
        self, track_name: str, track_type: TrackType = TrackType.VIDEO
    ) -> Optional[VideoTrack | AudioTrack | TextTrack]:
        """Get a track by name and type."""
        tracks = self._get_tracks_by_type(track_type)
        for track in tracks:
            if track.name == track_name:
                return track
        return None

    def add_video_track(self, track: VideoTrack) -> None:
        """Add a video track to the timeline."""
        self.video_tracks.append(track)
        # Sort tracks by z_order for consistent rendering
        self.video_tracks.sort(key=lambda t: t.z_order)

    def add_music_track(self, track: AudioTrack) -> None:
        """Add a music track to the timeline."""
        self.music_tracks.append(track)

    def add_voice_track(self, track: AudioTrack) -> None:
        """Add a voice track to the timeline."""
        self.voice_tracks.append(track)

    def add_sfx_track(self, track: AudioTrack) -> None:
        """Add an SFX track to the timeline."""
        self.sfx_tracks.append(track)

    def add_text_track(self, track: TextTrack) -> None:
        """Add a text track to the timeline."""
        self.text_tracks.append(track)
        # Sort tracks by z_order for consistent rendering
        self.text_tracks.sort(key=lambda t: t.z_order)

    def add_transition(self, transition: Transition) -> None:
        """Add a transition to the timeline."""
        self.transitions.append(transition)

    def remove_track(
        self, track_name: str, track_type: TrackType = TrackType.VIDEO
    ) -> bool:
        """Remove a track by name and type."""
        track_list = self._get_track_list_by_type(track_type)
        for i, track in enumerate(track_list):
            if track.name == track_name:
                track_list.pop(i)
                return True
        return False

    def remove_transition(self, transition_index: int) -> bool:
        """Remove a transition by index."""
        if 0 <= transition_index < len(self.transitions):
            self.transitions.pop(transition_index)
            return True
        return False
