"""Project Vine - Media Composition Framework

A modular, agent-compatible, track-based video composition framework built on top of MoviePy.
Provides an expressive and extensible API for AI-driven and human-assisted short-form video generation.
"""

from vine.builder.timeline_builder import TimelineBuilder
from vine.defaults.defaults_manager import DefaultsManager
from vine.models import (
    AnimationConfig,
    AudioClip,
    AudioConfig,
    AudioTrack,
    CrossfadeConfig,
    EffectConfig,
    FadeConfig,
    ImageClip,
    KenBurnsConfig,
    MusicConfig,
    SlideConfig,
    SlideTransitionConfig,
    StaticConfig,
    TextClip,
    TextTrack,
    Transition,
    TransitionType,
    VideoClip,
    VideoSpec,
    VideoTrack,
    VoiceConfig,
)
from vine.registry import AnimationRegistry, EffectRegistry, TransitionRegistry

__version__ = "0.1.0"
__author__ = "Jeff Richley"
__email__ = "jeffrichley@gmail.com"

__all__ = [
    # Main API
    "TimelineBuilder",
    "VideoSpec",
    # Track models
    "VideoTrack",
    "AudioTrack",
    "TextTrack",
    # Clip models
    "VideoClip",
    "ImageClip",
    "TextClip",
    "AudioClip",
    # Transition models
    "Transition",
    "TransitionType",
    "FadeConfig",
    "CrossfadeConfig",
    "SlideTransitionConfig",
    # Animation models
    "AnimationConfig",
    "EffectConfig",
    "KenBurnsConfig",
    "SlideConfig",
    "StaticConfig",
    # Audio models
    "AudioConfig",
    "VoiceConfig",
    "MusicConfig",
    # Registry system
    "AnimationRegistry",
    "TransitionRegistry",
    "EffectRegistry",
    # Defaults system
    "DefaultsManager",
]
