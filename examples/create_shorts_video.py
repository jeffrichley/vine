#!/usr/bin/env python3
"""
Example: Create a Shorts Video from Generated Assets

This example demonstrates how to use the Vine framework to create a shorts video
from AI-generated assets including voice clips, images, music, and sound effects.
"""

import json
import os
from typing import Any, Dict

from vine.builder.timeline_builder import TimelineBuilder
from vine.models.animation_config import AnimationConfig
from vine.models.effects import KenBurnsConfig


def load_test_output() -> Dict[str, Any]:
    """Load the test output JSON file."""
    with open("tmp/test_output.json", "r") as f:
        return json.load(f)


def create_shorts_video():
    """Create a shorts video from the generated assets."""

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

        # Add voice track
        if os.path.exists(voice_path):
            builder.add_voice_at(
                voice_path=voice_path,
                start_time=current_time,
                duration=duration,
                volume=1.0,
            )

        # Add video track with image
        if os.path.exists(image_path):
            # Add Ken Burns effect for visual interest
            ken_burns_effect = KenBurnsConfig(
                zoom_factor=1.1,
                pan_x=0.0,
                pan_y=0.0,
                duration=duration,
                easing="ease_in_out",
            )

            animation = AnimationConfig(
                effect=ken_burns_effect,
                start_time=0.0,
                duration=duration,
                easing="ease_in_out",
            )

            builder.add_image_at(
                image_path=image_path,
                start_time=current_time,
                duration=duration,
                animations=[animation],
            )

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

        current_time += duration

    # Add fade in/out transitions
    builder.add_transition_at(transition_type="fade", start_time=0.0, duration=1.0)

    builder.add_transition_at(
        transition_type="fade", start_time=builder.get_duration() - 1.0, duration=1.0
    )

    # Build the video specification
    final_spec = builder.build()

    # Export the video
    output_path = "output/inspirational_shorts.mp4"
    os.makedirs("output", exist_ok=True)

    print(f"Creating shorts video: {output_path}")
    print(f"Duration: {builder.get_duration():.2f} seconds")
    print(f"Resolution: {builder.width}x{builder.height}")
    print(f"FPS: {builder.fps}")
    print(f"Track counts: {builder.get_track_count()}")
    print(f"Clip counts: {builder.get_clip_count()}")

    # Save the specification for inspection
    with open("output/video_spec.json", "w") as f:
        f.write(final_spec.model_dump_json(indent=2))

    print("Video specification saved to output/video_spec.json")

    # Try to render the video if MoviePy is available
    try:
        print("Attempting to render video...")
        builder.export(output_path, codec="libx264", audio_codec="aac")
        print(f"Video successfully rendered to: {output_path}")
    except Exception as e:
        print(f"Rendering failed: {e}")
        print("The video specification has been saved and can be rendered later")


if __name__ == "__main__":
    create_shorts_video()
