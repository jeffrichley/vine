# 📽️ Project Vine - API Specification

**Project Vine** is a modular, agent-compatible, dual-mode video composition system built on top of MoviePy. Designed for AI-driven and human-assisted short-form video generation, it provides an expressive and extensible API, supports scene- and beat-based structures, and is optimized for integration with LLMs and declarative config pipelines.

---

## 🎯 Core Design Philosophy

Vine models timelines as composable blocks. Each block (scene, beat, or voice-image pair) can include voice, music, images, clips, effects, and transitions. The framework supports:

- **Scene-based narrative pacing** (e.g. documentaries, sermons)
- **Beat-driven precision editing** (e.g. TikToks, music videos)  
- **Hybrid combinations** (e.g. emotional shorts with rhythmic mid-sections)

Built for automation at scale, it allows:
- Pydantic-validated configs (YAML/JSON)
- Agent-generated inputs
- Global/timeline/block default overrides
- Extensible registries (for transitions, animations, audio FX)

---

## 🧱 Core API: TimelineBuilder

### Primary Interface

```python
from vine import TimelineBuilder

timeline = (
    TimelineBuilder()  # Defaults: verbose=True, strict_mode=True
    .with_defaults(animation="ken_burns", transition="crossfade")
    .add_music("assets/music/ambient.mp3", bpm=100)
    .add_voice_image_pair("voice/line1.mp3", "images/scene1.jpg")
        .with_animation("ken_burns", zoom="in")
        .with_subtitle("Keep going.")
        .with_transition("fade", duration=1.0)
    .add_voice_image_pair("voice/line2.mp3", "images/scene2.jpg")
        .with_animation("slide_in", direction="left")
        .with_subtitle("Don't stop now.")
    .export("output/final.mp4", resolution="1080x1920")
)
```

### TimelineBuilder Constructor

```python
TimelineBuilder(
    strict_mode=True,    # Fail on missing required values (default)
    verbose=True         # Show warnings for fallbacks (default)
)
```

**Configuration Options:**
- **`strict_mode=True`**: Raises `VineConfigError` when required values are missing
- **`strict_mode=False`**: Uses fallbacks with warnings (for rapid prototyping)
- **`verbose=True`**: Shows helpful warnings about fallback usage
- **`verbose=False`**: Silent fallbacks (for production use)

### TimelineBuilder Methods

| Method | Description | Parameters |
|--------|-------------|------------|
| `.with_defaults(**kwargs)` | Set timeline-level defaults | `animation`, `transition`, `resolution`, `font` |
| `.add_music(path, bpm=None)` | Add background music track | `path: str`, `bpm: Optional[int]` |
| `.add_voiceover(path)` | Add global voiceover track | `path: str` |
| `.add_voice_image_pair(voice, image)` | Add synced voice-image block | `voice: str`, `image: str` |
| `.with_animation(type, **params)` | Set animation for last block | `type: str`, `**params` |
| `.with_subtitle(text)` | Add subtitle overlay | `text: str` |
| `.with_transition(type, **params)` | Add transition to next block | `type: str`, `**params` |
| `.start_scene(name)` | Start story-driven scene block | `name: str` |
| `.start_beat_track(music, bpm)` | Start beat-driven block | `music: str`, `bpm: int` |
| `.on_beat(time).add_clip(...)` | Add beat-aligned elements | `time: float` |
| `.export(path, resolution)` | Render final video | `path: str`, `resolution: str` |
| `.get_defaults()` | Show current default values | None |

---

## 🎛️ Enhanced Defaults System

### Default Hierarchy with Warnings

The system uses a clear hierarchy with intelligent warnings:

```
Block Override > Timeline Default > Global Default > Fallback Value
```

### Global Defaults (Application-wide)

```python
from vine.defaults import set_global_defaults

set_global_defaults(
    animation="ken_burns",
    transition="crossfade", 
    resolution="1080x1920",
    font="Montserrat-Bold"
)
```

### Timeline Defaults (Per-timeline)

```python
timeline = (
    TimelineBuilder()
    .with_defaults(
        animation="slide_in",
        transition="fade",
        resolution="720x1280"
    )
    # All blocks use these defaults unless overridden
)
```

### Block Overrides (Per-block)

```python
.add_voice_image_pair("voice.mp3", "img.jpg")
    .with_animation("zoom_blur")  # Override animation only
    .with_subtitle("Custom text")  # Add subtitle
    # Uses timeline default for transition
```

### Discovering Current Defaults

```python
# Show all current default values
print(TimelineBuilder.get_defaults())
# Output:
# {
#   'animation': 'ken_burns',
#   'transition': 'crossfade',
#   'resolution': '1080x1920',
#   'font': 'Montserrat-Bold'
# }

# Show defaults for a specific timeline
timeline = TimelineBuilder().with_defaults(animation="slide_in")
print(timeline.get_defaults())
# Output:
# {
#   'animation': 'slide_in',
#   'transition': 'crossfade',  # From global
#   'resolution': '1080x1920',  # From global
#   'font': 'Montserrat-Bold'   # From global
# }
```

### Warning Examples

```python
# With verbose=True (default)
timeline = TimelineBuilder()
timeline.add_voice_image_pair("voice.mp3", "image.jpg")
# Warning: "No animation specified, using fallback: static"
# Warning: "No transition specified, using fallback: fade"

# With strict_mode=True (default)
timeline = TimelineBuilder(strict_mode=True)
timeline.add_voice_image_pair("voice.mp3", "image.jpg")
# Raises: VineConfigError("Animation must be explicitly set in strict mode")

# With both relaxed
timeline = TimelineBuilder(strict_mode=False, verbose=False)
timeline.add_voice_image_pair("voice.mp3", "image.jpg")
# Silent fallbacks, no warnings
```

---

## 🗂️ Registry System

### Animation Registry

```python
from vine.registry import register_animation

@register_animation("ken_burns")
def ken_burns_fx(clip, zoom="in", speed="slow"):
    """Ken Burns effect with zoom and speed control"""
    # Implementation using moviepy
    pass

@register_animation("slide_in") 
def slide_in_fx(clip, direction="left"):
    """Slide in from specified direction"""
    pass

@register_animation("static")
def static_fx(clip):
    """No motion effect"""
    return clip
```

### Transition Registry

```python
from vine.registry import register_transition

@register_transition("fade")
def fade_transition(clip_a, clip_b, duration=1.0):
    """Fade transition between clips"""
    pass

@register_transition("crossfade")
def crossfade_transition(clip_a, clip_b, duration=0.5):
    """Crossfade transition"""
    pass

@register_transition("slide")
def slide_transition(clip_a, clip_b, direction="left", duration=1.0):
    """Slide transition"""
    pass
```

### Registry Access

```python
# Get animation function
animation_fn = ANIMATION_REGISTRY["ken_burns"]
animated_clip = animation_fn(clip, zoom="in", speed="slow")

# Get transition function  
transition_fn = TRANSITION_REGISTRY["fade"]
final_clip = transition_fn(clip_a, clip_b, duration=1.0)
```

---

## 📜 Structured Data Models (Pydantic)

### Core Models

```python
from pydantic import BaseModel
from enum import Enum
from typing import Optional, List

class AnimationType(str, Enum):
    ken_burns = "ken_burns"
    slide_in = "slide_in" 
    static = "static"

class AnimationSpec(BaseModel):
    type: AnimationType
    zoom: Optional[str] = None  # "in", "out"
    direction: Optional[str] = None  # "left", "right", "up", "down"
    speed: Optional[str] = None  # "slow", "medium", "fast"

class VoiceImageBlock(BaseModel):
    voice: str  # Path to voice file (MP3)
    image: str  # Path to image file (JPG/PNG)
    subtitle: Optional[str] = None  # Text overlay shown during voice
    animation: Optional[AnimationSpec] = None  # Motion effect on image
    transition: Optional[str] = None  # Transition to next block

class VineSpec(BaseModel):
    defaults: Optional[dict] = {}  # Timeline defaults
    voice_image_pairs: List[VoiceImageBlock]  # Sequence of blocks
```

---

## 📄 Input Parsers

### From JSON (AI Agent Integration)

```python
from vine.loader import load_vine_from_json

# AI agent generates JSON
json_string = '''
{
  "voice_image_pairs": [
    {
      "voice": "voice/line1.mp3",
      "image": "images/scene1.jpg", 
      "subtitle": "Keep going.",
      "animation": {
        "type": "ken_burns",
        "zoom": "in"
      },
      "transition": "fade"
    }
  ]
}
'''

spec = load_vine_from_json(json_string)
timeline = TimelineBuilder().build_from_spec(spec)
```

### From YAML (Human Editing)

```python
from vine.loader import load_vine_from_yaml

# Human-editable YAML file
spec = load_vine_from_yaml("project.yaml")
timeline = TimelineBuilder().build_from_spec(spec)
```

Example YAML:
```yaml
defaults:
  animation: ken_burns
  transition: crossfade
  resolution: 1080x1920

voice_image_pairs:
  - voice: voice/line1.mp3
    image: images/scene1.jpg
    subtitle: "Keep going."
    animation:
      type: ken_burns
      zoom: in
    transition: fade
```

---

## 🧠 AI Agent Integration

### Preferred Workflow

1. **Agent generates JSON** matching `VineSpec` schema
2. **Parse with Pydantic** for validation
3. **Build timeline** from validated spec
4. **Export video** with full error handling

### Agent Output Example

```json
{
  "defaults": {
    "animation": "ken_burns",
    "transition": "crossfade"
  },
  "voice_image_pairs": [
    {
      "voice": "voice/line1.mp3",
      "image": "images/scene1.jpg",
      "subtitle": "When it hurts, it means you're growing.",
      "animation": {
        "type": "ken_burns",
        "zoom": "in",
        "speed": "slow"
      },
      "transition": "fade"
    }
  ]
}
```

### Schema Validation

```python
# Agent output validation
try:
    spec = VineSpec.model_validate_json(agent_output)
    timeline = TimelineBuilder().build_from_spec(spec)
    timeline.export("output.mp4")
except ValidationError as e:
    # Handle invalid agent output
    print(f"Agent output validation failed: {e}")
```

---

## 🎬 Scene vs Beat Editing

### Scene-Based Editing (Story-driven)

```python
timeline = (
    TimelineBuilder()
    .start_scene("Opening")
        .add_voiceover("voice/intro.mp3")
        .add_clip("clips/opening.mp4")
        .add_text("It starts here")
        .add_transition("fade", duration=1.0)
    .start_scene("B-roll")
        .add_clip("clips/broll1.mp4")
        .add_clip("clips/broll2.mp4")
        .set_transition("slide", direction="left")
    .export("output/scene_video.mp4")
)
```

### Beat-Driven Editing (Rhythm-driven)

```python
timeline = (
    TimelineBuilder()
    .add_music("music/drive.mp3", bpm=120)
    .sync_to_beats([
        {"time": 0.5, "clip": "clips/step1.mp4"},
        {"time": 1.0, "clip": "clips/step2.mp4"},
        {"time": 1.5, "text": "Keep moving"},
    ])
    .export("output/beat_video.mp4")
)
```

### Hybrid Mode

```python
timeline = (
    TimelineBuilder()
    .start_scene("Opening")
        .add_voiceover("voice/intro.mp3")
        .add_clip("clips/intro.mp4")
        .add_transition("fade", duration=1.0)
    .start_beat_track(music="music/drive.mp3", bpm=120)
        .on_beat(0.5).add_clip("punch1.mp4")
        .on_beat(1.0).add_clip("punch2.mp4")
        .on_beat(1.5).add_text("Stay strong")
        .set_transition("crossfade", duration=0.3)
    .start_scene("Closing")
        .add_clip("clips/outro.mp4")
    .export("output/hybrid_video.mp4")
)
```

---

## 🔧 Rendering Internals

### Voice-Image Pair Processing

Each `.add_voice_image_pair()` creates:

1. **AudioFileClip** from voice file
2. **ImageClip** with animation effect applied
3. **TextClip** if subtitle provided
4. **CompositeVideoClip** combining all elements
5. **Duration** determined by voice file length

### Transition Handling

- Transitions are attached to the **tail** of each block
- Each block has `transition_to_next` property
- Final block has no transition (ends cleanly)

### Audio Mixing

- Voice tracks are primary audio
- Music track is mixed underneath
- Optional ducking under voice
- All audio synchronized to video timeline

### Export Process

1. **Flatten timeline** into sequential clips
2. **Apply transitions** between clips
3. **Mix audio tracks** (voice + music)
4. **Render to MP4** with specified resolution
5. **Apply final encoding** settings

---

## 📁 Project Structure

```
vine/                           # Project root
├── src/                        # Source code
│   └── vine/                   # Main package
│       ├── __init__.py         # Main package exports
│       ├── builder/
│       │   ├── __init__.py
│       │   ├── timeline_builder.py     # Main TimelineBuilder class
│       │   ├── block_builders.py       # VoiceImageBlockBuilder, etc.
│       │   └── base_builder.py         # Base builder classes
│       ├── models/
│       │   ├── __init__.py
│       │   ├── video_spec.py          # Pydantic models
│       │   ├── blocks.py              # Block type definitions
│       │   └── enums.py               # AnimationType, etc.
│       ├── registry/
│       │   ├── __init__.py
│       │   ├── base.py                # Base Registry class
│       │   ├── animations.py          # Animation registry
│       │   ├── transitions.py         # Transition registry
│       │   └── effects.py             # Built-in effects
│       ├── loader/
│       │   ├── __init__.py
│       │   ├── json_loader.py         # JSON parsing
│       │   ├── yaml_loader.py         # YAML parsing
│       │   └── spec_builder.py        # Spec-to-timeline conversion
│       ├── render/
│       │   ├── __init__.py
│       │   ├── moviepy_integration.py # MoviePy wrapper
│       │   ├── audio_processor.py     # Audio mixing
│       │   └── exporter.py            # Export pipeline
│       ├── defaults.py                # Defaults management
│       ├── api.py                     # High-level API exports
│       └── exceptions.py              # Custom exceptions
├── tests/                     # Test suite
│   ├── unit/
│   │   ├── test_models.py          # Pydantic model tests
│   │   ├── test_registry.py        # Registry system tests
│   │   ├── test_defaults.py        # Defaults management tests
│   │   └── test_builder.py         # TimelineBuilder tests
│   ├── integration/
│   │   ├── test_rendering.py       # End-to-end rendering tests
│   │   ├── test_parsing.py         # JSON/YAML parsing tests
│   │   └── test_audio.py           # Audio processing tests
│   ├── fixtures/
│   │   ├── sample_audio/           # Test audio files
│   │   ├── sample_images/          # Test image files
│   │   └── sample_configs/         # Test YAML/JSON configs
│   └── conftest.py                 # Pytest configuration
├── examples/                   # Example projects
│   ├── basic_usage/
│   │   ├── simple_video.py        # Basic voice-image pair
│   │   ├── with_animations.py     # Animation examples
│   │   └── with_transitions.py    # Transition examples
│   ├── ai_integration/
│   │   ├── agent_example.py       # AI agent integration
│   │   ├── json_specs/            # Sample JSON specs
│   │   └── yaml_configs/          # Sample YAML configs
│   ├── advanced_features/
│   │   ├── scene_editing.py       # Scene-based editing
│   │   ├── beat_editing.py        # Beat-driven editing
│   │   └── hybrid_mode.py         # Hybrid editing
│   └── tutorials/
│       ├── getting_started.py     # Tutorial examples
│       ├── custom_effects.py      # Custom effect creation
│       └── best_practices.py      # Best practices guide
├── docs/                        # Documentation
│   ├── api/                      # API documentation
│   ├── tutorials/                # Tutorial guides
│   ├── examples/                 # Code examples
│   └── planning/                 # Project planning docs
├── scripts/                      # Utility scripts
│   ├── setup_dev.py              # Development setup
│   ├── run_tests.py              # Test runner
│   └── build_docs.py             # Documentation builder
├── .github/                      # GitHub workflows
│   └── workflows/
│       ├── ci.yml                # Continuous integration
│       └── release.yml           # Release automation
├── requirements/                 # Dependency management
│   ├── requirements.txt          # Production dependencies
│   ├── requirements-dev.txt      # Development dependencies
│   └── requirements-test.txt     # Testing dependencies
├── pyproject.toml               # Project configuration
├── setup.py                     # Package setup (legacy)
├── README.md                    # Project overview
├── CHANGELOG.md                 # Version history
├── LICENSE                      # License file
└── .gitignore                   # Git ignore rules
```

---

## ✅ Feature Checklist

| Feature | Status | Description |
|---------|--------|-------------|
| Voice-synced image blocks | ✅ | Auto-duration from voice files |
| Scene-based editing | ✅ | Story-driven narrative structure |
| Beat-driven blocks | ✅ | Music-synchronized timing |
| Transitions | ✅ | Extensible transition registry |
| Multiple animation types | ✅ | Ken Burns, slide, static, etc. |
| Subtitle overlays | ✅ | Text overlay during voice |
| Enhanced default hierarchy | ✅ | Global → Timeline → Block with warnings |
| JSON → Pydantic pipeline | ✅ | AI agent integration |
| YAML support for humans | ✅ | Human-editable configs |
| Registry system | ✅ | Extensible effects/transitions |
| AI agent compatibility | ✅ | Structured output validation |
| Export to MP4 | ✅ | Resolution and quality control |
| Extensible effects | ✅ | Plugin architecture |
| Intelligent warnings | ✅ | Verbose mode with helpful feedback |
| Strict validation | ✅ | Configurable strict mode for debugging |

---

## 🚀 Getting Started

### Basic Usage

```python
from vine import TimelineBuilder

# Simple voice-image pair (will show warnings for missing defaults)
timeline = (
    TimelineBuilder()  # verbose=True, strict_mode=True by default
    .add_voice_image_pair("voice.mp3", "image.jpg")
        .with_animation("ken_burns", zoom="in")
        .with_subtitle("Hello world")
    .export("output.mp4")
)
```

### With AI Agent

```python
from vine.loader import load_vine_from_json
from vine import TimelineBuilder

# Agent generates JSON
agent_output = ai_agent.generate_video_plan(prompt)

# Parse and build
spec = load_vine_from_json(agent_output)
timeline = TimelineBuilder().build_from_spec(spec)
timeline.export("output.mp4")
```

### With YAML Config

```python
from vine.loader import load_vine_from_yaml
from vine import TimelineBuilder

# Load from YAML file
spec = load_vine_from_yaml("project.yaml")
timeline = TimelineBuilder().build_from_spec(spec)
timeline.export("output.mp4")
```

### Relaxed Mode for Rapid Prototyping

```python
# For quick experimentation
timeline = TimelineBuilder(strict_mode=False, verbose=True)
timeline.add_voice_image_pair("voice.mp3", "image.jpg")
# Shows warnings but continues with fallbacks
```

### Production Mode

```python
# For production use
timeline = TimelineBuilder(strict_mode=False, verbose=False)
timeline.add_voice_image_pair("voice.mp3", "image.jpg")
# Silent fallbacks, no warnings
```

---

This API specification provides a complete foundation for building the Project Vine media composition framework, supporting both human and AI-driven video generation workflows with intelligent defaults and clear feedback. 