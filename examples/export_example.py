"""Example demonstrating the MoviePy export functionality."""

from pathlib import Path

from vine.builder.timeline_builder import TimelineBuilder


def create_simple_video():
    """Create a simple video with images and text."""
    builder = TimelineBuilder(width=1280, height=720, fps=30)

    # Add content in sequential mode
    builder.set_duration(3.0)  # Set default duration for subsequent elements

    builder.add_image("examples/assets/image1.jpg", duration=3.0)
    builder.add_text("Welcome to Project Vine!", duration=3.0)
    builder.add_voice("examples/assets/audio1_long.mp3", duration=3.0)

    return builder


def create_complex_video():
    """Create a more complex video with explicit timing."""
    builder = TimelineBuilder(width=1920, height=1080, fps=30)

    # Add content with explicit timing
    builder.add_image_at("examples/assets/image1.jpg", start_time=0.0, duration=5.0)
    builder.add_text_at("Hello World!", start_time=1.0, duration=3.0)
    builder.add_voice_at(
        "examples/assets/audio1_long.mp3", start_time=0.0, duration=5.0
    )

    # Add more content
    builder.add_image_at("examples/assets/image2.jpg", start_time=5.0, duration=5.0)
    builder.add_text_at("Goodbye World!", start_time=6.0, duration=3.0)
    builder.add_voice_at(
        "examples/assets/audio2_long.mp3", start_time=5.0, duration=5.0
    )

    return builder


def create_track_based_video():
    """Create a video using track-based approach."""
    builder = TimelineBuilder(width=1280, height=720, fps=30)

    # Add content to different tracks
    builder.add_image_at(
        "examples/assets/background.jpg", start_time=0.0, duration=10.0
    )
    builder.add_text_at(
        "Title",
        start_time=1.0,
        duration=8.0,
        font_size=72,
        x_position=640,
        y_position=100,
    )
    builder.add_text_at(
        "Subtitle",
        start_time=2.0,
        duration=7.0,
        font_size=48,
        x_position=640,
        y_position=200,
    )
    builder.add_voice_at(
        "examples/assets/narration_long.mp3", start_time=0.0, duration=10.0
    )

    return builder


def main():
    """Main function demonstrating the export functionality."""
    print("Creating simple video...")
    simple_builder = create_simple_video()

    # Render to MoviePy clip
    video_clip = simple_builder.render()
    print(f"Video clip duration: {video_clip.duration} seconds")
    print(f"Video clip size: {video_clip.size}")

    # Export to file
    print("Exporting simple video...")
    simple_builder.export("output/simple_video.mp4", codec="libx264", audio_codec="aac")

    print("\nCreating complex video...")
    complex_builder = create_complex_video()

    # Export complex video
    print("Exporting complex video...")
    complex_builder.export(
        "output/complex_video.mp4", codec="libx264", audio_codec="aac"
    )

    print("\nCreating track-based video...")
    track_builder = create_track_based_video()

    # Export track-based video
    print("Exporting track-based video...")
    track_builder.export("output/track_video.mp4", codec="libx264", audio_codec="aac")

    print("\nAll videos exported successfully!")
    print("Check the 'output' directory for the generated video files.")


if __name__ == "__main__":
    # Create output directory
    Path("output").mkdir(exist_ok=True)

    # Create assets directory for examples
    assets_dir = Path("examples/assets")
    assets_dir.mkdir(parents=True, exist_ok=True)

    # Create placeholder files for testing
    placeholder_files = [
        "examples/assets/image1.jpg",
        "examples/assets/image2.jpg",
        "examples/assets/background.jpg",
        "examples/assets/audio1_long.mp3",
        "examples/assets/audio2_long.mp3",
        "examples/assets/narration_long.mp3",
    ]

    for file_path in placeholder_files:
        Path(file_path).touch()

    main()
