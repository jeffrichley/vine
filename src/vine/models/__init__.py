"""Pydantic models for Project Vine video composition framework."""

from vine.models.animation_config import AnimationConfig
from vine.models.audio_config import AudioConfig, MusicConfig, VoiceConfig
from vine.models.base import BaseModel
from vine.models.effects import EffectConfig, KenBurnsConfig, SlideConfig, StaticConfig
from vine.models.timeline_block import TimelineBlock
from vine.models.transition_config import TransitionConfig
from vine.models.transitions import (
    CrossfadeConfig,
    FadeConfig,
    SlideTransitionConfig,
    TransitionType,
)
from vine.models.video_spec import VideoSpec

__all__ = [
    "BaseModel",
    "VideoSpec",
    "TimelineBlock",
    "AnimationConfig",
    "TransitionConfig",
    "AudioConfig",
    "VoiceConfig",
    "MusicConfig",
    "EffectConfig",
    "KenBurnsConfig",
    "SlideConfig",
    "StaticConfig",
    "TransitionType",
    "FadeConfig",
    "CrossfadeConfig",
    "SlideTransitionConfig",
]
