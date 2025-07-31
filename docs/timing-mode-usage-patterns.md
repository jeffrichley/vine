# Timing Mode Usage Patterns Analysis

This document analyzes different usage patterns for sequential, explicit, and mixed timing modes to determine the correct behavior for current time updates.

## Pattern Categories

### 1. Pure Sequential Mode Patterns
### 2. Pure Explicit Mode Patterns
### 3. Mixed Mode Patterns
### 4. Edge Cases and Complex Scenarios

---

## 1. Pure Sequential Mode Patterns

### Pattern 1.1: Simple Linear Presentation
**Use Case**: Basic slideshow with narration
```python
builder.add_image("slide1.jpg", duration=5.0)
builder.add_text("Welcome", duration=3.0)
builder.add_voice("intro.mp3", duration=8.0)
builder.add_image("slide2.jpg", duration=4.0)
```
**Expected Timeline**:
- Image1: 0.0-5.0
- Text1: 5.0-8.0
- Voice1: 8.0-16.0
- Image2: 16.0-20.0
**Current Times After**: video=20.0, text=8.0, voice=16.0

### Pattern 1.2: Sequential with Transitions
**Use Case**: Presentation with fade transitions
```python
builder.add_image("slide1.jpg", duration=5.0)
builder.add_transition(TransitionType.FADE, duration=1.0)
builder.add_image("slide2.jpg", duration=5.0)
builder.add_transition(TransitionType.FADE, duration=1.0)
```
**Expected Timeline**:
- Image1: 0.0-5.0
- Transition1: 4.0-5.0 (overlaps)
- Image2: 5.0-10.0
- Transition2: 9.0-10.0 (overlaps)
**Current Times After**: video=10.0

### Pattern 1.3: Sequential Audio Layering
**Use Case**: Background music with voice overlay
```python
builder.add_music("background.mp3", duration=30.0)
builder.add_voice("narration1.mp3", duration=10.0)
builder.add_voice("narration2.mp3", duration=8.0)
```
**Expected Timeline**:
- Music1: 0.0-30.0
- Voice1: 30.0-40.0
- Voice2: 40.0-48.0
**Current Times After**: music=30.0, voice=48.0

### Pattern 1.4: Sequential with Batch Duration
**Use Case**: Multiple elements with same duration
```python
builder.set_duration(3.0)
builder.add_image("slide1.jpg")
builder.add_text("Title 1")
builder.add_image("slide2.jpg")
builder.add_text("Title 2")
```
**Expected Timeline**:
- Image1: 0.0-3.0
- Text1: 3.0-6.0
- Image2: 6.0-9.0
- Text2: 9.0-12.0
**Current Times After**: video=9.0, text=12.0

---

## 2. Pure Explicit Mode Patterns

### Pattern 2.1: Precise Synchronization
**Use Case**: Video with perfectly timed overlays
```python
builder.add_image_at("background.jpg", 0.0, duration=10.0)
builder.add_text_at("Title", 2.0, duration=6.0)
builder.add_voice_at("narration.mp3", 1.0, duration=8.0)
```
**Expected Timeline**:
- Image1: 0.0-10.0
- Text1: 2.0-8.0 (overlaps)
- Voice1: 1.0-9.0 (overlaps)
**Current Times After**: video=0.0, text=0.0, voice=0.0 (no updates)

### Pattern 2.2: Complex Overlapping
**Use Case**: Multiple overlapping elements
```python
builder.add_image_at("bg.jpg", 0.0, duration=15.0)
builder.add_text_at("Intro", 0.0, duration=5.0)
builder.add_text_at("Main", 3.0, duration=8.0)
builder.add_text_at("End", 10.0, duration=5.0)
```
**Expected Timeline**:
- Image1: 0.0-15.0
- Text1: 0.0-5.0
- Text2: 3.0-11.0 (overlaps)
- Text3: 10.0-15.0 (overlaps)
**Current Times After**: video=0.0, text=0.0 (no updates)

### Pattern 2.3: Explicit with End Times
**Use Case**: Using end_time instead of duration
```python
builder.add_image_at("slide1.jpg", 0.0, end_time=5.0)
builder.add_image_at("slide2.jpg", 5.0, end_time=10.0)
builder.add_voice_at("narration.mp3", 0.0, end_time=8.0)
```
**Expected Timeline**:
- Image1: 0.0-5.0
- Image2: 5.0-10.0
- Voice1: 0.0-8.0 (overlaps)
**Current Times After**: video=0.0, voice=0.0 (no updates)

### Pattern 2.4: Professional Audio Mixing
**Use Case**: Complex audio arrangement
```python
builder.add_music_at("bg_music.mp3", 0.0, duration=20.0)
builder.add_voice_at("intro.mp3", 2.0, duration=5.0)
builder.add_sfx_at("whoosh.mp3", 1.5, duration=0.5)
builder.add_voice_at("main.mp3", 8.0, duration=10.0)
```
**Expected Timeline**:
- Music1: 0.0-20.0
- Voice1: 2.0-7.0
- SFX1: 1.5-2.0
- Voice2: 8.0-18.0
**Current Times After**: music=0.0, voice=0.0, sfx=0.0 (no updates)

---

## 3. Mixed Mode Patterns

### Pattern 3.1: Sequential Base + Explicit Overlays
**Use Case**: Base timeline with precise overlays
```python
builder.add_image("slide1.jpg", duration=5.0)
builder.add_image("slide2.jpg", duration=5.0)
builder.add_text_at("Overlay", 3.0, duration=4.0)  # Overlaps slide1
builder.add_voice_at("commentary.mp3", 1.0, duration=3.0)  # Overlaps slide1
```
**Expected Timeline**:
- Image1: 0.0-5.0
- Image2: 5.0-10.0
- Text1: 3.0-7.0 (overlaps slide1)
- Voice1: 1.0-4.0 (overlaps slide1)
**Current Times After**: video=10.0, text=0.0, voice=0.0

### Pattern 3.2: Explicit Setup + Sequential Continuation
**Use Case**: Precise setup followed by sequential content
```python
builder.add_image_at("intro.jpg", 0.0, duration=3.0)
builder.add_text_at("Welcome", 1.0, duration=2.0)
builder.add_voice("narration.mp3", duration=5.0)  # Starts at voice current time
builder.add_image("slide1.jpg", duration=4.0)  # Starts at video current time
```
**Expected Timeline**:
- Image1: 0.0-3.0
- Text1: 1.0-3.0 (overlaps)
- Voice1: 0.0-5.0 (sequential from 0.0)
- Image2: 0.0-4.0 (sequential from 0.0)
**Current Times After**: video=4.0, text=0.0, voice=5.0

### Pattern 3.3: Mixed Audio Strategy
**Use Case**: Background music + sequential voice + explicit effects
```python
builder.add_music_at("background.mp3", 0.0, duration=30.0)
builder.add_voice("intro.mp3", duration=5.0)
builder.add_voice("main.mp3", duration=10.0)
builder.add_sfx_at("explosion.mp3", 8.0, duration=1.0)
builder.add_sfx_at("whoosh.mp3", 12.0, duration=0.5)
```
**Expected Timeline**:
- Music1: 0.0-30.0
- Voice1: 0.0-5.0 (sequential)
- Voice2: 5.0-15.0 (sequential)
- SFX1: 8.0-9.0 (explicit)
- SFX2: 12.0-12.5 (explicit)
**Current Times After**: music=0.0, voice=15.0, sfx=0.0

### Pattern 3.4: Template + Customization
**Use Case**: Template content with custom timing adjustments
```python
builder.add_image("template_bg.jpg", duration=10.0)
builder.add_text("Template Title", duration=10.0)
builder.add_text_at("Custom Overlay", 3.0, duration=4.0)
builder.add_voice_at("custom_audio.mp3", 2.0, duration=6.0)
```
**Expected Timeline**:
- Image1: 0.0-10.0
- Text1: 0.0-10.0
- Text2: 3.0-7.0 (overlaps)
- Voice1: 2.0-8.0 (overlaps)
**Current Times After**: video=10.0, text=10.0, voice=0.0

---

## 4. Edge Cases and Complex Scenarios

### Pattern 4.1: Infinite Duration Clips
**Use Case**: Background elements with no end time
```python
builder.add_image_at("background.jpg", 0.0)  # No duration
builder.add_text("Title", duration=5.0)  # Sequential
builder.add_voice_at("narration.mp3", 2.0, duration=3.0)
```
**Expected Timeline**:
- Image1: 0.0-infinity
- Text1: 0.0-5.0
- Voice1: 2.0-5.0 (overlaps)
**Current Times After**: video=0.0, text=5.0, voice=0.0

### Pattern 4.2: Zero Duration Elements
**Use Case**: Instant effects or markers
```python
builder.add_image("slide1.jpg", duration=5.0)
builder.add_sfx_at("click.mp3", 2.5, duration=0.0)  # Instant
builder.add_text_at("Flash", 2.5, duration=0.1)  # Very short
```
**Expected Timeline**:
- Image1: 0.0-5.0
- SFX1: 2.5-2.5 (instant)
- Text1: 2.5-2.6 (very short)
**Current Times After**: video=5.0, sfx=0.0, text=0.0

### Pattern 4.3: Overlapping Sequential Elements
**Use Case**: Multiple sequential elements on same track
```python
builder.add_image("slide1.jpg", duration=5.0)
builder.add_image("slide2.jpg", duration=5.0)  # Starts at 5.0
builder.add_image_at("overlay.jpg", 3.0, duration=4.0)  # Overlaps both
```
**Expected Timeline**:
- Image1: 0.0-5.0
- Image2: 5.0-10.0
- Image3: 3.0-7.0 (overlaps both)
**Current Times After**: video=10.0

### Pattern 4.4: Cross-Track Sequential
**Use Case**: Sequential elements across different track types
```python
builder.add_image("slide1.jpg", duration=5.0)
builder.add_text("Title", duration=3.0)  # Different track
builder.add_voice("narration.mp3", duration=4.0)  # Different track
```
**Expected Timeline**:
- Image1: 0.0-5.0
- Text1: 0.0-3.0 (different track)
- Voice1: 0.0-4.0 (different track)
**Current Times After**: video=5.0, text=3.0, voice=4.0

### Pattern 4.5: Complex Mixed Timing
**Use Case**: Sophisticated video composition
```python
builder.add_music_at("background.mp3", 0.0, duration=20.0)
builder.add_image("slide1.jpg", duration=5.0)
builder.add_text_at("Overlay 1", 2.0, duration=2.0)
builder.add_image("slide2.jpg", duration=5.0)
builder.add_voice_at("commentary.mp3", 3.0, duration=8.0)
builder.add_sfx_at("transition.mp3", 4.5, duration=1.0)
```
**Expected Timeline**:
- Music1: 0.0-20.0
- Image1: 0.0-5.0
- Text1: 2.0-4.0 (overlaps slide1)
- Image2: 5.0-10.0
- Voice1: 3.0-11.0 (overlaps both slides)
- SFX1: 4.5-5.5 (overlaps slide1)
**Current Times After**: music=0.0, video=10.0, text=0.0, voice=0.0, sfx=0.0

### Pattern 4.6: Batch Operations with Mixed Modes
**Use Case**: Setting duration for some elements, explicit for others
```python
builder.set_duration(3.0)
builder.add_image("slide1.jpg")  # Uses batch duration
builder.add_text("Title")  # Uses batch duration
builder.add_image_at("overlay.jpg", 1.0, duration=2.0)  # Explicit timing
builder.add_voice("narration.mp3")  # Uses batch duration
```
**Expected Timeline**:
- Image1: 0.0-3.0
- Text1: 3.0-6.0
- Image2: 1.0-3.0 (overlaps slide1)
- Voice1: 0.0-3.0 (different track)
**Current Times After**: video=6.0, text=6.0, voice=3.0

### Pattern 4.7: Transition Integration
**Use Case**: Transitions with mixed timing modes
```python
builder.add_image("slide1.jpg", duration=5.0)
builder.add_transition(TransitionType.FADE, duration=1.0)
builder.add_image_at("slide2.jpg", 6.0, duration=5.0)  # After transition
builder.add_text_at("Overlay", 4.0, duration=3.0)  # Overlaps transition
```
**Expected Timeline**:
- Image1: 0.0-5.0
- Transition1: 4.0-5.0 (overlaps)
- Image2: 6.0-11.0
- Text1: 4.0-7.0 (overlaps transition and slide2)
**Current Times After**: video=11.0, text=0.0

### Pattern 4.8: Professional Video Editing
**Use Case**: Complex multi-track composition
```python
builder.add_music_at("background.mp3", 0.0, duration=30.0)
builder.add_image("intro.jpg", duration=3.0)
builder.add_text_at("Title", 1.0, duration=2.0)
builder.add_voice("intro_voice.mp3", duration=3.0)
builder.add_image("main_content.jpg", duration=10.0)
builder.add_text_at("Subtitle", 5.0, duration=5.0)
builder.add_voice_at("main_voice.mp3", 4.0, duration=8.0)
builder.add_sfx_at("highlight.mp3", 6.0, duration=0.5)
```
**Expected Timeline**:
- Music1: 0.0-30.0
- Image1: 0.0-3.0
- Text1: 1.0-3.0 (overlaps intro)
- Voice1: 0.0-3.0
- Image2: 3.0-13.0
- Text2: 5.0-10.0 (overlaps main content)
- Voice2: 4.0-12.0 (overlaps main content)
- SFX1: 6.0-6.5 (overlaps main content)
**Current Times After**: music=0.0, video=13.0, text=0.0, voice=3.0, sfx=0.0

---

## Key Questions for Behavior Determination

Based on these patterns, we need to answer:

1. **Should explicit methods update current times?**
   - If YES: Pattern 2.1-2.4 would have updated current times
   - If NO: Current implementation is correct

2. **How should mixed mode handle current times?**
   - Sequential elements should always update their track's current time
   - Explicit elements should either always or never update current times

3. **What happens when switching between modes?**
   - Should there be any state preservation?
   - Should there be warnings or validation?

4. **How should infinite duration clips affect current times?**
   - Should they set current time to infinity?
   - Should they be ignored for current time calculations?

This analysis will help determine the most intuitive and useful behavior for users.
