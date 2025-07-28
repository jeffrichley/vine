"""Pydantic models for Project Vine video composition framework."""

from vine.models.animation_config import AnimationConfig
from vine.models.audio_config import AudioConfig, MusicConfig, VoiceConfig
from vine.models.base import BaseModel
from vine.models.effects import EffectConfig, KenBurnsConfig, SlideConfig, StaticConfig
from vine.models.tracks import (
    AudioClip,
    AudioTrack,
    ImageClip,
    TextClip,
    TextTrack,
    VideoClip,
    VideoTrack,
)
from vine.models.transition import Transition
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
    "VideoTrack",
    "AudioTrack",
    "TextTrack",
    "VideoClip",
    "ImageClip",
    "TextClip",
    "AudioClip",
    "Transition",
    "AnimationConfig",
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
