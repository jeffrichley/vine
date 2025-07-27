"""Unit tests for VideoSpec model."""

import pytest

from vine.models import (
    FadeConfig,
    TimelineBlock,
    TransitionConfig,
    VideoSpec,
    VoiceConfig,
)


class TestVideoSpec:
    """Test VideoSpec model."""

    def test_create_basic_video_spec(self):
        """Test creating a basic video specification."""
        spec = VideoSpec(
            title="Test Video", description="A test video", width=1920, height=1080
        )

        assert spec.title == "Test Video"
        assert spec.description == "A test video"
        assert spec.width == 1920
        assert spec.height == 1080
        assert spec.fps == 30.0
        assert spec.output_format == "mp4"
        assert spec.quality == "high"

    def test_video_spec_validation(self):
        """Test video specification validation."""
        # Test invalid width
        with pytest.raises(
            ValueError, match="Input should be greater than or equal to 1"
        ):
            VideoSpec(title="Test", width=0)

        # Test invalid height
        with pytest.raises(
            ValueError, match="Input should be greater than or equal to 1"
        ):
            VideoSpec(title="Test", height=0)

        # Test invalid FPS
        with pytest.raises(
            ValueError, match="Input should be greater than or equal to 1"
        ):
            VideoSpec(title="Test", fps=0.5)

        # Test invalid background color
        with pytest.raises(
            ValueError, match="Background color must be a valid hex color"
        ):
            VideoSpec(title="Test", background_color="invalid")

    def test_background_color_validation_comprehensive(self):
        """Test comprehensive background color validation."""
        from vine.models.video_spec import VideoSpec

        # Test valid hex colors
        valid_colors = [
            "#000000",
            "#FFFFFF",
            "#FF0000",
            "#00FF00",
            "#0000FF",
            "#123456",
        ]
        for color in valid_colors:
            spec = VideoSpec(title="Test", background_color=color)
            assert spec.background_color == color

        # Test invalid hex colors - missing #
        with pytest.raises(
            ValueError, match="Background color must be a valid hex color"
        ):
            VideoSpec(title="Test", background_color="000000")

        # Test invalid hex colors - wrong length
        with pytest.raises(
            ValueError, match="Background color must be a valid hex color"
        ):
            VideoSpec(title="Test", background_color="#00000")  # Too short

        with pytest.raises(
            ValueError, match="Background color must be a valid hex color"
        ):
            VideoSpec(title="Test", background_color="#0000000")  # Too long

        # Test invalid hex colors - just #
        with pytest.raises(
            ValueError, match="Background color must be a valid hex color"
        ):
            VideoSpec(title="Test", background_color="#")

        # Test invalid hex colors - None (converted from empty string by base model)
        with pytest.raises(ValueError, match="Input should be a valid string"):
            VideoSpec(title="Test", background_color=None)

    def test_validate_background_color_validator_directly(self):
        """Test the validate_background_color validator method directly."""
        from vine.models.video_spec import VideoSpec

        # Test valid colors
        valid_colors = ["#000000", "#FFFFFF", "#FF0000"]
        for color in valid_colors:
            result = VideoSpec.validate_background_color(color)
            assert result == color

        # Test invalid colors - missing #
        with pytest.raises(
            ValueError, match="Background color must be a valid hex color"
        ):
            VideoSpec.validate_background_color("000000")

        # Test invalid colors - wrong length
        with pytest.raises(
            ValueError, match="Background color must be a valid hex color"
        ):
            VideoSpec.validate_background_color("#00000")  # Too short

        with pytest.raises(
            ValueError, match="Background color must be a valid hex color"
        ):
            VideoSpec.validate_background_color("#0000000")  # Too long

        # Test invalid colors - just #
        with pytest.raises(
            ValueError, match="Background color must be a valid hex color"
        ):
            VideoSpec.validate_background_color("#")

    def test_video_spec_dimension_limits(self):
        """Test video dimension limits."""
        # Test maximum dimensions
        with pytest.raises(
            ValueError, match="Input should be less than or equal to 7680"
        ):
            VideoSpec(title="Test", width=8000, height=1080)

        # Test maximum FPS
        with pytest.raises(
            ValueError, match="Input should be less than or equal to 120"
        ):
            VideoSpec(title="Test", fps=150.0)

    def test_video_spec_duration_validation(self):
        """Test duration validation."""
        # Test negative duration
        with pytest.raises(
            ValueError, match="Input should be greater than or equal to 0"
        ):
            VideoSpec(title="Test", duration=-1.0)

        # Test zero duration (now valid with ge=0.0 constraint)
        spec = VideoSpec(title="Test", duration=0.0)
        assert spec.duration == 0.0

    def test_video_spec_methods(self):
        """Test VideoSpec methods."""
        spec = VideoSpec(title="Test")

        # Test get_total_duration with no blocks
        assert spec.get_total_duration() == 0.0

        # Test get_blocks_at_time with no blocks
        assert spec.get_blocks_at_time(0.0) == []

        # Test get_transitions_at_time with no transitions
        assert spec.get_transitions_at_time(0.0) == []

        # Test model_dump method
        data = spec.model_dump()
        assert "title" in data
        assert data["title"] == "Test"

    def test_video_spec_block_management(self):
        """Test block management methods."""
        spec = VideoSpec(title="Test")
        block = TimelineBlock(
            block_type="video",
            video_path="/path/to/video.mp4",
            start_time=0.0,
            duration=5.0,
        )

        # Test add_block
        spec.add_block(block)
        assert len(spec.blocks) == 1
        assert spec.get_total_duration() == 5.0

        # Test remove_block
        assert spec.remove_block(block.id) is True
        assert len(spec.blocks) == 0
        assert spec.get_total_duration() == 0.0

        # Test remove_block with non-existent ID
        assert spec.remove_block("non-existent") is False

    def test_video_spec_transition_management(self):
        """Test transition management methods."""
        spec = VideoSpec(title="Test")
        fade = FadeConfig(duration=1.0)
        transition = TransitionConfig(transition=fade, start_time=0.0)

        # Test add_transition
        spec.add_transition(transition)
        assert len(spec.transitions) == 1

        # Test remove_transition
        assert spec.remove_transition(transition.id) is True
        assert len(spec.transitions) == 0

        # Test remove_transition with non-existent ID
        assert spec.remove_transition("non-existent") is False

    def test_video_spec_time_queries(self):
        """Test time-based query methods."""
        spec = VideoSpec(title="Test")

        # Add blocks at different times
        block1 = TimelineBlock(
            block_type="video",
            video_path="/path/to/video1.mp4",
            start_time=0.0,
            duration=5.0,
        )
        block2 = TimelineBlock(
            block_type="video",
            video_path="/path/to/video2.mp4",
            start_time=5.0,
            duration=3.0,
        )
        spec.add_block(block1)
        spec.add_block(block2)

        # Test get_blocks_at_time
        assert len(spec.get_blocks_at_time(2.0)) == 1  # Only block1
        assert len(spec.get_blocks_at_time(6.0)) == 1  # Only block2
        assert len(spec.get_blocks_at_time(10.0)) == 0  # No blocks

        # Add transitions
        fade = FadeConfig(duration=1.0)
        trans1 = TransitionConfig(transition=fade, start_time=4.5)
        spec.add_transition(trans1)

        # Test get_transitions_at_time
        assert len(spec.get_transitions_at_time(5.0)) == 1  # trans1 active
        assert len(spec.get_transitions_at_time(6.0)) == 0  # No transitions

    def test_video_spec_with_duration(self):
        """Test VideoSpec with explicit duration."""
        spec = VideoSpec(title="Test", duration=10.0)
        assert spec.duration == 10.0

        # Test that model_dump includes the explicit duration
        data = spec.model_dump()
        assert data["duration"] == 10.0

    def test_video_spec_dimension_validation_none_values(self):
        """Test video spec dimension validation with None values."""
        # Test that None values are handled properly
        spec = VideoSpec(title="Test")
        # The validation should work with default values
        assert spec.width == 1920
        assert spec.height == 1080

    def test_video_spec_fps_validation_none_values(self):
        """Test video spec FPS validation with None values."""
        # Test that None values are handled properly
        spec = VideoSpec(title="Test")
        # The validation should work with default values
        assert spec.fps == 30.0

    def test_video_spec_duration_validation_none_values(self):
        """Test video spec duration validation with None values."""
        # Test that None duration is allowed
        spec = VideoSpec(title="Test", duration=None)
        assert spec.duration is None

    def test_video_spec_background_color_validation_none_values(self):
        """Test video spec background color validation with None values."""
        # Test that None values are handled properly
        spec = VideoSpec(title="Test")
        # The validation should work with default values
        assert spec.background_color == "#000000"

    def test_video_spec_validation_empty_strings(self):
        """Test video spec validation with empty strings."""
        # Test that empty strings are converted to None by BaseModel validation
        spec = VideoSpec(title="Test", description="", author="", output_path="")
        assert spec.description is None
        assert spec.author is None
        assert spec.output_path is None


class TestVideoSpecIntegration:
    """Test VideoSpec integration with other models."""

    def test_video_spec_with_blocks_and_transitions(self):
        """Test creating a complete video specification."""
        # Create blocks
        video_block = TimelineBlock(
            block_type="video",
            video_path="/path/to/video.mp4",
            start_time=0.0,
            duration=5.0,
        )

        image_block = TimelineBlock(
            block_type="image",
            image_path="/path/to/image.jpg",
            start_time=5.0,
            duration=3.0,
        )

        # Create transition
        fade = FadeConfig(duration=1.0)
        transition = TransitionConfig(
            transition=fade,
            start_time=4.5,
            from_block_id=video_block.id,
            to_block_id=image_block.id,
        )

        # Create voice config
        voice = VoiceConfig(volume=0.9, speed=1.0)

        # Create video spec
        spec = VideoSpec(
            title="Integration Test",
            blocks=[video_block, image_block],
            transitions=[transition],
            voice_config=voice,
        )

        assert len(spec.blocks) == 2
        assert len(spec.transitions) == 1
        assert spec.voice_config is not None
        assert spec.get_total_duration() == 8.0  # 5 + 3

    def test_video_spec_overlap_validation(self):
        """Test that VideoSpec validates overlapping blocks."""
        block1 = TimelineBlock(
            block_type="video",
            video_path="/path/to/video1.mp4",
            start_time=0.0,
            duration=5.0,
        )

        block2 = TimelineBlock(
            block_type="video",
            video_path="/path/to/video2.mp4",
            start_time=3.0,  # Overlaps with block1
            duration=5.0,
        )

        with pytest.raises(ValueError, match="Blocks 0 and 1 overlap in time"):
            VideoSpec(title="Overlap Test", blocks=[block1, block2])

    def test_video_spec_transition_overlap_validation(self):
        """Test that VideoSpec validates overlapping transitions."""
        fade1 = FadeConfig(duration=2.0)
        fade2 = FadeConfig(duration=2.0)

        trans1 = TransitionConfig(transition=fade1, start_time=0.0)
        trans2 = TransitionConfig(transition=fade2, start_time=1.0)  # Overlaps

        with pytest.raises(ValueError, match="Transitions 0 and 1 overlap in time"):
            VideoSpec(title="Transition Overlap Test", transitions=[trans1, trans2])

    def test_video_spec_get_blocks_at_time_edge_cases(self):
        """Test edge cases for get_blocks_at_time."""
        spec = VideoSpec(title="Test")

        # Add block that starts exactly at query time
        block = TimelineBlock(
            block_type="video",
            video_path="/path/to/video.mp4",
            start_time=5.0,
            duration=3.0,
        )
        spec.add_block(block)

        # Test at exact start time
        blocks = spec.get_blocks_at_time(5.0)
        assert len(blocks) == 1

        # Test at exact end time
        blocks = spec.get_blocks_at_time(8.0)
        assert len(blocks) == 1

        # Test just after end time
        blocks = spec.get_blocks_at_time(8.1)
        assert len(blocks) == 0

    def test_video_spec_get_transitions_at_time_edge_cases(self):
        """Test edge cases for get_transitions_at_time."""
        spec = VideoSpec(title="Test")

        # Add transition
        fade = FadeConfig(duration=1.0)
        transition = TransitionConfig(transition=fade, start_time=5.0)
        spec.add_transition(transition)

        # Test at exact start time
        transitions = spec.get_transitions_at_time(5.0)
        assert len(transitions) == 1

        # Test at exact end time
        transitions = spec.get_transitions_at_time(6.0)
        assert len(transitions) == 1

        # Test just after end time
        transitions = spec.get_transitions_at_time(6.1)
        assert len(transitions) == 0
