"""Unit tests for TransitionConfig model."""

import pytest

from vine.models import FadeConfig, TransitionConfig


class TestTransitionConfig:
    """Test TransitionConfig model."""

    def test_create_fade_transition(self):
        """Test creating a fade transition."""
        fade = FadeConfig(duration=1.5, fade_type="cross")

        transition = TransitionConfig(
            transition=fade,
            start_time=5.0,
            from_block_id="block1",
            to_block_id="block2",
        )

        assert transition.transition.type == "fade"
        assert transition.transition.duration == 1.5
        assert transition.start_time == 5.0
        assert transition.get_end_time() == 6.5

    def test_transition_validation(self):
        """Test transition validation."""
        fade = FadeConfig()

        # Test invalid start time
        with pytest.raises(
            ValueError, match="Input should be greater than or equal to 0"
        ):
            TransitionConfig(transition=fade, start_time=-1.0)

    def test_transition_methods(self):
        """Test TransitionConfig methods."""
        fade = FadeConfig(duration=1.0)
        transition = TransitionConfig(transition=fade, start_time=2.0)

        # Test get_end_time
        assert transition.get_end_time() == 3.0

        # Test overlaps_with
        other_trans = TransitionConfig(transition=fade, start_time=2.5)
        assert transition.overlaps_with(other_trans) is True

        non_overlapping = TransitionConfig(transition=fade, start_time=4.0)
        assert transition.overlaps_with(non_overlapping) is False

        # Test is_valid_for_blocks
        assert transition.is_valid_for_blocks("block1", "block2") is True

        # Test with specific block IDs
        specific_trans = TransitionConfig(
            transition=fade,
            start_time=2.0,
            from_block_id="block1",
            to_block_id="block2",
        )
        assert specific_trans.is_valid_for_blocks("block1", "block2") is True
        assert specific_trans.is_valid_for_blocks("block3", "block2") is False
        assert specific_trans.is_valid_for_blocks("block1", "block3") is False

    def test_transition_block_id_validation(self):
        """Test transition block ID validation with empty strings."""
        fade = FadeConfig(duration=1.0)

        # Test with empty string block IDs (should be converted to None)
        transition = TransitionConfig(
            transition=fade, start_time=0.0, from_block_id="", to_block_id=""
        )

        assert transition.from_block_id is None
        assert transition.to_block_id is None

    def test_transition_validation_none_values(self):
        """Test transition validation with None values."""
        fade = FadeConfig(duration=1.0)

        # Test that None values are allowed for optional fields
        transition = TransitionConfig(
            transition=fade, start_time=0.0, from_block_id=None, to_block_id=None
        )

        assert transition.from_block_id is None
        assert transition.to_block_id is None

    def test_transition_validation_empty_strings(self):
        """Test transition validation with empty strings."""
        fade = FadeConfig(duration=1.0)

        # Test that empty strings are converted to None by BaseModel validation
        transition = TransitionConfig(
            transition=fade, start_time=0.0, from_block_id="", to_block_id=""
        )

        assert transition.from_block_id is None
        assert transition.to_block_id is None

    def test_transition_validation_non_empty_strings(self):
        """Test transition validation with non-empty strings."""
        fade = FadeConfig(duration=1.0)

        # Test that non-empty strings are returned unchanged
        transition = TransitionConfig(
            transition=fade,
            start_time=0.0,
            from_block_id="block1",
            to_block_id="block2",
        )

        assert transition.from_block_id == "block1"
        assert transition.to_block_id == "block2"

    def test_validate_block_ids_validator_directly(self):
        """Test the validate_block_ids validator method directly."""
        from vine.models.transition_config import TransitionConfig

        # Test the validator method directly
        result1 = TransitionConfig.validate_block_ids("block1")
        assert result1 == "block1"

        result2 = TransitionConfig.validate_block_ids("")
        assert result2 is None

        result3 = TransitionConfig.validate_block_ids(None)
        assert result3 is None
