# 📽️ Project Vine - Media Composition Framework

**Project Vine** is a modular, agent-compatible, dual-mode video composition framework built on top of MoviePy. It provides an expressive and extensible API for AI-driven and human-assisted short-form video generation, supporting both scene-based narrative pacing and beat-driven precision editing.

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

### Phase 1: Foundation (Weeks 1-2)
- [ ] Core architecture and basic functionality
- [ ] Pydantic models and registry system
- [ ] Basic TimelineBuilder API

### Phase 2: Advanced Features (Weeks 3-4)
- [ ] MoviePy integration and audio processing
- [ ] JSON/YAML parsing and AI agent integration
- [ ] Complete rendering pipeline

### Phase 3: Advanced Modes (Week 5)
- [ ] Scene-based and beat-driven editing
- [ ] Hybrid mode support
- [ ] Advanced animation effects

### Phase 4: Polish & Launch (Week 6)
- [ ] Comprehensive testing and documentation
- [ ] Performance optimization
- [ ] Production-ready release

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
