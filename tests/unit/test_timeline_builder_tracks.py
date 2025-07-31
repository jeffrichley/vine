"""Unit tests for track-based TimelineBuilder."""

import pytest

from vine.builder.timeline_builder import TimelineBuilder
from vine.models.tracks import AudioClip, ImageClip, TextClip
from vine.models.transition import TransitionType


class TestTimelineBuilderTracks:
    """Test TimelineBuilder with track-based architecture."""

    @pytest.mark.unit
    def test_timeline_builder_initialization(self) -> None:
        """Test TimelineBuilder initialization with tracks."""
        builder = TimelineBuilder()
        # Check default tracks are created
        assert len(builder.video_tracks) == 1
        assert len(builder.music_tracks) == 1
        assert len(builder.voice_tracks) == 1
        assert len(builder.sfx_tracks) == 1
        assert len(builder.text_tracks) == 1
        assert builder.video_tracks[0].name == "video_0"
        assert builder.music_tracks[0].name == "music_0"
        assert builder.voice_tracks[0].name == "voice_0"
        assert builder.sfx_tracks[0].name == "sfx_0"
        assert builder.text_tracks[0].name == "text_0"
        # Check track-specific current times
        assert builder._video_current_time == 0.0
        assert builder._music_current_time == 0.0
        assert builder._voice_current_time == 0.0
        assert builder._sfx_current_time == 0.0
        assert builder._text_current_time == 0.0

    @pytest.mark.unit
    def test_initialization_with_custom_parameters(self) -> None:
        """Test TimelineBuilder initialization with custom parameters."""
        builder = TimelineBuilder(width=1280, height=720, fps=60)
        assert builder.width == 1280
        assert builder.height == 720
        assert builder.fps == 60
        # Check default tracks are created
        assert len(builder.video_tracks) == 1
        assert len(builder.music_tracks) == 1
        assert len(builder.voice_tracks) == 1
        assert len(builder.sfx_tracks) == 1
        assert len(builder.text_tracks) == 1
        # Check track names
        assert builder.video_tracks[0].name == "video_0"
        assert builder.music_tracks[0].name == "music_0"
        assert builder.voice_tracks[0].name == "voice_0"
        assert builder.sfx_tracks[0].name == "sfx_0"
        assert builder.text_tracks[0].name == "text_0"

    @pytest.mark.unit
    def test_add_image_sequential(self) -> None:
        """Test adding image in sequential mode."""
        builder = TimelineBuilder()
        builder.add_image("test_image.jpg", duration=5.0)
        # Check clip was added to video track
        assert len(builder.video_tracks[0].clips) == 1
        clip = builder.video_tracks[0].clips[0]
        assert isinstance(clip, ImageClip)
        assert clip.path == "test_image.jpg"
        assert clip.start_time == 0.0
        assert clip.duration == 5.0
        # Check video track current time was updated
        assert builder._video_current_time == 5.0

    @pytest.mark.unit
    def test_add_image_at_explicit(self) -> None:
        """Test adding image with explicit timing."""
        builder = TimelineBuilder()
        builder.add_image_at("test_image.jpg", start_time=10.0, duration=5.0)
        # Check clip was added to video track
        assert len(builder.video_tracks[0].clips) == 1
        clip = builder.video_tracks[0].clips[0]
        assert isinstance(clip, ImageClip)
        assert clip.path == "test_image.jpg"
        assert clip.start_time == 10.0
        assert clip.duration == 5.0
        # Check video track current time was NOT updated in explicit mode
        assert builder._video_current_time == 0.0

    @pytest.mark.unit
    def test_add_text_sequential(self) -> None:
        """Test adding text in sequential mode."""
        builder = TimelineBuilder()
        builder.add_text("Hello World", duration=3.0)
        # Check clip was added to text track
        assert len(builder.text_tracks[0].clips) == 1
        clip = builder.text_tracks[0].clips[0]
        assert isinstance(clip, TextClip)
        assert clip.content == "Hello World"
        assert clip.start_time == 0.0
        assert clip.duration == 3.0
        # Check text track current time was updated
        assert builder._text_current_time == 3.0

    @pytest.mark.unit
    def test_add_text_at_explicit(self) -> None:
        """Test adding text with explicit timing."""
        builder = TimelineBuilder()
        builder.add_text_at("Hello World", start_time=5.0, duration=3.0)
        # Check clip was added to text track
        assert len(builder.text_tracks[0].clips) == 1
        clip = builder.text_tracks[0].clips[0]
        assert isinstance(clip, TextClip)
        assert clip.content == "Hello World"
        assert clip.start_time == 5.0
        assert clip.duration == 3.0
        # Check text track current time was NOT updated in explicit mode
        assert builder._text_current_time == 0.0

    @pytest.mark.unit
    def test_add_voice_sequential(self) -> None:
        """Test adding voice in sequential mode."""
        builder = TimelineBuilder()
        builder.add_voice("test_voice.mp3", duration=4.0)
        # Check clip was added to voice track
        assert len(builder.voice_tracks[0].clips) == 1
        clip = builder.voice_tracks[0].clips[0]
        assert isinstance(clip, AudioClip)
        assert clip.path == "test_voice.mp3"
        assert clip.start_time == 0.0
        assert clip.duration == 4.0
        # Check voice track current time was updated
        assert builder._voice_current_time == 4.0

    @pytest.mark.unit
    def test_add_voice_at_explicit(self) -> None:
        """Test adding voice with explicit timing."""
        builder = TimelineBuilder()
        builder.add_voice_at("test_voice.mp3", start_time=2.0, duration=4.0)
        # Check clip was added to voice track
        assert len(builder.voice_tracks[0].clips) == 1
        clip = builder.voice_tracks[0].clips[0]
        assert isinstance(clip, AudioClip)
        assert clip.path == "test_voice.mp3"
        assert clip.start_time == 2.0
        assert clip.duration == 4.0
        # Check voice track current time was NOT updated in explicit mode
        assert builder._voice_current_time == 0.0

    @pytest.mark.unit
    def test_auto_track_creation(self) -> None:
        """Test automatic track creation when needed."""
        builder = TimelineBuilder()
        # Add multiple clips to force track creation
        builder.add_image("image1.jpg", duration=5.0)
        builder.add_image("image2.jpg", duration=5.0)
        builder.add_text("text1", duration=3.0)
        builder.add_text("text2", duration=3.0)
        # Should have created additional tracks
        assert len(builder.video_tracks) >= 1
        assert len(builder.text_tracks) >= 1
        # Check clips are distributed across tracks
        total_video_clips = sum(len(track.clips) for track in builder.video_tracks)
        total_text_clips = sum(len(track.clips) for track in builder.text_tracks)
        assert total_video_clips == 2
        assert total_text_clips == 2

    @pytest.mark.unit
    def test_overlapping_clips_same_track(self) -> None:
        """Test handling of overlapping clips on the same track."""
        builder = TimelineBuilder()
        # Add overlapping clips
        builder.add_image_at("image1.jpg", start_time=0.0, duration=5.0)
        builder.add_image_at("image2.jpg", start_time=2.0, duration=5.0)
        # Both clips should be on the same track
        assert len(builder.video_tracks[0].clips) == 2
        assert builder.video_tracks[0].clips[0].start_time == 0.0
        assert builder.video_tracks[0].clips[1].start_time == 2.0

    @pytest.mark.unit
    def test_dual_mode_timing_combination(self) -> None:
        """Test combining sequential and explicit timing modes."""
        builder = TimelineBuilder()
        # Sequential mode
        builder.add_image("image1.jpg", duration=5.0)
        builder.add_text("text1", duration=3.0)
        # Explicit mode
        builder.add_image_at("image2.jpg", start_time=10.0, duration=5.0)
        builder.add_text_at("text2", start_time=12.0, duration=3.0)
        # Check sequential clips
        assert builder.video_tracks[0].clips[0].start_time == 0.0
        assert builder.text_tracks[0].clips[0].start_time == 0.0
        # Check explicit clips
        assert builder.video_tracks[0].clips[1].start_time == 10.0
        assert builder.text_tracks[0].clips[1].start_time == 12.0
        # Check current times (only sequential should update)
        assert builder._video_current_time == 5.0
        assert builder._text_current_time == 3.0

    @pytest.mark.unit
    def test_transition_sequential(self) -> None:
        """Test adding transition in sequential mode."""
        builder = TimelineBuilder()
        builder.add_image("image1.jpg", duration=5.0)
        builder.add_transition(TransitionType.FADE, duration=1.0)
        assert len(builder.transitions) == 1
        transition = builder.transitions[0]
        assert transition.transition_type == TransitionType.FADE
        assert transition.duration == 1.0
        assert transition.start_time == 4.0  # Overlaps with previous clip (5.0 - 1.0)

    @pytest.mark.unit
    def test_transition_at_explicit(self) -> None:
        """Test adding transition with explicit timing."""
        builder = TimelineBuilder()
        builder.add_transition_at(TransitionType.FADE, start_time=10.0, duration=1.0)
        assert len(builder.transitions) == 1
        transition = builder.transitions[0]
        assert transition.transition_type == TransitionType.FADE
        assert transition.duration == 1.0
        assert transition.start_time == 10.0

    @pytest.mark.unit
    def test_build_video_spec(self) -> None:
        """Test building VideoSpec from TimelineBuilder."""
        builder = TimelineBuilder(width=1920, height=1080, fps=30)
        # Add content
        builder.add_image("image1.jpg", duration=5.0)
        builder.add_text("Hello", duration=3.0)
        builder.add_voice("voice1.mp3", duration=4.0)
        builder.add_transition(TransitionType.FADE, duration=1.0)
        # Build VideoSpec
        video_spec = builder.build()
        # Check VideoSpec properties
        assert video_spec.width == 1920
        assert video_spec.height == 1080
        assert video_spec.fps == 30
        # Check tracks
        assert len(video_spec.video_tracks) == 1
        assert len(video_spec.text_tracks) == 1
        assert len(video_spec.voice_tracks) == 1
        # Check clips
        assert len(video_spec.video_tracks[0].clips) == 1
        assert len(video_spec.text_tracks[0].clips) == 1
        assert len(video_spec.voice_tracks[0].clips) == 1
        # Check transitions
        assert len(video_spec.transitions) == 1

    @pytest.mark.unit
    def test_get_duration(self) -> None:
        """Test getting total duration of timeline."""
        builder = TimelineBuilder()
        builder.add_image("image1.jpg", duration=5.0)
        builder.add_text("text1", duration=3.0)
        builder.add_voice("voice1.mp3", duration=4.0)
        duration = builder.get_duration()
        assert duration == 5.0  # Should be the longest track

    @pytest.mark.unit
    def test_get_track_count(self) -> None:
        """Test getting track counts."""
        builder = TimelineBuilder()
        counts = builder.get_track_count()
        assert counts["video"] == 1
        assert counts["music"] == 1
        assert counts["voice"] == 1
        assert counts["sfx"] == 1
        assert counts["text"] == 1

    @pytest.mark.unit
    def test_get_clip_count(self) -> None:
        """Test getting clip counts."""
        builder = TimelineBuilder()
        builder.add_image("image1.jpg", duration=5.0)
        builder.add_text("text1", duration=3.0)
        builder.add_voice("voice1.mp3", duration=4.0)
        counts = builder.get_clip_count()
        assert counts["video"] == 1
        assert counts["text"] == 1
        assert counts["voice"] == 1
        assert counts["music"] == 0
        assert counts["sfx"] == 0

    @pytest.mark.unit
    def test_clear(self) -> None:
        """Test clearing all content from TimelineBuilder."""
        builder = TimelineBuilder()
        # Add content
        builder.add_image("image1.jpg", duration=5.0)
        builder.add_text("text1", duration=3.0)
        builder.add_voice("voice1.mp3", duration=4.0)
        builder.add_transition(TransitionType.FADE, duration=1.0)
        # Clear everything
        builder.clear()
        # Check all tracks are empty
        assert len(builder.video_tracks[0].clips) == 0
        assert len(builder.text_tracks[0].clips) == 0
        assert len(builder.voice_tracks[0].clips) == 0
        assert len(builder.music_tracks[0].clips) == 0
        assert len(builder.sfx_tracks[0].clips) == 0
        # Check current times are reset
        assert builder._video_current_time == 0.0
        assert builder._text_current_time == 0.0
        assert builder._voice_current_time == 0.0
        assert builder._music_current_time == 0.0
        assert builder._sfx_current_time == 0.0
        # Check transitions are cleared
        assert len(builder.transitions) == 0
        # Check clip counts are zero
        counts = builder.get_clip_count()
        assert all(count == 0 for count in counts.values())

    @pytest.mark.unit
    def test_validation_errors(self) -> None:
        """Test validation error handling."""
        builder = TimelineBuilder()
        # Test invalid duration
        with pytest.raises(ValueError):
            builder.add_image("image1.jpg", duration=-1.0)
        # Test invalid start time
        with pytest.raises(ValueError):
            builder.add_image_at("image1.jpg", start_time=-1.0, duration=5.0)
        # Test invalid transition duration
        with pytest.raises(ValueError):
            builder.add_transition(TransitionType.FADE, duration=-1.0)

    @pytest.mark.unit
    def test_professional_audio_controls(self) -> None:
        """Test professional audio control features."""
        builder = TimelineBuilder()
        # Test basic voice addition (audio controls are handled in the context)
        builder.add_voice("voice1.mp3", duration=5.0)
        clip = builder.voice_tracks[0].clips[0]
        assert clip.path == "voice1.mp3"
        assert clip.duration == 5.0
        # Test basic voice addition with different duration
        builder.add_voice("voice2.mp3", duration=3.0)
        clip = builder.voice_tracks[0].clips[1]
        assert clip.path == "voice2.mp3"
        assert clip.duration == 3.0
        # Test basic voice addition with no duration
        builder.add_voice("voice3.mp3")
        clip = builder.voice_tracks[0].clips[2]
        assert clip.path == "voice3.mp3"
        assert clip.duration is None
