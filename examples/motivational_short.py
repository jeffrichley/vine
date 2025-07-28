#!/usr/bin/env python3
"""
Unyielding Spirit - Motivational Shorts Video 🏮
A powerful message about resilience and strength, featuring lighthouse imagery
and empowering themes of overcoming life's storms.
"""

from vine.builder.timeline_builder import TimelineBuilder


def create_unyielding_spirit_video():
    """Create the Unyielding Spirit motivational shorts video."""

    # Initialize timeline builder for 9:16 shorts
    builder = TimelineBuilder(width=1080, height=1920, fps=30)

    # Add background music for entire duration (23.92 seconds)
    builder.add_music_at(
        "tmp/music/music_1df9fa775fbb48709efea267d9bf7956.wav",
        start_time=0.0,
        duration=23.92,
        volume=0.3,  # Keep it subtle for background
    )

    # Segment 1: "In the eye of life's storms, your spirit shines brighter than ever!" (0-3.67s)
    builder.add_image_at(
        "tmp/images/fb34586ed041467fad76362573273855.png", start_time=0.0, duration=3.67
    )

    builder.add_voice_at(
        "tmp/chrona_voice/02f648b058c1485589f92177d82caf95.wav",
        start_time=0.0,
        duration=3.67,
        volume=0.8,
    )

    # Add SFX for segment 1
    builder.add_sfx_at(
        "tmp/sfx/sfx_659d621622fa413ebe2ce257d98e1d34.wav",
        start_time=0.0,
        duration=1.0,
        volume=0.5,
    )

    builder.add_sfx_at(
        "tmp/sfx/sfx_0c897f8f1c864606a0bdc5981f3229b6.wav",
        start_time=0.0,
        duration=1.5,
        volume=0.4,
    )

    builder.add_sfx_at(
        "tmp/sfx/sfx_44f8658147524dc6b47d3594497780bc.wav",
        start_time=0.0,
        duration=0.5,
        volume=0.3,
    )

    # Segment 2: "Let it be the unwavering lighthouse that guides you home, illuminating the path through darkness." (3.67-8.79s)
    builder.add_image_at(
        "tmp/images/dde12e61c6bc40eb82d3210d40635c7a.png",
        start_time=3.67,
        duration=5.12,
    )

    builder.add_voice_at(
        "tmp/chrona_voice/90ac3767c10048e6bfcc59aef38b9dc5.wav",
        start_time=3.67,
        duration=5.12,
        volume=0.8,
    )

    # Add SFX for segment 2
    builder.add_sfx_at(
        "tmp/sfx/sfx_84d31ca593c7462abfda0a4fef50c66c.wav",
        start_time=3.67,
        duration=1.5,
        volume=0.4,
    )

    builder.add_sfx_at(
        "tmp/sfx/sfx_ef7da977f2124e6c9fbc04b95adf5d80.wav",
        start_time=3.67,
        duration=1.0,
        volume=0.5,
    )

    # Segment 3: "Embrace each challenge as a powerful stepping stone, transforming adversity into an unbreakable strength." (8.79-14.14s)
    builder.add_image_at(
        "tmp/images/4c4bdd47e5484ceb9186d348fc8bc8ed.png",
        start_time=8.79,
        duration=5.35,
    )

    builder.add_voice_at(
        "tmp/chrona_voice/e3d35b1c4ba14533a5c57a5ce1c63139.wav",
        start_time=8.79,
        duration=5.35,
        volume=0.8,
    )

    # Add SFX for segment 3
    builder.add_voice_at(
        "tmp/sfx/sfx_d94e0458292d4645a0978c22d8ffdc64.wav",
        start_time=8.79,
        duration=1.0,
        volume=0.4,
    )

    builder.add_voice_at(
        "tmp/sfx/sfx_c525a92c26d0432e8105d32143fd6a27.wav",
        start_time=8.79,
        duration=1.5,
        volume=0.3,
    )

    # Segment 4: "Rise up, stand tall, and harness the resilience within you, for every setback is a setup for a comeback!" (14.14-19.78s)
    builder.add_image_at(
        "tmp/images/0edd3b03760f48868a7b517ba20095d2.png",
        start_time=14.14,
        duration=5.64,
    )

    builder.add_voice_at(
        "tmp/chrona_voice/8e72a880e6e049d7a72e73ae3e5429cc.wav",
        start_time=14.14,
        duration=5.64,
        volume=0.8,
    )

    # Add SFX for segment 4
    builder.add_voice_at(
        "tmp/sfx/sfx_1a1cf4a623654980a39b34e2175ea549.wav",
        start_time=14.14,
        duration=1.0,
        volume=0.5,
    )

    # Segment 5: "The journey ahead is yours to conquer—ignite your fire and let it lead you to greatness!" (19.78-23.92s)
    builder.add_image_at(
        "tmp/images/4571ca92d8234133a8cf64696d73a102.png",
        start_time=19.78,
        duration=4.13,
    )

    builder.add_voice_at(
        "tmp/chrona_voice/e4a0e767613f41f3a3206b0e656726f6.wav",
        start_time=19.78,
        duration=4.13,
        volume=0.8,
    )

    # Add SFX for segment 5
    builder.add_voice_at(
        "tmp/sfx/sfx_d827c1b93d764c44bd3c51598af44ee9.wav",
        start_time=19.78,
        duration=1.0,
        volume=0.4,
    )

    builder.add_voice_at(
        "tmp/sfx/sfx_94178b179f754b41a691d3f5ab34dccb.wav",
        start_time=19.78,
        duration=1.5,
        volume=0.3,
    )

    # Add fade transitions between segments ✨
    builder.add_transition_at("fade", start_time=3.47, duration=0.4)  # End of segment 1
    builder.add_transition_at("fade", start_time=8.59, duration=0.4)  # End of segment 2
    builder.add_transition_at(
        "fade", start_time=13.94, duration=0.4
    )  # End of segment 3
    builder.add_transition_at(
        "fade", start_time=19.58, duration=0.4
    )  # End of segment 4

    # Build and export 🎬
    video_spec = builder.build()

    # Export the video
    output_path = "output/unyielding_spirit_motivational.mp4"
    import os

    os.makedirs("output", exist_ok=True)

    print("=" * 60)
    print("🎬 UNYIELDING SPIRIT - MOTIVATIONAL SHORT")
    print("=" * 60)
    print(f"📱 Resolution: {builder.width}x{builder.height}")
    print(f"⏱️ Duration: {builder.get_duration():.2f} seconds")
    print(f"🎵 FPS: {builder.fps}")
    print(f"🎬 Video tracks: {builder.get_track_count()}")
    print(f"🎵 Audio clips: {builder.get_clip_count()}")
    print()

    # Save the specification for inspection
    with open("output/unyielding_spirit_spec.json", "w") as f:
        f.write(video_spec.model_dump_json(indent=2))

    print("📋 Video specification saved to output/unyielding_spirit_spec.json")

    # Try to render the video if MoviePy is available
    try:
        print("🎬 Attempting to render video...")
        builder.export(output_path, codec="libx264", audio_codec="aac")
        print(f"✅ Video successfully rendered to: {output_path}")
    except Exception as e:
        print(f"❌ Rendering failed: {e}")
        print("📋 The video specification has been saved and can be rendered later")
        print("\n🔧 To render manually:")
        print("1. Install MoviePy: pip install moviepy")
        print("2. Fix any volume issues in the rendering pipeline")
        print("3. Run the script again")

    print()
    print("🏮 Theme: Unyielding Spirit")
    print("💪 Message: Resilience and strength in life's storms")
    print("🎨 Style: Bold golds and deep blues with lighthouse imagery")
    print("✨ Effects: Radiant glow effects and empowering atmosphere")


if __name__ == "__main__":
    create_unyielding_spirit_video()
