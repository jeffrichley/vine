"""Stub file for moviepy.audio.io.AudioFileClip module."""


class AudioFileClip:
    def __init__(
        self,
        filename: str,
        decode_file: bool = False,
        buffersize: int = 200000,
        nbytes: int = 2,
        fps: int = 44100,
    ) -> None: ...
    def close(self) -> None: ...

__all__ = ["AudioFileClip"]
