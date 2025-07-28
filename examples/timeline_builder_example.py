"""TimelineBuilder examples for Project Vine."""

from vine.builder import TimelineBuilder


def demonstrate_basic_usage():
    """Demonstrate basic TimelineBuilder usage."""
    print("=== Basic Usage ===")

    builder = TimelineBuilder(width=1920, height=1080, fps=30)

    # Add elements with explicit timing
    builder.add_image_at("image1.jpg", start_time=0.0, duration=5.0)
    builder.add_text_at("Hello World", start_time=0.0, duration=3.0)
    builder.add_voice_at("voice1.mp3", start_time=0.0, duration=5.0)

    print(f"Video tracks: {len(builder.video_tracks)}")
    print(f"Text tracks: {len(builder.text_tracks)}")
    print(f"Music tracks: {len(builder.music_tracks)}")
    print(f"Voice tracks: {len(builder.voice_tracks)}")
    print(f"SFX tracks: {len(builder.sfx_tracks)}")
    print(f"Total duration: {builder.get_duration()}")
    print()


def demonstrate_sequential_mode():
    """Demonstrate sequential mode (auto-appending)."""
    print("=== Sequential Mode ===")

    builder = TimelineBuilder()

    # Elements are automatically appended to the end
    builder.add_image("image1.jpg", duration=3.0)
    builder.add_text("First scene", duration=3.0)
    builder.add_voice("voice1.mp3", duration=3.0)

    # Add more elements
    builder.add_image("image2.jpg", duration=2.0)
    builder.add_text("Second scene", duration=2.0)

    print(f"Video clips: {len(builder.video_tracks[0].clips)}")
    print(f"Text clips: {len(builder.text_tracks[0].clips)}")
    print(f"Voice clips: {len(builder.voice_tracks[0].clips)}")
    print(f"Total duration: {builder.get_duration()}")
    print()


def demonstrate_set_duration_batch():
    """Demonstrate set_duration for batch operations."""
    print("=== Set Duration Batch Example ===")

    builder = TimelineBuilder()

    # Set a default duration for a batch of elements
    builder.set_duration(3.0)

    # Add multiple elements without specifying duration each time
    builder.add_image("image1.jpg")
    builder.add_text("First scene")
    builder.add_voice("voice1.mp3")

    # All elements use the 3.0 second duration
    print(f"Video clips: {len(builder.video_tracks[0].clips)}")
    print(f"Text clips: {len(builder.text_tracks[0].clips)}")
    print(f"Voice clips: {len(builder.voice_tracks[0].clips)}")

    # Check that all clips have the set duration
    for clip in builder.video_tracks[0].clips:
        print(f"Video clip duration: {clip.duration}")
    for clip in builder.text_tracks[0].clips:
        print(f"Text clip duration: {clip.duration}")
    for clip in builder.voice_tracks[0].clips:
        print(f"Voice clip duration: {clip.duration}")

    # Clear the duration and add elements without duration
    builder.clear_duration()
    builder.add_image("image2.jpg")
    builder.add_text("No duration set")

    # These clips should have no duration
    print(
        f"After clear - Video clip duration: {builder.video_tracks[0].clips[1].duration}"
    )
    print(
        f"After clear - Text clip duration: {builder.text_tracks[0].clips[1].duration}"
    )
    print()


def demonstrate_transitions():
    """Demonstrate transition usage."""
    print("=== Transitions ===")

    builder = TimelineBuilder()

    # Add some content
    builder.add_image_at("image1.jpg", start_time=0.0, duration=5.0)
    builder.add_image_at("image2.jpg", start_time=5.0, duration=5.0)

    # Add transitions
    builder.add_transition_at("fade", start_time=4.5, duration=1.0)
    builder.add_transition_at("slide", start_time=9.5, duration=1.0)

    print(f"Transitions: {len(builder.transitions)}")
    for transition in builder.transitions:
        print(
            f"  {transition.transition_type}: {transition.start_time}s - {transition.get_end_time()}s"
        )
    print()


def demonstrate_track_auto_detection():
    """Demonstrate automatic track creation."""
    print("=== Track Auto-Detection ===")

    builder = TimelineBuilder()

    # Add overlapping clips - should create new tracks
    builder.add_image_at("image1.jpg", start_time=0.0, duration=5.0)
    builder.add_image_at("image2.jpg", start_time=2.0, duration=5.0)  # Overlaps

    builder.add_voice_at("voice1.mp3", start_time=0.0, duration=3.0)
    builder.add_voice_at("voice2.mp3", start_time=1.0, duration=3.0)  # Overlaps

    print(f"Video tracks: {len(builder.video_tracks)}")
    print(f"Voice tracks: {len(builder.voice_tracks)}")

    for i, track in enumerate(builder.video_tracks):
        print(f"  Video track {i}: {len(track.clips)} clips")

    for i, track in enumerate(builder.voice_tracks):
        print(f"  Voice track {i}: {len(track.clips)} clips")
    print()


def demonstrate_method_chaining():
    """Demonstrate method chaining."""
    print("=== Method Chaining ===")

    builder = (
        TimelineBuilder()
        .set_duration(2.0)
        .add_image("image1.jpg")
        .add_text("Chained text")
        .add_voice("voice1.mp3")
        .set_fps(60)
        .clear_duration()
        .add_image("image2.jpg")
    )

    print(f"FPS: {builder.fps}")
    print(f"Video clips: {len(builder.video_tracks[0].clips)}")
    print(f"Text clips: {len(builder.text_tracks[0].clips)}")
    print(f"Voice clips: {len(builder.voice_tracks[0].clips)}")
    print()


if __name__ == "__main__":
    print("🎬 TimelineBuilder Examples")
    print("=" * 50)

    demonstrate_basic_usage()
    demonstrate_sequential_mode()
    demonstrate_set_duration_batch()
    demonstrate_transitions()
    demonstrate_track_auto_detection()
    demonstrate_method_chaining()

    print("=" * 50)
    print("✅ All examples completed successfully!")
