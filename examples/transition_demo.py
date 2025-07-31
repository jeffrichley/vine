#!/usr/bin/env python3
"""
Demo showcasing the new .with_transitions() method with BaseTransition classes.
"""

from vine.builder.timeline_builder import TimelineBuilder
from vine.models.effects import KenBurnsEffect, SlideEffect
from vine.models.transition import TransitionDirection
from vine.models.transitions import CrossfadeTransition, FadeTransition, SlideTransition


def main():
    """Demonstrate the fluent transition API."""

    # Create a new timeline
    builder = TimelineBuilder(width=1920, height=1080, fps=30)

    print("🎬 Creating video with transitions...")

    # Add content with transitions - now using context methods
    builder.add_image("examples/assets/image1.jpg", duration=3.0).with_transitions(
        transition_in=FadeTransition(duration=1.5),
        transition_out=CrossfadeTransition(duration=2.0),
    )

    # Add more content
    builder.add_image("examples/assets/image2.jpg", duration=4.0).with_transitions(
        transition_in=SlideTransition(direction=TransitionDirection.LEFT, duration=1.0)
    )

    # Add text with effect and transition
    builder.add_text("Welcome to Project Vine!", duration=3.0).with_effect(
        KenBurnsEffect(zoom_factor=1.2)
    ).with_transitions(transition_out=FadeTransition(duration=1.0))

    # Add final content
    builder.add_text("Thanks for watching!", duration=2.0).with_effect(
        SlideEffect(direction=TransitionDirection.UP)
    ).with_transitions(
        transition_in=CrossfadeTransition(duration=0.5),
        transition_out=FadeTransition(duration=1.5),
    )

    # Build the video spec
    video_spec = builder.build()

    print("✅ Video spec created successfully!")
    print(f"📊 Total duration: {video_spec.get_total_duration():.2f} seconds")
    print(f"🎬 Video tracks: {len(video_spec.video_tracks)}")
    print(f"📝 Text tracks: {len(video_spec.text_tracks)}")

    # Show clip details with transitions
    for track in video_spec.video_tracks:
        for i, clip in enumerate(track.clips):
            print(f"  Video clip {i+1}: {clip.path}")
            if clip.transition_in:
                print(f"    Transition in: {type(clip.transition_in).__name__}")
            if clip.transition_out:
                print(f"    Transition out: {type(clip.transition_out).__name__}")

    for track in video_spec.text_tracks:
        for i, clip in enumerate(track.clips):
            print(f"  Text clip {i+1}: '{clip.content}'")
            if clip.transition_in:
                print(f"    Transition in: {type(clip.transition_in).__name__}")
            if clip.transition_out:
                print(f"    Transition out: {type(clip.transition_out).__name__}")

    print("\n🎉 Transition demo completed!")


if __name__ == "__main__":
    main()
