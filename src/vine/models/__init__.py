"""Pydantic models for Project Vine video composition framework."""

from vine.models.animation_config import AnimationConfig
from vine.models.audio_config import AudioConfig, MusicConfig, VoiceConfig
from vine.models.base import BaseModel
from vine.models.effects import BaseEffect, KenBurnsEffect, SlideEffect, StaticEffect
from vine.models.tracks import (
    AudioClip,
    AudioTrack,
    ImageClip,
    TextClip,
    TextTrack,
    VideoClip,
    VideoTrack,
)
from vine.models.transition import Transition, TransitionType
from vine.models.transitions import (
    BaseTransition,
    CrossfadeTransition,
    FadeTransition,
    SlideTransition,
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
    "BaseEffect",
    "KenBurnsEffect",
    "SlideEffect",
    "StaticEffect",
    "BaseTransition",
    "FadeTransition",
    "CrossfadeTransition",
    "SlideTransition",
    "TransitionType",
]
