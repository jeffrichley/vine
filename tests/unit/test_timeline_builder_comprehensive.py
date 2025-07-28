#!/usr/bin/env python3
"""
Comprehensive tests for TimelineBuilder functionality.

This module tests all major features of the TimelineBuilder class including
sequential and explicit timing modes, track management, and edge cases.
"""

from pathlib import Path
from typing import Any

import pytest

from vine.builder.timeline_builder import TimelineBuilder
from vine.models.video_spec import VideoSpec


def safe_assert(condition: Any, message: str = "") -> None:
    """Assert that helps mypy understand control flow."""
    assert condition, message


class TestTimelineBuilderComprehensive:
    """Comprehensive tests for TimelineBuilder functionality."""

    def test_initialization_with_custom_parameters(self):
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

    def test_sequential_mode_without_duration(self):
        """Test sequential mode when duration is not specified."""
        builder = TimelineBuilder()

        # Add clips without duration
        builder.add_image("test_image.jpg")
        builder.add_text("Test text")
        builder.add_voice("test_voice.mp3")

        # Check clips were added with start_time but no duration
        assert len(builder.video_tracks[0].clips) == 1
        assert len(builder.text_tracks[0].clips) == 1
        assert len(builder.voice_tracks[0].clips) == 1

        # Check start times
        assert builder.video_tracks[0].clips[0].start_time == 0.0
        assert builder.text_tracks[0].clips[0].start_time == 0.0
        assert builder.voice_tracks[0].clips[0].start_time == 0.0

        # Check durations are None
        assert builder.video_tracks[0].clips[0].duration is None
        assert builder.text_tracks[0].clips[0].duration is None
        assert builder.voice_tracks[0].clips[0].duration is None

        # Check current times were updated to start_time (no duration specified)
        assert builder._video_current_time == 0.0
        assert builder._text_current_time == 0.0
        assert builder._voice_current_time == 0.0

    def test_explicit_timing_with_end_time(self):
        """Test explicit timing using end_time instead of duration."""
        builder = TimelineBuilder()

        builder.add_image_at("image1.jpg", start_time=5.0, end_time=10.0)
        builder.add_text_at("text1", start_time=2.0, end_time=7.0)
        builder.add_voice_at("voice1.mp3", start_time=0.0, end_time=8.0)

        # Check durations were calculated correctly
        assert builder.video_tracks[0].clips[0].duration == 5.0  # 10.0 - 5.0
        assert builder.text_tracks[0].clips[0].duration == 5.0  # 7.0 - 2.0
        assert builder.voice_tracks[0].clips[0].duration == 8.0  # 8.0 - 0.0

        # Check current times were updated to end times
        assert builder._video_current_time == 10.0
        assert builder._text_current_time == 7.0
        assert builder._voice_current_time == 8.0

    def test_explicit_timing_without_duration_or_end_time(self):
        """Test explicit timing without duration or end_time."""
        builder = TimelineBuilder()

        builder.add_image_at("image1.jpg", start_time=5.0)
        builder.add_text_at("text1", start_time=2.0)
        builder.add_voice_at("voice1.mp3", start_time=0.0)

        # Check clips were added with start_time but no duration
        assert builder.video_tracks[0].clips[0].start_time == 5.0
        assert builder.video_tracks[0].clips[0].duration is None
        assert builder.text_tracks[0].clips[0].start_time == 2.0
        assert builder.text_tracks[0].clips[0].duration is None
        assert builder.voice_tracks[0].clips[0].start_time == 0.0
        assert builder.voice_tracks[0].clips[0].duration is None

        # Check current times were updated to start_time (no duration)
        assert builder._video_current_time == 5.0
        assert builder._text_current_time == 2.0
        assert builder._voice_current_time == 0.0

    def test_validation_errors_duration_and_end_time(self):
        """Test validation errors when both duration and end_time are specified."""
        builder = TimelineBuilder()

        # Test all three clip types
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

    def test_auto_track_creation_with_overlaps(self):
        """Test automatic track creation when tracks have overlapping clips."""
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

    def test_auto_track_creation_voice_tracks(self):
        """Test automatic track creation for voice tracks."""
        builder = TimelineBuilder()

        # Add overlapping voice clips
        builder.add_voice_at("voice1.mp3", start_time=0.0, duration=5.0)
        builder.add_voice_at("voice2.mp3", start_time=2.0, duration=5.0)  # Overlaps

        # Should keep clips in the same track (overlaps are allowed)
        assert len(builder.voice_tracks) == 1
        assert builder.voice_tracks[0].name == "voice_0"

        # Check both clips are in the same track
        assert len(builder.voice_tracks[0].clips) == 2
        assert builder.voice_tracks[0].clips[0].path == "voice1.mp3"
        assert builder.voice_tracks[0].clips[1].path == "voice2.mp3"

        # Track should detect overlaps
        assert builder.voice_tracks[0].has_overlapping_clips()

    def test_auto_track_creation_text_tracks(self):
        """Test automatic track creation for text tracks."""
        builder = TimelineBuilder()

        # Add overlapping text clips
        builder.add_text_at("text1", start_time=0.0, duration=5.0)
        builder.add_text_at("text2", start_time=2.0, duration=5.0)  # Overlaps

        # Should keep clips in the same track (overlaps are allowed)
        assert len(builder.text_tracks) == 1
        assert builder.text_tracks[0].name == "text_0"

        # Check both clips are in the same track
        assert len(builder.text_tracks[0].clips) == 2
        assert builder.text_tracks[0].clips[0].content == "text1"
        assert builder.text_tracks[0].clips[1].content == "text2"

        # Track should detect overlaps
        assert builder.text_tracks[0].has_overlapping_clips()

    def test_sequential_mode_track_specific_timing(self):
        """Test that sequential mode maintains separate timing for each track type."""
        builder = TimelineBuilder()

        # Add clips in different order to test track-specific timing
        builder.add_image("image1.jpg", duration=5.0)  # Video: 0.0 -> 5.0
        builder.add_text("text1", duration=3.0)  # Text: 0.0 -> 3.0
        builder.add_voice("voice1.mp3", duration=4.0)  # Audio: 0.0 -> 4.0
        builder.add_text("text2", duration=2.0)  # Text: 3.0 -> 5.0
        builder.add_image("image2.jpg", duration=3.0)  # Video: 5.0 -> 8.0

        # Check video track
        assert len(builder.video_tracks[0].clips) == 2
        assert builder.video_tracks[0].clips[0].start_time == 0.0
        assert builder.video_tracks[0].clips[0].duration == 5.0
        assert builder.video_tracks[0].clips[1].start_time == 5.0
        assert builder.video_tracks[0].clips[1].duration == 3.0

        # Check text track
        assert len(builder.text_tracks[0].clips) == 2
        assert builder.text_tracks[0].clips[0].start_time == 0.0
        assert builder.text_tracks[0].clips[0].duration == 3.0
        assert builder.text_tracks[0].clips[1].start_time == 3.0
        assert builder.text_tracks[0].clips[1].duration == 2.0

        # Check voice track
        assert len(builder.voice_tracks[0].clips) == 1
        assert builder.voice_tracks[0].clips[0].start_time == 0.0
        assert builder.voice_tracks[0].clips[0].duration == 4.0

        # Check current times
        assert builder._video_current_time == 8.0  # 5.0 + 3.0
        assert builder._text_current_time == 5.0  # 3.0 + 2.0
        assert builder._voice_current_time == 4.0  # 0.0 + 4.0

    def test_transition_sequential_mode_timing(self):
        """Test transition timing in sequential mode."""
        builder = TimelineBuilder()

        # Add content first
        builder.add_image("image1.jpg", duration=5.0)
        builder.add_text("text1", duration=3.0)
        builder.add_voice("voice1.mp3", duration=4.0)

        # Add transition
        builder.add_transition("fade", duration=1.0)

        # Check transition timing
        assert len(builder.transitions) == 1
        transition = builder.transitions[0]
        assert transition.transition_type == "fade"
        assert transition.duration == 1.0

        # Transition should start at max current time minus duration
        # max(5.0, 3.0, 4.0) = 5.0, so start_time = 5.0 - 1.0 = 4.0
        assert transition.start_time == 4.0

    def test_transition_explicit_mode(self):
        """Test transition with explicit timing."""
        builder = TimelineBuilder()

        builder.add_transition_at("crossfade", start_time=10.0, duration=2.0)

        assert len(builder.transitions) == 1
        transition = builder.transitions[0]
        assert transition.transition_type == "crossfade"
        assert transition.start_time == 10.0
        assert transition.duration == 2.0

    def test_transition_with_kwargs(self):
        """Test transition with additional parameters."""
        builder = TimelineBuilder()

        builder.add_transition_at(
            "slide",
            start_time=5.0,
            duration=1.5,
            direction="left",
            easing="ease_in_out",
            from_tracks=["video_0"],
            to_tracks=["video_1"],
        )

        assert len(builder.transitions) == 1
        transition = builder.transitions[0]
        assert transition.transition_type == "slide"
        assert transition.start_time == 5.0
        assert transition.duration == 1.5
        assert transition.direction == "left"
        assert transition.easing == "ease_in_out"
        assert transition.from_tracks == ["video_0"]
        assert transition.to_tracks == ["video_1"]

    def test_clip_properties_passed_through(self):
        """Test that clip properties are passed through correctly."""
        builder = TimelineBuilder()

        # Test image clip with properties
        builder.add_image_at(
            "image1.jpg",
            start_time=0.0,
            duration=5.0,
            width=800,
            height=600,
            x_position=100.0,
            y_position=50.0,
            opacity=0.8,
        )

        clip = builder.video_tracks[0].clips[0]
        assert clip.width == 800
        assert clip.height == 600
        assert clip.x_position == 100.0
        assert clip.y_position == 50.0
        assert clip.opacity == 0.8

        # Test text clip with properties
        builder.add_text_at(
            "Hello World",
            start_time=0.0,
            duration=3.0,
            font_size=24,
            font_color="#FF0000",
            font_family="Times New Roman",
            x_position=200.0,
            y_position=100.0,
            alignment="center",
        )

        text_clip = builder.text_tracks[0].clips[0]
        assert text_clip.font_size == 24
        assert text_clip.font_color == "#FF0000"
        assert text_clip.font_family == "Times New Roman"
        assert text_clip.x_position == 200.0
        assert text_clip.y_position == 100.0
        assert text_clip.alignment == "center"

        # Test audio clip with properties
        builder.add_voice_at(
            "voice1.mp3",
            start_time=0.0,
            duration=4.0,
            volume=0.8,
            fade_in=0.5,
            fade_out=1.0,
        )

        voice_clip = builder.voice_tracks[0].clips[0]
        assert voice_clip.volume == 0.8
        assert voice_clip.fade_in == 0.5
        assert voice_clip.fade_out == 1.0

    def test_pathlib_path_support(self):
        """Test that Path objects are supported for file paths."""
        builder = TimelineBuilder()

        image_path = Path("test_image.jpg")
        voice_path = Path("test_voice.mp3")

        builder.add_image_at(image_path, start_time=0.0, duration=5.0)
        builder.add_voice_at(voice_path, start_time=0.0, duration=4.0)

        # Check paths were converted to strings
        assert builder.video_tracks[0].clips[0].path == "test_image.jpg"
        assert builder.voice_tracks[0].clips[0].path == "test_voice.mp3"

    def test_get_duration_with_no_clips(self):
        """Test get_duration when no clips are present."""
        builder = TimelineBuilder()

        duration = builder.get_duration()
        assert duration == 0.0

    def test_get_duration_with_clips_no_duration(self):
        """Test get_duration when clips have no duration specified."""
        builder = TimelineBuilder()

        builder.add_image_at("image1.jpg", start_time=5.0)  # No duration
        builder.add_text_at("text1", start_time=10.0)  # No duration

        duration = builder.get_duration()
        assert duration == 0.0  # No duration clips are ignored in get_duration()

    def test_get_duration_with_mixed_clips(self):
        """Test get_duration with clips that have and don't have durations."""
        builder = TimelineBuilder()

        builder.add_image_at("image1.jpg", start_time=0.0, duration=5.0)  # Ends at 5.0
        builder.add_image_at(
            "image2.jpg", start_time=10.0
        )  # No duration, start at 10.0
        builder.add_text_at("text1", start_time=15.0, duration=8.0)  # Ends at 23.0
        builder.add_voice_at(
            "voice1.mp3", start_time=20.0, duration=5.0
        )  # Ends at 25.0

        duration = builder.get_duration()
        assert duration == 25.0  # Latest end time

    def test_get_duration_with_transitions(self):
        """Test get_duration including transitions."""
        builder = TimelineBuilder()

        builder.add_image_at("image1.jpg", start_time=0.0, duration=5.0)
        builder.add_transition_at("fade", start_time=10.0, duration=2.0)  # Ends at 12.0

        duration = builder.get_duration()
        assert duration == 12.0  # Latest end time from transition

    def test_set_fps(self):
        """Test setting FPS."""
        builder = TimelineBuilder()

        builder.set_fps(60)
        assert builder.fps == 60

        # Test method chaining
        result = builder.set_fps(30)
        assert result is builder
        assert builder.fps == 30

    def test_clear_resets_everything(self):
        """Test that clear resets all tracks and timing."""
        builder = TimelineBuilder()

        # Add content
        builder.add_image("image1.jpg", duration=5.0)
        builder.add_text("text1", duration=3.0)
        builder.add_voice("voice1.mp3", duration=4.0)
        builder.add_transition("fade", duration=1.0)

        # Modify FPS
        builder.set_fps(60)

        # Clear everything
        result = builder.clear()
        assert result is builder

        # Check tracks were reset
        assert len(builder.video_tracks) == 1
        assert len(builder.music_tracks) == 1
        assert len(builder.voice_tracks) == 1
        assert len(builder.sfx_tracks) == 1
        assert len(builder.text_tracks) == 1
        assert len(builder.transitions) == 0

        # Check track names were reset
        assert builder.video_tracks[0].name == "video_0"
        assert builder.music_tracks[0].name == "music_0"
        assert builder.voice_tracks[0].name == "voice_0"
        assert builder.sfx_tracks[0].name == "sfx_0"
        assert builder.text_tracks[0].name == "text_0"

        # Check timing was reset
        assert builder._video_current_time == 0.0
        assert builder._music_current_time == 0.0
        assert builder._voice_current_time == 0.0
        assert builder._sfx_current_time == 0.0
        assert builder._text_current_time == 0.0

        # Check tracks are empty
        assert len(builder.video_tracks[0].clips) == 0
        assert len(builder.music_tracks[0].clips) == 0
        assert len(builder.voice_tracks[0].clips) == 0
        assert len(builder.sfx_tracks[0].clips) == 0
        assert len(builder.text_tracks[0].clips) == 0

        # Check FPS was preserved (not reset)
        assert builder.fps == 60

    def test_get_track_count_with_multiple_tracks(self):
        """Test get_track_count with multiple tracks."""
        builder = TimelineBuilder()

        # Add overlapping clips (should stay in same tracks)
        builder.add_image_at("image1.jpg", start_time=0.0, duration=5.0)
        builder.add_image_at("image2.jpg", start_time=2.0, duration=5.0)

        builder.add_voice_at("voice1.mp3", start_time=0.0, duration=5.0)
        builder.add_voice_at("voice2.mp3", start_time=2.0, duration=5.0)

        builder.add_text_at("text1", start_time=0.0, duration=5.0)
        builder.add_text_at("text2", start_time=2.0, duration=5.0)

        counts = builder.get_track_count()
        assert counts["video"] == 1  # Should still be 1 track
        assert counts["music"] == 1
        assert counts["voice"] == 1
        assert counts["sfx"] == 1
        assert counts["text"] == 1

    def test_get_clip_count_with_multiple_tracks(self):
        """Test get_clip_count with multiple tracks."""
        builder = TimelineBuilder()

        # Add clips to multiple tracks
        builder.add_image_at("image1.jpg", start_time=0.0, duration=5.0)
        builder.add_image_at(
            "image2.jpg", start_time=2.0, duration=5.0
        )  # Different track

        builder.add_voice_at("voice1.mp3", start_time=0.0, duration=5.0)
        builder.add_voice_at(
            "voice2.mp3", start_time=2.0, duration=5.0
        )  # Different track

        builder.add_text_at("text1", start_time=0.0, duration=5.0)
        builder.add_text_at("text2", start_time=2.0, duration=5.0)  # Different track

        counts = builder.get_clip_count()
        assert counts["video"] == 2
        assert counts["voice"] == 2
        assert counts["text"] == 2

    def test_build_video_spec_complete(self):
        """Test building complete VideoSpec."""
        builder = TimelineBuilder(width=1920, height=1080, fps=30)

        # Add content
        builder.add_image("image1.jpg", duration=5.0)
        builder.add_text("Hello", duration=3.0)
        builder.add_voice("voice1.mp3", duration=4.0)
        builder.add_transition("fade", duration=1.0)

        # Build VideoSpec
        video_spec = builder.build()

        # Check VideoSpec properties
        assert isinstance(video_spec, VideoSpec)
        assert video_spec.width == 1920
        assert video_spec.height == 1080
        assert video_spec.fps == 30
        assert video_spec.title == "Generated Video"

        # Check tracks
        assert len(video_spec.video_tracks) == 1
        assert len(video_spec.music_tracks) == 1
        assert len(video_spec.voice_tracks) == 1
        assert len(video_spec.sfx_tracks) == 1
        assert len(video_spec.text_tracks) == 1
        assert len(video_spec.transitions) == 1

        # Check clips
        assert len(video_spec.video_tracks[0].clips) == 1
        assert len(video_spec.voice_tracks[0].clips) == 1
        assert len(video_spec.text_tracks[0].clips) == 1

        # Check clip properties
        assert video_spec.video_tracks[0].clips[0].path == "image1.jpg"
        assert video_spec.text_tracks[0].clips[0].content == "Hello"
        assert video_spec.voice_tracks[0].clips[0].path == "voice1.mp3"
        assert video_spec.transitions[0].transition_type == "fade"

    def test_build_video_spec_empty(self):
        """Test building VideoSpec with no content."""
        builder = TimelineBuilder(width=1280, height=720, fps=60)

        video_spec = builder.build()

        assert isinstance(video_spec, VideoSpec)
        assert video_spec.width == 1280
        assert video_spec.height == 720
        assert video_spec.fps == 60
        assert len(video_spec.video_tracks) == 1
        assert len(video_spec.music_tracks) == 1
        assert len(video_spec.voice_tracks) == 1
        assert len(video_spec.sfx_tracks) == 1
        assert len(video_spec.text_tracks) == 1
        assert len(video_spec.transitions) == 0

        # Check tracks are empty
        assert len(video_spec.video_tracks[0].clips) == 0
        assert len(video_spec.music_tracks[0].clips) == 0
        assert len(video_spec.voice_tracks[0].clips) == 0
        assert len(video_spec.sfx_tracks[0].clips) == 0
        assert len(video_spec.text_tracks[0].clips) == 0

    def test_method_chaining(self):
        """Test that all methods support method chaining."""
        builder = TimelineBuilder()

        # Test sequential methods
        result = builder.add_image("image1.jpg", duration=5.0)
        assert result is builder

        result = builder.add_text("text1", duration=3.0)
        assert result is builder

        result = builder.add_voice("voice1.mp3", duration=4.0)
        assert result is builder

        result = builder.add_transition("fade", duration=1.0)
        assert result is builder

        # Test explicit methods
        result = builder.add_image_at("image2.jpg", start_time=10.0, duration=5.0)
        assert result is builder

        result = builder.add_text_at("text2", start_time=8.0, duration=4.0)
        assert result is builder

        result = builder.add_voice_at("voice2.mp3", start_time=12.0, duration=6.0)
        assert result is builder

        result = builder.add_transition_at("crossfade", start_time=15.0, duration=2.0)
        assert result is builder

        # Test utility methods
        result = builder.set_fps(60)
        assert result is builder

        result = builder.clear()
        assert result is builder

    def test_track_auto_detection_edge_cases(self):
        """Test edge cases in track auto-detection."""
        builder = TimelineBuilder()

        # Test with empty tracks (should use first track)
        track = builder._get_or_create_video_track()
        assert track is builder.video_tracks[0]
        assert track.name == "video_0"

        track = builder._get_or_create_voice_track()
        assert track is builder.voice_tracks[0]
        assert track.name == "voice_0"

        track = builder._get_or_create_text_track()
        assert track is builder.text_tracks[0]
        assert track.name == "text_0"

        # Test with non-overlapping clips (should use existing track)
        builder.add_image_at("image1.jpg", start_time=0.0, duration=5.0)
        builder.add_image_at("image2.jpg", start_time=10.0, duration=5.0)  # No overlap

        track = builder._get_or_create_video_track()
        assert track is builder.video_tracks[0]  # Should use existing track

    def test_current_time_updates_with_explicit_timing(self):
        """Test that current times are updated correctly with explicit timing."""
        builder = TimelineBuilder()

        # Add clips with explicit timing
        builder.add_image_at("image1.jpg", start_time=5.0, duration=3.0)
        builder.add_text_at("text1", start_time=2.0, duration=4.0)
        builder.add_voice_at("voice1.mp3", start_time=10.0, duration=2.0)

        # Current times should be updated to the end of each clip
        assert builder._video_current_time == 8.0  # 5.0 + 3.0
        assert builder._text_current_time == 6.0  # 2.0 + 4.0
        assert builder._voice_current_time == 12.0  # 10.0 + 2.0

        # Add another clip that ends earlier than current time
        builder.add_image_at("image2.jpg", start_time=1.0, duration=2.0)  # Ends at 3.0

        # Current time should not decrease
        assert builder._video_current_time == 8.0  # Should stay at 8.0, not 3.0

    def test_current_time_updates_without_duration(self):
        """Test current time updates when duration is not specified."""
        builder = TimelineBuilder()

        # Add clips without duration
        builder.add_image_at("image1.jpg", start_time=5.0)
        builder.add_text_at("text1", start_time=2.0)
        builder.add_voice_at("voice1.mp3", start_time=10.0)

        # Current times should be updated to start_time (no duration)
        assert builder._video_current_time == 5.0
        assert builder._text_current_time == 2.0
        assert builder._voice_current_time == 10.0

    def test_metadata_preservation(self):
        """Test that metadata is preserved in clips."""
        builder = TimelineBuilder()

        # Add clips with metadata
        builder.add_image_at(
            "image1.jpg",
            start_time=0.0,
            duration=5.0,
            metadata={"source": "test", "category": "background"},
        )

        builder.add_text_at(
            "Hello",
            start_time=0.0,
            duration=3.0,
            metadata={"style": "title", "priority": "high"},
        )

        builder.add_voice_at(
            "voice1.mp3",
            start_time=0.0,
            duration=4.0,
            metadata={"speaker": "narrator", "language": "en"},
        )

        # Check metadata was preserved
        assert builder.video_tracks[0].clips[0].metadata == {
            "source": "test",
            "category": "background",
        }
        assert builder.text_tracks[0].clips[0].metadata == {
            "style": "title",
            "priority": "high",
        }
        assert builder.voice_tracks[0].clips[0].metadata == {
            "speaker": "narrator",
            "language": "en",
        }

    def test_set_duration_functionality(self):
        """Test that set_duration sets the default duration for subsequent sequential elements."""
        builder = TimelineBuilder()

        # Set a default duration
        builder.set_duration(5.0)

        # Add elements without specifying duration
        builder.add_image("image1.jpg")  # Should use 5.0 duration
        builder.add_text("text1")  # Should use 5.0 duration
        builder.add_voice("voice1.mp3")  # Should use 5.0 duration

        # Check that clips were created with the set duration
        assert builder.video_tracks[0].clips[0].duration == 5.0
        assert builder.text_tracks[0].clips[0].duration == 5.0
        assert builder.voice_tracks[0].clips[0].duration == 5.0

        # Check that current times were updated
        assert builder._video_current_time == 5.0
        assert builder._text_current_time == 5.0
        assert builder._voice_current_time == 5.0

        # Verify that _next_duration persists for batch operations
        assert builder._next_duration == 5.0

        # Test that explicit duration overrides set_duration
        builder.add_image("image2.jpg", duration=7.0)  # Should use 7.0, not 5.0
        assert builder.video_tracks[0].clips[1].duration == 7.0

        # Test that set_duration continues to work for subsequent elements
        builder.add_text("text2")  # Should use 5.0 duration
        assert builder.text_tracks[0].clips[1].duration == 5.0

        # Test clear_duration functionality
        builder.clear_duration()
        builder.add_voice("voice2.mp3")  # Should not use any duration
        assert builder.voice_tracks[0].clips[1].duration is None

    def test_clear_duration_functionality(self):
        """Test that clear_duration properly resets the default duration."""
        builder = TimelineBuilder()

        # Set a default duration
        builder.set_duration(5.0)
        assert builder._next_duration == 5.0

        # Clear the duration
        builder.clear_duration()
        # After clear_duration(), _next_duration should be None
        # Use safe_assert to help mypy understand the mutation
        safe_assert(
            builder._next_duration is None, "Duration should be None after clear"
        )

        # Add elements without specifying duration
        builder.add_image("image1.jpg")  # Should not use any duration
        builder.add_text("text1")  # Should not use any duration

        # Check that clips were created without duration
        safe_assert(
            builder.video_tracks[0].clips[0].duration is None,
            "Video clip should have no duration",
        )
        safe_assert(
            builder.text_tracks[0].clips[0].duration is None,
            "Text clip should have no duration",
        )

        # Test that setting duration again works
        builder.set_duration(3.0)
        builder.add_voice("voice1.mp3")  # Should use 3.0 duration
        safe_assert(
            builder.voice_tracks[0].clips[0].duration == 3.0,
            "Voice clip should have 3.0 duration",
        )

    def test_set_duration_batch_operations(self):
        """Test that set_duration works correctly for batch operations with multiple elements."""
        builder = TimelineBuilder()

        # Set a default duration for a batch
        builder.set_duration(4.0)

        # Add multiple elements in sequence - all should use the 4.0 duration
        builder.add_image("image1.jpg")
        builder.add_text("Scene 1")
        builder.add_voice("voice1.mp3")
        builder.add_image("image2.jpg")
        builder.add_text("Scene 2")
        builder.add_voice("voice2.mp3")

        # Verify all clips have the set duration
        assert len(builder.video_tracks[0].clips) == 2
        assert len(builder.text_tracks[0].clips) == 2
        assert len(builder.voice_tracks[0].clips) == 2

        for clip in builder.video_tracks[0].clips:
            assert (
                clip.duration == 4.0
            ), f"Video clip duration should be 4.0, got {clip.duration}"

        for clip in builder.text_tracks[0].clips:
            assert (
                clip.duration == 4.0
            ), f"Text clip duration should be 4.0, got {clip.duration}"

        for clip in builder.voice_tracks[0].clips:
            assert (
                clip.duration == 4.0
            ), f"Voice clip duration should be 4.0, got {clip.duration}"

        # Verify _next_duration persists throughout the batch
        assert (
            builder._next_duration == 4.0
        ), "_next_duration should persist for batch operations"

        # Test that explicit duration overrides for specific elements
        builder.add_image("image3.jpg", duration=6.0)  # Override with explicit duration
        assert builder.video_tracks[0].clips[2].duration == 6.0

        # But subsequent elements still use the set duration
        builder.add_text("Scene 3")
        assert builder.text_tracks[0].clips[2].duration == 4.0

        # Test changing duration mid-batch
        builder.set_duration(2.0)
        builder.add_voice("voice3.mp3")
        assert builder.voice_tracks[0].clips[2].duration == 2.0

        # Test clearing duration mid-batch
        builder.clear_duration()
        builder.add_image("image4.jpg")
        assert builder.video_tracks[0].clips[3].duration is None

        # Test that setting duration again works after clearing
        builder.set_duration(1.0)
        builder.add_text("Scene 4")
        assert builder.text_tracks[0].clips[3].duration == 1.0
