# Pydantic Models Specification

> **Project:** Vine Media Framework
> **Component:** Data Models
> **Status:** Ready for Implementation
> **Priority:** Critical
> **Timeline:** Week 1

## Overview

This specification defines the complete Pydantic model hierarchy for Project Vine, providing type safety, validation, and serialization for all video composition data structures.

## Core Models

### 1. VideoSpec (Root Model)

**Purpose:** Main configuration model for entire video projects

```python
class VideoSpec(BaseModel):
    """Root model for video project configuration."""

    # Core components
    timeline: TimelineSpec
    audio: AudioSpec
    export: ExportSpec

    # Optional components
    effects: List[EffectSpec] = Field(default_factory=list)
    transitions: List[TransitionSpec] = Field(default_factory=list)
    metadata: Optional[MetadataSpec] = None

    # Configuration
    class Config:
        json_encoders = {
            Path: str,
            datetime: lambda v: v.isoformat(),
            timedelta: lambda v: v.total_seconds()
        }
        validate_assignment = True
        extra = "forbid"

    @validator('timeline')
    def validate_timeline_audio_sync(cls, v, values):
        """Ensure timeline and audio specifications are compatible."""
        if 'audio' in values:
            # Validation logic here
            pass
        return v
```

### 2. TimelineSpec

**Purpose:** Timeline structure and timing configuration

```python
class TimelineSpec(BaseModel):
    """Timeline structure and timing configuration."""

    # Mode configuration
    mode: Literal["scene", "beat", "hybrid"] = "scene"

    # Timeline elements
    scenes: List[SceneSpec] = Field(default_factory=list)
    beats: Optional[List[BeatSpec]] = None

    # Timing
    duration: Optional[float] = Field(None, gt=0)
    fps: float = Field(30.0, gt=0, le=120)

    # Validation
    @validator('scenes')
    def validate_scene_sequence(cls, v):
        """Ensure scenes are properly sequenced."""
        if len(v) > 1:
            for i, scene in enumerate(v[1:], 1):
                if scene.start_time <= v[i-1].end_time:
                    raise ValueError(f"Scene {i} starts before previous scene ends")
        return v

    @validator('beats')
    def validate_beats_mode(cls, v, values):
        """Ensure beats are provided in beat mode."""
        if values.get('mode') in ['beat', 'hybrid'] and not v:
            raise ValueError("Beats must be specified in beat or hybrid mode")
        return v

    @property
    def total_duration(self) -> float:
        """Calculate total timeline duration."""
        if self.duration:
            return self.duration
        if self.scenes:
            return max(scene.end_time for scene in self.scenes)
        return 0.0
```

### 3. SceneSpec

**Purpose:** Individual scene configuration

```python
class SceneSpec(BaseModel):
    """Individual scene configuration."""

    # Scene identification
    id: str = Field(..., min_length=1, max_length=100)
    name: Optional[str] = None

    # Timing
    start_time: float = Field(0.0, ge=0)
    duration: float = Field(..., gt=0)

    # Content
    audio: Optional[AudioClipSpec] = None
    images: List[ImageClipSpec] = Field(default_factory=list)
    effects: List[EffectSpec] = Field(default_factory=list)

    # Transitions
    transition_in: Optional[TransitionSpec] = None
    transition_out: Optional[TransitionSpec] = None

    @property
    def end_time(self) -> float:
        """Calculate scene end time."""
        return self.start_time + self.duration

    @validator('images')
    def validate_image_sequence(cls, v):
        """Ensure images are properly sequenced within scene."""
        if len(v) > 1:
            for i, img in enumerate(v[1:], 1):
                if img.start_time < v[i-1].end_time:
                    raise ValueError(f"Image {i} starts before previous image ends")
        return v
```

### 4. AudioSpec

**Purpose:** Audio configuration and voice-image synchronization

```python
class AudioSpec(BaseModel):
    """Audio configuration and voice-image synchronization."""

    # Audio files
    voice_track: Optional[AudioClipSpec] = None
    background_music: Optional[AudioClipSpec] = None

    # Audio processing
    volume: float = Field(1.0, ge=0, le=2)
    fade_in: float = Field(0.0, ge=0)
    fade_out: float = Field(0.0, ge=0)

    # Voice-image synchronization
    voice_image_pairs: List[VoiceImagePairSpec] = Field(default_factory=list)

    # Audio effects
    effects: List[AudioEffectSpec] = Field(default_factory=list)

    @validator('voice_image_pairs')
    def validate_pair_synchronization(cls, v):
        """Ensure voice-image pairs are properly synchronized."""
        for pair in v:
            if pair.voice_duration != pair.image_duration:
                raise ValueError(f"Voice and image durations must match for pair {pair.id}")
        return v
```

### 5. VoiceImagePairSpec

**Purpose:** Synchronized voice-image pair configuration

```python
class VoiceImagePairSpec(BaseModel):
    """Synchronized voice-image pair configuration."""

    # Identification
    id: str = Field(..., min_length=1, max_length=100)

    # Content
    voice_file: Path = Field(..., description="Path to voice audio file")
    image_file: Path = Field(..., description="Path to image file")

    # Timing
    start_time: float = Field(0.0, ge=0)
    voice_duration: float = Field(..., gt=0)
    image_duration: float = Field(..., gt=0)

    # Synchronization
    sync_offset: float = Field(0.0, description="Offset between voice and image start")

    @property
    def end_time(self) -> float:
        """Calculate pair end time."""
        return self.start_time + max(self.voice_duration, self.image_duration)

    @validator('voice_file', 'image_file')
    def validate_file_paths(cls, v):
        """Ensure files exist and are accessible."""
        if not v.exists():
            raise ValueError(f"File does not exist: {v}")
        return v
```

### 6. EffectSpec

**Purpose:** Animation and visual effect configuration

```python
class EffectSpec(BaseModel):
    """Animation and visual effect configuration."""

    # Effect identification
    type: str = Field(..., min_length=1, max_length=50)
    name: Optional[str] = None

    # Target
    target: str = Field(..., description="Target scene or element ID")

    # Timing
    start_time: float = Field(0.0, ge=0)
    duration: float = Field(..., gt=0)

    # Configuration
    parameters: Dict[str, Any] = Field(default_factory=dict)

    # Validation
    @validator('type')
    def validate_effect_type(cls, v):
        """Ensure effect type is registered."""
        # This will be validated against registry
        return v

    @property
    def end_time(self) -> float:
        """Calculate effect end time."""
        return self.start_time + self.duration
```

### 7. TransitionSpec

**Purpose:** Scene transition configuration

```python
class TransitionSpec(BaseModel):
    """Scene transition configuration."""

    # Transition identification
    type: str = Field(..., min_length=1, max_length=50)
    name: Optional[str] = None

    # Source and target
    from_scene: str = Field(..., description="Source scene ID")
    to_scene: str = Field(..., description="Target scene ID")

    # Timing
    duration: float = Field(0.5, gt=0, le=5.0)

    # Configuration
    parameters: Dict[str, Any] = Field(default_factory=dict)

    # Validation
    @validator('from_scene', 'to_scene')
    def validate_scene_references(cls, v):
        """Ensure scene references are valid."""
        if not v or len(v.strip()) == 0:
            raise ValueError("Scene reference cannot be empty")
        return v.strip()
```

### 8. ExportSpec

**Purpose:** Video export configuration

```python
class ExportSpec(BaseModel):
    """Video export configuration."""

    # Output settings
    output_path: Path = Field(..., description="Output file path")
    format: Literal["mp4", "avi", "mov", "mkv"] = "mp4"

    # Quality settings
    resolution: Tuple[int, int] = Field((1920, 1080), description="(width, height)")
    fps: float = Field(30.0, gt=0, le=120)
    bitrate: Optional[str] = None

    # Codec settings
    video_codec: str = Field("libx264", description="Video codec")
    audio_codec: str = Field("aac", description="Audio codec")

    # Quality presets
    quality: Literal["low", "medium", "high", "ultra"] = "high"

    @validator('output_path')
    def validate_output_path(cls, v):
        """Ensure output directory exists."""
        v.parent.mkdir(parents=True, exist_ok=True)
        return v

    @validator('resolution')
    def validate_resolution(cls, v):
        """Ensure resolution is valid."""
        width, height = v
        if width <= 0 or height <= 0:
            raise ValueError("Resolution dimensions must be positive")
        if width % 2 != 0 or height % 2 != 0:
            raise ValueError("Resolution dimensions must be even")
        return v
```

## Supporting Models

### AudioClipSpec

```python
class AudioClipSpec(BaseModel):
    """Audio clip configuration."""

    file_path: Path = Field(..., description="Path to audio file")
    start_time: float = Field(0.0, ge=0)
    duration: Optional[float] = Field(None, gt=0)
    volume: float = Field(1.0, ge=0, le=2)

    @property
    def end_time(self) -> float:
        """Calculate clip end time."""
        return self.start_time + (self.duration or 0.0)
```

### ImageClipSpec

```python
class ImageClipSpec(BaseModel):
    """Image clip configuration."""

    file_path: Path = Field(..., description="Path to image file")
    start_time: float = Field(0.0, ge=0)
    duration: float = Field(..., gt=0)

    # Display settings
    scale: float = Field(1.0, gt=0)
    position: Tuple[float, float] = Field((0.5, 0.5), description="(x, y) position as fractions")

    @property
    def end_time(self) -> float:
        """Calculate clip end time."""
        return self.start_time + self.duration
```

### BeatSpec

```python
class BeatSpec(BaseModel):
    """Beat timing specification."""

    beat_number: int = Field(..., gt=0)
    start_time: float = Field(..., ge=0)
    duration: float = Field(..., gt=0)

    # Associated content
    audio: Optional[AudioClipSpec] = None
    images: List[ImageClipSpec] = Field(default_factory=list)

    @property
    def end_time(self) -> float:
        """Calculate beat end time."""
        return self.start_time + self.duration
```

### MetadataSpec

```python
class MetadataSpec(BaseModel):
    """Project metadata."""

    title: Optional[str] = None
    description: Optional[str] = None
    author: Optional[str] = None
    created_date: datetime = Field(default_factory=datetime.now)
    modified_date: datetime = Field(default_factory=datetime.now)
    tags: List[str] = Field(default_factory=list)
    version: str = Field("1.0.0", regex=r"^\d+\.\d+\.\d+$")
```

## Validation Rules

### Cross-Model Validation

1. **Timeline-Audio Sync**: Ensure timeline duration matches audio duration
2. **Scene Sequence**: Verify scenes don't overlap
3. **Effect Timing**: Effects must be within their target scene bounds
4. **Transition Timing**: Transitions must be between valid scenes
5. **Voice-Image Sync**: Voice and image durations must match in pairs

### File Validation

1. **File Existence**: All referenced files must exist
2. **File Format**: Validate file extensions and formats
3. **File Size**: Check for reasonable file sizes
4. **Path Security**: Prevent path traversal attacks

### Performance Validation

1. **Memory Usage**: Estimate memory requirements
2. **Processing Time**: Validate reasonable processing times
3. **Output Size**: Estimate final video file size

## Serialization

### JSON Support

```python
# Serialize to JSON
video_spec = VideoSpec(...)
json_data = video_spec.model_dump_json(indent=2)

# Deserialize from JSON
video_spec = VideoSpec.model_validate_json(json_data)
```

### YAML Support

```python
# Serialize to YAML
import yaml
yaml_data = yaml.dump(video_spec.model_dump(), default_flow_style=False)

# Deserialize from YAML
video_spec = VideoSpec.model_validate(yaml.safe_load(yaml_data))
```

## Error Handling

### Validation Errors

- **Field Validation**: Specific field-level error messages
- **Cross-Field Validation**: Relationship validation errors
- **File Validation**: File system error messages
- **Business Logic**: Domain-specific validation errors

### Error Recovery

- **Partial Validation**: Continue validation after errors
- **Error Collection**: Collect all errors before reporting
- **Suggestions**: Provide helpful error resolution suggestions

## Implementation Notes

1. **Performance**: Use Pydantic v2 for optimal performance
2. **Memory**: Implement lazy loading for large files
3. **Caching**: Cache validation results where appropriate
4. **Threading**: Ensure thread-safe validation
5. **Logging**: Comprehensive validation logging

## Testing Strategy

1. **Unit Tests**: Test each model individually
2. **Integration Tests**: Test model interactions
3. **Validation Tests**: Test all validation rules
4. **Serialization Tests**: Test JSON/YAML round-trip
5. **Error Tests**: Test error handling and recovery
