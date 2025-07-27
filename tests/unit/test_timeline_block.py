"""Unit tests for TimelineBlock model."""

import pytest

from vine.models import AnimationConfig, KenBurnsConfig, TimelineBlock


class TestTimelineBlock:
    """Test TimelineBlock model."""

    def test_create_video_block(self):
        """Test creating a video block."""
        block = TimelineBlock(
            block_type="video",
            video_path="/path/to/video.mp4",
            start_time=0.0,
            duration=10.0,
        )

        assert block.block_type == "video"
        assert block.video_path == "/path/to/video.mp4"
        assert block.start_time == 0.0
        assert block.duration == 10.0
        assert block.get_end_time() == 10.0

    def test_create_image_block(self):
        """Test creating an image block."""
        block = TimelineBlock(
            block_type="image",
            image_path="/path/to/image.jpg",
            start_time=5.0,
            duration=3.0,
        )

        assert block.block_type == "image"
        assert block.image_path == "/path/to/image.jpg"
        assert block.start_time == 5.0
        assert block.duration == 3.0
        assert block.get_end_time() == 8.0

    def test_create_audio_block(self):
        """Test creating an audio block."""
        block = TimelineBlock(
            block_type="audio",
            audio_path="/path/to/audio.mp3",
            start_time=0.0,
            duration=5.0,
        )

        assert block.block_type == "audio"
        assert block.audio_path == "/path/to/audio.mp3"

    def test_create_text_block(self):
        """Test creating a text block."""
        block = TimelineBlock(
            block_type="text", text_content="Hello World", start_time=0.0, duration=3.0
        )

        assert block.block_type == "text"
        assert block.text_content == "Hello World"

    def test_block_validation(self):
        """Test block validation."""
        # Test video block without video_path
        with pytest.raises(ValueError, match="Video blocks must have a video_path"):
            TimelineBlock(block_type="video", start_time=0.0)

        # Test image block without image_path
        with pytest.raises(ValueError, match="Image blocks must have an image_path"):
            TimelineBlock(block_type="image", start_time=0.0)

        # Test audio block without audio_path
        with pytest.raises(ValueError, match="Audio blocks must have an audio_path"):
            TimelineBlock(block_type="audio", start_time=0.0)

        # Test text block without text_content
        with pytest.raises(ValueError, match="Text blocks must have text_content"):
            TimelineBlock(block_type="text", start_time=0.0)

        # Test invalid opacity
        with pytest.raises(ValueError, match="Input should be less than or equal to 1"):
            TimelineBlock(
                block_type="video", video_path="/path/to/video.mp4", opacity=1.5
            )

    def test_block_validation_empty_strings(self):
        """Test block validation with empty strings."""
        # Test video block with empty video_path
        with pytest.raises(ValueError, match="Video blocks must have a video_path"):
            TimelineBlock(block_type="video", video_path="", start_time=0.0)

        # Test image block with empty image_path
        with pytest.raises(ValueError, match="Image blocks must have an image_path"):
            TimelineBlock(block_type="image", image_path="", start_time=0.0)

        # Test audio block with empty audio_path
        with pytest.raises(ValueError, match="Audio blocks must have an audio_path"):
            TimelineBlock(block_type="audio", audio_path="", start_time=0.0)

        # Test text block with empty text_content
        with pytest.raises(ValueError, match="Text blocks must have text_content"):
            TimelineBlock(block_type="text", text_content="", start_time=0.0)

    def test_block_overlap_detection(self):
        """Test block overlap detection."""
        block1 = TimelineBlock(
            block_type="video",
            video_path="/path/to/video1.mp4",
            start_time=0.0,
            duration=5.0,
        )

        block2 = TimelineBlock(
            block_type="video",
            video_path="/path/to/video2.mp4",
            start_time=3.0,
            duration=5.0,
        )

        block3 = TimelineBlock(
            block_type="video",
            video_path="/path/to/video3.mp4",
            start_time=10.0,
            duration=5.0,
        )

        assert block1.overlaps_with(block2)  # Overlaps
        assert not block1.overlaps_with(block3)  # No overlap
        assert not block2.overlaps_with(block3)  # No overlap

    def test_block_methods(self):
        """Test TimelineBlock methods."""
        block = TimelineBlock(
            block_type="video",
            video_path="/path/to/video.mp4",
            start_time=0.0,
            duration=5.0,
        )

        # Test get_end_time
        assert block.get_end_time() == 5.0

        # Test is_active_at_time
        assert block.is_active_at_time(2.0) is True
        assert block.is_active_at_time(6.0) is False
        assert block.is_active_at_time(-1.0) is False

        # Test add_animation
        ken_burns = KenBurnsConfig()
        animation = AnimationConfig(effect=ken_burns, start_time=0.0, duration=3.0)
        block.add_animation(animation)
        assert len(block.animations) == 1

        # Test get_animations_at_time
        active_anims = block.get_animations_at_time(1.0)
        assert len(active_anims) == 1
        assert active_anims[0] == animation

        # Test get_animations_at_time outside animation
        active_anims = block.get_animations_at_time(4.0)
        assert len(active_anims) == 0

    def test_block_without_duration(self):
        """Test block without duration."""
        block = TimelineBlock(
            block_type="video", video_path="/path/to/video.mp4", start_time=0.0
        )

        assert block.get_end_time() is None
        assert block.is_active_at_time(100.0) is True  # Always active after start
        assert block.is_active_at_time(-1.0) is False

    def test_block_overlap_without_duration(self):
        """Test block overlap when one or both blocks have no duration."""
        block1 = TimelineBlock(
            block_type="video",
            video_path="/path/to/video1.mp4",
            start_time=0.0,
            duration=5.0,
        )

        block2 = TimelineBlock(
            block_type="video",
            video_path="/path/to/video2.mp4",
            start_time=5.0,  # No duration
        )

        # Should return False when either block has no duration
        assert block1.overlaps_with(block2) is False
        assert block2.overlaps_with(block1) is False

    def test_block_dimension_validation(self):
        """Test block dimension validation."""
        # Test invalid width
        with pytest.raises(
            ValueError, match="Input should be greater than or equal to 1"
        ):
            TimelineBlock(block_type="video", video_path="/path/to/video.mp4", width=0)

        # Test invalid height
        with pytest.raises(
            ValueError, match="Input should be greater than or equal to 1"
        ):
            TimelineBlock(block_type="video", video_path="/path/to/video.mp4", height=0)

    def test_block_time_validation(self):
        """Test block time validation."""
        # Test negative start_time
        with pytest.raises(
            ValueError, match="Input should be greater than or equal to 0"
        ):
            TimelineBlock(
                block_type="video", video_path="/path/to/video.mp4", start_time=-1.0
            )

        # Test negative duration
        with pytest.raises(
            ValueError, match="Input should be greater than or equal to 0"
        ):
            TimelineBlock(
                block_type="video", video_path="/path/to/video.mp4", duration=-1.0
            )

    def test_block_time_validation_none_values(self):
        """Test block time validation with None values."""
        # Test that None duration is allowed
        block = TimelineBlock(
            block_type="video",
            video_path="/path/to/video.mp4",
            start_time=0.0,
            duration=None,
        )
        assert block.duration is None

    def test_block_opacity_validation(self):
        """Test block opacity validation."""
        # Test opacity too low
        with pytest.raises(
            ValueError, match="Input should be greater than or equal to 0"
        ):
            TimelineBlock(
                block_type="video", video_path="/path/to/video.mp4", opacity=-0.1
            )

        # Test opacity too high
        with pytest.raises(ValueError, match="Input should be less than or equal to 1"):
            TimelineBlock(
                block_type="video", video_path="/path/to/video.mp4", opacity=1.1
            )

    def test_block_dimension_validation_none_values(self):
        """Test block dimension validation with None values."""
        # Test that None dimensions are allowed
        block = TimelineBlock(
            block_type="video", video_path="/path/to/video.mp4", width=None, height=None
        )
        assert block.width is None
        assert block.height is None
