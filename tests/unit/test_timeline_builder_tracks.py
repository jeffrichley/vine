"""Unit tests for track-based TimelineBuilder."""

import pytest

from vine.builder.timeline_builder import TimelineBuilder
from vine.models.tracks import AudioClip, ImageClip, TextClip


class TestTimelineBuilderTracks:
    """Test TimelineBuilder with track-based architecture."""

    def test_timeline_builder_initialization(self):
        """Test TimelineBuilder initialization with tracks."""
        builder = TimelineBuilder()

        # Check default tracks are created
        assert len(builder.video_tracks) == 1
        assert len(builder.audio_tracks) == 1
        assert len(builder.text_tracks) == 1

        assert builder.video_tracks[0].name == "video_0"
        assert builder.audio_tracks[0].name == "audio_0"
        assert builder.text_tracks[0].name == "text_0"

        # Check track-specific current times
        assert builder._video_current_time == 0.0
        assert builder._audio_current_time == 0.0
        assert builder._text_current_time == 0.0

    def test_add_image_sequential(self):
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

    def test_add_image_at_explicit(self):
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

        # Check video track current time was updated to reflect the end of the clip
        assert builder._video_current_time == 15.0

    def test_add_text_sequential(self):
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

    def test_add_text_at_explicit(self):
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

        # Check text track current time was updated to reflect the end of the clip
        assert builder._text_current_time == 8.0

    def test_add_voice_sequential(self):
        """Test adding voice in sequential mode."""
        builder = TimelineBuilder()

        builder.add_voice("test_voice.mp3", duration=4.0)

        # Check clip was added to audio track
        assert len(builder.audio_tracks[0].clips) == 1
        clip = builder.audio_tracks[0].clips[0]
        assert isinstance(clip, AudioClip)
        assert clip.path == "test_voice.mp3"
        assert clip.start_time == 0.0
        assert clip.duration == 4.0

        # Check audio track current time was updated
        assert builder._audio_current_time == 4.0

    def test_add_voice_at_explicit(self):
        """Test adding voice with explicit timing."""
        builder = TimelineBuilder()

        builder.add_voice_at("test_voice.mp3", start_time=2.0, duration=4.0)

        # Check clip was added to audio track
        assert len(builder.audio_tracks[0].clips) == 1
        clip = builder.audio_tracks[0].clips[0]
        assert isinstance(clip, AudioClip)
        assert clip.path == "test_voice.mp3"
        assert clip.start_time == 2.0
        assert clip.duration == 4.0

        # Check audio track current time was updated to reflect the end of the clip
        assert builder._audio_current_time == 6.0

    def test_auto_track_creation(self):
        """Test automatic track creation when tracks have overlaps."""
        builder = TimelineBuilder()

        # Add clips that will overlap
        builder.add_image_at("image1.jpg", start_time=0.0, duration=5.0)
        builder.add_image_at(
            "image2.jpg", start_time=2.0, duration=5.0
        )  # Overlaps with image1

        # Should keep clips in the same track (overlaps are allowed)
        assert len(builder.video_tracks) == 1
        assert builder.video_tracks[0].name == "video_0"

        # Check both clips are in the same track
        assert len(builder.video_tracks[0].clips) == 2
        assert builder.video_tracks[0].clips[0].path == "image1.jpg"
        assert builder.video_tracks[0].clips[1].path == "image2.jpg"

        # Track should detect overlaps
        assert builder.video_tracks[0].has_overlapping_clips()

    def test_overlapping_clips_same_track(self):
        """Test that overlapping clips can exist in the same track."""
        builder = TimelineBuilder()

        # Add overlapping clips to same track (explicit timing)
        builder.add_image_at("image1.jpg", start_time=0.0, duration=5.0)
        builder.add_image_at("image2.jpg", start_time=2.0, duration=5.0)

        # Both clips should be in the first track
        assert len(builder.video_tracks) == 1
        assert len(builder.video_tracks[0].clips) == 2

        # Track should detect overlaps
        assert builder.video_tracks[0].has_overlapping_clips()

    def test_dual_mode_timing_combination(self):
        """Test combining sequential and explicit timing modes."""
        builder = TimelineBuilder()

        # Sequential mode
        builder.add_image("image1.jpg", duration=5.0)
        builder.add_text("Text 1", duration=3.0)

        # Explicit mode
        builder.add_image_at("image2.jpg", start_time=10.0, duration=5.0)
        builder.add_text_at("Text 2", start_time=8.0, duration=4.0)

        # Check sequential clips
        assert builder.video_tracks[0].clips[0].start_time == 0.0
        assert (
            builder.text_tracks[0].clips[0].start_time == 0.0
        )  # Text track starts at 0.0

        # Check explicit clips
        assert builder.video_tracks[0].clips[1].start_time == 10.0
        assert builder.text_tracks[0].clips[1].start_time == 8.0

        # Check track-specific current times
        assert builder._video_current_time == 15.0  # 10.0 + 5.0 (from explicit clip)
        assert builder._text_current_time == 12.0  # 8.0 + 4.0 (from explicit clip)
        assert builder._audio_current_time == 0.0  # No audio clips added

    def test_transition_sequential(self):
        """Test adding transition in sequential mode."""
        builder = TimelineBuilder()

        builder.add_image("image1.jpg", duration=5.0)
        builder.add_transition("fade", duration=1.0)

        # Check transition was added
        assert len(builder.transitions) == 1
        transition = builder.transitions[0]
        assert transition.transition_type == "fade"
        assert transition.start_time == 4.0  # 5.0 - 1.0 (overlaps with previous)
        assert transition.duration == 1.0

    def test_transition_at_explicit(self):
        """Test adding transition with explicit timing."""
        builder = TimelineBuilder()

        builder.add_transition_at("crossfade", start_time=5.0, duration=2.0)

        # Check transition was added
        assert len(builder.transitions) == 1
        transition = builder.transitions[0]
        assert transition.transition_type == "crossfade"
        assert transition.start_time == 5.0
        assert transition.duration == 2.0

    def test_build_video_spec(self):
        """Test building VideoSpec from TimelineBuilder."""
        builder = TimelineBuilder(width=1920, height=1080, fps=30)

        # Add some content
        builder.add_image("image1.jpg", duration=5.0)
        builder.add_text("Hello", duration=3.0)
        builder.add_voice("voice1.mp3", duration=4.0)
        builder.add_transition("fade", duration=1.0)

        # Build VideoSpec
        video_spec = builder.build()

        # Check VideoSpec properties
        assert video_spec.width == 1920
        assert video_spec.height == 1080
        assert video_spec.fps == 30

        # Check tracks were transferred
        assert len(video_spec.video_tracks) == 1
        assert len(video_spec.audio_tracks) == 1
        assert len(video_spec.text_tracks) == 1
        assert len(video_spec.transitions) == 1

        # Check clips were transferred
        assert len(video_spec.video_tracks[0].clips) == 1
        assert len(video_spec.audio_tracks[0].clips) == 1
        assert len(video_spec.text_tracks[0].clips) == 1

    def test_get_duration(self):
        """Test getting total duration from all tracks."""
        builder = TimelineBuilder()

        # Add clips with different end times
        builder.add_image_at("image1.jpg", start_time=0.0, duration=5.0)
        builder.add_image_at(
            "image2.jpg", start_time=10.0, duration=8.0
        )  # Ends at 18.0
        builder.add_text_at("text1", start_time=15.0, duration=10.0)  # Ends at 25.0

        duration = builder.get_duration()
        assert duration == 25.0  # Latest end time

    def test_get_track_count(self):
        """Test getting track counts."""
        builder = TimelineBuilder()

        # Add overlapping clips (should stay in same track)
        builder.add_image_at("image1.jpg", start_time=0.0, duration=5.0)
        builder.add_image_at("image2.jpg", start_time=2.0, duration=5.0)

        counts = builder.get_track_count()
        assert counts["video"] == 1  # Should still be 1 track
        assert counts["audio"] == 1
        assert counts["text"] == 1

    def test_get_clip_count(self):
        """Test getting clip counts."""
        builder = TimelineBuilder()

        # Add clips
        builder.add_image("image1.jpg", duration=5.0)
        builder.add_image_at("image2.jpg", start_time=10.0, duration=5.0)
        builder.add_text("text1", duration=3.0)
        builder.add_voice("voice1.mp3", duration=4.0)

        counts = builder.get_clip_count()
        assert counts["video"] == 2
        assert counts["audio"] == 1
        assert counts["text"] == 1

    def test_clear(self):
        """Test clearing all tracks."""
        builder = TimelineBuilder()

        # Add some content
        builder.add_image("image1.jpg", duration=5.0)
        builder.add_text("text1", duration=3.0)
        builder.add_voice("voice1.mp3", duration=4.0)

        # Clear
        builder.clear()

        # Check everything was reset
        assert len(builder.video_tracks) == 1
        assert len(builder.audio_tracks) == 1
        assert len(builder.text_tracks) == 1
        assert len(builder.transitions) == 0

        # Check track-specific current times were reset
        assert builder._video_current_time == 0.0
        assert builder._audio_current_time == 0.0
        assert builder._text_current_time == 0.0

        # Check default tracks are empty
        assert len(builder.video_tracks[0].clips) == 0
        assert len(builder.audio_tracks[0].clips) == 0
        assert len(builder.text_tracks[0].clips) == 0

    def test_validation_errors(self):
        """Test validation errors in clip creation."""
        builder = TimelineBuilder()

        # Test both duration and end_time specified
        with pytest.raises(
            ValueError, match="Cannot specify both duration and end_time"
        ):
            builder.add_image_at(
                "image1.jpg", start_time=0.0, duration=5.0, end_time=10.0
            )

        with pytest.raises(
            ValueError, match="Cannot specify both duration and end_time"
        ):
            builder.add_text_at("text1", start_time=0.0, duration=3.0, end_time=8.0)

        with pytest.raises(
            ValueError, match="Cannot specify both duration and end_time"
        ):
            builder.add_voice_at(
                "voice1.mp3", start_time=0.0, duration=4.0, end_time=12.0
            )
