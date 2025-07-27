# Phase 1 Core Architecture Specification

> **Project:** Vine Media Framework
> **Phase:** 1 - Foundation
> **Status:** In Development
> **Priority:** High
> **Timeline:** Weeks 1-2

## Overview

This specification defines the core architecture components for Phase 1 of Project Vine, establishing the foundation for the modular, agent-compatible video composition framework.

## Core Components

### 1. Pydantic Models (`vine/models/`)

**Purpose:** Data validation and type safety for video specifications

**Components:**
- `VideoSpec` - Main video configuration model
- `TimelineSpec` - Timeline structure and timing
- `AudioSpec` - Audio configuration and voice-image pairs
- `EffectSpec` - Animation and transition specifications
- `ExportSpec` - Output configuration and quality settings

**Key Features:**
- Full type validation with Pydantic v2
- JSON/YAML serialization support
- Nested model relationships
- Custom validators for video-specific constraints

### 2. Registry System (`vine/registry/`)

**Purpose:** Extensible plugin system for effects and transitions

**Components:**
- `EffectRegistry` - Animation effects (Ken Burns, slide, static)
- `TransitionRegistry` - Transition effects (fade, crossfade, slide)
- `RegistryBase` - Abstract base class for all registries
- `RegistryManager` - Central registry coordination

**Key Features:**
- Plugin discovery and loading
- Effect/transition registration
- Configuration validation
- Hot-reload capability

### 3. TimelineBuilder (`vine/builder/`)

**Purpose:** Fluent API for video timeline construction

**Components:**
- `TimelineBuilder` - Main builder class
- `SceneBuilder` - Scene-based timeline construction
- `BeatBuilder` - Beat-driven timeline construction
- `TimelineNode` - Individual timeline elements

**Key Features:**
- Method chaining for intuitive API
- Scene and beat mode support
- Voice-image pair synchronization
- Timeline validation and optimization

### 4. Defaults Management (`vine/defaults/`)

**Purpose:** Hierarchical configuration system

**Components:**
- `DefaultsManager` - Central defaults coordination
- `ProjectDefaults` - Project-level settings
- `UserDefaults` - User-specific preferences
- `SystemDefaults` - Framework-level defaults

**Key Features:**
- Hierarchical override system
- Environment-specific defaults
- Validation and fallback mechanisms
- Hot-reload support

### 5. Loader System (`vine/loader/`)

**Purpose:** Resource loading and management

**Components:**
- `AudioLoader` - Audio file loading and processing
- `ImageLoader` - Image file loading and optimization
- `ConfigLoader` - JSON/YAML configuration loading
- `ResourceManager` - Central resource coordination

**Key Features:**
- Multiple format support (MP3, WAV, PNG, JPG, etc.)
- Memory optimization and caching
- Error handling and fallbacks
- Progress tracking for large files

## API Design

### TimelineBuilder API

```python
# Basic usage
timeline = (
    TimelineBuilder()
    .add_scene("intro", duration=3.0)
    .add_voice_image_pair("intro", "intro_audio.mp3", "intro_image.jpg")
    .add_effect("intro", "ken_burns", {"zoom": 1.2})
    .add_transition("intro", "main", "fade", {"duration": 0.5})
    .build()
)

# Beat-driven usage
timeline = (
    TimelineBuilder()
    .set_beat_mode(True)
    .add_beat_section("verse", beats=[1, 2, 3, 4])
    .add_voice_image_pair("verse", "verse_audio.mp3", "verse_images/")
    .add_effect("verse", "slide", {"direction": "left"})
    .build()
)
```

### Registry API

```python
# Register custom effects
@EffectRegistry.register("custom_zoom")
class CustomZoomEffect:
    def apply(self, clip, config):
        # Implementation
        pass

# Use registered effects
timeline.add_effect("scene", "custom_zoom", {"scale": 1.5})
```

## Data Models

### VideoSpec Model

```python
class VideoSpec(BaseModel):
    timeline: TimelineSpec
    audio: AudioSpec
    effects: List[EffectSpec] = []
    transitions: List[TransitionSpec] = []
    export: ExportSpec

    class Config:
        json_encoders = {
            Path: str,
            datetime: lambda v: v.isoformat()
        }
```

### TimelineSpec Model

```python
class TimelineSpec(BaseModel):
    mode: Literal["scene", "beat", "hybrid"] = "scene"
    scenes: List[SceneSpec] = []
    beats: Optional[List[BeatSpec]] = None
    duration: Optional[float] = None

    @validator('duration')
    def validate_duration(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Duration must be positive")
        return v
```

## Implementation Priorities

### Week 1 (High Priority)
1. **Pydantic Models** - Core data validation
2. **Registry System** - Plugin architecture foundation
3. **Basic TimelineBuilder** - Minimal viable API

### Week 2 (Medium Priority)
1. **Defaults Management** - Configuration system
2. **Loader System** - Resource management
3. **Voice-Image Pairs** - Core synchronization

## Success Criteria

- [ ] All Pydantic models pass validation tests
- [ ] Registry system can load and register effects
- [ ] TimelineBuilder creates valid timelines
- [ ] Voice-image pairs synchronize correctly
- [ ] Basic video export functionality works
- [ ] Error handling provides meaningful messages

## Dependencies

- Python 3.11+
- Pydantic v2
- MoviePy
- Pillow (PIL)
- NumPy

## Testing Strategy

- Unit tests for all Pydantic models
- Integration tests for TimelineBuilder
- Registry system tests
- End-to-end video generation tests

## Documentation Requirements

- API reference documentation
- Usage examples and tutorials
- Architecture diagrams
- Development setup guide
