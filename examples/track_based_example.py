"""Example demonstrating the new track-based TimelineBuilder API."""

from vine.builder.timeline_builder import TimelineBuilder


def demonstrate_sequential_mode(builder):
    """Demonstrate sequential mode functionality."""
    print("\n📹 Sequential Mode (auto-appending):")
    print("-" * 40)

    # Sequential mode - elements are added one after another
    builder.add_image("background.jpg", duration=5.0)
    print("  ✓ Added background image (0.0s - 5.0s)")
    print(f"  ✓ Video track current time: {builder._video_current_time}s")

    builder.add_text("Welcome to Project Vine!", duration=3.0)
    print("  ✓ Added welcome text (0.0s - 3.0s)")
    print(f"  ✓ Text track current time: {builder._text_current_time}s")

    builder.add_voice("narration.mp3", duration=4.0)
    print("  ✓ Added voice narration (0.0s - 4.0s)")
    print(f"  ✓ Audio track current time: {builder._audio_current_time}s")


def demonstrate_explicit_mode(builder):
    """Demonstrate explicit mode functionality."""
    print("\n🎯 Explicit Mode (precise timing):")
    print("-" * 40)

    # Explicit mode - elements are positioned at specific times
    builder.add_image_at("overlay.png", start_time=2.0, duration=6.0)
    print("  ✓ Added overlay image (2.0s - 8.0s) - overlaps with background!")

    builder.add_text_at("Overlay Text", start_time=3.0, duration=4.0)
    print("  ✓ Added overlay text (3.0s - 7.0s) - overlaps with welcome text!")

    builder.add_voice_at("sound_effect.mp3", start_time=1.0, duration=2.0)
    print("  ✓ Added sound effect (1.0s - 3.0s) - overlaps with narration!")


def demonstrate_transitions(builder):
    """Demonstrate transition functionality."""
    print("\n🔄 Transitions:")
    print("-" * 40)

    # Add transitions
    builder.add_transition("fade", duration=1.0)  # Sequential mode
    print("  ✓ Added fade transition (4.0s - 5.0s)")

    builder.add_transition_at(
        "crossfade", start_time=5.0, duration=2.0
    )  # Explicit mode
    print("  ✓ Added crossfade transition (5.0s - 7.0s)")


def show_timeline_statistics(builder):
    """Show timeline statistics."""
    print("\n📊 Timeline Statistics:")
    print("-" * 40)

    # Get statistics
    track_counts = builder.get_track_count()
    clip_counts = builder.get_clip_count()
    total_duration = builder.get_duration()

    print(f"  📹 Video tracks: {track_counts['video']}")
    print(f"  🎵 Audio tracks: {track_counts['audio']}")
    print(f"  📝 Text tracks: {track_counts['text']}")
    print(f"  🎬 Video clips: {clip_counts['video']}")
    print(f"  🎵 Audio clips: {clip_counts['audio']}")
    print(f"  📝 Text clips: {clip_counts['text']}")
    print(f"  ⏱️  Total duration: {total_duration}s")


def show_track_details(builder):
    """Show detailed track information."""
    print("\n🎭 Track Details:")
    print("-" * 40)

    # Show track details
    for i, track in enumerate(builder.video_tracks):
        print(f"  📹 Video Track {i} ({track.name}):")
        for j, clip in enumerate(track.clips):
            print(
                f"    - Clip {j}: {clip.path} ({clip.start_time}s - {clip.get_end_time()}s)"
            )
        if track.has_overlapping_clips():
            print("    ⚠️  Has overlapping clips")

    for i, track in enumerate(builder.audio_tracks):
        print(f"  🎵 Audio Track {i} ({track.name}):")
        for j, clip in enumerate(track.clips):
            print(
                f"    - Clip {j}: {clip.path} ({clip.start_time}s - {clip.get_end_time()}s)"
            )
        if track.has_overlapping_clips():
            print("    ⚠️  Has overlapping clips")

    for i, track in enumerate(builder.text_tracks):
        print(f"  📝 Text Track {i} ({track.name}):")
        for j, clip in enumerate(track.clips):
            print(
                f"    - Clip {j}: '{clip.content}' ({clip.start_time}s - {clip.get_end_time()}s)"
            )
        if track.has_overlapping_clips():
            print("    ⚠️  Has overlapping clips")


def show_transitions(builder):
    """Show transition information."""
    print("\n🔄 Transitions:")
    print("-" * 40)

    for i, transition in enumerate(builder.transitions):
        print(
            f"  - Transition {i}: {transition.transition_type} ({transition.start_time}s - {transition.get_end_time()}s)"
        )


def build_video_spec(builder):
    """Build and display VideoSpec information."""
    print("\n🏗️  Building VideoSpec...")
    print("-" * 40)

    # Build the final VideoSpec
    video_spec = builder.build()

    print("  ✓ VideoSpec created successfully!")
    print(f"  ✓ Title: {video_spec.title}")
    print(f"  ✓ Resolution: {video_spec.width}x{video_spec.height}")
    print(f"  ✓ FPS: {video_spec.fps}")
    print(f"  ✓ Duration: {video_spec.get_total_duration()}s")


def show_summary():
    """Show demonstration summary."""
    print("\n🎉 Track-based architecture demonstration complete!")
    print("\nKey Features Demonstrated:")
    print("  ✅ Dual-mode timing (sequential + explicit)")
    print("  ✅ Auto-detection of track types")
    print("  ✅ Overlapping clips within tracks")
    print("  ✅ Global transitions")
    print("  ✅ Fluent API with method chaining")
    print("  ✅ Professional video editing workflow")


def main():
    """Demonstrate track-based TimelineBuilder functionality."""
    print("🎬 Project Vine - Track-Based TimelineBuilder Example")
    print("=" * 60)

    # Initialize TimelineBuilder
    builder = TimelineBuilder(width=1920, height=1080, fps=30)

    # Demonstrate different modes and features
    demonstrate_sequential_mode(builder)
    demonstrate_explicit_mode(builder)
    demonstrate_transitions(builder)
    show_timeline_statistics(builder)
    show_track_details(builder)
    show_transitions(builder)
    build_video_spec(builder)
    show_summary()


if __name__ == "__main__":
    main()
