# 📽️ Project Vine - Media Composition Framework

[![CI](https://github.com/jeffrichley/vine/actions/workflows/ci.yml/badge.svg)](https://github.com/jeffrichley/vine/actions/workflows/ci.yml)
[![Codecov](https://codecov.io/gh/jeffrichley/vine/branch/main/graph/badge.svg)](https://codecov.io/gh/jeffrichley/vine)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![pre-commit enabled](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![pip-audit](https://img.shields.io/badge/pip--audit-enabled-brightgreen?logo=security&logoColor=white)](https://pypi.org/project/pip-audit/)
[![Ruff](https://img.shields.io/badge/ruff-enabled-brightgreen?logo=ruff&logoColor=white)](https://github.com/astral-sh/ruff)
[![MyPy](https://img.shields.io/badge/mypy-enabled-brightgreen?logo=mypy&logoColor=white)](https://mypy-lang.org/)
![pyproject validated](https://img.shields.io/badge/pyproject%20schema-valid-brightgreen?style=flat-square)


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

# Install with uv (recommended)
uv sync

# Or install with pip
pip install -r requirements.txt

# Install in editable mode for development
uv pip install -e .
```

## 🎯 Quick Start

### Installation for Development

```bash
# Install in editable mode to enable development CLI
uv pip install -e .

# Verify installation
uv run dev info

# After installation, you can also call commands directly:
dev info
```

### Development CLI

Project Vine includes a professional development CLI for streamlined workflows:

```bash
# Quality checks
uv run dev lint          # Run linting
uv run dev typecheck     # Run type checking
uv run dev test          # Run tests
uv run dev checkit       # Run all quality checks

# Code formatting
uv run dev format        # Format code with black and ruff

# Documentation
uv run dev docs          # Build documentation
uv run dev docs-serve    # Serve documentation locally

# Analysis
uv run dev vulture       # Find dead code
uv run dev quality-gates # Run quality gates

# Help and info
uv run dev --help        # Show all commands
uv run dev info          # Show project status
```

**Note**: You can also use `uv run vine-dev` as an alternative to `uv run dev`.

**Direct Commands**: After installing with `uv pip install -e .`, you can call commands directly (when virtual environment is active):
```bash
# Activate virtual environment first
source .venv/bin/activate

# Then use direct commands
dev lint
dev test
dev checkit
vine-dev info
```

### Basic Usage

```python
from vine import TimelineBuilder

# Create a simple video with sequential timing
timeline = TimelineBuilder()
timeline.add_image("slide1.jpg", duration=5.0)
timeline.add_text("Welcome", duration=3.0)
timeline.add_voice("narration.mp3", duration=8.0)
timeline.export("output.mp4")

# Or use explicit timing for precise control
timeline = TimelineBuilder()
timeline.add_image_at("background.jpg", 0.0, duration=10.0)
timeline.add_text_at("Title", 2.0, duration=6.0)
timeline.add_voice_at("narration.mp3", 1.0, duration=8.0)
timeline.export("output.mp4")
```

### AI Agent Integration

```python
from vine import TimelineBuilder

# Load from AI-generated JSON (coming in Phase 2)
timeline = TimelineBuilder()
timeline.load_from_json(ai_generated_spec)
timeline.export("ai_video.mp4")
```

### YAML Configuration

```yaml
# video_spec.yaml (coming in Phase 2)
defaults:
  animation: "ken_burns"
  transition: "crossfade"
  resolution: "1080x1920"

timeline:
  - type: "image"
    path: "intro.jpg"
    start_time: 0.0
    duration: 5.0
  - type: "text"
    content: "Welcome"
    start_time: 2.0
    duration: 3.0
  - type: "voice"
    path: "narration.mp3"
    start_time: 1.0
    duration: 8.0
```

```python
from vine import TimelineBuilder

# Load from YAML (coming in Phase 2)
timeline = TimelineBuilder()
timeline.load_from_yaml("video_spec.yaml")
timeline.export("configured_video.mp4")
```

## 🛠️ Development

### Development Environment Setup

```bash
# Install development dependencies
uv pip install -e ".[dev,docs]"

# Run quality checks
uv run dev checkit

# Format code
uv run dev format

# Run tests with coverage
uv run dev test-cov
```

**Direct Commands**: After installation, you can also use (when virtual environment is active):
```bash
# Activate virtual environment first
source .venv/bin/activate

# Then use direct commands
dev checkit
dev format
dev test-cov
```

### Available Development Commands

| Command | Description |
|---------|-------------|
| `uv run dev lint` / `dev lint` | Run linting checks with ruff |
| `uv run dev format` / `dev format` | Format code with black and ruff |
| `uv run dev typecheck` / `dev typecheck` | Run type checking with mypy |
| `uv run dev test` / `dev test` | Run tests with pytest |
| `uv run dev test-cov` / `dev test-cov` | Run tests with coverage reporting |
| `uv run dev test-cov-check` / `dev test-cov-check` | Run tests with coverage threshold check |
| `uv run dev docs` / `dev docs` | Build documentation |
| `uv run dev docs-serve` / `dev docs-serve` | Serve documentation locally |
| `uv run dev docs-watch` / `dev docs-watch` | Watch for changes and rebuild docs |
| `uv run dev vulture` / `dev vulture` | Find dead code |
| `uv run dev quality-gates` / `dev quality-gates` | Run all quality gates |
| `uv run dev checkit` / `dev checkit` | Run comprehensive quality checks |
| `uv run dev dev` / `dev dev` | Run all quality checks (presubmit) |
| `uv run dev build` / `dev build` | Build the package |
| `uv run dev info` / `dev info` | Show project information and status |

**Note**: After installing with `uv pip install -e .`, you can use either format. The direct commands (`dev <command>`) are more convenient for daily development when the virtual environment is active.

### IDE Integration

The development CLI integrates seamlessly with VS Code:

- **Tasks**: Use `Ctrl+Shift+P` → "Tasks: Run Task" to access all commands
- **Debugging**: Use the debug configurations for step-by-step debugging
- **Terminal**: All commands work in the integrated terminal

### Quality Standards

Project Vine maintains high quality standards:

- **Type Safety**: Full MyPy type checking with strict mode
- **Code Quality**: Ruff linting with comprehensive rules
- **Test Coverage**: Minimum 80% test coverage required
- **Documentation**: Comprehensive docstrings and examples
- **Performance**: Xenon complexity analysis
- **Security**: Regular dependency vulnerability scanning

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

## 🎯 Quality Standards

Project Vine maintains rigorous quality standards to ensure reliability, maintainability, and professional-grade code. Our quality gates enforce these standards automatically.

### Quality Gates

We enforce 7 quality gates that must pass before any code is merged:

1. **🔍 Linting (Ruff)**: Code style and best practices enforcement
2. **🧠 Type Safety (MyPy)**: Strict type checking with zero errors
3. **📊 Coverage (≥80%)**: Comprehensive test coverage requirements
4. **📈 Complexity (Xenon)**: Maintainable code complexity levels
5. **🧹 Dead Code (Vulture)**: Removal of unused code and imports
6. **🔒 Security (pip-audit)**: Dependency vulnerability scanning


### Development Requirements

- **Python 3.11+**: Modern Python features and type hints
- **Strict MyPy**: Zero type errors, comprehensive type annotations
- **100% Test Coverage**: All new code must be fully tested
- **Documentation**: All public APIs must be documented
- **Code Style**: Black formatting + Ruff linting enforced
- **Security**: Regular dependency vulnerability scanning

### Quality Commands

```bash
# Run all quality checks
uv run dev checkit

# Individual quality gates
uv run dev lint          # Ruff linting
uv run dev typecheck     # MyPy type checking
uv run dev test          # Pytest with coverage
uv run dev quality-gates # All quality gates
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Quick Contribution Setup

```bash
# Install in editable mode with all development dependencies
uv pip install -e ".[dev,docs]"

# Run quality checks before contributing
uv run dev checkit

# Format your code
uv run dev format

# Run tests
uv run dev test
```

### Dependency Groups

Project Vine uses dependency groups for modular installation:

```bash
# Core runtime dependencies (default)
uv pip install -e .

# Development dependencies (linting, testing, type checking)
uv pip install -e ".[dev]"

# Documentation dependencies (Sphinx, themes)
uv pip install -e ".[docs]"

# Type checking dependencies (MyPy)
uv pip install -e ".[typecheck]"

# Security dependencies (pip-audit)
uv pip install -e ".[security]"

# All dependencies for full development
uv pip install -e ".[dev,docs,typecheck,security]"
```

**Available Groups:**
- **`dev`**: Development tools (Ruff, Black, pytest, MyPy, etc.)
- **`docs`**: Documentation tools (Sphinx, themes, etc.)
- **`typecheck`**: Type checking tools (MyPy)
- **`security`**: Security tools (pip-audit)
- **`test`**: Testing tools (pytest, hypothesis, benchmarks)

**Direct Commands**: After installation, you can also use (when virtual environment is active):
```bash
# Activate virtual environment first
source .venv/bin/activate

# Then use direct commands
dev checkit
dev format
dev test
```

### Development Workflow

1. **Setup**: Install dependencies with `uv pip install -e ".[dev,docs]"`
2. **Develop**: Use `dev lint` and `dev typecheck` during development
3. **Test**: Run `dev test` to ensure all tests pass
4. **Quality**: Run `dev checkit` before submitting changes
5. **Format**: Use `dev format` to maintain code style

**Note**: After installation, you can use either `uv run dev <command>` or `dev <command>` directly (when virtual environment is active).

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
