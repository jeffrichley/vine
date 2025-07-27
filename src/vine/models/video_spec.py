"""Video specification models for Project Vine."""

from typing import List, Literal, Optional

from pydantic import Field, field_validator, model_validator

from vine.models.audio_config import MusicConfig, VoiceConfig
from vine.models.base import BaseModel
from vine.models.timeline_block import TimelineBlock
from vine.models.transition_config import TransitionConfig


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

    # Timeline configuration
    blocks: List[TimelineBlock] = Field(
        default_factory=list, description="Timeline blocks"
    )
    transitions: List[TransitionConfig] = Field(
        default_factory=list, description="Transitions between blocks"
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
    background_color: str = Field("#000000", description="Background color (hex)")
    enable_audio: bool = Field(True, description="Enable audio processing")
    enable_video: bool = Field(True, description="Enable video processing")

    @field_validator("background_color")
    @classmethod
    def validate_background_color(cls, v: str) -> str:
        """Validate background color is a valid hex color."""
        if not v.startswith("#") or len(v) != 7:
            raise ValueError(
                "Background color must be a valid hex color (e.g., #000000)"
            )
        return v

    @model_validator(mode="after")
    def validate_video_configuration(self) -> "VideoSpec":
        """Validate overall video configuration."""
        blocks = self.blocks
        transitions = self.transitions

        # Check for overlapping blocks
        for i, block1 in enumerate(blocks):
            for j, block2 in enumerate(blocks[i + 1 :], i + 1):
                if block1.overlaps_with(block2):
                    raise ValueError(f"Blocks {i} and {j} overlap in time")

        # Check for overlapping transitions
        for i, trans1 in enumerate(transitions):
            for j, trans2 in enumerate(transitions[i + 1 :], i + 1):
                if trans1.overlaps_with(trans2):
                    raise ValueError(f"Transitions {i} and {j} overlap in time")

        return self

    def get_total_duration(self) -> float:
        """Calculate total duration from blocks."""
        if not self.blocks:
            return 0.0

        max_end_time = 0.0
        for block in self.blocks:
            end_time = block.get_end_time()
            if end_time is not None:
                max_end_time = max(max_end_time, end_time)

        return max_end_time

    def get_blocks_at_time(self, time: float) -> List[TimelineBlock]:
        """Get blocks active at the given time."""
        return [block for block in self.blocks if block.is_active_at_time(time)]

    def get_transitions_at_time(self, time: float) -> List[TransitionConfig]:
        """Get transitions active at the given time."""
        return [
            trans
            for trans in self.transitions
            if trans.start_time <= time <= trans.get_end_time()
        ]

    def add_block(self, block: TimelineBlock) -> None:
        """Add a block to the timeline."""
        self.blocks.append(block)

    def add_transition(self, transition: TransitionConfig) -> None:
        """Add a transition to the timeline."""
        self.transitions.append(transition)

    def remove_block(self, block_id: str) -> bool:
        """Remove a block by ID."""
        for i, block in enumerate(self.blocks):
            if block.id == block_id:
                self.blocks.pop(i)
                return True
        return False

    def remove_transition(self, transition_id: str) -> bool:
        """Remove a transition by ID."""
        for i, transition in enumerate(self.transitions):
            if transition.id == transition_id:
                self.transitions.pop(i)
                return True
        return False
