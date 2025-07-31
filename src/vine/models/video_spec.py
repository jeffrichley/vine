"""Video specification models for Project Vine."""

from collections.abc import Sequence
from typing import Literal

from pydantic import Field, model_validator

from vine.models.audio_config import MusicConfig, VoiceConfig
from vine.models.base import BaseModel
from vine.models.protocols import HasEndTime
from vine.models.tracks import (
    AudioClip,
    AudioTrack,
    ImageClip,
    TextClip,
    TextTrack,
    TrackType,
    VideoClip,
    VideoTrack,
)
from vine.models.transition import Transition


class VideoSpec(BaseModel):
    """Complete video specification for Project Vine."""

    # Basic metadata
    title: str = Field(..., description="Video title")
    description: str | None = Field(None, description="Video description")
    author: str | None = Field(None, description="Video author")

    # Video settings
    width: int = Field(1920, ge=1, le=7680, description="Video width in pixels")
    height: int = Field(1080, ge=1, le=7680, description="Video height in pixels")
    fps: float = Field(30.0, ge=1.0, le=120.0, description="Frames per second")
    duration: float | None = Field(
        None, ge=0.0, description="Total video duration in seconds"
    )

    # Track-based timeline configuration
    video_tracks: list[VideoTrack] = Field(
        default_factory=lambda: [VideoTrack(name="video_0")], description="Video tracks"
    )
    music_tracks: list[AudioTrack] = Field(
        default_factory=lambda: [AudioTrack(name="music_0")], description="Music tracks"
    )
    voice_tracks: list[AudioTrack] = Field(
        default_factory=lambda: [AudioTrack(name="voice_0")], description="Voice tracks"
    )
    sfx_tracks: list[AudioTrack] = Field(
        default_factory=lambda: [AudioTrack(name="sfx_0")], description="SFX tracks"
    )
    text_tracks: list[TextTrack] = Field(
        default_factory=lambda: [TextTrack(name="text_0")], description="Text tracks"
    )
    transitions: list[Transition] = Field(
        default_factory=list, description="Global transitions"
    )

    # Audio configuration
    voice_config: VoiceConfig | None = Field(
        None, description="Global voice configuration"
    )
    music_config: MusicConfig | None = Field(
        None, description="Global music configuration"
    )

    # Export settings
    output_path: str | None = Field(None, description="Output video file path")
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
        def get_video_z_order(track: VideoTrack) -> int:
            return track.z_order

        def get_text_z_order(track: TextTrack) -> int:
            return track.z_order

        self.video_tracks.sort(key=get_video_z_order)
        self.text_tracks.sort(key=get_text_z_order)

        return self

    def _get_max_end_time_from_clips(self, clips: Sequence[HasEndTime]) -> float:
        """Get the maximum end time from a list of clips."""
        max_end_time = 0.0
        for clip in clips:
            end_time = clip.get_end_time()
            if end_time is not None:
                max_end_time = max(max_end_time, end_time)
        return max_end_time

    def _get_max_end_time_from_tracks(
        self, tracks: Sequence[VideoTrack | AudioTrack | TextTrack]
    ) -> float:
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

    def get_active_clips_at_time(
        self, time: float
    ) -> dict[str, list[VideoClip | ImageClip | AudioClip | TextClip]]:
        """Get all active clips at the given time, organized by track type."""
        result: dict[str, list[VideoClip | ImageClip | AudioClip | TextClip]] = {
            "video": [],
            "music": [],
            "voice": [],
            "sfx": [],
            "text": [],
        }

        self._collect_video_clips(time, result)
        self._collect_music_clips(time, result)
        self._collect_voice_clips(time, result)
        self._collect_sfx_clips(time, result)
        self._collect_text_clips(time, result)

        return result

    def _collect_video_clips(
        self,
        time: float,
        result: dict[str, list[VideoClip | ImageClip | AudioClip | TextClip]],
    ) -> None:
        """Collect active video clips at the given time."""
        for video_track in self.video_tracks:
            for video_clip in video_track.get_active_clips_at_time(time):
                result["video"].append(video_clip)

    def _collect_music_clips(
        self,
        time: float,
        result: dict[str, list[VideoClip | ImageClip | AudioClip | TextClip]],
    ) -> None:
        """Collect active music clips at the given time."""
        for music_track in self.music_tracks:
            for music_clip in music_track.get_active_clips_at_time(time):
                result["music"].append(music_clip)

    def _collect_voice_clips(
        self,
        time: float,
        result: dict[str, list[VideoClip | ImageClip | AudioClip | TextClip]],
    ) -> None:
        """Collect active voice clips at the given time."""
        for voice_track in self.voice_tracks:
            for voice_clip in voice_track.get_active_clips_at_time(time):
                result["voice"].append(voice_clip)

    def _collect_sfx_clips(
        self,
        time: float,
        result: dict[str, list[VideoClip | ImageClip | AudioClip | TextClip]],
    ) -> None:
        """Collect active SFX clips at the given time."""
        for sfx_track in self.sfx_tracks:
            for sfx_clip in sfx_track.get_active_clips_at_time(time):
                result["sfx"].append(sfx_clip)

    def _collect_text_clips(
        self,
        time: float,
        result: dict[str, list[VideoClip | ImageClip | AudioClip | TextClip]],
    ) -> None:
        """Collect active text clips at the given time."""
        for text_track in self.text_tracks:
            for text_clip in text_track.get_active_clips_at_time(time):
                result["text"].append(text_clip)

    def get_transitions_at_time(self, time: float) -> list[Transition]:
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
        else:  # pragma: no cover  # we are putting this here only for when and if we are adding new track types
            raise ValueError(f"Unknown track type: {track_type}")

    def get_track_by_name(
        self, track_name: str, track_type: TrackType = TrackType.VIDEO
    ) -> VideoTrack | AudioTrack | TextTrack | None:
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
        def get_video_z_order(track: VideoTrack) -> int:
            return track.z_order

        self.video_tracks.sort(key=get_video_z_order)

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
        def get_text_z_order(track: TextTrack) -> int:
            return track.z_order

        self.text_tracks.sort(key=get_text_z_order)

    def add_transition(self, transition: Transition) -> None:
        """Add a transition to the timeline."""
        self.transitions.append(transition)

    def remove_video_track(self, track_name: str) -> bool:
        """Remove a video track by name."""
        for i, track in enumerate(self.video_tracks):
            if track.name == track_name:
                self.video_tracks.pop(i)
                return True
        return False

    def remove_music_track(self, track_name: str) -> bool:
        """Remove a music track by name."""
        for i, track in enumerate(self.music_tracks):
            if track.name == track_name:
                self.music_tracks.pop(i)
                return True
        return False

    def remove_voice_track(self, track_name: str) -> bool:
        """Remove a voice track by name."""
        for i, track in enumerate(self.voice_tracks):
            if track.name == track_name:
                self.voice_tracks.pop(i)
                return True
        return False

    def remove_sfx_track(self, track_name: str) -> bool:
        """Remove an SFX track by name."""
        for i, track in enumerate(self.sfx_tracks):
            if track.name == track_name:
                self.sfx_tracks.pop(i)
                return True
        return False

    def remove_text_track(self, track_name: str) -> bool:
        """Remove a text track by name."""
        for i, track in enumerate(self.text_tracks):
            if track.name == track_name:
                self.text_tracks.pop(i)
                return True
        return False

    def remove_track(
        self, track_name: str, track_type: TrackType = TrackType.VIDEO
    ) -> bool:
        """Remove a track by name and type (legacy method for backward compatibility)."""
        if track_type == TrackType.VIDEO:
            return self.remove_video_track(track_name)
        elif track_type == TrackType.MUSIC:
            return self.remove_music_track(track_name)
        elif track_type == TrackType.VOICE:
            return self.remove_voice_track(track_name)
        elif track_type == TrackType.SFX:
            return self.remove_sfx_track(track_name)
        elif track_type == TrackType.TEXT:
            return self.remove_text_track(track_name)
        else:
            # This branch is intentionally excluded from coverage as it's defensive code
            # that should only be reached if a new TrackType is added to the enum but
            # the corresponding removal logic is not implemented in this method.
            # It serves as a safety net to catch missing implementations during development.
            raise ValueError(f"Unknown track type: {track_type}")  # pragma: no cover

    def remove_transition(self, transition_index: int) -> bool:
        """Remove a transition by index."""
        if 0 <= transition_index < len(self.transitions):
            self.transitions.pop(transition_index)
            return True
        return False
