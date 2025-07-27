# Defaults Management Specification

> **Project:** Vine Media Framework
> **Component:** Defaults Management
> **Status:** Ready for Implementation
> **Priority:** Medium
> **Timeline:** Week 2

## Overview

The Defaults Management system provides hierarchical configuration management for Project Vine, enabling flexible default settings that can be overridden at multiple levels (system, user, project, session). This system supports hot-reloading, validation, and environment-specific configurations.

## Architecture

### Core Components

#### 1. DefaultsManager (Main Class)

**Purpose:** Central coordination for all default settings

```python
from typing import Dict, Any, Optional, Union, List
from pathlib import Path
import json
import yaml
from dataclasses import dataclass
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

@dataclass
class DefaultsLevel:
    """Represents a level in the defaults hierarchy."""
    name: str
    priority: int
    path: Optional[Path] = None
    data: Dict[str, Any] = None
    auto_reload: bool = False

class DefaultsManager:
    """Central defaults management and coordination."""

    def __init__(self, config_dir: Optional[Path] = None):
        self.config_dir = config_dir or Path.home() / ".vine"
        self.levels: Dict[str, DefaultsLevel] = {}
        self._observer: Optional[Observer] = None
        self._cache: Dict[str, Any] = {}
        self._initialize_levels()

    def _initialize_levels(self):
        """Initialize the defaults hierarchy levels."""
        # System defaults (lowest priority)
        self.levels["system"] = DefaultsLevel(
            name="system",
            priority=0,
            path=self.config_dir / "system",
            auto_reload=False
        )

        # User defaults
        self.levels["user"] = DefaultsLevel(
            name="user",
            priority=1,
            path=self.config_dir / "user",
            auto_reload=True
        )

        # Project defaults
        self.levels["project"] = DefaultsLevel(
            name="project",
            priority=2,
            path=Path.cwd() / ".vine",
            auto_reload=True
        )

        # Session defaults (highest priority)
        self.levels["session"] = DefaultsLevel(
            name="session",
            priority=3,
            data={},
            auto_reload=False
        )

    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from the defaults hierarchy."""
        # Check cache first
        if key in self._cache:
            return self._cache[key]

        # Search through levels in priority order
        for level_name in sorted(self.levels.keys(),
                               key=lambda x: self.levels[x].priority):
            level = self.levels[level_name]
            value = self._get_from_level(level, key)
            if value is not None:
                self._cache[key] = value
                return value

        return default

    def set(self, key: str, value: Any, level: str = "session") -> None:
        """Set a value at a specific level."""
        if level not in self.levels:
            raise ValueError(f"Invalid level: {level}")

        level_obj = self.levels[level]
        if level_obj.data is None:
            level_obj.data = {}

        level_obj.data[key] = value
        self._cache[key] = value

        # Save to file if level has a path
        if level_obj.path:
            self._save_level(level_obj)

    def get_all(self, prefix: str = "") -> Dict[str, Any]:
        """Get all values with optional prefix filtering."""
        result = {}
        for level_name in sorted(self.levels.keys(),
                               key=lambda x: self.levels[x].priority):
            level = self.levels[level_name]
            level_data = self._get_level_data(level)

            for key, value in level_data.items():
                if prefix and not key.startswith(prefix):
                    continue
                if key not in result:  # Higher priority levels override
                    result[key] = value

        return result

    def load_level(self, level_name: str) -> None:
        """Load data for a specific level."""
        if level_name not in self.levels:
            raise ValueError(f"Invalid level: {level_name}")

        level = self.levels[level_name]
        if level.path and level.path.exists():
            level.data = self._load_from_file(level.path)
        else:
            level.data = {}

    def save_level(self, level_name: str) -> None:
        """Save data for a specific level."""
        if level_name not in self.levels:
            raise ValueError(f"Invalid level: {level_name}")

        level = self.levels[level_name]
        if level.path:
            self._save_level(level)

    def reload_all(self) -> None:
        """Reload all levels from files."""
        self._cache.clear()
        for level_name in self.levels:
            self.load_level(level_name)

    def start_watching(self) -> None:
        """Start watching for file changes."""
        if self._observer:
            return

        self._observer = Observer()
        for level in self.levels.values():
            if level.auto_reload and level.path:
                self._observer.schedule(
                    DefaultsFileHandler(self),
                    str(level.path.parent),
                    recursive=False
                )
        self._observer.start()

    def stop_watching(self) -> None:
        """Stop watching for file changes."""
        if self._observer:
            self._observer.stop()
            self._observer.join()
            self._observer = None

    def _get_from_level(self, level: DefaultsLevel, key: str) -> Any:
        """Get a value from a specific level."""
        if level.data is None:
            self.load_level(level.name)

        return level.data.get(key) if level.data else None

    def _get_level_data(self, level: DefaultsLevel) -> Dict[str, Any]:
        """Get all data from a level."""
        if level.data is None:
            self.load_level(level.name)

        return level.data or {}

    def _load_from_file(self, path: Path) -> Dict[str, Any]:
        """Load data from a file."""
        if not path.exists():
            return {}

        try:
            if path.suffix == ".json":
                with open(path, "r") as f:
                    return json.load(f)
            elif path.suffix in [".yml", ".yaml"]:
                with open(path, "r") as f:
                    return yaml.safe_load(f)
            else:
                # Try to detect format
                with open(path, "r") as f:
                    content = f.read().strip()
                    if content.startswith("{"):
                        return json.loads(content)
                    else:
                        return yaml.safe_load(content)
        except Exception as e:
            logger.warning(f"Failed to load defaults from {path}: {e}")
            return {}

    def _save_level(self, level: DefaultsLevel) -> None:
        """Save level data to file."""
        if not level.path or not level.data:
            return

        level.path.parent.mkdir(parents=True, exist_ok=True)

        try:
            if level.path.suffix == ".json":
                with open(level.path, "w") as f:
                    json.dump(level.data, f, indent=2)
            elif level.path.suffix in [".yml", ".yaml"]:
                with open(level.path, "w") as f:
                    yaml.dump(level.data, f, default_flow_style=False)
            else:
                # Default to JSON
                level.path = level.path.with_suffix(".json")
                with open(level.path, "w") as f:
                    json.dump(level.data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save defaults to {level.path}: {e}")
```

#### 2. SystemDefaults

**Purpose:** Framework-level default settings

```python
class SystemDefaults:
    """System-level default settings."""

    DEFAULTS = {
        # Video settings
        "video.fps": 30.0,
        "video.resolution": (1920, 1080),
        "video.quality": "high",
        "video.format": "mp4",
        "video.codec": "libx264",
        "video.audio_codec": "aac",

        # Audio settings
        "audio.volume": 1.0,
        "audio.fade_in": 0.0,
        "audio.fade_out": 0.0,
        "audio.background_volume": 0.3,

        # Effect settings
        "effects.ken_burns.zoom": 1.2,
        "effects.ken_burns.pan_x": 0.0,
        "effects.ken_burns.pan_y": 0.0,
        "effects.slide.direction": "left",
        "effects.slide.distance": 100,

        # Transition settings
        "transitions.fade.duration": 0.5,
        "transitions.crossfade.duration": 0.5,
        "transitions.slide.duration": 0.5,
        "transitions.slide.direction": "left",

        # Performance settings
        "performance.cache_size": 100,
        "performance.enable_caching": True,
        "performance.threading": True,
        "performance.memory_limit": "2GB",

        # Validation settings
        "validation.strict": True,
        "validation.allow_unknown": False,
        "validation.max_file_size": "100MB",

        # Registry settings
        "registry.auto_discover": True,
        "registry.reload_on_change": False,
        "registry.plugin_dirs": [],

        # Export settings
        "export.auto_cleanup": True,
        "export.temp_dir": None,
        "export.backup_enabled": True,
        "export.backup_count": 3
    }

    @classmethod
    def get_defaults(cls) -> Dict[str, Any]:
        """Get all system defaults."""
        return cls.DEFAULTS.copy()

    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """Get a system default value."""
        return cls.DEFAULTS.get(key, default)

    @classmethod
    def validate_key(cls, key: str) -> bool:
        """Validate if a key exists in system defaults."""
        return key in cls.DEFAULTS
```

#### 3. UserDefaults

**Purpose:** User-specific default settings

```python
class UserDefaults:
    """User-specific default settings."""

    def __init__(self, config_dir: Path):
        self.config_dir = config_dir
        self.file_path = config_dir / "user_defaults.json"
        self._data = {}
        self._load()

    def _load(self):
        """Load user defaults from file."""
        if self.file_path.exists():
            try:
                with open(self.file_path, "r") as f:
                    self._data = json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load user defaults: {e}")
                self._data = {}
        else:
            self._data = {}

    def save(self):
        """Save user defaults to file."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(self.file_path, "w") as f:
                json.dump(self._data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save user defaults: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get a user default value."""
        return self._data.get(key, default)

    def set(self, key: str, value: Any):
        """Set a user default value."""
        self._data[key] = value
        self.save()

    def get_all(self) -> Dict[str, Any]:
        """Get all user defaults."""
        return self._data.copy()

    def reset(self):
        """Reset user defaults to empty."""
        self._data = {}
        self.save()
```

#### 4. ProjectDefaults

**Purpose:** Project-specific default settings

```python
class ProjectDefaults:
    """Project-specific default settings."""

    def __init__(self, project_dir: Path):
        self.project_dir = project_dir
        self.file_path = project_dir / ".vine" / "project_defaults.json"
        self._data = {}
        self._load()

    def _load(self):
        """Load project defaults from file."""
        if self.file_path.exists():
            try:
                with open(self.file_path, "r") as f:
                    self._data = json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load project defaults: {e}")
                self._data = {}
        else:
            self._data = {}

    def save(self):
        """Save project defaults to file."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(self.file_path, "w") as f:
                json.dump(self._data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save project defaults: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get a project default value."""
        return self._data.get(key, default)

    def set(self, key: str, value: Any):
        """Set a project default value."""
        self._data[key] = value
        self.save()

    def get_all(self) -> Dict[str, Any]:
        """Get all project defaults."""
        return self._data.copy()

    def reset(self):
        """Reset project defaults to empty."""
        self._data = {}
        self.save()
```

### File System Handler

```python
class DefaultsFileHandler(FileSystemEventHandler):
    """File system event handler for defaults files."""

    def __init__(self, defaults_manager: DefaultsManager):
        self.defaults_manager = defaults_manager

    def on_modified(self, event):
        """Handle file modification events."""
        if event.is_directory:
            return

        # Check if the modified file is a defaults file
        for level in self.defaults_manager.levels.values():
            if level.path and event.src_path == str(level.path):
                logger.info(f"Defaults file modified: {event.src_path}")
                self.defaults_manager.reload_all()
                break
```

## Configuration Files

### System Defaults (JSON)

```json
{
  "video": {
    "fps": 30.0,
    "resolution": [1920, 1080],
    "quality": "high",
    "format": "mp4",
    "codec": "libx264",
    "audio_codec": "aac"
  },
  "audio": {
    "volume": 1.0,
    "fade_in": 0.0,
    "fade_out": 0.0,
    "background_volume": 0.3
  },
  "effects": {
    "ken_burns": {
      "zoom": 1.2,
      "pan_x": 0.0,
      "pan_y": 0.0
    },
    "slide": {
      "direction": "left",
      "distance": 100
    }
  },
  "transitions": {
    "fade": {
      "duration": 0.5
    },
    "crossfade": {
      "duration": 0.5
    },
    "slide": {
      "duration": 0.5,
      "direction": "left"
    }
  },
  "performance": {
    "cache_size": 100,
    "enable_caching": true,
    "threading": true,
    "memory_limit": "2GB"
  },
  "validation": {
    "strict": true,
    "allow_unknown": false,
    "max_file_size": "100MB"
  }
}
```

### User Defaults (YAML)

```yaml
# User-specific preferences
video:
  fps: 60.0  # Override system default
  quality: "ultra"

audio:
  volume: 0.8
  background_volume: 0.2

effects:
  ken_burns:
    zoom: 1.5  # More dramatic zoom

transitions:
  fade:
    duration: 0.3  # Faster transitions

# Personal preferences
ui:
  theme: "dark"
  language: "en"

export:
  default_path: "~/Videos/vine_output"
  auto_open: true
```

### Project Defaults (JSON)

```json
{
  "project": {
    "name": "My Video Project",
    "version": "1.0.0",
    "author": "John Doe"
  },
  "video": {
    "resolution": [1280, 720],  // Project-specific resolution
    "fps": 24.0  // Film-like frame rate
  },
  "audio": {
    "background_volume": 0.1  // Lower background music
  },
  "effects": {
    "ken_burns": {
      "zoom": 1.1  // Subtle zoom for this project
    }
  },
  "export": {
    "path": "./output",
    "format": "mp4",
    "quality": "high"
  }
}
```

## Environment-Specific Configuration

### Environment Variables

```python
class EnvironmentDefaults:
    """Environment-specific default settings."""

    ENV_MAPPING = {
        "VINE_VIDEO_FPS": "video.fps",
        "VINE_VIDEO_RESOLUTION": "video.resolution",
        "VINE_AUDIO_VOLUME": "audio.volume",
        "VINE_EXPORT_PATH": "export.path",
        "VINE_CACHE_SIZE": "performance.cache_size",
        "VINE_MEMORY_LIMIT": "performance.memory_limit"
    }

    @classmethod
    def get_env_defaults(cls) -> Dict[str, Any]:
        """Get defaults from environment variables."""
        env_defaults = {}

        for env_var, config_key in cls.ENV_MAPPING.items():
            value = os.getenv(env_var)
            if value is not None:
                # Convert value to appropriate type
                env_defaults[config_key] = cls._convert_value(value)

        return env_defaults

    @classmethod
    def _convert_value(cls, value: str) -> Any:
        """Convert environment variable value to appropriate type."""
        # Try to convert to number
        try:
            if "." in value:
                return float(value)
            else:
                return int(value)
        except ValueError:
            # Try to convert to boolean
            if value.lower() in ["true", "yes", "1"]:
                return True
            elif value.lower() in ["false", "no", "0"]:
                return False
            else:
                return value
```

## Validation and Error Handling

### Defaults Validation

```python
class DefaultsValidator:
    """Validator for default settings."""

    VALIDATION_RULES = {
        "video.fps": {
            "type": "float",
            "min": 1.0,
            "max": 120.0
        },
        "video.resolution": {
            "type": "tuple",
            "length": 2,
            "item_type": "int",
            "min": 1
        },
        "audio.volume": {
            "type": "float",
            "min": 0.0,
            "max": 2.0
        },
        "performance.cache_size": {
            "type": "int",
            "min": 1,
            "max": 10000
        }
    }

    @classmethod
    def validate(cls, key: str, value: Any) -> bool:
        """Validate a default value."""
        if key not in cls.VALIDATION_RULES:
            return True  # Unknown keys are allowed

        rule = cls.VALIDATION_RULES[key]
        return cls._validate_value(value, rule)

    @classmethod
    def _validate_value(cls, value: Any, rule: Dict[str, Any]) -> bool:
        """Validate a value against a rule."""
        # Type validation
        expected_type = rule.get("type")
        if expected_type == "float" and not isinstance(value, (int, float)):
            return False
        elif expected_type == "int" and not isinstance(value, int):
            return False
        elif expected_type == "tuple" and not isinstance(value, tuple):
            return False

        # Range validation
        if "min" in rule and value < rule["min"]:
            return False
        if "max" in rule and value > rule["max"]:
            return False

        # Length validation
        if "length" in rule and len(value) != rule["length"]:
            return False

        return True
```

## Performance Optimization

### Caching Strategy

```python
class DefaultsCache:
    """Cache for default values."""

    def __init__(self, max_size: int = 1000):
        self._cache = {}
        self._max_size = max_size
        self._access_count = {}
        self._last_modified = {}

    def get(self, key: str) -> Optional[Any]:
        """Get a value from cache."""
        if key in self._cache:
            self._access_count[key] += 1
            return self._cache[key]
        return None

    def set(self, key: str, value: Any):
        """Set a value in cache."""
        if len(self._cache) >= self._max_size:
            self._evict_least_used()

        self._cache[key] = value
        self._access_count[key] = 1
        self._last_modified[key] = time.time()

    def invalidate(self, key: str):
        """Invalidate a cached value."""
        if key in self._cache:
            del self._cache[key]
            del self._access_count[key]
            del self._last_modified[key]

    def clear(self):
        """Clear all cached values."""
        self._cache.clear()
        self._access_count.clear()
        self._last_modified.clear()

    def _evict_least_used(self):
        """Evict least used item from cache."""
        if not self._access_count:
            return

        least_used = min(self._access_count.items(), key=lambda x: x[1])
        del self._cache[least_used[0]]
        del self._access_count[least_used[0]]
        del self._last_modified[least_used[0]]
```

## Testing Strategy

### Unit Tests

1. **Defaults Loading**: Test loading from different file formats
2. **Hierarchy Resolution**: Test priority-based value resolution
3. **Validation**: Test value validation rules
4. **Caching**: Test cache performance and eviction
5. **File Watching**: Test hot-reload functionality

### Integration Tests

1. **TimelineBuilder Integration**: Test defaults integration with timeline builder
2. **Registry Integration**: Test defaults integration with registry system
3. **Model Integration**: Test defaults integration with Pydantic models
4. **End-to-End**: Test complete defaults workflow

### Performance Tests

1. **Large Configurations**: Test with many default values
2. **File I/O Performance**: Test file loading and saving performance
3. **Cache Performance**: Test cache hit rates and memory usage
4. **Hot-Reload Performance**: Test file watching performance

## Documentation Requirements

1. **Configuration Guide**: How to set up and use defaults
2. **File Format Reference**: JSON and YAML format specifications
3. **Environment Variables**: List of supported environment variables
4. **Best Practices**: Recommended configuration patterns
5. **Migration Guide**: How to migrate between versions
