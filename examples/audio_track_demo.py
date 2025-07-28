#!/usr/bin/env python3
"""
Audio Track Demo - Demonstrates the new audio track refactor functionality.

This example shows how to use the new separate audio tracks for music, voice, and SFX
with professional controls like fade-in, fade-out, and volume management.
"""

from vine.builder.timeline_builder import TimelineBuilder


def _print_timeline_config(builder):
    """Print timeline configuration information."""
    print("\n📋 Timeline Configuration:")
    print(f"• Video dimensions: {builder.width}x{builder.height}")
    print(f"• Frame rate: {builder.fps} fps")
    print(f"• Music tracks: {len(builder.music_tracks)}")
    print(f"• Voice tracks: {len(builder.voice_tracks)}")
    print(f"• SFX tracks: {len(builder.sfx_tracks)}")

    print("\n🎚️ Default Audio Volumes:")
    print(f"• Music: {builder.defaults.get_music_volume()} (subtle background)")
    print(f"• Voice: {builder.defaults.get_voice_volume()} (prominent narration)")
    print(f"• SFX: {builder.defaults.get_sfx_volume()} (noticeable effects)")


def _add_visual_content(builder):
    """Add visual content to the timeline."""
    print("\n🎬 Adding Visual Content...")
    builder.add_image("examples/assets/image1.jpg", duration=3.0)
    builder.add_image("examples/assets/image2.jpg", duration=3.0)
    builder.add_image("examples/assets/background.jpg", duration=4.0)

    print("📝 Adding Text Overlays...")
    builder.add_text("Welcome to Audio Track Demo", duration=2.0)
    builder.add_text("Professional Audio Mixing", duration=2.0)
    builder.add_text("Music + Voice + SFX", duration=2.0)


def _add_sequential_audio(builder):
    """Add sequential audio content."""
    print("\n🎵 Sequential Audio Methods:")

    print("• Adding background music...")
    try:
        builder.add_music("examples/assets/music/background.mp3", duration=10.0)
        print("  ✓ Background music added")
    except Exception as e:
        print(f"  ⚠️ Music file not found: {e}")

    print("• Adding voice narration...")
    try:
        builder.add_voice("examples/assets/voice/narration.mp3", duration=8.0)
        print("  ✓ Voice narration added")
    except Exception as e:
        print(f"  ⚠️ Voice file not found: {e}")

    print("• Adding sound effects...")
    try:
        builder.add_sfx("examples/assets/sfx/transition.wav", duration=1.0)
        print("  ✓ Sound effects added")
    except Exception as e:
        print(f"  ⚠️ SFX file not found: {e}")


def _add_explicit_timing_audio(builder):
    """Add audio with explicit timing and professional controls."""
    print("\n⏰ Explicit Timing with Professional Controls:")

    print("• Adding music with fade-in...")
    try:
        builder.add_music_at(
            "examples/assets/music/intro.mp3",
            start_time=0.0,
            duration=5.0,
            volume=0.4,  # Slightly louder than default
            fade_in=1.0,  # 1-second fade-in
            fade_out=0.5,  # 0.5-second fade-out
        )
        print("  ✓ Music with fade-in added")
    except Exception as e:
        print(f"  ⚠️ Music file not found: {e}")

    print("• Adding voice with crossfade...")
    try:
        builder.add_voice_at(
            "examples/assets/voice/intro.mp3",
            start_time=1.0,
            duration=4.0,
            volume=0.9,  # Louder than default
            fade_in=0.5,
            fade_out=0.5,
            crossfade_duration=0.3,
        )
        print("  ✓ Voice with crossfade added")
    except Exception as e:
        print(f"  ⚠️ Voice file not found: {e}")


def _add_sfx_with_timing(builder):
    """Add SFX with precise timing."""
    print("• Adding SFX with precise timing...")
    try:
        builder.add_sfx_at(
            "examples/assets/sfx/impact.wav",
            start_time=2.5,
            duration=0.5,
            volume=0.6,  # Louder than default
            fade_in=0.1,
            fade_out=0.2,
        )
        print("  ✓ SFX with precise timing added")
    except Exception as e:
        print(f"  ⚠️ SFX file not found: {e}")


def _show_track_information(builder):
    """Show track and clip information."""
    print("\n📊 Track Information:")
    track_counts = builder.get_track_count()
    print(f"• Track counts: {track_counts}")

    clip_counts = builder.get_clip_count()
    print(f"• Clip counts: {clip_counts}")

    duration = builder.get_duration()
    print(f"• Timeline duration: {duration:.2f} seconds")


def _add_overlapping_audio(builder):
    """Add overlapping audio clips to demonstrate mixing."""
    print("\n🔄 Adobe-Style Overlap Behavior:")
    print("• Music tracks: Allow overlaps, MoviePy mixes automatically")
    print("• Voice tracks: Allow overlaps, MoviePy mixes automatically")
    print("• SFX tracks: Allow overlaps, MoviePy mixes automatically")
    print("• Cross-track: All audio types mix in final output via MoviePy")

    print("\n🎛️ Adding Overlapping Audio Clips...")
    try:
        # Add overlapping music clips
        builder.add_music_at("examples/assets/music/loop1.mp3", 5.0, duration=3.0)
        builder.add_music_at("examples/assets/music/loop2.mp3", 6.0, duration=3.0)
        print("  ✓ Overlapping music clips added (will mix)")

        # Add overlapping voice clips
        builder.add_voice_at("examples/assets/voice/part1.mp3", 7.0, duration=2.0)
        builder.add_voice_at("examples/assets/voice/part2.mp3", 8.0, duration=2.0)
        print("  ✓ Overlapping voice clips added (will mix)")

        # Add overlapping SFX clips
        builder.add_sfx_at("examples/assets/sfx/effect1.wav", 9.0, duration=0.5)
        builder.add_sfx_at("examples/assets/sfx/effect2.wav", 9.2, duration=0.5)
        print("  ✓ Overlapping SFX clips added (will mix)")

    except Exception as e:
        print(f"  ⚠️ Some audio files not found: {e}")


def _build_and_show_video_spec(builder):
    """Build video spec and show information."""
    print("\n🔨 Building Video Specification...")
    try:
        video_spec = builder.build()
        print("✓ VideoSpec created successfully")
        print(f"• Music tracks in spec: {len(video_spec.music_tracks)}")
        print(f"• Voice tracks in spec: {len(video_spec.voice_tracks)}")
        print(f"• SFX tracks in spec: {len(video_spec.sfx_tracks)}")

        # Show active clips at different times
        print("\n🎬 Active Clips at Different Times:")
        for time in [0.0, 2.0, 5.0, 8.0]:
            active_clips = video_spec.get_active_clips_at_time(time)
            print(f"• At {time}s:")
            for track_type, clips in active_clips.items():
                if clips:
                    print(f"  - {track_type}: {len(clips)} clips")

    except Exception as e:
        print(f"✗ Error building VideoSpec: {e}")


def _test_clear_functionality(builder):
    """Test the clear functionality."""
    print("\n🧹 Testing Clear Functionality...")
    builder.clear()
    print(f"• After clear - Music tracks: {len(builder.music_tracks)}")
    print(f"• After clear - Voice tracks: {len(builder.voice_tracks)}")
    print(f"• After clear - SFX tracks: {len(builder.sfx_tracks)}")


def create_audio_track_demo():
    """Create a demo video showcasing the new audio track functionality."""
    print("🎵 Audio Track Refactor Demo")
    print("=" * 50)

    # Initialize the timeline builder
    builder = TimelineBuilder(width=1920, height=1080, fps=30)

    _print_timeline_config(builder)
    _add_visual_content(builder)
    _add_sequential_audio(builder)
    _add_explicit_timing_audio(builder)
    _add_sfx_with_timing(builder)
    _show_track_information(builder)
    _add_overlapping_audio(builder)
    _build_and_show_video_spec(builder)
    _test_clear_functionality(builder)

    print("\n" + "=" * 50)
    print("🎉 Audio Track Refactor Demo Complete!")
    print("\nKey Features Demonstrated:")
    print("✅ Separate music, voice, and SFX tracks")
    print("✅ Professional audio controls (fade-in, fade-out, volume)")
    print("✅ Adobe-style overlap behavior")
    print("✅ MoviePy automatic audio mixing")
    print("✅ Default volume settings per track type")
    print("✅ File validation and error handling")
    print("✅ Sequential and explicit timing methods")
    print("✅ Track management and information methods")


if __name__ == "__main__":
    create_audio_track_demo()
