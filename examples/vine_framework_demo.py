#!/usr/bin/env python3
"""
Vine Framework Demo: Comprehensive Video Creation Examples

This demo showcases the various capabilities of the Vine framework using the
generated assets from the tmp directory.
"""

import json
import os
from typing import Any, Dict

from vine.builder.timeline_builder import TimelineBuilder
from vine.models.effects import KenBurnsConfig, SlideConfig, StaticConfig


def load_test_output() -> Dict[str, Any]:
    """Load the test output JSON file."""
    with open("tmp/test_output.json", "r") as f:
        return json.load(f)


def demo_sequential_mode():
    """Demonstrate sequential mode (auto-appending elements)."""
    print("=" * 60)
    print("DEMO 1: Sequential Mode")
    print("=" * 60)

    data = load_test_output()
    voice_clips = data.get("voice_wavs_json", [])
    image_renders = data.get("image_renders", [])

    # Create builder
    builder = TimelineBuilder(width=1080, height=1920, fps=30)

    # Set a default duration for all elements
    builder.set_duration(4.0)

    # Add elements sequentially
    for i, (voice_clip, image_render) in enumerate(
        zip(voice_clips[:3], image_renders[:3], strict=False)
    ):
        voice_path = voice_clip["path"]
        image_path = image_render["image_path"]

        if os.path.exists(voice_path) and os.path.exists(image_path):
            # Add voice and image - they'll be auto-appended
            builder.add_voice(voice_path, volume=1.0)
            builder.add_image(image_path)

            print(f"Added segment {i+1}: {voice_path.split('/')[-1]}")

    # Clear the duration setting
    builder.clear_duration()

    # Add a transition
    builder.add_transition("fade", duration=1.0)

    print(f"Sequential video duration: {builder.get_duration():.2f}s")
    print(f"Track counts: {builder.get_track_count()}")
    print(f"Clip counts: {builder.get_clip_count()}")

    # Save specification
    spec = builder.build()
    with open("output/sequential_demo_spec.json", "w") as f:
        f.write(spec.model_dump_json(indent=2))

    print("✓ Sequential demo specification saved")
    print()


def demo_explicit_timing():
    """Demonstrate explicit timing mode."""
    print("=" * 60)
    print("DEMO 2: Explicit Timing Mode")
    print("=" * 60)

    data = load_test_output()
    voice_clips = data.get("voice_wavs_json", [])
    image_renders = data.get("image_renders", [])

    # Create builder
    builder = TimelineBuilder(width=1080, height=1920, fps=30)

    # Add background music
    music_path = "tmp/music/music_1df9fa775fbb48709efea267d9bf7956.wav"
    if os.path.exists(music_path):
        builder.add_voice_at(music_path, start_time=0.0, volume=0.2)
        print("✓ Background music added")

    # Add elements with explicit timing
    current_time = 0.0
    for i, (voice_clip, image_render) in enumerate(
        zip(voice_clips, image_renders, strict=False)
    ):
        voice_path = voice_clip["path"]
        image_path = image_render["image_path"]
        duration = voice_clip["duration"]

        if os.path.exists(voice_path) and os.path.exists(image_path):
            # Add with explicit timing
            builder.add_voice_at(
                voice_path, start_time=current_time, duration=duration, volume=1.0
            )
            builder.add_image_at(image_path, start_time=current_time, duration=duration)

            print(
                f"✓ Segment {i+1}: {current_time:.2f}s - {current_time + duration:.2f}s"
            )
            current_time += duration

    # Add transitions at specific times
    builder.add_transition_at("fade", start_time=0.0, duration=1.0)
    builder.add_transition_at(
        "fade", start_time=builder.get_duration() - 1.0, duration=1.0
    )

    print(f"Explicit timing video duration: {builder.get_duration():.2f}s")
    print(f"Track counts: {builder.get_track_count()}")
    print(f"Clip counts: {builder.get_clip_count()}")

    # Save specification
    spec = builder.build()
    with open("output/explicit_timing_spec.json", "w") as f:
        f.write(spec.model_dump_json(indent=2))

    print("✓ Explicit timing demo specification saved")
    print()


def demo_effects():
    """Demonstrate different video effects."""
    print("=" * 60)
    print("DEMO 3: Video Effects")
    print("=" * 60)

    data = load_test_output()
    image_renders = data.get("image_renders", [])

    # Create builder
    builder = TimelineBuilder(width=1080, height=1920, fps=30)

    # Add images with different effects
    effects = [
        ("Ken Burns", KenBurnsConfig(zoom_factor=1.2, pan_x=0.1, pan_y=0.1)),
        ("Slide Left", SlideConfig(direction="left", distance=200)),
        ("Static", StaticConfig()),
        ("Ken Burns Reverse", KenBurnsConfig(zoom_factor=1.1, pan_x=-0.1, pan_y=-0.1)),
        ("Slide Right", SlideConfig(direction="right", distance=200)),
    ]

    current_time = 0.0
    for i, (image_render, (effect_name, effect_config)) in enumerate(
        zip(image_renders, effects, strict=False)
    ):
        image_path = image_render["image_path"]
        duration = 4.0

        if os.path.exists(image_path):
            from vine.models.animation_config import AnimationConfig

            animation = AnimationConfig(
                effect=effect_config,
                start_time=0.0,
                duration=duration,
                easing="ease_in_out",
            )

            builder.add_image_at(
                image_path,
                start_time=current_time,
                duration=duration,
                animations=[animation],
            )

            print(
                f"✓ Image {i+1} with {effect_name} effect: {current_time:.2f}s - {current_time + duration:.2f}s"
            )
            current_time += duration

    print(f"Effects demo duration: {builder.get_duration():.2f}s")
    print(f"Track counts: {builder.get_track_count()}")
    print(f"Clip counts: {builder.get_clip_count()}")

    # Save specification
    spec = builder.build()
    with open("output/effects_demo_spec.json", "w") as f:
        f.write(spec.model_dump_json(indent=2))

    print("✓ Effects demo specification saved")
    print()


def demo_audio_mixing():
    """Demonstrate audio mixing with multiple tracks."""
    print("=" * 60)
    print("DEMO 4: Audio Mixing")
    print("=" * 60)

    data = load_test_output()
    voice_clips = data.get("voice_wavs_json", [])
    sfx_results = data.get("sfx_results", [])

    # Create builder
    builder = TimelineBuilder(width=1080, height=1920, fps=30)

    # Add background music
    music_path = "tmp/music/music_1df9fa775fbb48709efea267d9bf7956.wav"
    if os.path.exists(music_path):
        builder.add_voice_at(music_path, start_time=0.0, volume=0.3)
        print("✓ Background music (volume: 0.3)")

    # Add voice clips
    current_time = 0.0
    for i, voice_clip in enumerate(voice_clips):
        voice_path = voice_clip["path"]
        duration = voice_clip["duration"]

        if os.path.exists(voice_path):
            builder.add_voice_at(
                voice_path, start_time=current_time, duration=duration, volume=1.0
            )
            print(
                f"✓ Voice {i+1} (volume: 1.0): {current_time:.2f}s - {current_time + duration:.2f}s"
            )
            current_time += duration

    # Add sound effects
    for sfx in sfx_results:
        sfx_path = sfx["file_path"]
        if os.path.exists(sfx_path):
            builder.add_voice_at(
                sfx_path,
                start_time=sfx.get("start", 0.0),
                duration=sfx.get("duration", 1.0),
                volume=0.5,
            )
            print(f"✓ SFX: {sfx_path.split('/')[-1]} (volume: 0.5)")

    print(f"Audio mixing demo duration: {builder.get_duration():.2f}s")
    print(f"Track counts: {builder.get_track_count()}")
    print(f"Clip counts: {builder.get_clip_count()}")

    # Save specification
    spec = builder.build()
    with open("output/audio_mixing_spec.json", "w") as f:
        f.write(spec.model_dump_json(indent=2))

    print("✓ Audio mixing demo specification saved")
    print()


def main():
    """Run all demos."""
    print("VINE FRAMEWORK COMPREHENSIVE DEMO")
    print("Using assets from tmp/test_output.json")
    print()

    # Create output directory
    os.makedirs("output", exist_ok=True)

    # Run all demos
    demo_sequential_mode()
    demo_explicit_timing()
    demo_effects()
    demo_audio_mixing()

    print("=" * 60)
    print("ALL DEMOS COMPLETED")
    print("=" * 60)
    print("Generated specifications:")
    print("  - output/sequential_demo_spec.json")
    print("  - output/explicit_timing_spec.json")
    print("  - output/effects_demo_spec.json")
    print("  - output/audio_mixing_spec.json")
    print()
    print("To render videos, implement the rendering pipeline or use MoviePy directly.")
    print("The specifications contain all the information needed to create the videos.")


if __name__ == "__main__":
    main()
