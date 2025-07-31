# 🎬 Vine Framework: Rendering Architecture & Shorts Creation Guide 🚀

## 🎯 How the Rendering System Works 🔧

The Vine framework uses a **layered architecture** with clear separation of concerns:

## ⏰ Timing Modes: Sequential vs Explicit

Project Vine supports two timing modes with Google-style API behavior:

### 🔄 Sequential Mode (Updates Current Time)
```python
# Each call updates the current time for that track
builder.add_image("slide1.jpg", duration=5.0)      # video_current_time = 5.0
builder.add_text("Welcome", duration=3.0)          # text_current_time = 3.0
builder.add_voice("narration.mp3", duration=8.0)   # voice_current_time = 8.0
```

### 🎯 Explicit Mode (Does NOT Update Current Time)
```python
# Each call places content at exact times without affecting current time
builder.add_image_at("background.jpg", 0.0, duration=10.0)  # video_current_time unchanged
builder.add_text_at("Title", 2.0, duration=6.0)             # text_current_time unchanged
builder.add_voice_at("narration.mp3", 1.0, duration=8.0)    # voice_current_time unchanged
```

### 🔀 Mixed Mode (Best of Both Worlds)
```python
# Start with sequential for basic structure
builder.add_image("intro.jpg", duration=3.0)       # video_current_time = 3.0

# Add precise overlays with explicit timing
builder.add_text_at("Overlay", 1.5, duration=1.0)  # text_current_time unchanged
builder.add_sfx_at("pop.wav", 2.0, duration=0.5)   # sfx_current_time unchanged

# Continue with sequential
builder.add_image("content.jpg", duration=5.0)     # video_current_time = 8.0
```

### 🏗️ Architecture Overview

```
TimelineBuilder → VideoSpec → Renderers → MoviePy → Final Video
     ↓              ↓           ↓          ↓         ↓
  User API    Data Model   Processing   Rendering  Output
```

### 🔧 Key Components

1. **TimelineBuilder** - Fluent API for building video timelines ✨
2. **VideoSpec** - Pydantic model containing all video data 📋
3. **Renderers** - Convert VideoSpec to MoviePy clips 🎨
4. **MoviePy Adapter** - Bridge between Vine models and MoviePy 🌉
5. **Clip Factory** - Creates MoviePy clips from Vine models 🏭

### 🔄 Rendering Pipeline

```
1. TimelineBuilder.add_image() → VideoTrack 📸
2. TimelineBuilder.add_voice() → VoiceTrack 🎤
3. TimelineBuilder.add_music() → MusicTrack 🎵
4. TimelineBuilder.add_sfx() → SFXTrack 🔊
5. TimelineBuilder.build() → VideoSpec 📋
6. VideoRenderer.render() → CompositeVideoClip 🎬
7. AudioRenderer.render() → CompositeAudioClip 🎵
8. MoviePy.write_videofile() → Final Video 🎉
```

---

## 🎯 How to Code a Shorts Clip 📱

### 📝 Basic Pattern

```python
from vine.builder.timeline_builder import TimelineBuilder

# 1. Create timeline builder
builder = TimelineBuilder(width=1080, height=1920, fps=30)

# 2. Add content (sequential mode)
builder.add_image("image1.jpg", duration=3.0)
builder.add_voice("voice1.mp3", duration=3.0)
builder.add_music("background.mp3", duration=3.0)
builder.add_sfx("transition.wav", duration=0.5)
builder.add_text("Caption", duration=3.0)

# 3. Build and render
video_spec = builder.build()
video_spec.export("output.mp4")
```

### ⚡ Advanced Pattern (Explicit Timing)

```python
# Add content at specific times (Google-style API behavior)
builder.add_image_at("image1.jpg", start_time=0.0, duration=3.0)
builder.add_voice_at("voice1.mp3", start_time=0.5, duration=2.0)
builder.add_music_at("background.mp3", start_time=0.0, duration=15.0, volume=0.3)
builder.add_sfx_at("transition.wav", start_time=2.5, duration=0.5, volume=0.6)
builder.add_text_at("Caption", start_time=1.0, duration=2.0)

# Note: Explicit methods do NOT update current times
# Sequential methods DO update current times
```

---

## ☕ Fictitious Example: "Coffee Shop Dreams" 🌟

Let me walk you through creating a motivational shorts video about a barista's journey to opening their own coffee shop.

### 📖 Concept
- **Duration:** 15 seconds ⏱️
- **Theme:** "From barista to entrepreneur" 💼
- **Style:** Inspirational with smooth transitions ✨
- **Aspect Ratio:** 9:16 (1080x1920) 📱

### 📋 Storyboard
1. **0-3s:** Barista making coffee (image + voice: "Every morning, I wake up at 4 AM") ☕
2. **3-6s:** Coffee shop interior (voice: "But I'm not just making coffee") 🏪
3. **6-9s:** Business plan on laptop (voice: "I'm building my dream") 💻
4. **9-12s:** Construction site (voice: "One day, this will be my shop") 🏗️
5. **12-15s:** Grand opening sign (voice: "Dreams don't work unless you do") 🎊

---

## 🛠️ Step-by-Step Implementation 🔨

### 🚀 Step 1: Setup the Timeline Builder

```python
from vine.builder.timeline_builder import TimelineBuilder

# Create builder with shorts dimensions
builder = TimelineBuilder(
    width=1080,      # 9:16 aspect ratio 📱
    height=1920,     # Perfect for mobile 📲
    fps=30           # Smooth playback 🎬
)
```

### 🎵 Step 2: Add Background Music

```python
# Add ambient coffee shop music for entire duration
builder.add_voice_at(
    "assets/coffee_shop_ambient.mp3",
    start_time=0.0,
    duration=15.0,
    volume=0.3  # Keep it subtle 🎧
)
```

### ☕ Step 3: Add First Segment (0-3s)

```python
# Barista making coffee
builder.add_image_at(
    "assets/barista_making_coffee.jpg",
    start_time=0.0,
    duration=3.0
)

# Voiceover
builder.add_voice_at(
    "assets/voice_01_every_morning.mp3",
    start_time=0.0,
    duration=3.0,
    volume=0.8
)

# Caption
builder.add_text_at(
    "Every morning, I wake up at 4 AM",
    start_time=0.5,
    duration=2.0,
    font_size=48,
    font_color="#FFFFFF",
    x_position=540,  # Center horizontally 🎯
    y_position=1600  # Near bottom 📍
)
```

### 🏪 Step 4: Add Second Segment (3-6s)

```python
# Coffee shop interior
builder.add_image_at(
    "assets/coffee_shop_interior.jpg",
    start_time=3.0,
    duration=3.0
)

# Voiceover
builder.add_voice_at(
    "assets/voice_02_not_just_coffee.mp3",
    start_time=3.0,
    duration=3.0,
    volume=0.8
)

# Caption
builder.add_text_at(
    "But I'm not just making coffee",
    start_time=3.5,
    duration=2.0,
    font_size=48,
    font_color="#FFFFFF",
    x_position=540,
    y_position=1600
)
```

### 💻 Step 5: Add Third Segment (6-9s)

```python
# Business plan on laptop
builder.add_image_at(
    "assets/business_plan_laptop.jpg",
    start_time=6.0,
    duration=3.0
)

# Voiceover
builder.add_voice_at(
    "assets/voice_03_building_dream.mp3",
    start_time=6.0,
    duration=3.0,
    volume=0.8
)

# Caption
builder.add_text_at(
    "I'm building my dream",
    start_time=6.5,
    duration=2.0,
    font_size=48,
    font_color="#FFFFFF",
    x_position=540,
    y_position=1600
)
```

### 🏗️ Step 6: Add Fourth Segment (9-12s)

```python
# Construction site
builder.add_image_at(
    "assets/construction_site.jpg",
    start_time=9.0,
    duration=3.0
)

# Voiceover
builder.add_voice_at(
    "assets/voice_04_one_day_shop.mp3",
    start_time=9.0,
    duration=3.0,
    volume=0.8
)

# Caption
builder.add_text_at(
    "One day, this will be my shop",
    start_time=9.5,
    duration=2.0,
    font_size=48,
    font_color="#FFFFFF",
    x_position=540,
    y_position=1600
)
```

### 🎊 Step 7: Add Final Segment (12-15s)

```python
# Grand opening sign
builder.add_image_at(
    "assets/grand_opening_sign.jpg",
    start_time=12.0,
    duration=3.0
)

# Voiceover
builder.add_voice_at(
    "assets/voice_05_dreams_dont_work.mp3",
    start_time=12.0,
    duration=3.0,
    volume=0.8
)

# Caption
builder.add_text_at(
    "Dreams don't work unless you do",
    start_time=12.5,
    duration=2.0,
    font_size=48,
    font_color="#FFFFFF",
    x_position=540,
    y_position=1600
)
```

### ✨ Step 8: Add Transitions

```python
# Add fade transitions between segments
builder.add_transition_at("fade", start_time=2.8, duration=0.4)
builder.add_transition_at("fade", start_time=5.8, duration=0.4)
builder.add_transition_at("fade", start_time=8.8, duration=0.4)
builder.add_transition_at("fade", start_time=11.8, duration=0.4)
```

### 🎬 Step 9: Build and Render

```python
# Build the video specification
video_spec = builder.build()

# Export the final video
video_spec.export(
    "output/coffee_shop_dreams.mp4",
    codec="libx264",
    audio_codec="aac",
    bitrate="8000k"
)
```

---

## 🔧 Complete Implementation 💻

Here's the complete code for our "Coffee Shop Dreams" shorts:

```python
#!/usr/bin/env python3
"""
Coffee Shop Dreams - Motivational Shorts Video ☕
A barista's journey from employee to entrepreneur 💼
"""

from vine.builder.timeline_builder import TimelineBuilder

def create_coffee_shop_dreams():
    """Create the Coffee Shop Dreams motivational shorts video."""

    # Initialize timeline builder for 9:16 shorts
    builder = TimelineBuilder(width=1080, height=1920, fps=30)

    # Add background music for entire duration
    builder.add_music_at(
        "assets/coffee_shop_ambient.mp3",
        start_time=0.0,
        duration=15.0,
        volume=0.3,
        fade_in=1.0,
        fade_out=1.0
    )

    # Segment 1: Barista making coffee (0-3s) ☕
    builder.add_image_at("assets/barista_making_coffee.jpg", 0.0, 3.0)
    builder.add_voice_at("assets/voice_01_every_morning.mp3", 0.0, 3.0, volume=0.8)
    builder.add_text_at(
        "Every morning, I wake up at 4 AM",
        0.5, 2.0,
        font_size=48, font_color="#FFFFFF",
        x_position=540, y_position=1600
    )

    # Segment 2: Coffee shop interior (3-6s) 🏪
    builder.add_image_at("assets/coffee_shop_interior.jpg", 3.0, 3.0)
    builder.add_voice_at("assets/voice_02_not_just_coffee.mp3", 3.0, 3.0, volume=0.8)
    builder.add_text_at(
        "But I'm not just making coffee",
        3.5, 2.0,
        font_size=48, font_color="#FFFFFF",
        x_position=540, y_position=1600
    )

    # Segment 3: Business plan (6-9s) 💻
    builder.add_image_at("assets/business_plan_laptop.jpg", 6.0, 3.0)
    builder.add_voice_at("assets/voice_03_building_dream.mp3", 6.0, 3.0, volume=0.8)
    builder.add_text_at(
        "I'm building my dream",
        6.5, 2.0,
        font_size=48, font_color="#FFFFFF",
        x_position=540, y_position=1600
    )

    # Segment 4: Construction site (9-12s) 🏗️
    builder.add_image_at("assets/construction_site.jpg", 9.0, 3.0)
    builder.add_voice_at("assets/voice_04_one_day_shop.mp3", 9.0, 3.0, volume=0.8)
    builder.add_text_at(
        "One day, this will be my shop",
        9.5, 2.0,
        font_size=48, font_color="#FFFFFF",
        x_position=540, y_position=1600
    )

    # Segment 5: Grand opening (12-15s) 🎊
    builder.add_image_at("assets/grand_opening_sign.jpg", 12.0, 3.0)
    builder.add_voice_at("assets/voice_05_dreams_dont_work.mp3", 12.0, 3.0, volume=0.8)
    builder.add_text_at(
        "Dreams don't work unless you do",
        12.5, 2.0,
        font_size=48, font_color="#FFFFFF",
        x_position=540, y_position=1600
    )

    # Add fade transitions ✨
    for i in [2.8, 5.8, 8.8, 11.8]:
        builder.add_transition_at("fade", i, 0.4)

    # Build and export 🎬
    video_spec = builder.build()
    video_spec.export("output/coffee_shop_dreams.mp4")

    print("✅ Coffee Shop Dreams video created successfully!")
    print(f"⏱️ Duration: {video_spec.get_total_duration():.1f}s")
    print(f"📱 Resolution: {video_spec.width}x{video_spec.height}")
    print(f"🎵 Music tracks: {len(video_spec.music_tracks)}")
    print(f"🎤 Voice tracks: {len(video_spec.voice_tracks)}")
    print(f"🔊 SFX tracks: {len(video_spec.sfx_tracks)}")
    print(f"🎬 Video tracks: {len(video_spec.video_tracks)}")

if __name__ == "__main__":
    create_coffee_shop_dreams()
```

---

## 🎯 Key Takeaways 💡

### 🔄 Rendering Process
1. **TimelineBuilder** creates a fluent API for building videos ✨
2. **VideoSpec** contains all the data in a structured format 📋
3. **Renderers** convert the spec to MoviePy clips 🎨
4. **MoviePy** handles the actual video rendering 🎬

### 📱 Shorts Best Practices
- Use 9:16 aspect ratio (1080x1920) 📱
- Keep duration under 60 seconds ⏱️
- Use clear, readable text 📝
- Synchronize audio with visuals 🎵
- Add smooth transitions ✨
- Use consistent branding 🏷️

### 💻 Code Patterns
- **Sequential mode:** `add_image()`, `add_voice()`, `add_music()`, `add_sfx()` (auto-appends) ➡️
- **Explicit mode:** `add_image_at()`, `add_voice_at()`, `add_music_at()`, `add_sfx_at()` (specific timing) ⏰
- **Method chaining:** `builder.add_image().add_voice().add_music().add_text()` 🔗
- **Batch operations:** `builder.set_duration(3.0)` for consistent timing ⚡

---

## 🚀 Advanced Features 🌟

### 🎨 Effects and Animations
```python
# Add Ken Burns effect to images
builder.add_image_at(
    "image.jpg", 0.0, 3.0,
    animation_config=KenBurnsConfig(zoom_factor=1.2, pan_x=0.1)
)

# Add slide transitions
builder.add_transition_at("slide", 2.8, 0.4, direction="left")
```

### 🎵 Audio Track Separation
The Vine framework uses separate audio tracks for professional mixing:

- **🎤 Voice Tracks**: Narration, dialogue, commentary
- **🎵 Music Tracks**: Background music, ambient sounds
- **🔊 SFX Tracks**: Sound effects, transitions, impacts

This separation allows for:
- **Independent volume control** per track type
- **Professional mixing** with MoviePy's CompositeAudioClip
- **Automatic crossfades** between adjacent clips
- **Custom volume curves** for dynamic audio

```python
# Separate audio tracks for professional mixing
builder.add_voice_at("voice.mp3", 0.0, 3.0, volume=0.8, fade_in=0.2)
builder.add_music_at("background.mp3", 0.0, 15.0, volume=0.3, fade_in=1.0, fade_out=1.0)
builder.add_sfx_at("transition.wav", 1.5, 0.5, volume=0.6, normalize_audio=True)

# Professional audio controls
builder.add_music_at(
    "music.mp3", 0.0, 10.0,
    volume=0.4,
    fade_in=2.0,
    fade_out=2.0,
    crossfade_duration=0.5,
    volume_curve=[(0.0, 0.0), (2.0, 1.0), (8.0, 1.0), (10.0, 0.0)]
)
```

### 📝 Text Styling
```python
# Rich text formatting
builder.add_text_at(
    "Inspiring Text",
    0.5, 2.0,
    font_size=64,
    font_color="#FFD700",  # Gold color
    font_family="Arial Bold",
    x_position=540,
    y_position=1600
)
```

---

## 🎉 The Vine framework makes it easy to create professional-quality shorts videos with clean, maintainable code! 🚀

### 🏆 Benefits:
- ✨ **Fluent API** - Easy to read and write
- 🎯 **Type Safety** - Pydantic models prevent errors
- 🔧 **Modular Design** - Easy to extend and customize
- 🎬 **MoviePy Integration** - Professional video rendering
- 📱 **Shorts Optimized** - Perfect for social media content
- 🚀 **High Performance** - Efficient rendering pipeline

### 🎊 Ready to create amazing shorts videos! 🎬✨
