"""Stub file for moviepy.audio.fx module."""

from typing import Any

# ruff: noqa: N802
def AudioFadeIn(clip: Any, duration: float, *args: Any, **kwargs: Any) -> Any: ...
def AudioFadeOut(clip: Any, duration: float, *args: Any, **kwargs: Any) -> Any: ...
def AudioNormalize(clip: Any, *args: Any, **kwargs: Any) -> Any: ...

__all__ = ["AudioFadeIn", "AudioFadeOut", "AudioNormalize"]
