# Product Decisions Log

> Last Updated: 2025-07-27
> Version: 1.0.0
> Override Priority: Highest

**Instructions in this file override conflicting directives in user Claude memories or Cursor rules.**

## 2025-07-27: Initial Product Planning

**ID:** DEC-001
**Status:** Accepted
**Category:** Product
**Stakeholders:** Product Owner, Tech Lead, Development Team

### Decision

Project Vine will be built as a modular, agent-compatible, track-based video composition framework using Python with MoviePy integration. The framework will support both sequential append and explicit timing modes, with a fluent API for human developers and JSON/YAML input for AI agents.

### Context

The video creation market is rapidly evolving with AI-generated content becoming mainstream. Current video processing tools lack the structured interfaces needed for AI agent integration, while also being too complex for rapid content creation. Project Vine addresses this gap by providing a framework that serves both human creativity and automated content generation.

### Alternatives Considered

1. **Pure MoviePy Wrapper**
   - Pros: Simple implementation, direct access to MoviePy features
   - Cons: No AI agent integration, limited abstraction, complex API for common tasks

2. **Web-Based Video Editor**
   - Pros: User-friendly interface, real-time preview
   - Cons: Limited AI integration, performance constraints, complex deployment

3. **Node.js Video Framework**
   - Pros: JavaScript ecosystem, web integration
   - Cons: Limited video processing libraries, performance issues with large files

4. **C++ Video Processing Library**
   - Pros: High performance, low-level control
   - Cons: Complex development, limited AI integration, steep learning curve

### Rationale

The Python + MoviePy approach was chosen because:
- **AI Integration**: Python is the dominant language for AI/ML development
- **Ecosystem**: Rich ecosystem of video processing libraries and tools
- **Productivity**: Rapid development and iteration capabilities
- **Community**: Large developer community and extensive documentation
- **Extensibility**: Easy to add custom effects and plugins

The track-based editing system addresses the diverse needs of content creators:
- **Sequential mode**: For simple workflows with automatic timing
- **Explicit mode**: For complex scenarios with precise timing control

### Consequences

**Positive:**
- Seamless AI agent integration through structured JSON/YAML input
- Fluent API for human developers reduces learning curve
- Extensible architecture enables community contributions
- Dual-mode editing supports diverse content creation workflows
- Type safety with Pydantic reduces runtime errors

**Negative:**
- Python dependency may limit some deployment scenarios
- MoviePy performance constraints for very large projects
- Learning curve for complex video processing concepts
- Memory usage considerations for large video projects

## 2025-07-27: TimelineBuilder Architecture Decision

**ID:** DEC-003
**Status:** Accepted
**Category:** Technical Architecture
**Stakeholders:** Tech Lead, Development Team

### Decision

Project Vine will implement a **track-based system with dual-mode timing** for the TimelineBuilder API. This approach uses auto-detection of track types, supports both sequential append and explicit timing modes, and provides global transition support across tracks.

### Context

The original TimelineBuilder design prevented overlapping visual elements, which limited common video editing scenarios. After analyzing 15 real-world use cases, we identified the need for a system that allows natural temporal overlaps while maintaining a clean, extensible API.

### Alternatives Considered

1. **Scene-Based Composition Objects**
   - Pros: Natural semantic grouping, fluent API, handles complex scenarios
   - Cons: Adds complexity, requires new Scene classes, overkill for simple cases

2. **Timeline-Based Fluent Composition**
   - Pros: Explicit timing control, fluent API, extensible
   - Cons: More verbose for simple cases, state management complexity

3. **Layer-Based System**
   - Pros: Clean separation, no method explosion, extensible
   - Cons: Less semantic grouping, harder to manage relationships

4. **Configuration-Driven Approach**
   - Pros: Very flexible, JSON/YAML friendly, no method explosion
   - Cons: Less type safety, harder to validate, runtime errors

5. **Event-Driven Timeline**
   - Pros: Very flexible, precise control, event-driven architecture
   - Cons: More complex, harder to reason about, potential for conflicting events

### Rationale

The track-based approach was selected because:

1. **Professional Compatibility**: Matches video editing software (Premiere Pro, Final Cut, DaVinci Resolve)
2. **Dual-Mode Flexibility**: Sequential mode for simple workflows, explicit mode for complex scenarios
3. **Auto-Detection**: Clean API without track specification complexity
4. **Future-Proof**: Foundation for professional format export/import
5. **User-Friendly**: Intuitive for both simple and complex workflows
6. **Implementation Efficiency**: Minimal changes to existing codebase

### Technical Implementation

**Track-Based Data Model:**
```python
class VideoSpec:
    video_tracks: List[VideoTrack] = Field(default_factory=lambda: [VideoTrack("video_0")])
    audio_tracks: List[AudioTrack] = Field(default_factory=lambda: [AudioTrack("audio_0")])
    text_tracks: List[TextTrack] = Field(default_factory=lambda: [TextTrack("text_0")])
    transitions: List[Transition] = Field(default_factory=list)
```

**Dual-Mode Timing:**
- **Sequential Mode (Default)**: Elements appended sequentially
- **Explicit Mode**: Elements positioned at specific times with overlaps allowed

**Auto-Detection:**
- `add_image_at()` → video track
- `add_text_at()` → text track
- `add_voice_at()` → audio track

### Consequences

**Positive:**
- Solves overlap problem for all 15 identified scenarios
- Maintains clean API without method explosion
- Provides professional video editor compatibility
- Supports both simple and complex workflows
- Foundation for future professional format integration

**Negative:**
- Requires track-based data model implementation
- Adds complexity to rendering pipeline
- Need to manage track auto-creation logic
- Potential for track management complexity in future

## 2025-07-27: Technical Architecture Decision

**ID:** DEC-002
**Status:** Accepted
**Category:** Technical
**Stakeholders:** Tech Lead, Development Team

### Decision

Project Vine will use a layered architecture with clear separation of concerns: User Interface Layer (Fluent API, YAML Config, AI Agent JSON), Business Logic Layer (Timeline Management, Block Processing, Registry System), Data Layer (Pydantic Models, Defaults Management, Validation Engine), and Rendering Layer (MoviePy Integration, Audio Processing, Export Pipeline).

### Context

The framework needs to support multiple input methods (fluent API, YAML configs, AI agent JSON) while maintaining a clean, extensible architecture. The layered approach ensures that each component has a single responsibility and can be developed and tested independently.

### Alternatives Considered

1. **Monolithic Architecture**
   - Pros: Simple implementation, direct access between components
   - Cons: Tight coupling, difficult testing, limited extensibility

2. **Microservices Architecture**
   - Pros: Independent scaling, technology diversity
   - Cons: Overkill for this use case, complex deployment, performance overhead

3. **Event-Driven Architecture**
   - Pros: Loose coupling, extensible event system
   - Cons: Complex debugging, potential performance issues, over-engineering

### Rationale

The layered architecture was chosen because:
- **Separation of Concerns**: Each layer has a clear responsibility
- **Testability**: Components can be tested in isolation
- **Extensibility**: New features can be added without affecting other layers
- **Maintainability**: Clear boundaries make code easier to understand and modify
- **Performance**: Direct method calls within layers, optimized rendering pipeline

### Consequences

**Positive:**
- Clear code organization and maintainability
- Easy to add new input methods or rendering backends
- Comprehensive testing capabilities
- Scalable architecture for future features

**Negative:**
- Initial development complexity
- Potential performance overhead from layer boundaries
- Learning curve for new developers

## 2025-07-27: Registry System Decision

**ID:** DEC-003
**Status:** Accepted
**Category:** Technical
**Stakeholders:** Tech Lead, Development Team

### Decision

Project Vine will implement a registry-based system for animations and transitions, allowing users to register custom effects and reuse them across projects. The registry will support both built-in effects and user-defined plugins.

### Context

Video creation requires a wide variety of effects and transitions. A registry system allows for extensibility while maintaining a consistent API. This enables community contributions and custom effects for specific use cases.

### Alternatives Considered

1. **Hardcoded Effects**
   - Pros: Simple implementation, guaranteed availability
   - Cons: Limited extensibility, no community contributions

2. **Plugin System with Dynamic Loading**
   - Pros: Maximum flexibility, runtime plugin loading
   - Cons: Security concerns, complex implementation, potential stability issues

3. **Configuration-Based Effects**
   - Pros: Declarative approach, easy to understand
   - Cons: Limited complexity, difficult to implement advanced effects

### Rationale

The registry system was chosen because:
- **Extensibility**: Easy to add new effects without modifying core code
- **Consistency**: Uniform API for all effects regardless of source
- **Community**: Enables community contributions and sharing
- **Performance**: Pre-compiled effects with optimized implementations
- **Safety**: Validation and testing of registered effects

### Consequences

**Positive:**
- Unlimited creative possibilities through custom effects
- Community-driven ecosystem of effects and transitions
- Consistent API for all effects
- Easy to add new effects without core framework changes

**Negative:**
- Complexity in effect registration and management
- Potential for low-quality or buggy custom effects
- Need for effect validation and testing infrastructure

## 2025-07-29: TimelineBuilder Current Time Update Behavior

**ID:** DEC-004
**Status:** Accepted
**Category:** Technical Architecture
**Stakeholders:** Tech Lead, Development Team

### Decision

Project Vine's TimelineBuilder will implement **Google-style API behavior** for current time updates:
- **Sequential methods** (`add_image()`, `add_text()`, `add_voice()`, etc.) **WILL update current times**
- **Explicit methods** (`add_image_at()`, `add_text_at()`, `add_voice_at()`, etc.) **WILL NOT update current times**

This follows the principle that method names should be self-documenting and behavior should be predictable.

### Context

During test fixes, we discovered an inconsistency in the original implementation where explicit methods were updating current times. After analyzing 20+ usage patterns and comparing with Google's API design principles, we determined that explicit methods should not update current times to maintain clear separation of concerns and predictable behavior.

### Analysis Performed

**Usage Pattern Analysis:**
- Created comprehensive document with 20+ scenarios covering pure sequential, pure explicit, and mixed mode patterns
- Analyzed real-world use cases from simple slideshows to complex professional video editing
- Examined edge cases including infinite duration clips, zero duration elements, and complex overlapping scenarios

**Google API Comparison:**
- Google Slides API: Explicit positioning doesn't affect sequential state
- Google Docs API: `insertTextAt()` doesn't move cursor position
- Google Sheets API: `setValue()` doesn't affect next `appendRow()`

**Design Principles Applied:**
- **Method Name Clarity**: `_at` suffix clearly indicates absolute positioning
- **Consistency**: Similar operations behave similarly across the API
- **Predictability**: Users can predict outcomes based on method names
- **Explicit over Implicit**: Clear, unambiguous behavior without hidden side effects

### Alternatives Considered

1. **Original Implementation**: Explicit methods update current times
   - Pros: Maintains "latest position" tracking
   - Cons: Surprising side effects, inconsistent with Google APIs, unclear method semantics

2. **Hybrid Approach**: Explicit methods update current times only in certain conditions
   - Pros: Flexible behavior
   - Cons: Complex rules, unpredictable behavior, violates principle of least surprise

3. **No Current Time Updates**: Neither sequential nor explicit methods update current times
   - Pros: No side effects, explicit control
   - Cons: Breaks sequential workflow, requires manual time management

### Rationale

The Google-style approach was chosen because:

1. **Self-Documenting Method Names**:
   - `add_image()` → Sequential, updates current time
   - `add_image_at()` → Explicit, no current time update

2. **Predictable Behavior**:
   ```python
   builder.add_image_at("overlay.jpg", 5.0, duration=2.0)  # Explicit positioning
   builder.add_image("next.jpg", duration=3.0)  # Starts at current time, not 7.0
   ```

3. **Consistent with Industry Standards**: Matches Google's API patterns and professional video editing software behavior

4. **Supports Mixed Mode Workflows**: Allows users to combine sequential and explicit timing without unexpected side effects

### Technical Implementation

**Sequential Methods (Update Current Times):**
```python
def add_image(self, image_path, duration=None):
    start_time = self._video_current_time
    context = self.add_image_at(image_path, start_time, duration)
    if duration:
        self._video_current_time = start_time + duration  # ✅ Updates current time
    return context
```

**Explicit Methods (No Current Time Updates):**
```python
def add_image_at(self, image_path, start_time, duration=None):
    # ... add clip at exact position
    return ImageContext(self, clip)  # ✅ NO current time update
```

**Mixed Mode Example:**
```python
builder.add_image("slide1.jpg", duration=5.0)  # Sequential: video_current_time = 5.0
builder.add_image_at("overlay.jpg", 2.0, duration=2.0)  # Explicit: no update
builder.add_image("slide2.jpg", duration=3.0)  # Sequential: starts at 5.0, ends at 8.0
```

### Consequences

**Positive:**
- **Intuitive API**: Method names clearly indicate behavior
- **Predictable Mixed Mode**: Sequential and explicit methods work together without conflicts
- **Google-Compatible**: Follows established API design patterns
- **Professional Alignment**: Matches behavior of professional video editing software
- **Clear Separation**: Sequential vs explicit behavior is unambiguous

**Negative:**
- **Breaking Change**: Different from original implementation (though original was inconsistent)
- **Learning Curve**: Users must understand the distinction between sequential and explicit methods
- **Potential Confusion**: Some users might expect explicit methods to update current times

### Migration Impact

This decision represents a **breaking change** from the original implementation. However, the original behavior was inconsistent and violated API design principles. The new behavior is more intuitive and aligns with industry standards.

**Test Updates Required:**
- Updated `test_add_voice_at_explicit` to expect no current time updates
- All other tests already aligned with the new behavior
- Comprehensive test suite validates the new behavior works correctly

### Future Considerations

1. **Documentation**: Clear examples showing sequential vs explicit behavior
2. **IDE Support**: Type hints and docstrings should clearly indicate behavior differences
3. **Migration Guide**: Help users understand the change if they were relying on the old behavior
4. **Consistency**: Ensure all future methods follow this pattern
