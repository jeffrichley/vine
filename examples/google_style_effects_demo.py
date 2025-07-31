"""Demo of the new Google-style effect system."""

from vine import KenBurnsEffect, SlideEffect, TimelineBuilder


def demo_direct_effects():
    """Demo using effects directly."""
    print("=== Direct Effect Usage ===")

    # Create effects directly
    ken_burns = KenBurnsEffect(zoom_factor=1.5, pan_x=0.2, duration=3.0)
    slide = SlideEffect(direction="left", distance=200, duration=2.0)

    print(
        f"Ken Burns effect: {ken_burns.get_type()}, duration: {ken_burns.get_duration()}"
    )
    print(f"Slide effect: {slide.get_type()}, direction: {slide.direction}")

    # Use with TimelineBuilder - now using context methods
    builder = TimelineBuilder()
    builder.add_image("examples/assets/image1.jpg").with_effect(ken_burns)
    builder.add_image("examples/assets/image2.jpg").with_effect(slide)

    print("✓ Direct effect usage works!")


def demo_type_safety():
    """Demo type safety of the effect system."""
    print("\n=== Type Safety Demo ===")

    # This should work - KenBurnsEffect implements the Effect protocol
    ken_burns: KenBurnsEffect = KenBurnsEffect(zoom_factor=1.2)
    print(f"Type-safe effect: {ken_burns.get_type()}")

    # The protocol ensures all effects have the required methods
    print(f"Duration: {ken_burns.get_duration()}")
    print(f"Start time: {ken_burns.get_start_time()}")

    print("✓ Type safety works!")


if __name__ == "__main__":
    demo_direct_effects()
    demo_type_safety()
    print("\n🎉 Google-style effect system is working!")
