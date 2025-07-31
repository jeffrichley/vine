"""Stub file for moviepy.audio.fx module."""

from typing import Any

# ruff: noqa: N802
class AudioFadeIn:
    def __init__(self, duration: float, *args: Any, **kwargs: Any) -> None: ...

class AudioFadeOut:
    def __init__(self, duration: float, *args: Any, **kwargs: Any) -> None: ...

class AudioNormalize:
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

__all__ = ["AudioFadeIn", "AudioFadeOut", "AudioNormalize"]
