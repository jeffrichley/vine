"""Protocol validation utilities for Project Vine."""

import inspect


def validate_builder_implementation() -> None:  # noqa: PLC0415
    """Runtime validation to ensure TimelineBuilder and BuilderMethodsMixin implement all BuilderProtocol methods."""
    # Import here to avoid circular dependency
    from vine.builder.timeline_builder import TimelineBuilder  # noqa: PLC0415
    from vine.models.contexts import (  # noqa: PLC0415
        BuilderMethodsMixin,
        BuilderProtocol,
    )

    # Get all methods from the protocol
    protocol_methods = {
        name: method
        for name, method in inspect.getmembers(BuilderProtocol, inspect.isfunction)
        if not name.startswith("_")
    }

    # Check TimelineBuilder
    builder_methods = {
        name: method
        for name, method in inspect.getmembers(TimelineBuilder, inspect.isfunction)
        if not name.startswith("_")
    }

    missing_in_builder = set(protocol_methods.keys()) - set(builder_methods.keys())
    if missing_in_builder:
        raise RuntimeError(
            f"TimelineBuilder is missing protocol methods: {missing_in_builder}"
        )

    # Check BuilderMethodsMixin
    mixin_methods = {
        name: method
        for name, method in inspect.getmembers(BuilderMethodsMixin, inspect.isfunction)
        if not name.startswith("_")
    }

    missing_in_mixin = set(protocol_methods.keys()) - set(mixin_methods.keys())
    if missing_in_mixin:
        raise RuntimeError(
            f"BuilderMethodsMixin is missing protocol methods: {missing_in_mixin}"
        )

    print("✅ Runtime validation: All protocol methods are implemented")
