"""Protocol definitions for Project Vine models."""

from typing import Protocol, runtime_checkable


@runtime_checkable
class HasEndTime(Protocol):
    """Protocol for objects that have an end time."""

    def get_end_time(self) -> float | None: ...


@runtime_checkable
class Clip(Protocol):
    """Protocol for clip objects that have timing and activity methods."""

    start_time: float

    def get_end_time(self) -> float | None: ...
    def is_active_at_time(self, time: float) -> bool: ...


@runtime_checkable
class HasClips(Protocol):
    """Protocol for objects that have clips."""

    @property
    def clips(self) -> list[Clip]: ...
