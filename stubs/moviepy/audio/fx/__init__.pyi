"""Stub file for moviepy.audio.fx module."""

from typing import Any

from ... import AudioClip

def AudioFadeIn(
    clip: AudioClip, duration: float, *args: Any, **kwargs: Any
) -> AudioClip: ...
def AudioFadeOut(
    clip: AudioClip, duration: float, *args: Any, **kwargs: Any
) -> AudioClip: ...
def AudioNormalize(clip: AudioClip, *args: Any, **kwargs: Any) -> AudioClip: ...

__all__ = ["AudioFadeIn", "AudioFadeOut", "AudioNormalize"]
