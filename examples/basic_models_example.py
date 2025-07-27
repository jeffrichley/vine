#!/usr/bin/env python3
"""Basic example demonstrating Project Vine Pydantic models."""

from vine.models import (
    AnimationConfig,
    FadeConfig,
    KenBurnsConfig,
    MusicConfig,
    TimelineBlock,
    TransitionConfig,
    VideoSpec,
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

    # Create a video block
    video_block = TimelineBlock(
        block_type="video",
        video_path="/path/to/intro.mp4",
        start_time=0.0,
        duration=5.0,
        width=1920,
        height=1080,
        opacity=1.0,
    )
    video_block.add_animation(animation)

    # Create an image block
    image_block = TimelineBlock(
        block_type="image",
        image_path="/path/to/slide.jpg",
        start_time=5.0,
        duration=3.0,
        width=1920,
        height=1080,
    )

    # Create a fade transition
    fade = FadeConfig(duration=1.0, fade_type="cross")

    transition = TransitionConfig(
        transition=fade,
        start_time=4.5,
        from_block_id=video_block.id,
        to_block_id=image_block.id,
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

    # Add blocks and transitions
    video_spec.add_block(video_block)
    video_spec.add_block(image_block)
    video_spec.add_transition(transition)

    # Display the specification
    print(f"📹 Video Title: {video_spec.title}")
    print(f"📝 Description: {video_spec.description}")
    print(f"👤 Author: {video_spec.author}")
    print(f"📐 Resolution: {video_spec.width}x{video_spec.height}")
    print(f"🎬 FPS: {video_spec.fps}")
    print(f"⏱️  Duration: {video_spec.get_total_duration():.1f} seconds")
    print(f"🎞️  Blocks: {len(video_spec.blocks)}")
    print(f"🔄 Transitions: {len(video_spec.transitions)}")

    print("\n📋 Timeline Blocks:")
    for i, block in enumerate(video_spec.blocks):
        print(f"  {i+1}. {block.block_type} block (ID: {block.id[:8]}...)")
        print(f"     Start: {block.start_time}s, Duration: {block.duration}s")
        if block.animations:
            print(f"     Animations: {len(block.animations)}")

    print("\n🔄 Transitions:")
    for i, trans in enumerate(video_spec.transitions):
        print(f"  {i+1}. {trans.transition.type} transition")
        print(
            f"     Start: {trans.start_time}s, Duration: {trans.transition.duration}s"
        )

    # Convert to JSON
    json_data = video_spec.model_dump_json()
    print(f"\n📄 JSON Size: {len(json_data)} characters")

    # Validate the specification
    print("\n✅ Validation: All models are valid!")

    return video_spec


if __name__ == "__main__":
    main()
