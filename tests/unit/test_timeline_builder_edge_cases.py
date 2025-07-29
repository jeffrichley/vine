"""Edge case and error scenario tests for TimelineBuilder."""

from pathlib import Path

import pytest

from vine.builder.timeline_builder import TimelineBuilder
from vine.models.transition import TransitionType
from vine.models.video_spec import VideoSpec


class TestTimelineBuilderEdgeCases:
    """Test edge cases and error scenarios for TimelineBuilder."""

    def test_negative_start_time_validation(self) -> None:
        """Test that negative start times are rejected by the models."""
        builder = TimelineBuilder()

        # These should raise validation errors from the Pydantic models
        with pytest.raises(ValueError):
            builder.add_image_at("image1.jpg", start_time=-1.0, duration=5.0)

        with pytest.raises(ValueError):
            builder.add_text_at("text1", start_time=-2.0, duration=3.0)

        with pytest.raises(ValueError):
            builder.add_voice_at("voice1.mp3", start_time=-0.5, duration=4.0)

    def test_negative_duration_validation(self) -> None:
        """Test that negative durations are rejected by the models."""
        builder = TimelineBuilder()

        with pytest.raises(ValueError):
            builder.add_image_at("image1.jpg", start_time=0.0, duration=-5.0)

        with pytest.raises(ValueError):
            builder.add_text_at("text1", start_time=0.0, duration=-3.0)

        with pytest.raises(ValueError):
            builder.add_voice_at("voice1.mp3", start_time=0.0, duration=-4.0)

    def test_end_time_before_start_time_validation(self) -> None:
        """Test that end_time before start_time is rejected."""
        builder = TimelineBuilder()

        with pytest.raises(ValueError):
            builder.add_image_at("image1.jpg", start_time=10.0, end_time=5.0)

        with pytest.raises(ValueError):
            builder.add_text_at("text1", start_time=8.0, end_time=3.0)

        with pytest.raises(ValueError):
            builder.add_voice_at("voice1.mp3", start_time=12.0, end_time=6.0)

    def test_end_time_equal_to_start_time_validation(self) -> None:
        """Test that end_time equal to start_time is allowed (creates zero-duration clip)."""
        builder = TimelineBuilder()

        # This should be allowed (creates a zero-duration clip)
        builder.add_image_at("image1.jpg", start_time=5.0, end_time=5.0)
        builder.add_text_at("text1", start_time=3.0, end_time=3.0)
        builder.add_voice_at("voice1.mp3", start_time=4.0, end_time=4.0)

        # Check that clips were created with zero duration
        assert builder.video_tracks[0].clips[0].duration == 0.0
        assert builder.text_tracks[0].clips[0].duration == 0.0
        assert builder.voice_tracks[0].clips[0].duration == 0.0

    def test_transition_validation(self) -> None:
        """Test transition validation."""
        builder = TimelineBuilder()

        # Test invalid transition type
        with pytest.raises(ValueError):
            builder.add_transition_at("invalid_type", start_time=0.0, duration=1.0)  # type: ignore[arg-type]  # intentional invalid input for testing

        # Test negative transition duration
        with pytest.raises(ValueError):
            builder.add_transition_at(
                TransitionType.FADE, start_time=0.0, duration=-1.0
            )

        # Test negative transition start time
        with pytest.raises(ValueError):
            builder.add_transition_at(
                TransitionType.FADE, start_time=-1.0, duration=1.0
            )

    def test_empty_string_content(self) -> None:
        """Test handling of empty string content."""
        builder = TimelineBuilder()

        # Empty text should be allowed
        text_content = ""
        builder.add_text_at(text_content, start_time=0.0, duration=3.0)
        assert len(builder.text_tracks[0].clips) == 1
        assert builder.text_tracks[0].clips[0].content == ""

    def test_whitespace_only_content(self) -> None:
        """Test handling of whitespace-only content."""
        builder = TimelineBuilder()

        # Whitespace-only text should be allowed
        builder.add_text("   \n\t  ", duration=3.0)
        assert len(builder.text_tracks[0].clips) == 1
        assert builder.text_tracks[0].clips[0].content == "   \n\t  "

    def test_very_large_numbers(self) -> None:
        """Test handling of very large numbers."""
        builder = TimelineBuilder()

        # Test with very large start times and durations
        large_time = 1e6  # 1 million seconds
        large_duration = 1e5  # 100 thousand seconds

        builder.add_image_at(
            "image1.jpg", start_time=large_time, duration=large_duration
        )
        builder.add_text_at("text1", start_time=large_time, duration=large_duration)
        builder.add_voice_at(
            "voice1.mp3", start_time=large_time, duration=large_duration
        )

        # Check that large numbers are handled correctly
        assert builder.video_tracks[0].clips[0].start_time == large_time
        assert builder.video_tracks[0].clips[0].duration == large_duration
        assert builder.text_tracks[0].clips[0].start_time == large_time
        assert builder.text_tracks[0].clips[0].duration == large_duration
        assert builder.voice_tracks[0].clips[0].start_time == large_time
        assert builder.voice_tracks[0].clips[0].duration == large_duration

    def test_floating_point_precision(self) -> None:
        """Test handling of floating point precision."""
        builder = TimelineBuilder()

        # Test with very small floating point values
        small_time = 0.000001
        small_duration = 0.000002

        builder.add_image_at(
            "image1.jpg", start_time=small_time, duration=small_duration
        )

        # Check that small floating point values are preserved
        assert builder.video_tracks[0].clips[0].start_time == small_time
        assert builder.video_tracks[0].clips[0].duration == small_duration

    def test_concurrent_access_simulation(self) -> None:
        """Test that the builder can handle rapid successive calls."""
        builder = TimelineBuilder()

        # Rapidly add many clips
        for i in range(100):
            builder.add_image_at(f"image_{i}.jpg", start_time=i, duration=1.0)
            builder.add_text_at(f"text_{i}", start_time=i, duration=1.0)
            builder.add_voice_at(f"voice_{i}.mp3", start_time=i, duration=1.0)

        # Check that all clips were added
        assert len(builder.video_tracks[0].clips) == 100
        assert len(builder.text_tracks[0].clips) == 100
        assert len(builder.voice_tracks[0].clips) == 100

    def test_mixed_path_types(self) -> None:
        """Test mixing string and Path objects for file paths."""
        builder = TimelineBuilder()

        # Mix string and Path objects
        builder.add_image("string_path.jpg", duration=5.0)
        builder.add_image_at(Path("pathlib_path.jpg"), start_time=5.0, duration=5.0)

        builder.add_voice("string_voice.mp3", duration=4.0)
        builder.add_voice_at(Path("pathlib_voice.mp3"), start_time=4.0, duration=4.0)

        # Check that paths were handled correctly
        assert builder.video_tracks[0].clips[0].path == "string_path.jpg"
        assert builder.video_tracks[0].clips[1].path == "pathlib_path.jpg"
        assert builder.voice_tracks[0].clips[0].path == "string_voice.mp3"
        assert builder.voice_tracks[0].clips[1].path == "pathlib_voice.mp3"

    def test_unicode_content(self) -> None:
        """Test handling of unicode content in text clips."""
        builder = TimelineBuilder()

        # Test various unicode content
        unicode_texts = [
            "Hello 世界",  # Chinese characters
            "Привет мир",  # Cyrillic
            "こんにちは",  # Japanese
            "안녕하세요",  # Korean
            "مرحبا بالعالم",  # Arabic
            "नमस्ते दुनिया",  # Devanagari
            "Hello 🌍",  # Emoji
            "Test with 🎬🎭🎪",  # Multiple emojis
        ]

        for i, text in enumerate(unicode_texts):
            builder.add_text_at(text, start_time=i, duration=1.0)

        # Check that all unicode content was preserved
        for i, text in enumerate(unicode_texts):
            assert builder.text_tracks[0].clips[i].content == text

    def test_special_characters_in_paths(self) -> None:
        """Test handling of special characters in file paths."""
        builder = TimelineBuilder()

        # Test paths with special characters
        special_paths = [
            "image with spaces.jpg",
            "image-with-dashes.jpg",
            "image_with_underscores.jpg",
            "image.with.dots.jpg",
            "image(1).jpg",
            "image[2].jpg",
            "image{3}.jpg",
            "image@#$%.jpg",
        ]

        for i, path in enumerate(special_paths):
            builder.add_image_at(path, start_time=i, duration=1.0)

        # Check that all paths were preserved
        for i, path in enumerate(special_paths):
            assert builder.video_tracks[0].clips[i].path == path

    def test_extreme_clip_properties(self) -> None:
        """Test extreme values for clip properties."""
        builder = TimelineBuilder()

        # Test extreme values for various properties
        builder.add_image_at(
            "image1.jpg",
            start_time=0.0,
            duration=5.0,
            width=1,  # Minimum width
            height=1,  # Minimum height
            x_position=-1000.0,  # Large negative position
            y_position=1000.0,  # Large positive position
            opacity=0.0,  # Minimum opacity
        )

        builder.add_text_at(
            "text1",
            start_time=0.0,
            duration=5.0,
            font_size=1,  # Minimum font size
            x_position=-500.0,
            y_position=500.0,
            opacity=1.0,  # Maximum opacity
        )

        builder.add_voice_at(
            "voice1.mp3",
            start_time=0.0,
            duration=5.0,
            volume=0.0,  # Minimum volume
            fade_in=0.0,
            fade_out=0.0,
        )

        # Check that extreme values were accepted
        image_clip = builder.video_tracks[0].clips[0]
        assert image_clip.width == 1
        assert image_clip.height == 1
        assert image_clip.x_position == -1000.0
        assert image_clip.y_position == 1000.0
        assert image_clip.opacity == 0.0

        text_clip = builder.text_tracks[0].clips[0]
        assert text_clip.font_size == 1
        assert text_clip.x_position == -500.0
        assert text_clip.y_position == 500.0
        assert text_clip.opacity == 1.0

        voice_clip = builder.voice_tracks[0].clips[0]
        assert voice_clip.volume == 0.0
        assert voice_clip.fade_in == 0.0
        assert voice_clip.fade_out == 0.0

    def test_invalid_property_values(self) -> None:
        """Test that invalid property values are rejected."""
        builder = TimelineBuilder()

        # Test invalid opacity values
        with pytest.raises(ValueError):
            builder.add_image_at(
                "image1.jpg", start_time=0.0, duration=5.0, opacity=1.5
            )

        with pytest.raises(ValueError):
            builder.add_image_at(
                "image1.jpg", start_time=0.0, duration=5.0, opacity=-0.5
            )

        # Test invalid volume values
        with pytest.raises(ValueError):
            builder.add_voice_at("voice1.mp3", start_time=0.0, duration=5.0, volume=3.0)

        with pytest.raises(ValueError):
            builder.add_voice_at(
                "voice1.mp3", start_time=0.0, duration=5.0, volume=-0.5
            )

        # Test invalid font size
        with pytest.raises(ValueError):
            builder.add_text_at("text1", start_time=0.0, duration=5.0, font_size=0)

        # Test invalid dimensions
        with pytest.raises(ValueError):
            builder.add_image_at("image1.jpg", start_time=0.0, duration=5.0, width=0)

        with pytest.raises(ValueError):
            builder.add_image_at("image1.jpg", start_time=0.0, duration=5.0, height=0)

    def test_clear_preserves_custom_parameters(self) -> None:
        """Test that clear preserves custom initialization parameters."""
        builder = TimelineBuilder(width=1280, height=720, fps=60)

        # Add some content
        builder.add_image("image1.jpg", duration=5.0)
        builder.add_text("text1", duration=3.0)
        builder.add_voice("voice1.mp3", duration=4.0)

        # Clear
        builder.clear()

        # Check that custom parameters were preserved
        assert builder.width == 1280
        assert builder.height == 720
        assert builder.fps == 60

        # Check that tracks were reset to defaults
        assert len(builder.video_tracks) == 1
        assert len(builder.voice_tracks) == 1
        assert len(builder.text_tracks) == 1
        assert builder.video_tracks[0].name == "video_0"
        assert builder.voice_tracks[0].name == "voice_0"
        assert builder.text_tracks[0].name == "text_0"

    def test_get_duration_with_infinite_clips(self) -> None:
        """Test get_duration when clips have no end time (infinite duration)."""
        builder = TimelineBuilder()

        # Add clips without duration (infinite)
        builder.add_image_at("image1.jpg", start_time=0.0)  # No duration
        builder.add_text_at("text1", start_time=5.0)  # No duration
        builder.add_voice_at("voice1.mp3", start_time=10.0)  # No duration

        # Duration should be 0.0 since no duration clips are ignored
        duration = builder.get_duration()
        assert duration == 0.0

    def test_get_duration_with_mixed_infinite_and_finite_clips(self) -> None:
        """Test get_duration with mix of infinite and finite duration clips."""
        builder = TimelineBuilder()

        # Add clips with mixed duration types
        builder.add_image_at("image1.jpg", start_time=0.0, duration=5.0)  # Ends at 5.0
        builder.add_text_at("text1", start_time=10.0)  # No duration (infinite)
        builder.add_voice_at(
            "voice1.mp3", start_time=15.0, duration=8.0
        )  # Ends at 23.0

        # Duration should be the latest end time from finite clips
        duration = builder.get_duration()
        assert duration == 23.0  # 15.0 + 8.0

    def test_track_creation_under_high_load(self) -> None:
        """Test track creation behavior under high load."""
        builder = TimelineBuilder()

        # Create many overlapping clips (creates multiple tracks)
        for i in range(50):
            # Each clip overlaps with the previous one
            builder.add_image_at(f"image_{i}.jpg", start_time=i, duration=2.0)
            builder.add_text_at(f"text_{i}", start_time=i, duration=2.0)
            builder.add_voice_at(f"voice_{i}.mp3", start_time=i, duration=2.0)

        # Check that multiple tracks were created
        assert len(builder.video_tracks) > 1
        assert len(builder.voice_tracks) > 1
        assert len(builder.text_tracks) > 1

        # Check track naming
        for i, video_track in enumerate(builder.video_tracks):
            assert video_track.name == f"video_{i}"

        for i, voice_track in enumerate(builder.voice_tracks):
            assert voice_track.name == f"voice_{i}"

        for i, text_track in enumerate(builder.text_tracks):
            assert text_track.name == f"text_{i}"

        # Check that clips are distributed across tracks
        total_video_clips = sum(len(track.clips) for track in builder.video_tracks)
        total_text_clips = sum(len(track.clips) for track in builder.text_tracks)
        total_voice_clips = sum(len(track.clips) for track in builder.voice_tracks)

        assert total_video_clips == 50
        assert total_text_clips == 50
        assert total_voice_clips == 50

    def test_method_chaining_with_clear(self) -> None:
        """Test method chaining with clear operation."""
        builder = TimelineBuilder()

        # Test chaining with clear
        result = (
            builder.add_image("image1.jpg", duration=5.0)
            .add_text("text1", duration=3.0)
            .clear()
            .add_image("image2.jpg", duration=4.0)
            .add_text("text2", duration=2.0)
        )

        assert result is builder

        # Check that only the post-clear content remains
        assert len(builder.video_tracks[0].clips) == 1
        assert len(builder.text_tracks[0].clips) == 1
        assert builder.video_tracks[0].clips[0].path == "image2.jpg"
        assert builder.text_tracks[0].clips[0].content == "text2"

    def test_build_with_empty_builder(self) -> None:
        """Test building VideoSpec with completely empty builder."""
        builder = TimelineBuilder()

        video_spec = builder.build()

        # Check that VideoSpec was created with default values
        assert isinstance(video_spec, VideoSpec)
        assert video_spec.width == 1920  # Default width
        assert video_spec.height == 1080  # Default height
        assert video_spec.fps == 30  # Default fps
        assert video_spec.title == "Generated Video"

        # Check that empty tracks are included
        assert len(video_spec.video_tracks) == 1
        assert len(video_spec.voice_tracks) == 1
        assert len(video_spec.text_tracks) == 1
        assert len(video_spec.transitions) == 0

        # Check that tracks are empty
        assert len(video_spec.video_tracks[0].clips) == 0
        assert len(video_spec.voice_tracks[0].clips) == 0
        assert len(video_spec.text_tracks[0].clips) == 0
