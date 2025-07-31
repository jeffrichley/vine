"""Protocol definitions for Project Vine models."""

from typing import Protocol, runtime_checkable


@runtime_checkable
class HasEndTime(Protocol):
    """Protocol for objects that have an end time."""

    def get_end_time(self) -> float | None:
        """Get the end time of the object."""
        ...


@runtime_checkable
class Clip(Protocol):
    """Protocol for clip objects that have timing and activity methods."""

    start_time: float

    def get_end_time(self) -> float | None:
        """Get the end time of the clip."""
        ...

    def is_active_at_time(self, time: float) -> bool:
        """Check if the clip is active at the given time."""
        ...


@runtime_checkable
class HasClips(Protocol):
    """Protocol for objects that have clips."""

    @property
    def clips(self) -> list[Clip]:
        """Get the list of clips."""
        ...
