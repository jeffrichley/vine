#!/usr/bin/env python3
"""Basic example demonstrating Project Vine Pydantic models."""

from vine.models import (
    AnimationConfig,
    AudioClip,
    AudioTrack,
    ImageClip,
    KenBurnsConfig,
    MusicConfig,
    TextClip,
    TextTrack,
    Transition,
    VideoClip,
    VideoSpec,
    VideoTrack,
    VoiceConfig,
)


def main():
    """Demonstrate basic model usage."""
    print("🎬 Project Vine - Pydantic Models Example")
    print("=" * 50)

    # Create a Ken Burns effect
    ken_burns = KenBurnsConfig(zoom_factor=1.3, pan_x=0.1, pan_y=-0.05)

    # Create an animation with the Ken Burns effect
    animation = AnimationConfig(
        effect=ken_burns, start_time=0.0, duration=5.0, easing="ease_in_out"
    )

    # Create video clips
    video_clip = VideoClip(
        path="/path/to/intro.mp4",
        start_time=0.0,
        duration=5.0,
        width=1920,
        height=1080,
        opacity=1.0,
        animations=[animation],
    )

    image_clip = ImageClip(
        path="/path/to/slide.jpg",
        start_time=5.0,
        duration=3.0,
        width=1920,
        height=1080,
    )

    # Create text clip
    text_clip = TextClip(
        content="Welcome to Project Vine!",
        start_time=2.0,
        duration=2.0,
        font_size=48,
        font_color="#FFFFFF",
        x_position=960,
        y_position=540,
    )

    # Create audio clip
    audio_clip = AudioClip(
        path="/path/to/narration.mp3",
        start_time=0.0,
        duration=8.0,
        volume=0.9,
        fade_in=0.5,
    )

    # Create tracks and add clips
    video_track = VideoTrack(name="main_video", z_order=0)
    video_track.add_clip(video_clip)
    video_track.add_clip(image_clip)

    text_track = TextTrack(name="main_text", z_order=1)
    text_track.add_clip(text_clip)

    voice_track = AudioTrack(name="main_voice")
    voice_track.add_clip(audio_clip)

    # Create a fade transition
    transition = Transition(
        transition_type="fade",
        start_time=4.5,
        duration=1.0,
        direction="in",
        easing="ease_in_out",
    )

    # Create voice configuration
    voice = VoiceConfig(volume=0.9, speed=1.0, pitch=1.0, fade_in=0.5)

    # Create music configuration
    music = MusicConfig(volume=0.3, loop=True, duck_voice=True, duck_level=0.4)

    # Create the complete video specification
    video_spec = VideoSpec(
        title="Demo Video",
        description="A demonstration of Project Vine models",
        author="Project Vine Team",
        width=1920,
        height=1080,
        fps=30.0,
        output_format="mp4",
        quality="high",
        background_color="#000000",
        voice_config=voice,
        music_config=music,
    )

    # Add tracks and transitions
    video_spec.add_video_track(video_track)
    video_spec.add_text_track(text_track)
    video_spec.add_voice_track(voice_track)
    video_spec.add_transition(transition)

    # Display the specification
    print(f"📹 Video Title: {video_spec.title}")
    print(f"📝 Description: {video_spec.description}")
    print(f"👤 Author: {video_spec.author}")
    print(f"📐 Resolution: {video_spec.width}x{video_spec.height}")
    print(f"🎬 FPS: {video_spec.fps}")
    print(f"⏱️  Duration: {video_spec.get_total_duration():.1f} seconds")
    print(f"📹 Video Tracks: {len(video_spec.video_tracks)}")
    print(f"🎵 Voice Tracks: {len(video_spec.voice_tracks)}")
    print(f"📝 Text Tracks: {len(video_spec.text_tracks)}")
    print(f"🔄 Transitions: {len(video_spec.transitions)}")

    print("\n📋 Timeline Clips:")
    for i, track in enumerate(video_spec.video_tracks):
        print(f"  📹 Video Track {i} ({track.name}):")
        for j, clip in enumerate(track.clips):
            print(
                f"    - Clip {j}: {clip.path} ({clip.start_time}s - {clip.get_end_time()}s)"
            )

    for i, track in enumerate(video_spec.text_tracks):
        print(f"  📝 Text Track {i} ({track.name}):")
        for j, clip in enumerate(track.clips):
            print(
                f"    - Clip {j}: '{clip.content}' ({clip.start_time}s - {clip.get_end_time()}s)"
            )

    for i, track in enumerate(video_spec.voice_tracks):
        print(f"  🎵 Voice Track {i} ({track.name}):")
        for j, clip in enumerate(track.clips):
            print(
                f"    - Clip {j}: {clip.path} ({clip.start_time}s - {clip.get_end_time()}s)"
            )

    print("\n🔄 Transitions:")
    for i, trans in enumerate(video_spec.transitions):
        print(f"  {i+1}. {trans.transition_type} transition")
        print(f"     Start: {trans.start_time}s, Duration: {trans.duration}s")

    # Convert to JSON
    json_data = video_spec.model_dump_json()
    print(f"\n📄 JSON Size: {len(json_data)} characters")

    # Validate the specification
    print("\n✅ Validation: All models are valid!")

    return video_spec


if __name__ == "__main__":
    main()
