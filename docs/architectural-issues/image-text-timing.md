# Image-Text Timing Architectural Issue

## Overview

This document details a critical architectural challenge in the TimelineBuilder API: how to handle scenarios where visual elements (images, text, audio, music, etc) need to overlap in time while maintaining clean, extensible API design.

## The Core Problem

### User Scenario
```python
# User wants to create:
# - Image: 0s - 10s (full duration)
# - Text: 0s - 6s (disappears at 6s, but image continues)
```

### Current Limitation
The VideoSpec model prevents overlapping visual blocks:
```python
@model_validator(mode="after")
def validate_video_configuration(self) -> "VideoSpec":
    # Check for overlapping blocks
    for i, block1 in enumerate(blocks):
        for j, block2 in enumerate(blocks[i + 1 :], i + 1):
            if block1.overlaps_with(block2):
                raise ValueError(f"Blocks {i} and {j} overlap in time")
```

This validation prevents the user scenario from working:
```python
# This FAILS with current validation:
builder.add_image_at("background.jpg", start_time=0.0, duration=10.0)
builder.add_text_at("Hello World", start_time=0.0, duration=6.0)  # ❌ Overlap error!
```

## Current Implemented Solutions

### 1. Enhanced Composite Blocks (Current Implementation)

**Approach:**
```python
builder.add_image_with_text(
    image_path="assets/background.jpg",
    text="Hello World",
    start_time=0.0,
    duration=10.0,      # Image shows for 10 seconds
    text_duration=6.0,  # Text shows for 6 seconds
    text_position="center",
    text_font_size=72,
    text_color="#FFFFFF"
)
```

**Implementation Details:**
- Stores text timing in block metadata
- Single block avoids overlap validation
- Text timing controlled via `text_duration` parameter

**Pros:**
- ✅ Works with current validation
- ✅ Single block approach
- ✅ Clean semantic structure

**Cons:**
- ❌ **Method explosion problem** (see below)
- ❌ Limited to image + text combinations
- ❌ Not extensible to other element types

### 2. Multiple Composite Blocks

**Approach:**
```python
# Split into two blocks
builder.add_image_with_text(
    image_path="assets/background.jpg",
    text="Hello World",
    start_time=0.0,
    duration=6.0  # Image + text for first 6 seconds
)
builder.add_image_at(
    "assets/background.jpg",
    start_time=6.0,
    duration=4.0  # Image only for remaining 4 seconds
)
```

**Pros:**
- ✅ Works with current validation
- ✅ No metadata complexity

**Cons:**
- ❌ Duplicates image reference
- ❌ Less efficient rendering
- ❌ Still limited to image + text

## The Method Explosion Problem

The composite block approach becomes unwieldy when considering more complex scenarios:

### Simple Case (Current)
```python
builder.add_image_with_text(
    image_path="background.jpg",
    text="Hello World",
    start_time=0.0,
    duration=10.0,
    text_duration=6.0
)
```

### Complex Case (Problematic)
```python
# This would require a massive method signature:
builder.add_image_with_text_and_voice_and_3_sound_effects(
    image_path="background.jpg",
    text="Hello World",
    voice_path="narration.mp3",
    sound_effects=["effect1.mp3", "effect2.mp3", "effect3.mp3"],
    start_time=0.0,
    duration=10.0,
    text_duration=6.0,
    voice_duration=8.0,
    effect1_duration=2.0,
    effect1_start_time=2.0,
    effect2_duration=1.5,
    effect2_start_time=4.0,
    effect3_duration=3.0,
    effect3_start_time=7.0,
    text_position="center",
    text_font_size=72,
    text_color="#FFFFFF",
    voice_volume=1.0,
    effect1_volume=0.5,
    effect2_volume=0.3,
    effect3_volume=0.7,
    # ... potentially 50+ parameters
)
```

### Combinatorial Explosion
For N element types, we'd need:
- 1 method for each element type
- 1 method for each 2-element combination
- 1 method for each 3-element combination
- ... up to 2^N - 1 total methods

This is clearly unsustainable.

## Proposed Alternative Solutions

### Option 1: Layer-Based System
```python
# Define layers and add elements to them
builder.add_to_layer("background", "image.jpg", start_time=0.0, duration=10.0)
builder.add_to_layer("text", "Hello World", start_time=0.0, duration=6.0)
builder.add_to_layer("voice", "narration.mp3", start_time=0.0)
builder.add_to_layer("effects", "effect1.mp3", start_time=2.0, duration=1.0)
```

**Pros:**
- ✅ Clean separation
- ✅ No method explosion
- ✅ Extensible to any element type

**Cons:**
- ❌ Less semantic grouping
- ❌ Harder to manage relationships
- ❌ More complex rendering logic

### Option 2: Scene/Composition Objects
```python
# Create composition objects that can contain multiple elements
scene = builder.create_scene(start_time=0.0, duration=10.0)
scene.add_image("background.jpg")
scene.add_text("Hello World", duration=6.0)
scene.add_voice("narration.mp3")
scene.add_sound_effect("effect1.mp3", start_time=2.0, duration=1.0)

# Or more fluent:
scene = (builder.create_scene(0.0, 10.0)
    .add_image("background.jpg")
    .add_text("Hello World", duration=6.0)
    .add_voice("narration.mp3")
    .add_sound_effect("effect1.mp3", 2.0, 1.0)
)
```

**Pros:**
- ✅ Natural grouping
- ✅ Fluent API
- ✅ Extensible
- ✅ Type safe

**Cons:**
- ❌ Adds complexity
- ❌ Might be overkill for simple cases

### Option 3: Timeline Segments with Overlap
```python
# Allow overlapping elements within segments
segment = builder.create_segment(start_time=0.0, duration=10.0)
segment.add_image("background.jpg")  # Full duration
segment.add_text("Hello World", start_time=0.0, duration=6.0)  # Overlaps
segment.add_voice("narration.mp3", start_time=0.0)  # Auto-duration
segment.add_sound_effect("effect1.mp3", start_time=2.0, duration=1.0)  # Overlaps
```

**Pros:**
- ✅ Natural overlap
- ✅ Semantic grouping
- ✅ Extensible

**Cons:**
- ❌ Still has overlap validation issues
- ❌ Requires VideoSpec changes

### Option 4: Configuration-Driven Approach
```python
# Pass configuration objects instead of parameters
composition = {
    "background": {"type": "image", "path": "background.jpg", "duration": 10.0},
    "text": {"type": "text", "content": "Hello World", "duration": 6.0},
    "voice": {"type": "voice", "path": "narration.mp3"},
    "effects": [
        {"type": "sound", "path": "effect1.mp3", "start_time": 2.0, "duration": 1.0},
        {"type": "sound", "path": "effect2.mp3", "start_time": 4.0, "duration": 0.5}
    ]
}

builder.add_composition(composition, start_time=0.0)
```

**Pros:**
- ✅ Very flexible
- ✅ JSON/YAML friendly
- ✅ No method explosion
- ✅ AI generation friendly

**Cons:**
- ❌ Less type safety
- ❌ Harder to validate
- ❌ Runtime errors instead of compile-time

### Option 5: Event-Driven Timeline
```python
# Add events at specific times
builder.add_event(0.0, "show_image", {"path": "background.jpg"})
builder.add_event(0.0, "show_text", {"content": "Hello World"})
builder.add_event(0.0, "play_voice", {"path": "narration.mp3"})
builder.add_event(2.0, "play_sound", {"path": "effect1.mp3"})
builder.add_event(6.0, "hide_text", {})
builder.add_event(10.0, "hide_image", {})
```

**Pros:**
- ✅ Very flexible
- ✅ Precise control
- ✅ Event-driven architecture

**Cons:**
- ❌ More complex
- ❌ Harder to reason about
- ❌ Potential for conflicting events

### Option 6: Declarative Timeline DSL
```python
# Define timeline in a more declarative way
timeline = """
0s-10s: image(background.jpg)
0s-6s:  text("Hello World")
0s-*:   voice(narration.mp3)
2s-3s:  sound(effect1.mp3)
4s-4.5s: sound(effect2.mp3)
"""

builder.parse_timeline(timeline)
```

**Pros:**
- ✅ Very readable
- ✅ Compact
- ✅ Flexible
- ✅ Human-friendly

**Cons:**
- ❌ Custom DSL
- ❌ Parsing complexity
- ❌ Less type safety

### Option 7: Builder Pattern with Fluent Composition
```python
# Use fluent composition with explicit timing
(builder
    .at_time(0.0)
    .add_image("background.jpg").for_duration(10.0)
    .add_text("Hello World").for_duration(6.0)
    .add_voice("narration.mp3")
    .at_time(2.0)
    .add_sound_effect("effect1.mp3").for_duration(1.0)
    .at_time(4.0)
    .add_sound_effect("effect2.mp3").for_duration(0.5)
)
```

**Pros:**
- ✅ Very readable
- ✅ Fluent
- ✅ Explicit timing
- ✅ Extensible

**Cons:**
- ❌ More complex builder implementation
- ❌ State management complexity

### Option 8: Override VideoSpec Validation (Simplest)
```python
# Just allow overlapping visual elements
builder = TimelineBuilder(allow_visual_overlap=True)
builder.add_image_at("background.jpg", start_time=0.0, duration=10.0)
builder.add_text_at("Hello World", start_time=0.0, duration=6.0)  # ✅ Works!
builder.add_voice_at("narration.mp3", start_time=0.0)
```

**Pros:**
- ✅ Simplest solution
- ✅ Uses existing API
- ✅ Minimal changes required

**Cons:**
- ❌ Might cause rendering issues
- ❌ Less semantic
- ❌ Could lead to visual conflicts

## Technical Considerations

### Rendering Pipeline Impact
Different approaches have varying impacts on the rendering pipeline:

1. **Composite blocks**: Single render call per block
2. **Separate blocks**: Multiple render calls, potential conflicts
3. **Layer-based**: Z-order management required
4. **Event-driven**: Complex state management

### Performance Implications
- **Memory usage**: How many objects are created
- **Rendering efficiency**: Number of draw calls
- **Validation overhead**: Runtime checks vs compile-time

### AI Generation Compatibility
- **JSON/YAML input**: Which approaches work well with AI
- **Error handling**: How to handle invalid configurations
- **Validation**: Type safety vs flexibility

## Recommendation

Based on the analysis, I recommend **Option 2: Scene/Composition Objects** or **Option 7: Fluent Composition** because they:

1. **Avoid method explosion** - no combinatorial API
2. **Maintain semantic grouping** - related elements stay together
3. **Are extensible** - easy to add new element types
4. **Keep type safety** - still use Pydantic models
5. **Support the user scenario** - natural overlap handling
6. **Are AI-friendly** - can be serialized to JSON/YAML

## Next Steps

1. **Prototype the recommended approach**
2. **Evaluate performance impact**
3. **Test with AI generation scenarios**
4. **Consider backward compatibility**
5. **Update VideoSpec validation if needed**

## Test Scenarios for Overlapping Elements

The following scenarios represent real-world use cases with various temporal overlaps. Any solution should handle these naturally:

### Scenario 1: Simple Image + Text Overlap
```
Timeline: 0s - 10s
- Background image: 0s - 10s (full duration)
- Title text: 0s - 6s (disappears early)
- Subtitle text: 2s - 8s (starts late, ends early)
```

### Scenario 2: Multi-Layer Text Animation
```
Timeline: 0s - 15s
- Background image: 0s - 15s (full duration)
- Main title: 0s - 5s (fades out)
- Subtitle: 3s - 8s (overlaps with main title)
- Call-to-action: 7s - 12s (overlaps with subtitle)
- Footer text: 10s - 15s (overlaps with CTA)
```

### Scenario 3: Audio-Visual Synchronization
```
Timeline: 0s - 20s
- Background image: 0s - 20s (full duration)
- Background music: 0s - 20s (full duration)
- Voice narration: 2s - 18s (starts late, ends early)
- Text captions: 3s - 17s (syncs with voice)
- Sound effect 1: 5s - 6s (punch effect)
- Sound effect 2: 12s - 13s (transition effect)
```

### Scenario 4: Complex Multi-Media Scene
```
Timeline: 0s - 30s
- Background image: 0s - 30s (full duration)
- Background music: 0s - 30s (full duration)
- Voice intro: 0s - 8s
- Text intro: 1s - 7s (syncs with voice)
- Sound effect 1: 3s - 4s (emphasis)
- Voice main: 10s - 25s
- Text main: 11s - 24s (syncs with voice)
- Sound effect 2: 15s - 16s (punch)
- Sound effect 3: 20s - 21s (emphasis)
- Voice outro: 26s - 29s
- Text outro: 27s - 28s (syncs with voice)
```

### Scenario 5: Staggered Text Reveal
```
Timeline: 0s - 12s
- Background image: 0s - 12s (full duration)
- Line 1: 0s - 4s
- Line 2: 2s - 6s (overlaps with line 1)
- Line 3: 4s - 8s (overlaps with line 2)
- Line 4: 6s - 10s (overlaps with line 3)
- Line 5: 8s - 12s (overlaps with line 4)
```

### Scenario 6: Audio-Driven Visual Effects
```
Timeline: 0s - 25s
- Background image: 0s - 25s (full duration)
- Background music: 0s - 25s (full duration)
- Beat-sync effect 1: 2s - 3s (on beat)
- Beat-sync effect 2: 4s - 5s (on beat)
- Beat-sync effect 3: 6s - 7s (on beat)
- Voice narration: 8s - 20s
- Text captions: 9s - 19s (syncs with voice)
- Beat-sync effect 4: 10s - 11s (during voice)
- Beat-sync effect 5: 12s - 13s (during voice)
- Beat-sync effect 6: 14s - 15s (during voice)
```

### Scenario 7: Multi-Camera Style
```
Timeline: 0s - 18s
- Background image: 0s - 18s (full duration)
- Background music: 0s - 18s (full duration)
- Voice narration: 0s - 18s (full duration)
- Main text: 0s - 6s
- Side text 1: 4s - 10s (overlaps with main)
- Side text 2: 8s - 14s (overlaps with side 1)
- Side text 3: 12s - 18s (overlaps with side 2)
```

### Scenario 8: Interactive-Style Timing
```
Timeline: 0s - 20s
- Background image: 0s - 20s (full duration)
- Background music: 0s - 20s (full duration)
- Question text: 0s - 5s
- Answer text: 5s - 10s
- Question text 2: 10s - 15s
- Answer text 2: 15s - 20s
- Transition effect 1: 4s - 6s (between Q&A)
- Transition effect 2: 14s - 16s (between Q&A)
```

### Scenario 9: Complex Audio Layering
```
Timeline: 0s - 40s
- Background image: 0s - 40s (full duration)
- Background music: 0s - 40s (full duration)
- Voice main: 5s - 35s
- Voice echo: 6s - 36s (slight delay)
- Ambient sound: 0s - 40s (full duration)
- Sound effect 1: 10s - 11s
- Sound effect 2: 20s - 21s
- Sound effect 3: 30s - 31s
- Text captions: 6s - 34s (syncs with voice)
```

### Scenario 10: Rapid-Fire Effects
```
Timeline: 0s - 10s
- Background image: 0s - 10s (full duration)
- Background music: 0s - 10s (full duration)
- Effect 1: 1s - 2s
- Effect 2: 2s - 3s
- Effect 3: 3s - 4s
- Effect 4: 4s - 5s
- Effect 5: 5s - 6s
- Effect 6: 6s - 7s
- Effect 7: 7s - 8s
- Effect 8: 8s - 9s
- Voice narration: 0s - 10s (full duration)
- Text captions: 0s - 10s (full duration)
```

### Scenario 11: Long-Form Content
```
Timeline: 0s - 120s (2 minutes)
- Background image: 0s - 120s (full duration)
- Background music: 0s - 120s (full duration)
- Chapter 1 voice: 0s - 30s
- Chapter 1 text: 5s - 25s
- Chapter 2 voice: 35s - 65s
- Chapter 2 text: 40s - 60s
- Chapter 3 voice: 70s - 100s
- Chapter 3 text: 75s - 95s
- Chapter 4 voice: 105s - 120s
- Chapter 4 text: 110s - 118s
- Transition effects: 28s - 32s, 63s - 67s, 98s - 102s
```

### Scenario 12: Micro-Content (TikTok Style)
```
Timeline: 0s - 15s
- Background image: 0s - 15s (full duration)
- Background music: 0s - 15s (full duration)
- Hook text: 0s - 3s
- Main point 1: 3s - 6s
- Main point 2: 6s - 9s
- Main point 3: 9s - 12s
- Call to action: 12s - 15s
- Sound effect: 2s - 3s, 5s - 6s, 8s - 9s, 11s - 12s
```

### Scenario 13: Educational Content
```
Timeline: 0s - 45s
- Background image: 0s - 45s (full duration)
- Background music: 0s - 45s (full duration)
- Instructor voice: 0s - 45s (full duration)
- Slide 1 text: 0s - 15s
- Slide 1 diagram: 5s - 12s
- Slide 2 text: 15s - 30s
- Slide 2 diagram: 20s - 27s
- Slide 3 text: 30s - 45s
- Slide 3 diagram: 35s - 42s
- Transition effects: 13s - 17s, 28s - 32s
```

### Scenario 14: Music Video Style
```
Timeline: 0s - 60s
- Background image: 0s - 60s (full duration)
- Background music: 0s - 60s (full duration)
- Lyrics line 1: 0s - 4s
- Lyrics line 2: 4s - 8s
- Lyrics line 3: 8s - 12s
- Lyrics line 4: 12s - 16s
- Lyrics line 5: 16s - 20s
- Lyrics line 6: 20s - 24s
- Lyrics line 7: 24s - 28s
- Lyrics line 8: 28s - 32s
- Visual effect 1: 2s - 6s
- Visual effect 2: 10s - 14s
- Visual effect 3: 18s - 22s
- Visual effect 4: 26s - 30s
```

### Scenario 15: Complex Narrative
```
Timeline: 0s - 90s
- Background image: 0s - 90s (full duration)
- Background music: 0s - 90s (full duration)
- Narrator voice: 0s - 90s (full duration)
- Character 1 voice: 10s - 25s
- Character 1 text: 12s - 23s
- Character 2 voice: 30s - 45s
- Character 2 text: 32s - 43s
- Character 3 voice: 50s - 65s
- Character 3 text: 52s - 63s
- Character 4 voice: 70s - 85s
- Character 4 text: 72s - 83s
- Sound effects: 8s - 9s, 28s - 29s, 48s - 49s, 68s - 69s
- Transition effects: 24s - 26s, 44s - 46s, 64s - 66s, 84s - 86s
```

## Evaluation Criteria

When evaluating architectural solutions against these scenarios, consider:

1. **API Clarity**: How intuitive is the syntax for each scenario?
2. **Type Safety**: Does the solution maintain compile-time validation?
3. **Extensibility**: Can new element types be added easily?
4. **Performance**: How does the solution scale with complex scenarios?
5. **AI Generation**: How well does it work with JSON/YAML input?
6. **Error Handling**: How gracefully does it handle invalid configurations?
7. **Rendering Complexity**: What impact does it have on the rendering pipeline?

## Recommended Solutions: Detailed Analysis

After analyzing all scenarios and architectural options, two primary solutions emerge as the most viable:

### Option 1: Scene-Based Composition with Fluent API

**Core Concept:**
Create composition objects that group related elements together, allowing natural temporal overlaps within a scene.

**API Design:**
```python
# Basic scene creation
scene = builder.create_scene(start_time=0.0, duration=10.0)

# Fluent composition within scene
scene = (builder.create_scene(0.0, 10.0)
    .add_image("background.jpg")
    .add_text("Hello World", duration=6.0)
    .add_voice("narration.mp3")
    .add_sound_effect("effect1.mp3", start_time=2.0, duration=1.0)
)

# Multiple scenes
builder.create_scene(0.0, 10.0).add_image("bg1.jpg").add_text("Scene 1")
builder.create_scene(10.0, 20.0).add_image("bg2.jpg").add_text("Scene 2")
```

**Implementation Details:**

1. **Scene Class Structure:**
```python
class Scene:
    def __init__(self, start_time: float, duration: float):
        self.start_time = start_time
        self.duration = duration
        self.elements = []

    def add_image(self, path: str, **kwargs) -> "Scene":
        # Add image element with timing relative to scene
        return self

    def add_text(self, content: str, duration: Optional[float] = None, **kwargs) -> "Scene":
        # Add text element, auto-duration if not specified
        return self

    def add_voice(self, path: str, **kwargs) -> "Scene":
        # Add voice element
        return self

    def add_sound_effect(self, path: str, start_time: float = 0.0, duration: Optional[float] = None, **kwargs) -> "Scene":
        # Add sound effect with relative timing
        return self
```

2. **TimelineBuilder Integration:**
```python
class TimelineBuilder:
    def create_scene(self, start_time: float, duration: float) -> Scene:
        scene = Scene(start_time, duration)
        self.scenes.append(scene)
        return scene

    def build(self) -> VideoSpec:
        # Convert scenes to VideoSpec blocks
        blocks = []
        for scene in self.scenes:
            for element in scene.elements:
                # Convert scene-relative timing to absolute timing
                block = element.to_timeline_block(scene.start_time)
                blocks.append(block)
        return VideoSpec(blocks=blocks)
```

**Pros:**
- ✅ Natural semantic grouping
- ✅ Fluent, readable API
- ✅ Handles all 15 scenarios elegantly
- ✅ Extensible to new element types
- ✅ Type-safe with Pydantic models
- ✅ AI generation friendly (can serialize scenes to JSON)
- ✅ No method explosion
- ✅ Clear separation of concerns

**Cons:**
- ❌ Adds complexity to the codebase
- ❌ Requires new Scene/Composition classes
- ❌ Might be overkill for very simple cases
- ❌ State management complexity in Scene objects

**Handles Scenarios:**
- **Scenario 1**: `scene.add_image("bg.jpg").add_text("Title", duration=6.0).add_text("Subtitle", start_time=2.0, duration=6.0)`
- **Scenario 4**: Complex multi-media handled naturally with multiple `.add_*()` calls
- **Scenario 10**: Rapid-fire effects with multiple `.add_sound_effect()` calls
- **Scenario 15**: Complex narrative with multiple scenes

### Option 2: Timeline-Based Fluent Composition

**Core Concept:**
Use a timeline-based approach where elements are added at specific times with explicit duration control, maintaining a fluent API throughout.

**API Design:**
```python
# Timeline-based composition
(builder
    .at_time(0.0)
    .add_image("background.jpg").for_duration(10.0)
    .add_text("Hello World").for_duration(6.0)
    .add_voice("narration.mp3")
    .at_time(2.0)
    .add_sound_effect("effect1.mp3").for_duration(1.0)
    .at_time(4.0)
    .add_sound_effect("effect2.mp3").for_duration(0.5)
)

# Alternative syntax with explicit timing
builder.at_time(0.0).add_image("bg.jpg", duration=10.0)
builder.at_time(0.0).add_text("Hello", duration=6.0)
builder.at_time(2.0).add_sound_effect("effect.mp3", duration=1.0)
```

**Implementation Details:**

1. **TimelineBuilder State Management:**
```python
class TimelineBuilder:
    def __init__(self):
        self.current_time = 0.0
        self.elements = []

    def at_time(self, time: float) -> "TimelineBuilder":
        self.current_time = time
        return self

    def add_image(self, path: str, duration: Optional[float] = None) -> "TimelineBuilder":
        element = ImageElement(path, self.current_time, duration)
        self.elements.append(element)
        return self

    def add_text(self, content: str, duration: Optional[float] = None) -> "TimelineBuilder":
        element = TextElement(content, self.current_time, duration)
        self.elements.append(element)
        return self

    def for_duration(self, duration: float) -> "TimelineBuilder":
        # Set duration for the last added element
        if self.elements:
            self.elements[-1].duration = duration
        return self
```

2. **Element Classes:**
```python
class TimelineElement:
    def __init__(self, start_time: float, duration: Optional[float] = None):
        self.start_time = start_time
        self.duration = duration

    def for_duration(self, duration: float) -> "TimelineElement":
        self.duration = duration
        return self

class ImageElement(TimelineElement):
    def __init__(self, path: str, start_time: float, duration: Optional[float] = None):
        super().__init__(start_time, duration)
        self.path = path

class TextElement(TimelineElement):
    def __init__(self, content: str, start_time: float, duration: Optional[float] = None):
        super().__init__(start_time, duration)
        self.content = content
```

**Pros:**
- ✅ Very explicit timing control
- ✅ Fluent and readable
- ✅ Handles complex timing scenarios
- ✅ No semantic grouping complexity
- ✅ Extensible to new element types
- ✅ Type-safe
- ✅ AI generation friendly

**Cons:**
- ❌ More verbose for simple cases
- ❌ State management complexity (current_time tracking)
- ❌ Less semantic grouping
- ❌ Requires careful state management
- ❌ Might be harder to reason about complex scenarios

**Handles Scenarios:**
- **Scenario 1**: Explicit timing with `.at_time()` and `.for_duration()`
- **Scenario 5**: Staggered reveals with multiple `.at_time()` calls
- **Scenario 10**: Rapid-fire effects with precise timing control
- **Scenario 15**: Complex narrative with explicit timing for each element

### Comparison Summary

| Aspect | Scene-Based | Timeline-Based |
|--------|-------------|----------------|
| **API Clarity** | High (semantic grouping) | High (explicit timing) |
| **Complexity** | Medium (Scene objects) | Medium (state management) |
| **Extensibility** | High | High |
| **Type Safety** | High | High |
| **AI Generation** | Excellent | Good |
| **Simple Cases** | Good | Verbose |
| **Complex Cases** | Excellent | Good |
| **Learning Curve** | Low | Medium |

## Final Architectural Decision: Track-Based System with Dual-Mode Timing

After extensive analysis of all scenarios and architectural options, we have selected a **track-based system with dual-mode timing** as the optimal solution.

### Selected Approach: Track-Based with Auto-Detection

**Core Design:**
- **Track-based data model** for professional video editor compatibility
- **Auto-detection of track type** based on media element
- **Dual-mode timing**: Sequential append and explicit timing
- **Global transitions** that work across tracks
- **Z-order within tracks** for layering

### Implementation Strategy

#### 1. Track-Based Data Model
```python
class VideoSpec:
    video_tracks: List[VideoTrack] = Field(default_factory=lambda: [VideoTrack("video_0")])
    audio_tracks: List[AudioTrack] = Field(default_factory=lambda: [AudioTrack("audio_0")])
    text_tracks: List[TextTrack] = Field(default_factory=lambda: [TextTrack("text_0")])
    transitions: List[Transition] = Field(default_factory=list)

class VideoTrack:
    name: str
    clips: List[VideoClip] = []
    z_order: int = 0

class AudioTrack:
    name: str
    clips: List[AudioClip] = []
    volume: float = 1.0
    muted: bool = False

class TextTrack:
    name: str
    clips: List[TextClip] = []
    z_order: int = 0
```

#### 2. Auto-Detection of Track Type
```python
class TimelineBuilder:
    def add_image_at(self, path, start_time, duration=None, **kwargs):
        """Auto-add to video track"""
        track = self._get_or_create_video_track()
        clip = ImageClip(path, start_time, duration, **kwargs)
        track.add_clip(clip)
        return self

    def add_text_at(self, text, start_time, duration=None, **kwargs):
        """Auto-add to text track"""
        track = self._get_or_create_text_track()
        clip = TextClip(text, start_time, duration, **kwargs)
        track.add_clip(clip)
        return self

    def add_voice_at(self, path, start_time, duration=None, **kwargs):
        """Auto-add to audio track"""
        track = self._get_or_create_audio_track()
        clip = VoiceClip(path, start_time, duration, **kwargs)
        track.add_clip(clip)
        return self
```

#### 3. Dual-Mode Timing System

**Sequential Mode (Default):**
```python
# Elements are appended sequentially
builder.add_image("bg.jpg", duration=10.0)      # Starts at 0.0
builder.add_text("Hello", duration=6.0)         # Starts at 10.0
builder.add_voice("narration.mp3")              # Starts at 16.0
```

**Explicit Mode:**
```python
# Elements positioned at specific times (overlaps allowed)
builder.add_image_at("bg.jpg", 0.0, 10.0)
builder.add_text_at("Hello", 0.0, 6.0)         # Overlaps with image
builder.add_voice_at("narration.mp3", 0.0, 8.0) # Overlaps with both
```

**Mode Switching:**
```python
builder.set_sequential_mode(True)   # Default: sequential append
builder.set_sequential_mode(False)  # Explicit timing mode
```

#### 4. Consistent Timing Options Across All Media Types

All media types support the same timing patterns:
```python
# All support these timing options:
element_at(path, start_time, duration=value)
element_at(path, start_time, end_time=value)
element_at(path, start_time)  # Auto-duration

# Examples:
builder.add_image_at("bg.jpg", 0.0, duration=10.0)
builder.add_image_at("bg.jpg", 0.0, end_time=10.0)
builder.add_image_at("bg.jpg", 0.0)  # Auto-duration

builder.add_text_at("Hello", 0.0, duration=6.0)
builder.add_text_at("Hello", 0.0, end_time=6.0)
builder.add_text_at("Hello", 0.0)  # Auto-duration

builder.add_voice_at("narration.mp3", 0.0, duration=8.0)
builder.add_voice_at("narration.mp3", 0.0, end_time=8.0)
builder.add_voice_at("narration.mp3", 0.0)  # Auto-duration
```

#### 5. Global Transition System

Transitions work across all tracks and both timing modes:
```python
# Sequential mode transitions
builder.add_image("bg1.jpg", duration=5.0)
builder.add_transition("fade", duration=1.0)  # Auto-inserted
builder.add_image("bg2.jpg", duration=5.0)

# Explicit mode transitions
builder.add_image_at("bg1.jpg", 0.0, 5.0)
builder.add_transition_at("fade", 4.0, 1.0)  # Overlaps with bg1
builder.add_image_at("bg2.jpg", 5.0, 5.0)
```

### Why This Approach Was Selected

#### Advantages:
1. **Professional Compatibility**: Track-based model matches video editing software
2. **Dual-Mode Flexibility**: Simple sequential mode + powerful explicit mode
3. **Auto-Detection**: Clean API without track specification complexity
4. **Consistent Timing**: Same timing options across all media types
5. **Transition Support**: Global transitions work with both modes
6. **Future-Proof**: Foundation for professional format export/import
7. **User-Friendly**: Intuitive for both simple and complex workflows

#### Handles All 15 Test Scenarios:
- **Scenario 1**: `add_image_at(0, 10) + add_text_at(0, 6)` (explicit mode)
- **Scenario 4**: Complex multi-media with multiple overlapping elements
- **Scenario 10**: Rapid-fire effects with precise timing
- **Scenario 15**: Complex narrative with multiple scenes

#### Implementation Complexity:
- **Medium**: Track-based data model + dual-mode timing
- **Manageable**: Auto-detection reduces user complexity
- **Evolvable**: Can add named tracks and advanced features later

### Migration Strategy

#### Phase 1: Core Implementation
1. Implement track-based data model
2. Add auto-detection to TimelineBuilder
3. Implement dual-mode timing system
4. Add global transition support
5. Remove overlap validation from VideoSpec

#### Phase 2: Enhanced Features (Future)
1. Named tracks for advanced users
2. Track management (create, delete, reorder)
3. Professional format export/import
4. Advanced transition types

### API Examples

#### Simple Sequential Workflow:
```python
builder = TimelineBuilder()
(builder
    .add_image("background.jpg", duration=10.0)
    .add_text("Hello World", duration=6.0)
    .add_voice("narration.mp3")
    .add_transition("fade", duration=1.0)
    .add_text("Goodbye", duration=4.0)
)
```

#### Complex Explicit Workflow:
```python
builder = TimelineBuilder()
builder.set_sequential_mode(False)
(builder
    .add_image_at("background.jpg", 0.0, 20.0)
    .add_text_at("Title", 0.0, 5.0)
    .add_text_at("Subtitle", 2.0, 8.0)
    .add_voice_at("narration.mp3", 0.0, 18.0)
    .add_sound_effect_at("effect.mp3", 5.0, 1.0)
    .add_transition_at("fade", 18.0, 2.0)
)
```

This architectural decision provides the optimal balance of simplicity, power, and future extensibility while solving the core overlap problem and supporting all identified use cases.

## Related Issues

- [TimelineBuilder API Design](../timeline-builder-api.md)
- [VideoSpec Validation](../video-spec-validation.md)
- [Rendering Pipeline](../rendering-pipeline.md)
- [AI Generation Compatibility](../ai-generation.md)
