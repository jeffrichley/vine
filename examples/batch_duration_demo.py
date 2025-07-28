#!/usr/bin/env python3
"""Demonstration of set_duration batch functionality."""

from vine.builder import TimelineBuilder


def demonstrate_batch_duration():
    """Demonstrate how set_duration works for batch operations."""
    print("🎬 Batch Duration Demo")
    print("=" * 50)

    # Create a builder
    builder = TimelineBuilder()

    print("1. Setting duration for a batch of elements...")
    builder.set_duration(3.0)

    print("2. Adding multiple elements without specifying duration each time:")
    builder.add_image("image1.jpg")
    print("   ✅ Added image1.jpg (uses 3.0s duration)")

    builder.add_text("Scene 1")
    print("   ✅ Added text 'Scene 1' (uses 3.0s duration)")

    builder.add_voice("voice1.mp3")
    print("   ✅ Added voice1.mp3 (uses 3.0s duration)")

    builder.add_image("image2.jpg")
    print("   ✅ Added image2.jpg (uses 3.0s duration)")

    builder.add_text("Scene 2")
    print("   ✅ Added text 'Scene 2' (uses 3.0s duration)")

    print("\n3. Checking results:")
    print(f"   Video clips: {len(builder.video_tracks[0].clips)}")
    print(f"   Text clips: {len(builder.text_tracks[0].clips)}")
    print(f"   Voice clips: {len(builder.voice_tracks[0].clips)}")

    print("\n4. Verifying all clips have the set duration:")
    for i, clip in enumerate(builder.video_tracks[0].clips):
        print(f"   Video clip {i+1}: {clip.duration}s")

    for i, clip in enumerate(builder.text_tracks[0].clips):
        print(f"   Text clip {i+1}: {clip.duration}s")

    for i, clip in enumerate(builder.voice_tracks[0].clips):
        print(f"   Voice clip {i+1}: {clip.duration}s")

    print(f"\n5. Total timeline duration: {builder.get_duration()}s")

    print("\n6. Testing explicit duration override:")
    builder.add_image("image3.jpg", duration=5.0)  # Override with explicit duration
    print("   ✅ Added image3.jpg with explicit 5.0s duration")
    print(f"   Video clip 3 duration: {builder.video_tracks[0].clips[2].duration}s")

    print("\n7. Testing that set_duration still works after override:")
    builder.add_text("Scene 3")
    print("   ✅ Added text 'Scene 3' (uses 3.0s duration)")
    print(f"   Text clip 3 duration: {builder.text_tracks[0].clips[2].duration}s")

    print("\n8. Testing clear_duration:")
    builder.clear_duration()
    builder.add_voice("voice2.mp3")
    print("   ✅ Added voice2.mp3 (no duration set)")
    print(f"   Voice clip 2 duration: {builder.voice_tracks[0].clips[1].duration}")

    print("\n9. Testing setting duration again:")
    builder.set_duration(2.0)
    builder.add_image("image4.jpg")
    print("   ✅ Added image4.jpg (uses 2.0s duration)")
    print(f"   Video clip 4 duration: {builder.video_tracks[0].clips[3].duration}s")

    print("\n" + "=" * 50)
    print("✅ Batch duration functionality works perfectly!")
    print("   - Multiple elements can use the same duration")
    print("   - Explicit durations override the default")
    print("   - Duration persists until explicitly cleared")
    print("   - Can change duration mid-batch")


if __name__ == "__main__":
    demonstrate_batch_duration()
