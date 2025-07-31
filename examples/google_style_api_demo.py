"""Google-Style API Behavior Demo for Project Vine.

This example demonstrates the Google-style API behavior where:
- Sequential methods (add_image, add_text, etc.) UPDATE current times
- Explicit methods (add_image_at, add_text_at, etc.) do NOT update current times
"""

from vine.builder import TimelineBuilder


def demonstrate_google_style_behavior():
    """Demonstrate Google-style API behavior for timing modes."""
    print("=== Google-Style API Behavior Demo ===")
    print("Rule: Sequential methods update current times, explicit methods do not")
    print()

    # Create a fresh builder
    builder = TimelineBuilder(width=1920, height=1080, fps=30)

    print("1. Starting with sequential mode (updates current times):")
    print(f"   Initial voice current time: {builder._voice_current_time}")

    builder.add_voice("intro.mp3", duration=3.0)
    print(f"   After add_voice(): voice_current_time = {builder._voice_current_time}")

    builder.add_voice("content.mp3", duration=5.0)
    print(f"   After add_voice(): voice_current_time = {builder._voice_current_time}")

    builder.add_voice("outro.mp3", duration=2.0)
    print(f"   After add_voice(): voice_current_time = {builder._voice_current_time}")
    print()

    # Create a new builder for explicit mode demo
    builder2 = TimelineBuilder(width=1920, height=1080, fps=30)

    print("2. Using explicit mode (does NOT update current times):")
    print(f"   Initial voice current time: {builder2._voice_current_time}")

    builder2.add_voice_at("intro.mp3", start_time=0.0, duration=3.0)
    print(
        f"   After add_voice_at(): voice_current_time = {builder2._voice_current_time}"
    )

    builder2.add_voice_at("content.mp3", start_time=5.0, duration=5.0)
    print(
        f"   After add_voice_at(): voice_current_time = {builder2._voice_current_time}"
    )

    builder2.add_voice_at("outro.mp3", start_time=12.0, duration=2.0)
    print(
        f"   After add_voice_at(): voice_current_time = {builder2._voice_current_time}"
    )
    print()

    # Create a new builder for mixed mode demo
    builder3 = TimelineBuilder(width=1920, height=1080, fps=30)

    print("3. Mixed mode (best of both worlds):")
    print(f"   Initial voice current time: {builder3._voice_current_time}")

    # Start with sequential for basic structure
    builder3.add_voice("intro.mp3", duration=3.0)
    print(
        f"   After sequential add_voice(): voice_current_time = {builder3._voice_current_time}"
    )

    # Add precise overlays with explicit timing
    builder3.add_voice_at("overlay.mp3", start_time=1.5, duration=1.0)
    print(
        f"   After explicit add_voice_at(): voice_current_time = {builder3._voice_current_time}"
    )

    # Continue with sequential
    builder3.add_voice("content.mp3", duration=5.0)
    print(
        f"   After sequential add_voice(): voice_current_time = {builder3._voice_current_time}"
    )

    # Add another precise overlay
    builder3.add_voice_at("emphasis.mp3", start_time=6.0, duration=0.5)
    print(
        f"   After explicit add_voice_at(): voice_current_time = {builder3._voice_current_time}"
    )

    # Finish with sequential
    builder3.add_voice("outro.mp3", duration=2.0)
    print(
        f"   After sequential add_voice(): voice_current_time = {builder3._voice_current_time}"
    )
    print()


def demonstrate_why_this_matters():
    """Demonstrate why the Google-style behavior is important."""
    print("=== Why This Behavior Matters ===")

    # Scenario 1: Pure sequential workflow
    print("Scenario 1: Pure sequential workflow")
    builder = TimelineBuilder()

    # Each call builds on the previous one
    builder.add_image("slide1.jpg", duration=3.0)
    builder.add_text("Welcome", duration=3.0)
    builder.add_voice("narration1.mp3", duration=3.0)

    # Current times reflect the end of each track
    print(f"   Video current time: {builder._video_current_time}")
    print(f"   Text current time: {builder._text_current_time}")
    print(f"   Voice current time: {builder._voice_current_time}")
    print()

    # Scenario 2: Pure explicit workflow
    print("Scenario 2: Pure explicit workflow")
    builder2 = TimelineBuilder()

    # Each call places content at exact times
    builder2.add_image_at("background.jpg", 0.0, duration=10.0)
    builder2.add_text_at("Title", 2.0, duration=6.0)
    builder2.add_voice_at("narration.mp3", 1.0, duration=8.0)

    # Current times remain at 0 (not updated)
    print(f"   Video current time: {builder2._video_current_time}")
    print(f"   Text current time: {builder2._text_current_time}")
    print(f"   Voice current time: {builder2._voice_current_time}")
    print()

    # Scenario 3: Mixed workflow (most powerful)
    print("Scenario 3: Mixed workflow (most powerful)")
    builder3 = TimelineBuilder()

    # Start with sequential for basic structure
    builder3.add_image("intro.jpg", duration=3.0)
    builder3.add_voice("intro_narration.mp3", duration=3.0)

    # Add precise overlays without affecting sequential flow
    builder3.add_text_at("Overlay text", 1.5, duration=1.0)
    builder3.add_sfx_at("pop.wav", 2.0, duration=0.5)

    # Continue with sequential
    builder3.add_image("content.jpg", duration=5.0)
    builder3.add_voice("content_narration.mp3", duration=5.0)

    print(f"   Video current time: {builder3._video_current_time}")
    print(f"   Voice current time: {builder3._voice_current_time}")
    print("   Note: Text and SFX current times remain at 0 (explicit mode)")
    print()


def demonstrate_api_consistency():
    """Demonstrate API consistency across all track types."""
    print("=== API Consistency Across Track Types ===")

    print("Sequential methods (all update current times):")
    print("   add_image()     → updates _video_current_time")
    print("   add_text()      → updates _text_current_time")
    print("   add_voice()     → updates _voice_current_time")
    print("   add_music()     → updates _music_current_time")
    print("   add_sfx()       → updates _sfx_current_time")
    print()

    print("Explicit methods (none update current times):")
    print("   add_image_at()  → does NOT update _video_current_time")
    print("   add_text_at()   → does NOT update _text_current_time")
    print("   add_voice_at()  → does NOT update _voice_current_time")
    print("   add_music_at()  → does NOT update _music_current_time")
    print("   add_sfx_at()    → does NOT update _sfx_current_time")
    print()

    print("This consistency makes the API predictable and intuitive!")


def main():
    """Run all demonstrations."""
    demonstrate_google_style_behavior()
    demonstrate_why_this_matters()
    demonstrate_api_consistency()

    print("=== Summary ===")
    print("✅ Sequential methods: Self-documenting, update current times")
    print("✅ Explicit methods: Self-documenting, do NOT update current times")
    print("✅ Mixed mode: Best of both worlds for complex workflows")
    print("✅ Consistent behavior: All track types follow the same pattern")
    print("✅ Google-style: Follows established API design patterns")


if __name__ == "__main__":
    main()
