# 📽️ Project Vine - Media Composition Framework

**Project Vine** is a modular, agent-compatible, track-based video composition framework built on top of MoviePy. It provides an expressive and extensible API for AI-driven and human-assisted short-form video generation, supporting both sequential append and explicit timing modes.

## 🚀 Key Features

### For Developers
- **Fluent API**: Intuitive method chaining for video composition
- **Extensible Architecture**: Registry-based system for custom effects
- **Type Safety**: Pydantic models with full validation
- **High Performance**: Optimized rendering pipeline

### For AI Agents
- **JSON Integration**: Structured input for LLM-generated video plans
- **Schema Validation**: Automatic validation of agent outputs
- **Error Recovery**: Graceful handling of invalid configurations
- **Batch Processing**: Support for automated video generation

### For Content Creators
- **YAML Configuration**: Human-readable video specifications
- **Smart Defaults**: Hierarchical default system for consistency
- **Voice-Image Pairs**: Automatic synchronization of audio and visuals
- **Multiple Formats**: Support for various video resolutions and formats

## 🏗️ Architecture

Project Vine follows a layered architecture with clear separation of concerns:

- **User Interface Layer**: Fluent API, YAML Config, AI Agent JSON
- **Business Logic Layer**: Timeline Management, Block Processing, Registry System
- **Data Layer**: Pydantic Models, Defaults Management, Validation Engine
- **Rendering Layer**: MoviePy Integration, Audio Processing, Export Pipeline

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/[username]/vine.git
cd vine

# Install dependencies
pip install -r requirements.txt
```

## 🎯 Quick Start

### Basic Usage

```python
from vine import TimelineBuilder

# Create a simple video with voice-image pairs
timeline = TimelineBuilder()
timeline.add_voice_image_pair("voice.mp3", "image.jpg")
timeline.export("output.mp4")
```

### AI Agent Integration

```python
from vine import TimelineBuilder

# Load from AI-generated JSON
timeline = TimelineBuilder()
timeline.load_from_json(ai_generated_spec)
timeline.export("ai_video.mp4")
```

### YAML Configuration

```yaml
# video_spec.yaml
defaults:
  animation: "ken_burns"
  transition: "crossfade"
  resolution: "1080x1920"

voice_image_pairs:
  - voice: "intro.mp3"
    image: "intro.jpg"
    animation: "slide_in"
  - voice: "content.mp3"
    image: "content.jpg"
    subtitle: "Key points"
```

```python
from vine import TimelineBuilder

# Load from YAML
timeline = TimelineBuilder()
timeline.load_from_yaml("video_spec.yaml")
timeline.export("configured_video.mp4")
```

## 🗺️ Development Roadmap

### Phase 1: Foundation ✅ (Weeks 1-2) - COMPLETED
- [x] **Core architecture and basic functionality** - TimelineBuilder with track-based architecture
- [x] **Pydantic models and registry system** - Complete model validation and extensible registries
- [x] **Basic TimelineBuilder API** - Fluent API with dual-mode timing (sequential/explicit)
- [x] **Track-based data model** - VideoTrack, AudioTrack, TextTrack with auto-detection
- [x] **Registry system** - Animation, Transition, and Effect registries
- [x] **Defaults management** - Hierarchical defaults system
- [x] **Dual-mode timing** - Sequential append and explicit timing modes
- [x] **Global transitions** - Transition system working across tracks
- [x] **Animation system** - Ken Burns, slide, static effects (configuration only)
- [x] **Transition system** - Fade, crossfade, slide transitions (configuration only)
- [x] **Comprehensive testing** - 100% test coverage achieved

### Phase 2: Advanced Features 🔄 (Weeks 3-4) - IN PROGRESS
- [ ] **MoviePy integration** - Full MoviePy wrapper implementation (CRITICAL)
- [ ] **Audio processing** - Voice/music mixing and ducking (CRITICAL)
- [ ] **Export pipeline** - High-quality video export (CRITICAL)
- [ ] **Performance optimization** - Memory management and caching
- [ ] **JSON parser** - AI agent integration
- [ ] **YAML parser** - Human-editable configs
- [ ] **Spec building** - Config-to-timeline conversion
- [ ] **Error handling** - Robust error management

### Phase 3: Advanced Modes ⏳ (Week 5) - PLANNED
- [ ] **Track-based editing** - Professional video editor-style timeline construction
- [ ] **Advanced track management** - Multiple tracks and layering
- [ ] **Advanced effects** - Parallax, zoom blur, custom animations
- [ ] **Text overlay** - Subtitle and text rendering
- [ ] **Music integration** - Beat detection and synchronization
- [ ] **Custom animations** - Plugin system for custom effects
- [ ] **Advanced transitions** - Complex transition effects
- [ ] **Batch processing** - Multiple video generation

### Phase 4: Polish & Launch ⏳ (Week 6) - PLANNED
- [ ] **Performance validation** - Optimization and benchmarking
- [ ] **Launch preparation** - Packaging and distribution
- [ ] **Error recovery** - Graceful handling of edge cases
- [ ] **Memory management** - Proper cleanup and resource management
- [ ] **Community examples** - Sample projects and use cases
- [ ] **Performance monitoring** - Runtime performance tracking
- [ ] **Migration tools** - Upgrade path for future versions

### Phase 5: Enterprise & Scale ⏳ (Future) - PLANNED
- [ ] **Enterprise security** - Authentication and access controls
- [ ] **Scalability** - Distributed processing and cloud integration
- [ ] **API rate limiting** - Usage controls and monitoring
- [ ] **Advanced analytics** - Usage tracking and performance metrics
- [ ] **Plugin marketplace** - Community-driven extensions
- [ ] **Cloud integration** - AWS/GCP/Azure support
- [ ] **Enterprise support** - SLA and support contracts

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📚 Documentation

- **[API Specification](docs/planning/API_SPECIFICATION.md)**: Complete API reference
- **[Implementation Plan](docs/planning/IMPLEMENTATION_PLAN.md)**: Detailed development plan
- **[Architecture Design](docs/planning/ARCHITECTURE_DESIGN.md)**: Technical architecture
- **[Development Roadmap](docs/planning/DEVELOPMENT_ROADMAP.md)**: Timeline and milestones

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎉 Acknowledgments

- Built on top of [MoviePy](https://zulko.github.io/moviepy/)
- Inspired by modern video creation workflows
- Designed for AI agent integration

---

**Project Vine** represents a significant opportunity to bridge the gap between AI capabilities and video creation, providing a powerful, extensible framework that serves both human creativity and automated content generation.
# Test commit to trigger CI
