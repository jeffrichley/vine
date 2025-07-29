"""Unit tests for track-based data models."""

import pytest

from vine.models.tracks import (
    AudioClip,
    AudioTrack,
    ImageClip,
    TextClip,
    TextTrack,
    VideoClip,
    VideoTrack,
)


class TestVideoClip:
    """Test VideoClip model."""

    def test_video_clip_creation(self) -> None:
        """Test basic video clip creation."""
        clip = VideoClip(path="test_video.mp4", start_time=0.0, duration=10.0)
        assert clip.path == "test_video.mp4"
        assert clip.start_time == 0.0
        assert clip.duration == 10.0
        assert clip.get_end_time() == 10.0

    def test_video_clip_with_end_time(self) -> None:
        """Test video clip with end_time instead of duration."""
        clip = VideoClip(path="test_video.mp4", start_time=5.0, end_time=15.0)
        assert clip.start_time == 5.0
        assert clip.duration is None
        assert clip.end_time == 15.0
        assert clip.get_end_time() == 15.0

    def test_video_clip_validation_error(self) -> None:
        """Test validation error when both duration and end_time are specified."""
        with pytest.raises(
            ValueError, match="Cannot specify both duration and end_time"
        ):
            VideoClip(
                path="test_video.mp4", start_time=0.0, duration=10.0, end_time=15.0
            )

    def test_video_clip_is_active_at_time(self) -> None:
        """Test is_active_at_time method."""
        clip = VideoClip(path="test_video.mp4", start_time=5.0, duration=10.0)
        assert not clip.is_active_at_time(0.0)
        assert not clip.is_active_at_time(4.9)
        assert clip.is_active_at_time(5.0)
        assert clip.is_active_at_time(10.0)
        assert clip.is_active_at_time(14.9)
        assert not clip.is_active_at_time(15.0)  # End time is exclusive
        assert not clip.is_active_at_time(20.0)

    def test_video_clip_validate_end_time_after_start_time(self) -> None:
        """Test validate_end_time when end_time is after start_time."""
        # This should work fine
        clip = VideoClip(path="test_video.mp4", start_time=5.0, end_time=15.0)
        assert clip.end_time == 15.0

    def test_video_clip_validate_end_time_before_start_time(self) -> None:
        """Test validate_end_time error when end_time is before or equal to start_time."""
        # End time equal to start time
        with pytest.raises(ValueError, match="End time must be after start time"):
            VideoClip(path="test_video.mp4", start_time=10.0, end_time=10.0)

        # End time before start time
        with pytest.raises(ValueError, match="End time must be after start time"):
            VideoClip(path="test_video.mp4", start_time=10.0, end_time=5.0)

    def test_video_clip_validate_end_time_with_duration_conflict(self) -> None:
        """Test validate_end_time error when both duration and end_time are specified."""
        with pytest.raises(
            ValueError, match="Cannot specify both duration and end_time"
        ):
            VideoClip(
                path="test_video.mp4", start_time=0.0, duration=10.0, end_time=15.0
            )

    def test_video_clip_is_active_at_time_with_end_time_only(self) -> None:
        """Test is_active_at_time with end_time instead of duration."""
        clip = VideoClip(path="test_video.mp4", start_time=5.0, end_time=15.0)
        assert not clip.is_active_at_time(0.0)
        assert not clip.is_active_at_time(4.9)
        assert clip.is_active_at_time(5.0)
        assert clip.is_active_at_time(10.0)
        assert clip.is_active_at_time(14.9)
        assert not clip.is_active_at_time(15.0)  # End time is exclusive
        assert not clip.is_active_at_time(20.0)

    def test_video_clip_is_active_at_time_with_no_end(self) -> None:
        """Test is_active_at_time when clip has no end time (infinite duration)."""
        clip = VideoClip(path="test_video.mp4", start_time=5.0)
        assert not clip.is_active_at_time(0.0)
        assert not clip.is_active_at_time(4.9)
        assert clip.is_active_at_time(5.0)
        assert clip.is_active_at_time(10.0)
        assert clip.is_active_at_time(100.0)  # Should be active indefinitely
        assert clip.is_active_at_time(1000.0)  # Should be active indefinitely

    def test_video_clip_return_time_gte_start_time_specific(self) -> None:
        """Test the specific 'return time >= self.start_time' line in is_active_at_time."""
        # Test with start_time = 0.0
        clip = VideoClip(path="test_video.mp4", start_time=0.0)
        assert not clip.is_active_at_time(-1.0)  # time < start_time
        assert clip.is_active_at_time(0.0)  # time == start_time
        assert clip.is_active_at_time(1.0)  # time > start_time

        # Test with start_time = 5.0
        clip = VideoClip(path="test_video.mp4", start_time=5.0)
        assert not clip.is_active_at_time(4.9)  # time < start_time
        assert clip.is_active_at_time(5.0)  # time == start_time
        assert clip.is_active_at_time(5.1)  # time > start_time

        # Test with start_time = 10.0
        clip = VideoClip(path="test_video.mp4", start_time=10.0)
        assert not clip.is_active_at_time(9.9)  # time < start_time
        assert clip.is_active_at_time(10.0)  # time == start_time
        assert clip.is_active_at_time(10.1)  # time > start_time

    def test_video_clip_return_time_gte_start_time_edge_cases(self) -> None:
        """Test edge cases for the 'return time >= self.start_time' line."""
        # Test with very small start_time
        clip = VideoClip(path="test_video.mp4", start_time=0.0001)
        assert not clip.is_active_at_time(0.0)
        assert clip.is_active_at_time(0.0001)
        assert clip.is_active_at_time(0.0002)

        # Test with very large start_time
        clip = VideoClip(path="test_video.mp4", start_time=1000000.0)
        assert not clip.is_active_at_time(999999.9)
        assert clip.is_active_at_time(1000000.0)
        assert clip.is_active_at_time(1000000.1)

        # Test with zero start_time
        clip = VideoClip(path="test_video.mp4", start_time=0.0)
        assert not clip.is_active_at_time(-1.0)
        assert clip.is_active_at_time(0.0)
        assert clip.is_active_at_time(1.0)


class TestImageClip:
    """Test ImageClip model."""

    def test_image_clip_creation(self) -> None:
        """Test basic image clip creation."""
        clip = ImageClip(path="test_image.jpg", start_time=0.0, duration=5.0)
        assert clip.path == "test_image.jpg"
        assert clip.start_time == 0.0
        assert clip.duration == 5.0
        assert clip.get_end_time() == 5.0

    def test_image_clip_display_settings(self) -> None:
        """Test image clip with display settings."""
        clip = ImageClip(
            path="test_image.jpg",
            start_time=0.0,
            duration=5.0,
            width=1920,
            height=1080,
            x_position=100.0,
            y_position=200.0,
            opacity=0.8,
        )
        assert clip.width == 1920
        assert clip.height == 1080
        assert clip.x_position == 100.0
        assert clip.y_position == 200.0
        assert clip.opacity == 0.8

    def test_image_clip_validate_end_time_after_start_time(self) -> None:
        """Test validate_end_time when end_time is after start_time."""
        clip = ImageClip(path="test_image.jpg", start_time=5.0, end_time=15.0)
        assert clip.end_time == 15.0

    def test_image_clip_validate_end_time_before_start_time(self) -> None:
        """Test validate_end_time error when end_time is before or equal to start_time."""
        with pytest.raises(ValueError, match="End time must be after start time"):
            ImageClip(path="test_image.jpg", start_time=10.0, end_time=10.0)

        with pytest.raises(ValueError, match="End time must be after start time"):
            ImageClip(path="test_image.jpg", start_time=10.0, end_time=5.0)

    def test_image_clip_validate_end_time_with_duration_conflict(self) -> None:
        """Test validate_end_time error when both duration and end_time are specified."""
        with pytest.raises(
            ValueError, match="Cannot specify both duration and end_time"
        ):
            ImageClip(
                path="test_image.jpg", start_time=0.0, duration=10.0, end_time=15.0
            )

    def test_image_clip_is_active_at_time_edge_cases(self) -> None:
        """Test is_active_at_time edge cases."""
        clip = ImageClip(path="test_image.jpg", start_time=5.0, duration=10.0)
        # Test exact boundary conditions
        assert not clip.is_active_at_time(5.0 - 1e-10)  # Just before start
        assert clip.is_active_at_time(5.0)  # Exactly at start
        assert clip.is_active_at_time(15.0 - 1e-10)  # Just before end
        assert not clip.is_active_at_time(15.0)  # Exactly at end

    def test_image_clip_return_time_gte_start_time_specific(self) -> None:
        """Test the specific 'return time >= self.start_time' line in is_active_at_time."""
        # Test with start_time = 0.0
        clip = ImageClip(path="test_image.jpg", start_time=0.0)
        assert not clip.is_active_at_time(-1.0)  # time < start_time
        assert clip.is_active_at_time(0.0)  # time == start_time
        assert clip.is_active_at_time(1.0)  # time > start_time

        # Test with start_time = 5.0
        clip = ImageClip(path="test_image.jpg", start_time=5.0)
        assert not clip.is_active_at_time(4.9)  # time < start_time
        assert clip.is_active_at_time(5.0)  # time == start_time
        assert clip.is_active_at_time(5.1)  # time > start_time


class TestTextClip:
    """Test TextClip model."""

    def test_text_clip_creation(self) -> None:
        """Test basic text clip creation."""
        clip = TextClip(content="Hello World", start_time=0.0, duration=3.0)
        assert clip.content == "Hello World"
        assert clip.start_time == 0.0
        assert clip.duration == 3.0
        assert clip.get_end_time() == 3.0

    def test_text_clip_styling(self) -> None:
        """Test text clip with styling options."""
        clip = TextClip(
            content="Styled Text",
            start_time=0.0,
            duration=3.0,
            font_size=72,
            font_color="#FF0000",
            font_family="Times New Roman",
            font_weight="bold",
            alignment="left",
        )
        assert clip.font_size == 72
        assert clip.font_color == "#FF0000"
        assert clip.font_family == "Times New Roman"
        assert clip.font_weight == "bold"
        assert clip.alignment == "left"

    def test_text_clip_validate_end_time_after_start_time(self) -> None:
        """Test validate_end_time when end_time is after start_time."""
        clip = TextClip(content="Test text", start_time=5.0, end_time=15.0)
        assert clip.end_time == 15.0

    def test_text_clip_validate_end_time_before_start_time(self) -> None:
        """Test validate_end_time error when end_time is before or equal to start_time."""
        with pytest.raises(ValueError, match="End time must be after start time"):
            TextClip(content="Test text", start_time=10.0, end_time=10.0)

        with pytest.raises(ValueError, match="End time must be after start time"):
            TextClip(content="Test text", start_time=10.0, end_time=5.0)

    def test_text_clip_validate_end_time_with_duration_conflict(self) -> None:
        """Test validate_end_time error when both duration and end_time are specified."""
        with pytest.raises(
            ValueError, match="Cannot specify both duration and end_time"
        ):
            TextClip(content="Test text", start_time=0.0, duration=10.0, end_time=15.0)

    def test_text_clip_is_active_at_time_edge_cases(self) -> None:
        """Test is_active_at_time edge cases."""
        clip = TextClip(content="Test text", start_time=5.0, duration=10.0)
        # Test exact boundary conditions
        assert not clip.is_active_at_time(5.0 - 1e-10)  # Just before start
        assert clip.is_active_at_time(5.0)  # Exactly at start
        assert clip.is_active_at_time(15.0 - 1e-10)  # Just before end
        assert not clip.is_active_at_time(15.0)  # Exactly at end

    def test_text_clip_return_time_gte_start_time_specific(self) -> None:
        """Test the specific 'return time >= self.start_time' line in is_active_at_time."""
        # Test with start_time = 0.0
        clip = TextClip(content="Test text", start_time=0.0)
        assert not clip.is_active_at_time(-1.0)  # time < start_time
        assert clip.is_active_at_time(0.0)  # time == start_time
        assert clip.is_active_at_time(1.0)  # time > start_time

        # Test with start_time = 5.0
        clip = TextClip(content="Test text", start_time=5.0)
        assert not clip.is_active_at_time(4.9)  # time < start_time
        assert clip.is_active_at_time(5.0)  # time == start_time
        assert clip.is_active_at_time(5.1)  # time > start_time


class TestAudioClip:
    """Test AudioClip model."""

    def test_audio_clip_creation(self) -> None:
        """Test basic audio clip creation."""
        clip = AudioClip(path="test_audio.mp3", start_time=0.0, duration=10.0)
        assert clip.path == "test_audio.mp3"
        assert clip.start_time == 0.0
        assert clip.duration == 10.0
        assert clip.get_end_time() == 10.0

    def test_audio_clip_settings(self) -> None:
        """Test audio clip with audio settings."""
        clip = AudioClip(
            path="test_audio.mp3",
            start_time=0.0,
            duration=10.0,
            volume=0.8,
            fade_in=1.0,
            fade_out=2.0,
        )
        assert clip.volume == 0.8
        assert clip.fade_in == 1.0
        assert clip.fade_out == 2.0

    def test_audio_clip_validate_end_time_after_start_time(self) -> None:
        """Test validate_end_time when end_time is after start_time."""
        clip = AudioClip(path="test_audio.mp3", start_time=5.0, end_time=15.0)
        assert clip.end_time == 15.0

    def test_audio_clip_validate_end_time_before_start_time(self) -> None:
        """Test validate_end_time error when end_time is before or equal to start_time."""
        with pytest.raises(ValueError, match="End time must be after start time"):
            AudioClip(path="test_audio.mp3", start_time=10.0, end_time=10.0)

        with pytest.raises(ValueError, match="End time must be after start time"):
            AudioClip(path="test_audio.mp3", start_time=10.0, end_time=5.0)

    def test_audio_clip_validate_end_time_with_duration_conflict(self) -> None:
        """Test validate_end_time error when both duration and end_time are specified."""
        with pytest.raises(
            ValueError, match="Cannot specify both duration and end_time"
        ):
            AudioClip(
                path="test_audio.mp3", start_time=0.0, duration=10.0, end_time=15.0
            )

    def test_audio_clip_is_active_at_time_edge_cases(self) -> None:
        """Test is_active_at_time edge cases."""
        clip = AudioClip(path="test_audio.mp3", start_time=5.0, duration=10.0)
        # Test exact boundary conditions
        assert not clip.is_active_at_time(5.0 - 1e-10)  # Just before start
        assert clip.is_active_at_time(5.0)  # Exactly at start
        assert clip.is_active_at_time(15.0 - 1e-10)  # Just before end
        assert not clip.is_active_at_time(15.0)  # Exactly at end

    def test_audio_clip_return_time_gte_start_time_specific(self) -> None:
        """Test the specific 'return time >= self.start_time' line in is_active_at_time."""
        # Test with start_time = 0.0
        clip = AudioClip(path="test_audio.mp3", start_time=0.0)
        assert not clip.is_active_at_time(-1.0)  # time < start_time
        assert clip.is_active_at_time(0.0)  # time == start_time
        assert clip.is_active_at_time(1.0)  # time > start_time

        # Test with start_time = 5.0
        clip = AudioClip(path="test_audio.mp3", start_time=5.0)
        assert not clip.is_active_at_time(4.9)  # time < start_time
        assert clip.is_active_at_time(5.0)  # time == start_time
        assert clip.is_active_at_time(5.1)  # time > start_time


class TestVideoTrack:
    """Test VideoTrack model."""

    def test_video_track_creation(self) -> None:
        """Test basic video track creation."""
        track = VideoTrack(name="test_video_track")
        assert track.name == "test_video_track"
        assert len(track.clips) == 0
        assert track.z_order == 0
        assert track.visible is True

    def test_video_track_add_clip(self) -> None:
        """Test adding clips to video track."""
        track = VideoTrack(name="test_video_track")
        clip = ImageClip(path="test_image.jpg", start_time=0.0, duration=5.0)
        track.add_clip(clip)
        assert len(track.clips) == 1
        assert track.clips[0] == clip

    def test_video_track_get_active_clips(self) -> None:
        """Test getting active clips at a specific time."""
        track = VideoTrack(name="test_video_track")

        # Add clips with different timing
        clip1 = ImageClip(path="image1.jpg", start_time=0.0, duration=5.0)
        clip2 = ImageClip(path="image2.jpg", start_time=3.0, duration=5.0)
        clip3 = ImageClip(path="image3.jpg", start_time=10.0, duration=5.0)

        track.add_clip(clip1)
        track.add_clip(clip2)
        track.add_clip(clip3)

        # Test active clips at different times
        assert len(track.get_active_clips_at_time(0.0)) == 1
        assert len(track.get_active_clips_at_time(4.0)) == 2  # clip1 and clip2 overlap
        assert len(track.get_active_clips_at_time(7.0)) == 1  # only clip2
        assert len(track.get_active_clips_at_time(12.0)) == 1  # only clip3
        assert len(track.get_active_clips_at_time(20.0)) == 0  # no clips active

    def test_video_track_has_overlapping_clips(self) -> None:
        """Test detection of overlapping clips."""
        track = VideoTrack(name="test_video_track")

        # No overlaps initially
        assert not track.has_overlapping_clips()

        # Add non-overlapping clips
        clip1 = ImageClip(path="image1.jpg", start_time=0.0, duration=5.0)
        clip2 = ImageClip(path="image2.jpg", start_time=5.0, duration=5.0)
        track.add_clip(clip1)
        track.add_clip(clip2)
        assert not track.has_overlapping_clips()

        # Add overlapping clip
        clip3 = ImageClip(path="image3.jpg", start_time=3.0, duration=5.0)
        track.add_clip(clip3)
        assert track.has_overlapping_clips()

    def test_video_track_return_true_infinite_duration_specific(self) -> None:
        """Test the specific 'return True  # Infinite duration clips overlap with everything' line."""
        track = VideoTrack(name="test_video_track")

        # Test with first clip having infinite duration (earlier start time)
        clip1 = ImageClip(
            path="image1.jpg", start_time=0.0
        )  # No duration/end_time = infinite
        clip2 = ImageClip(path="image2.jpg", start_time=5.0, duration=5.0)
        track.add_clip(clip1)
        track.add_clip(clip2)
        assert (
            track.has_overlapping_clips()
        )  # Should return True due to infinite duration

        # Test with second clip having infinite duration (later start time - won't trigger the line)
        track = VideoTrack(name="test_video_track")
        clip1 = ImageClip(path="image1.jpg", start_time=0.0, duration=5.0)
        clip2 = ImageClip(
            path="image2.jpg", start_time=5.0
        )  # No duration/end_time = infinite
        track.add_clip(clip1)
        track.add_clip(clip2)
        assert (
            not track.has_overlapping_clips()
        )  # Won't trigger because infinite clip is second

        # Test with middle clip having infinite duration (middle start time)
        track = VideoTrack(name="test_video_track")
        clip1 = ImageClip(path="image1.jpg", start_time=0.0, duration=5.0)
        clip2 = ImageClip(
            path="image2.jpg", start_time=3.0
        )  # No duration/end_time = infinite
        clip3 = ImageClip(path="image3.jpg", start_time=10.0, duration=5.0)
        track.add_clip(clip1)
        track.add_clip(clip2)
        track.add_clip(clip3)
        assert (
            track.has_overlapping_clips()
        )  # Should return True due to infinite duration

    def test_video_track_return_true_infinite_duration_edge_cases(self) -> None:
        """Test edge cases for the 'return True  # Infinite duration clips overlap with everything' line."""
        track = VideoTrack(name="test_video_track")

        # Test with single infinite duration clip (should not trigger overlap check)
        clip = ImageClip(
            path="image1.jpg", start_time=0.0
        )  # No duration/end_time = infinite
        track.add_clip(clip)
        assert not track.has_overlapping_clips()  # Only one clip, no overlap possible

        # Test with two infinite duration clips
        track = VideoTrack(name="test_video_track")
        clip1 = ImageClip(
            path="image1.jpg", start_time=0.0
        )  # No duration/end_time = infinite
        clip2 = ImageClip(
            path="image2.jpg", start_time=5.0
        )  # No duration/end_time = infinite
        track.add_clip(clip1)
        track.add_clip(clip2)
        assert (
            track.has_overlapping_clips()
        )  # Should return True due to infinite duration

        # Test with all clips having infinite duration
        track = VideoTrack(name="test_video_track")
        clip1 = ImageClip(
            path="image1.jpg", start_time=0.0
        )  # No duration/end_time = infinite
        clip2 = ImageClip(
            path="image2.jpg", start_time=5.0
        )  # No duration/end_time = infinite
        clip3 = ImageClip(
            path="image3.jpg", start_time=10.0
        )  # No duration/end_time = infinite
        track.add_clip(clip1)
        track.add_clip(clip2)
        track.add_clip(clip3)
        assert (
            track.has_overlapping_clips()
        )  # Should return True due to infinite duration


class TestAudioTrack:
    """Test AudioTrack model."""

    def test_audio_track_creation(self) -> None:
        """Test basic audio track creation."""
        track = AudioTrack(name="test_audio_track")
        assert track.name == "test_audio_track"
        assert len(track.clips) == 0
        assert track.volume == 1.0
        assert track.muted is False

    def test_audio_track_add_clip(self) -> None:
        """Test adding clips to audio track."""
        track = AudioTrack(name="test_audio_track")
        clip = AudioClip(path="test_audio.mp3", start_time=0.0, duration=10.0)
        track.add_clip(clip)
        assert len(track.clips) == 1
        assert track.clips[0] == clip

    def test_audio_track_return_true_infinite_duration_specific(self) -> None:
        """Test the specific 'return True  # Infinite duration clips overlap with everything' line."""
        track = AudioTrack(name="test_audio_track")

        # Test with first clip having infinite duration (earlier start time)
        clip1 = AudioClip(
            path="audio1.mp3", start_time=0.0
        )  # No duration/end_time = infinite
        clip2 = AudioClip(path="audio2.mp3", start_time=5.0, duration=5.0)
        track.add_clip(clip1)
        track.add_clip(clip2)
        assert (
            track.has_overlapping_clips()
        )  # Should return True due to infinite duration

        # Test with second clip having infinite duration (later start time - won't trigger the line)
        track = AudioTrack(name="test_audio_track")
        clip1 = AudioClip(path="audio1.mp3", start_time=0.0, duration=5.0)
        clip2 = AudioClip(
            path="audio2.mp3", start_time=5.0
        )  # No duration/end_time = infinite
        track.add_clip(clip1)
        track.add_clip(clip2)
        assert (
            not track.has_overlapping_clips()
        )  # Won't trigger because infinite clip is second


class TestTextTrack:
    """Test TextTrack model."""

    def test_text_track_creation(self) -> None:
        """Test basic text track creation."""
        track = TextTrack(name="test_text_track")
        assert track.name == "test_text_track"
        assert len(track.clips) == 0
        assert track.z_order == 0
        assert track.visible is True

    def test_text_track_add_clip(self) -> None:
        """Test adding clips to text track."""
        track = TextTrack(name="test_text_track")
        clip = TextClip(content="Test text", start_time=0.0, duration=5.0)
        track.add_clip(clip)
        assert len(track.clips) == 1
        assert track.clips[0] == clip

    def test_text_track_return_true_infinite_duration_specific(self) -> None:
        """Test the specific 'return True  # Infinite duration clips overlap with everything' line."""
        track = TextTrack(name="test_text_track")

        # Test with first clip having infinite duration (earlier start time)
        clip1 = TextClip(
            content="Text 1", start_time=0.0
        )  # No duration/end_time = infinite
        clip2 = TextClip(content="Text 2", start_time=5.0, duration=5.0)
        track.add_clip(clip1)
        track.add_clip(clip2)
        assert (
            track.has_overlapping_clips()
        )  # Should return True due to infinite duration

        # Test with second clip having infinite duration (later start time - won't trigger the line)
        track = TextTrack(name="test_text_track")
        clip1 = TextClip(content="Text 1", start_time=0.0, duration=5.0)
        clip2 = TextClip(
            content="Text 2", start_time=5.0
        )  # No duration/end_time = infinite
        track.add_clip(clip1)
        track.add_clip(clip2)
        assert (
            not track.has_overlapping_clips()
        )  # Won't trigger because infinite clip is second
