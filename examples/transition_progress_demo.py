#!/usr/bin/env python3
"""Demonstration of Transition.get_progress_at_time functionality."""

from vine.models.transition import Transition


def demo_basic_progress():
    """Demonstrate basic progress calculation."""
    print("=== Basic Progress Calculation ===")
    transition = Transition(transition_type="fade", start_time=5.0, duration=2.0)

    times = [4.0, 4.9, 5.0, 5.5, 6.0, 6.5, 7.0, 7.1, 10.0]

    for time in times:
        progress = transition.get_progress_at_time(time)
        status = (
            "before"
            if time < transition.start_time
            else "during" if time <= transition.get_end_time() else "after"
        )
        print(f"Time: {time:4.1f}s -> Progress: {progress:5.3f} ({status})")


def demo_edge_cases():
    """Demonstrate edge cases."""
    print("\n=== Edge Cases ===")

    # Zero duration transition
    zero_transition = Transition(transition_type="fade", start_time=5.0, duration=0.0)
    print(
        f"Zero duration transition at 5.0s: {zero_transition.get_progress_at_time(5.0)}"
    )

    # Very short duration
    short_transition = Transition(
        transition_type="crossfade", start_time=10.0, duration=0.001
    )
    print(
        f"Short transition at 10.0005s: {short_transition.get_progress_at_time(10.0005):.6f}"
    )

    # Long duration
    long_transition = Transition(transition_type="slide", start_time=0.0, duration=30.0)
    print(f"Long transition at 15.0s: {long_transition.get_progress_at_time(15.0):.6f}")


def demo_multiple_transitions():
    """Demonstrate multiple transitions."""
    print("\n=== Multiple Transitions ===")

    transitions = [
        Transition(transition_type="fade", start_time=0.0, duration=1.0),
        Transition(transition_type="crossfade", start_time=5.0, duration=2.0),
        Transition(transition_type="slide", start_time=10.0, duration=0.5),
    ]

    times = [0.5, 1.0, 2.0, 6.0, 7.0, 10.25, 10.5, 11.0]

    for time in times:
        print(f"\nTime: {time}s")
        for i, transition in enumerate(transitions, 1):
            progress = transition.get_progress_at_time(time)
            print(f"  Transition {i} ({transition.transition_type}): {progress:.3f}")


def demo_all_transition_types():
    """Demonstrate all transition types have identical progress calculation."""
    print("\n=== All Transition Types ===")

    transition_types = ["fade", "crossfade", "slide", "wipe", "dissolve"]
    time = 11.0  # During transition

    for transition_type in transition_types:
        transition = Transition(
            transition_type=transition_type, start_time=10.0, duration=2.0
        )
        progress = transition.get_progress_at_time(time)
        print(f"{transition_type:10s}: {progress:.3f}")


def demo_with_metadata_and_tracks():
    """Demonstrate that metadata and track targeting don't affect progress."""
    print("\n=== Metadata and Track Targeting ===")

    # Basic transition
    basic = Transition(transition_type="fade", start_time=5.0, duration=2.0)

    # Transition with metadata
    with_metadata = Transition(
        transition_type="fade",
        start_time=5.0,
        duration=2.0,
        metadata={"intensity": 0.8, "custom_param": "value"},
    )

    # Transition with track targeting
    with_tracks = Transition(
        transition_type="fade",
        start_time=5.0,
        duration=2.0,
        from_tracks=["track1", "track2"],
        to_tracks=["track3", "track4"],
    )

    time = 6.0  # During transition

    print(f"Basic transition at {time}s: {basic.get_progress_at_time(time):.3f}")
    print(f"With metadata at {time}s: {with_metadata.get_progress_at_time(time):.3f}")
    print(f"With tracks at {time}s: {with_tracks.get_progress_at_time(time):.3f}")


if __name__ == "__main__":
    demo_basic_progress()
    demo_edge_cases()
    demo_multiple_transitions()
    demo_all_transition_types()
    demo_with_metadata_and_tracks()

    print("\n=== Summary ===")
    print("The get_progress_at_time method provides:")
    print("- Linear progress from 0.0 to 1.0 during transition")
    print("- 0.0 before transition starts")
    print("- 1.0 after transition ends")
    print("- Handles zero duration transitions")
    print("- Works consistently across all transition types")
    print("- Unaffected by metadata or track targeting")
