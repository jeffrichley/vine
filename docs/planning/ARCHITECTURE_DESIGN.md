# 🏗️ Project Vine - Architecture Design

This document outlines the technical architecture and design decisions for the Project Vine media composition framework.

---

## 🎯 Architecture Overview

Project Vine follows a **layered architecture** with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface Layer                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │   Fluent API    │  │   YAML Config   │  │  AI Agent    │ │
│  │  TimelineBuilder│  │     Parser      │  │   JSON       │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                   Business Logic Layer                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │   Timeline      │  │   Block         │  │  Registry    │ │
│  │   Management    │  │   Processing    │  │   System     │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                   Data Layer                                │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │   Pydantic      │  │   Defaults      │  │  Validation  │ │
│  │   Models        │  │   Management    │  │   Engine     │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                   Rendering Layer                           │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │   MoviePy       │  │   Audio         │  │  Export      │ │
│  │   Integration   │  │   Processing    │  │   Pipeline   │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧱 Core Components

### 1. TimelineBuilder (Fluent API)

The main entry point for building video timelines with intelligent defaults and warnings.

```python
class TimelineBuilder:
    """Main builder class for creating video timelines"""
    
    def __init__(self, strict_mode=True, verbose=True):
        self.blocks: List[TimelineBlock] = []
        self.defaults: Dict[str, Any] = {}
        self.current_mode: str = "scene"
        self.music_track: Optional[AudioTrack] = None
        self.global_voiceover: Optional[AudioTrack] = None
        self.strict_mode = strict_mode
        self.verbose = verbose
        
    def with_defaults(self, **kwargs) -> 'TimelineBuilder':
        """Set timeline-level defaults"""
        
    def add_voice_image_pair(self, voice: str, image: str) -> VoiceImageBlockBuilder:
        """Add a voice-image pair block with intelligent fallbacks"""
        
    def start_scene(self, name: str) -> SceneBlockBuilder:
        """Start a new scene block"""
        
    def start_beat_track(self, music: str, bpm: int) -> BeatTrackBuilder:
        """Start a beat-driven block"""
        
    def export(self, path: str, resolution: str = "1080x1920") -> None:
        """Export the final video"""
        
    def get_defaults(self) -> Dict[str, Any]:
        """Show current default values with hierarchy"""
```

### 2. Block System

Different types of timeline blocks for various editing modes.

```python
class TimelineBlock(ABC):
    """Base class for all timeline blocks"""
    
    @abstractmethod
    def render(self) -> VideoClip:
        """Render this block to a VideoClip"""
        pass

class VoiceImageBlock(TimelineBlock):
    """Block containing a voice file and corresponding image"""
    
    def __init__(self, voice: str, image: str):
        self.voice_path = voice
        self.image_path = image
        self.subtitle: Optional[str] = None
        self.animation: Optional[AnimationSpec] = None
        self.transition_to_next: Optional[TransitionSpec] = None
        
    def with_animation(self, type: str, **params) -> 'VoiceImageBlock':
        """Set animation for this block"""
        
    def with_subtitle(self, text: str) -> 'VoiceImageBlock':
        """Add subtitle to this block"""
        
    def with_transition(self, type: str, **params) -> 'VoiceImageBlock':
        """Set transition to next block"""

class SceneBlock(TimelineBlock):
    """Block for scene-based editing"""
    
    def __init__(self, name: str):
        self.name = name
        self.elements: List[VideoElement] = []
        self.transition_to_next: Optional[TransitionSpec] = None

class BeatTrack(TimelineBlock):
    """Block for beat-driven editing"""
    
    def __init__(self, music: str, bpm: int):
        self.music_path = music
        self.bpm = bpm
        self.beats: List[BeatMarker] = []
```

### 3. Registry System

Extensible system for animations and transitions.

```python
class Registry:
    """Base registry class"""
    
    def __init__(self):
        self._registry: Dict[str, Callable] = {}
    
    def register(self, name: str):
        """Decorator for registering functions"""
        def decorator(func: Callable) -> Callable:
            self._registry[name] = func
            return func
        return decorator
    
    def get(self, name: str) -> Callable:
        """Get function by name"""
        if name not in self._registry:
            raise ValueError(f"Unknown {self.__class__.__name__}: {name}")
        return self._registry[name]

class AnimationRegistry(Registry):
    """Registry for animation effects"""
    
    def apply(self, clip: VideoClip, name: str, **params) -> VideoClip:
        """Apply animation to clip"""
        animation_fn = self.get(name)
        return animation_fn(clip, **params)

class TransitionRegistry(Registry):
    """Registry for transition effects"""
    
    def apply(self, clip_a: VideoClip, clip_b: VideoClip, name: str, **params) -> VideoClip:
        """Apply transition between clips"""
        transition_fn = self.get(name)
        return transition_fn(clip_a, clip_b, **params)
```

### 4. Enhanced Defaults Management

Hierarchical defaults system with intelligent warnings and strict validation.

```python
class DefaultsManager:
    """Manages global and timeline defaults with intelligent fallbacks"""
    
    def __init__(self, strict_mode=True, verbose=True):
        self._global_defaults: Dict[str, Any] = {}
        self._timeline_defaults: Dict[str, Any] = {}
        self.strict_mode = strict_mode
        self.verbose = verbose
    
    def set_global_defaults(self, **kwargs) -> None:
        """Set application-wide defaults"""
        self._global_defaults.update(kwargs)
    
    def set_timeline_defaults(self, **kwargs) -> None:
        """Set timeline-specific defaults"""
        self._timeline_defaults.update(kwargs)
    
    def get(self, key: str, block_override: Optional[Any] = None) -> Any:
        """Get value with hierarchy: block > timeline > global > fallback"""
        if block_override is not None:
            return block_override
            
        if key in self._timeline_defaults:
            if self.verbose:
                warnings.warn(f"Using timeline default {key}: {self._timeline_defaults[key]}")
            return self._timeline_defaults[key]
            
        if key in self._global_defaults:
            if self.verbose:
                warnings.warn(f"Using global default {key}: {self._global_defaults[key]}")
            return self._global_defaults[key]
            
        # Final fallback
        fallback_value = FALLBACK_VALUES.get(key)
        if self.strict_mode:
            raise VineConfigError(f"Required value '{key}' not specified and no fallback available")
        elif self.verbose:
            warnings.warn(f"Using fallback {key}: {fallback_value}")
        return fallback_value
    
    def get_all_defaults(self) -> Dict[str, Any]:
        """Show all current default values with hierarchy"""
        return {
            **FALLBACK_VALUES,
            **self._global_defaults,
            **self._timeline_defaults
        }
```

---

## 🔄 Data Flow

### 1. Timeline Construction Flow

```
User Input → TimelineBuilder → Block Creation → Registry Lookup → Rendering
     ↓              ↓              ↓              ↓              ↓
  JSON/YAML    Fluent API    VoiceImageBlock  Animation     MoviePy
  or Python    Methods       SceneBlock        Transition    Clips
               Chain         BeatTrack         Effects
```

### 2. Rendering Pipeline

```
Timeline Blocks → Flatten → Apply Effects → Mix Audio → Export
      ↓            ↓           ↓           ↓         ↓
   VoiceImage   Sequential  Ken Burns   Voice +    MP4
   SceneBlock   Timeline    Transitions Music      File
   BeatTrack    Array       Subtitles   Ducking
```

### 3. Enhanced Default Resolution Flow

```
Block Request → Timeline Defaults → Global Defaults → Fallback Value
     ↓              ↓                  ↓              ↓
  with_animation  .with_defaults()  set_global_     "static"
  ("ken_burns")   (animation="fade") defaults()     animation
     ↓              ↓                  ↓              ↓
  Explicit       Warning:           Warning:        Error/fallback
  Override       "Using timeline"   "Using global"  based on mode
```

---

## 🗂️ File Structure

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
│       ├── defaults.py                # Enhanced defaults management
│       ├── api.py                     # High-level API exports
│       └── exceptions.py              # Custom exceptions
├── tests/                     # Test suite
│   ├── unit/
│   │   ├── test_models.py          # Pydantic model tests
│   │   ├── test_registry.py        # Registry system tests
│   │   ├── test_defaults.py        # Enhanced defaults tests
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

## 🔧 Technical Design Decisions

### 1. Enhanced Fluent API Design

**Decision**: Use method chaining with intelligent defaults and warnings
**Rationale**: 
- More readable than nested function calls
- Natural progression from setup to execution
- Clear feedback about what's happening
- Flexible for different use cases

```python
# Good: Enhanced Fluent API with warnings
timeline = (
    TimelineBuilder()  # verbose=True, strict_mode=True by default
    .with_defaults(animation="ken_burns")
    .add_voice_image_pair("voice.mp3", "image.jpg")
        .with_animation("slide_in")  # Explicit override
        .with_subtitle("Hello")      # Explicit subtitle
    .export("output.mp4")
)
# Shows helpful warnings about fallbacks when needed

# Bad: Silent behavior
timeline = TimelineBuilder()
timeline.add_voice_image_pair("voice.mp3", "image.jpg")
# User doesn't know what animation/transition is being used
```

### 2. Registry Pattern with Validation

**Decision**: Use registry pattern with enhanced validation
**Rationale**:
- Extensible without modifying core code
- Clear error messages for missing effects
- Testable in isolation
- Supports both strict and relaxed modes

### 3. Pydantic for Data Validation

**Decision**: Use Pydantic for all data models with enhanced error messages
**Rationale**:
- Built-in validation and error handling
- JSON serialization/deserialization
- Type hints for better IDE support
- Schema generation for AI agents
- Clear error messages for debugging

### 4. Intelligent Defaults with Warnings

**Decision**: Three-level default system with configurable behavior
**Rationale**:
- Flexible configuration for different use cases
- Clear feedback about what's happening
- Debugging support when needed
- Production-ready with silent fallbacks

---

## 🎨 Animation System Design

### Animation Pipeline with Validation

```python
def apply_animation(clip: VideoClip, spec: AnimationSpec) -> VideoClip:
    """Apply animation to a video clip with validation"""
    
    # Validate animation spec
    if not spec:
        if strict_mode:
            raise VineConfigError("Animation specification required")
        elif verbose:
            warnings.warn("No animation specified, using static")
        return clip
    
    # Get animation function from registry
    try:
        animation_fn = ANIMATION_REGISTRY.get(spec.type)
    except ValueError as e:
        if strict_mode:
            raise VineConfigError(f"Invalid animation type: {spec.type}")
        elif verbose:
            warnings.warn(f"Unknown animation '{spec.type}', using static")
        return clip
    
    # Apply animation with parameters
    animated_clip = animation_fn(clip, **spec.dict(exclude={'type'}))
    
    return animated_clip
```

### Built-in Animations

```python
@register_animation("ken_burns")
def ken_burns_fx(clip: VideoClip, zoom: str = "in", speed: str = "slow") -> VideoClip:
    """Ken Burns effect with zoom and speed control"""
    
    # Validate parameters
    if zoom not in ["in", "out"]:
        raise ValueError(f"Invalid zoom direction: {zoom}")
    if speed not in ["slow", "medium", "fast"]:
        raise ValueError(f"Invalid speed: {speed}")
    
    # Calculate zoom parameters based on speed
    zoom_factor = {"slow": 1.1, "medium": 1.2, "fast": 1.3}[speed]
    
    # Apply zoom effect
    if zoom == "in":
        return clip.resize(zoom_factor)
    else:
        return clip.resize(1/zoom_factor)

@register_animation("slide_in")
def slide_in_fx(clip: VideoClip, direction: str = "left") -> VideoClip:
    """Slide in from specified direction"""
    
    # Validate direction
    valid_directions = ["left", "right", "up", "down"]
    if direction not in valid_directions:
        raise ValueError(f"Invalid direction: {direction}. Must be one of {valid_directions}")
    
    # Calculate slide parameters
    slide_params = {
        "left": {"x_start": -clip.w, "x_end": 0},
        "right": {"x_start": clip.w, "x_end": 0},
        "up": {"y_start": -clip.h, "y_end": 0},
        "down": {"y_start": clip.h, "y_end": 0}
    }[direction]
    
    # Apply slide effect
    return clip.set_position((slide_params["x_start"], slide_params["y_start"]))
```

---

## 🔄 Transition System Design

### Transition Pipeline with Validation

```python
def apply_transition(clip_a: VideoClip, clip_b: VideoClip, spec: TransitionSpec) -> VideoClip:
    """Apply transition between two clips with validation"""
    
    # Validate transition spec
    if not spec:
        if strict_mode:
            raise VineConfigError("Transition specification required")
        elif verbose:
            warnings.warn("No transition specified, using fade")
        return clip_b
    
    # Get transition function from registry
    try:
        transition_fn = TRANSITION_REGISTRY.get(spec.type)
    except ValueError as e:
        if strict_mode:
            raise VineConfigError(f"Invalid transition type: {spec.type}")
        elif verbose:
            warnings.warn(f"Unknown transition '{spec.type}', using fade")
        return clip_b
    
    # Apply transition with parameters
    transitioned_clip = transition_fn(clip_a, clip_b, **spec.dict(exclude={'type'}))
    
    return transitioned_clip
```

### Built-in Transitions

```python
@register_transition("fade")
def fade_transition(clip_a: VideoClip, clip_b: VideoClip, duration: float = 1.0) -> VideoClip:
    """Fade transition between clips"""
    
    # Validate duration
    if duration < 0:
        raise ValueError("Duration must be positive")
    
    # Create fade out for clip_a
    fade_out = clip_a.fadeout(duration)
    
    # Create fade in for clip_b
    fade_in = clip_b.fadein(duration)
    
    # Overlay during transition period
    return CompositeVideoClip([fade_out, fade_in])

@register_transition("crossfade")
def crossfade_transition(clip_a: VideoClip, clip_b: VideoClip, duration: float = 0.5) -> VideoClip:
    """Crossfade transition between clips"""
    
    # Validate duration
    if duration < 0:
        raise ValueError("Duration must be positive")
    
    # Simple crossfade using MoviePy's crossfadein
    return clip_b.crossfadein(duration)
```

---

## 🔊 Audio System Design

### Audio Pipeline with Validation

```python
class AudioProcessor:
    """Handles audio mixing and processing with validation"""
    
    def __init__(self, strict_mode=True, verbose=True):
        self.voice_tracks: List[AudioFileClip] = []
        self.music_track: Optional[AudioFileClip] = None
        self.global_voiceover: Optional[AudioFileClip] = None
        self.strict_mode = strict_mode
        self.verbose = verbose
    
    def add_voice(self, voice_path: str, start_time: float) -> None:
        """Add voice track at specific time with validation"""
        
        # Validate file exists
        if not os.path.exists(voice_path):
            if self.strict_mode:
                raise VineConfigError(f"Voice file not found: {voice_path}")
            elif self.verbose:
                warnings.warn(f"Voice file not found: {voice_path}")
            return
        
        # Validate start time
        if start_time < 0:
            raise ValueError("Start time must be non-negative")
        
        voice_clip = AudioFileClip(voice_path)
        voice_clip = voice_clip.set_start(start_time)
        self.voice_tracks.append(voice_clip)
    
    def set_music(self, music_path: str, duck_under_voice: bool = True) -> None:
        """Set background music track with validation"""
        
        # Validate file exists
        if not os.path.exists(music_path):
            if self.strict_mode:
                raise VineConfigError(f"Music file not found: {music_path}")
            elif self.verbose:
                warnings.warn(f"Music file not found: {music_path}")
            return
        
        self.music_track = AudioFileClip(music_path)
        if duck_under_voice:
            self.music_track = self.apply_ducking(self.music_track)
    
    def mix_audio(self) -> AudioFileClip:
        """Mix all audio tracks together with validation"""
        
        if not self.voice_tracks and not self.music_track:
            if self.strict_mode:
                raise VineConfigError("No audio tracks specified")
            elif self.verbose:
                warnings.warn("No audio tracks specified")
            return None
        
        # Combine voice tracks
        if self.voice_tracks:
            voice_mix = CompositeAudioClip(self.voice_tracks)
        else:
            voice_mix = None
        
        # Add music if present
        if self.music_track:
            if voice_mix:
                final_audio = CompositeAudioClip([voice_mix, self.music_track])
            else:
                final_audio = self.music_track
        else:
            final_audio = voice_mix
        
        return final_audio
```

---

## 🧪 Testing Architecture

### Test Structure with Enhanced Coverage

```
tests/
├── unit/
│   ├── test_models.py          # Pydantic model tests
│   ├── test_registry.py        # Registry system tests
│   ├── test_defaults.py        # Enhanced defaults tests
│   ├── test_builder.py         # TimelineBuilder tests
│   └── test_validation.py      # Validation and error handling
├── integration/
│   ├── test_rendering.py       # End-to-end rendering tests
│   ├── test_parsing.py         # JSON/YAML parsing tests
│   ├── test_audio.py           # Audio processing tests
│   └── test_warnings.py        # Warning and fallback tests
├── fixtures/
│   ├── sample_audio/           # Test audio files
│   ├── sample_images/          # Test image files
│   └── sample_configs/         # Test YAML/JSON configs
└── conftest.py                 # Pytest configuration
```

### Mock Strategy with Enhanced Validation

```python
class MockMoviePy:
    """Mock MoviePy for testing without actual video processing"""
    
    def __init__(self):
        self.clips_created = []
        self.export_calls = []
        self.warnings_issued = []
    
    def VideoFileClip(self, path: str):
        # Validate path
        if not path or not path.strip():
            raise ValueError("Invalid video file path")
        
        clip = MockVideoClip(path)
        self.clips_created.append(clip)
        return clip
    
    def ImageClip(self, path: str):
        # Validate path
        if not path or not path.strip():
            raise ValueError("Invalid image file path")
        
        clip = MockImageClip(path)
        self.clips_created.append(clip)
        return clip
    
    def AudioFileClip(self, path: str):
        # Validate path
        if not path or not path.strip():
            raise ValueError("Invalid audio file path")
        
        clip = MockAudioClip(path)
        self.clips_created.append(clip)
        return clip
    
    def warn(self, message: str):
        """Track warnings for testing"""
        self.warnings_issued.append(message)
```

---

## 🚀 Performance Considerations

### 1. Memory Management with Validation

- **Clip Caching**: Cache processed clips to avoid reprocessing
- **Garbage Collection**: Explicit cleanup of MoviePy objects
- **Streaming**: Process large videos in chunks
- **Validation Overhead**: Minimize validation cost in production

### 2. Rendering Optimization

- **Parallel Processing**: Render multiple blocks concurrently
- **Lazy Loading**: Load assets only when needed
- **Preview Mode**: Fast preview with lower quality
- **Warning Suppression**: Disable warnings in production for performance

### 3. Audio Processing

- **Audio Ducking**: Efficient volume reduction during voice
- **Format Optimization**: Use efficient audio formats
- **Caching**: Cache processed audio tracks
- **Validation**: Validate audio files early to avoid processing errors

---

## 🔒 Enhanced Error Handling Strategy

### 1. Validation Errors with Context

```python
class VineValidationError(Exception):
    """Raised when input validation fails"""
    def __init__(self, message: str, context: Optional[Dict] = None):
        self.message = message
        self.context = context or {}
        super().__init__(self.message)

class VineConfigError(Exception):
    """Raised when configuration is invalid"""
    def __init__(self, message: str, suggestion: Optional[str] = None):
        self.message = message
        self.suggestion = suggestion
        super().__init__(self.message)

class VineRenderError(Exception):
    """Raised when rendering fails"""
    def __init__(self, message: str, clip_info: Optional[Dict] = None):
        self.message = message
        self.clip_info = clip_info or {}
        super().__init__(self.message)
```

### 2. Graceful Degradation with Feedback

- **Missing Assets**: Use placeholder images/audio with warnings
- **Invalid Effects**: Fall back to default effects with clear messages
- **Render Failures**: Provide detailed error messages with suggestions
- **Validation Errors**: Show helpful context and suggestions

### 3. Recovery Mechanisms with Logging

- **Partial Rendering**: Render what's possible with progress reporting
- **Error Reporting**: Detailed error logs with context
- **Retry Logic**: Automatic retry for transient failures
- **Warning Aggregation**: Collect warnings for summary reporting

---

This enhanced architecture design provides a solid foundation for building Project Vine, ensuring scalability, maintainability, and extensibility while maintaining high performance and reliability with intelligent defaults and clear feedback. 