#!/usr/bin/env python3
"""
Simple Example: Create a Shorts Video from Generated Assets

This example demonstrates the basic usage of the Vine framework to create a shorts video
from AI-generated assets without complex animations.
"""

import json
import os
from typing import Any, Dict

from vine.builder.timeline_builder import TimelineBuilder


def load_test_output() -> Dict[str, Any]:
    """Load the test output JSON file."""
    with open("tmp/test_output.json", "r") as f:
        return json.load(f)


def create_simple_shorts_video():
    """Create a simple shorts video from the generated assets."""

    # Load the test output data
    data = load_test_output()

    # Create a new timeline builder with shorts dimensions
    builder = TimelineBuilder(width=1080, height=1920, fps=30)

    # Add background music track
    music_path = "tmp/music/music_1df9fa775fbb48709efea267d9bf7956.wav"
    if os.path.exists(music_path):
        builder.add_voice_at(
            voice_path=music_path,
            start_time=0.0,
            volume=0.3,  # Lower volume for background
        )

    # Process voice clips and corresponding images
    voice_clips = data.get("voice_wavs_json", [])
    image_renders = data.get("image_renders", [])

    current_time = 0.0

    for i, (voice_clip, image_render) in enumerate(
        zip(voice_clips, image_renders, strict=False)
    ):
        voice_path = voice_clip["path"]
        image_path = image_render["image_path"]
        duration = voice_clip["duration"]

        print(f"Processing segment {i+1}:")
        print(f"  Voice: {voice_path}")
        print(f"  Image: {image_path}")
        print(f"  Duration: {duration:.2f}s")
        print(f"  Start time: {current_time:.2f}s")

        # Add voice track
        if os.path.exists(voice_path):
            builder.add_voice_at(
                voice_path=voice_path,
                start_time=current_time,
                duration=duration,
                volume=1.0,
            )
            print("  ✓ Voice added")
        else:
            print("  ✗ Voice file not found")

        # Add video track with image
        if os.path.exists(image_path):
            builder.add_image_at(
                image_path=image_path, start_time=current_time, duration=duration
            )
            print("  ✓ Image added")
        else:
            print("  ✗ Image file not found")

        # Add sound effects for this segment
        sfx_results = data.get("sfx_results", [])
        segment_sfx = [sfx for sfx in sfx_results if sfx.get("beat_number") == i + 1]

        for sfx in segment_sfx:
            sfx_path = sfx["file_path"]
            if os.path.exists(sfx_path):
                builder.add_voice_at(
                    voice_path=sfx_path,
                    start_time=current_time + sfx.get("start", 0.0),
                    duration=sfx.get("duration", 1.0),
                    volume=0.5,
                )
                print(f"  ✓ SFX added: {sfx_path.split('/')[-1]}")
            else:
                print(f"  ✗ SFX file not found: {sfx_path}")

        current_time += duration
        print()

    # Add fade in/out transitions
    builder.add_transition_at(transition_type="fade", start_time=0.0, duration=1.0)

    builder.add_transition_at(
        transition_type="fade", start_time=builder.get_duration() - 1.0, duration=1.0
    )

    # Build the video specification
    final_spec = builder.build()

    # Export the video
    output_path = "output/simple_inspirational_shorts.mp4"
    os.makedirs("output", exist_ok=True)

    print("=" * 50)
    print("VIDEO SUMMARY")
    print("=" * 50)
    print(f"Output path: {output_path}")
    print(f"Duration: {builder.get_duration():.2f} seconds")
    print(f"Resolution: {builder.width}x{builder.height}")
    print(f"FPS: {builder.fps}")
    print(f"Track counts: {builder.get_track_count()}")
    print(f"Clip counts: {builder.get_clip_count()}")
    print()

    # Save the specification for inspection
    with open("output/simple_video_spec.json", "w") as f:
        f.write(final_spec.model_dump_json(indent=2))

    print("Video specification saved to output/simple_video_spec.json")

    # Try to render the video if MoviePy is available
    try:
        print("Attempting to render video...")
        builder.export(output_path, codec="libx264", audio_codec="aac")
        print(f"✓ Video successfully rendered to: {output_path}")
    except Exception as e:
        print(f"✗ Rendering failed: {e}")
        print("The video specification has been saved and can be rendered later")
        print("\nTo render manually, you can:")
        print("1. Install MoviePy: pip install moviepy")
        print("2. Fix the volume issue in the rendering pipeline")
        print("3. Run the script again")


if __name__ == "__main__":
    create_simple_shorts_video()
