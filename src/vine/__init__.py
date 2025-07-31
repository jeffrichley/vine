"""Project Vine - Media Composition Framework

A modular, agent-compatible, track-based video composition framework built on top of MoviePy.
Provides an expressive and extensible API for AI-driven and human-assisted short-form video generation.
"""

from vine._version import __version__, __version_info__
from vine.builder.timeline_builder import TimelineBuilder
from vine.defaults.defaults_manager import DefaultsManager
from vine.models import (
    AnimationConfig,
    AudioClip,
    AudioConfig,
    AudioTrack,
    CrossfadeTransition,
    FadeTransition,
    ImageClip,
    MusicConfig,
    SlideTransition,
    TextClip,
    TextTrack,
    Transition,
    TransitionType,
    VideoClip,
    VideoSpec,
    VideoTrack,
    VoiceConfig,
)
from vine.models.effects import KenBurnsEffect, SlideEffect, StaticEffect

__author__ = "Jeff Richley"
__email__ = "jeffrichley@gmail.com"

__all__ = [
    # Version info
    "__version__",
    "__version_info__",
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
    "FadeTransition",
    "CrossfadeTransition",
    "SlideTransition",
    # Animation models
    "AnimationConfig",
    # Effect models
    "KenBurnsEffect",
    "SlideEffect",
    "StaticEffect",
    # Audio models
    "AudioConfig",
    "VoiceConfig",
    "MusicConfig",
    # Defaults system
    "DefaultsManager",
]
