# Registry System Specification

> **Project:** Vine Media Framework
> **Component:** Registry System
> **Status:** Ready for Implementation
> **Priority:** High
> **Timeline:** Week 1

## Overview

The Registry System provides an extensible plugin architecture for Project Vine, enabling dynamic loading and registration of effects, transitions, and other components. This system supports both built-in and third-party plugins with full validation and error handling.

## Architecture

### Core Components

#### 1. RegistryBase (Abstract Base Class)

**Purpose:** Common interface for all registry types

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Type, Callable, List
from pathlib import Path
import importlib
import inspect

class RegistryBase(ABC):
    """Abstract base class for all registries."""

    def __init__(self, name: str):
        self.name = name
        self._registry: Dict[str, Any] = {}
        self._metadata: Dict[str, Dict[str, Any]] = {}
        self._validators: Dict[str, Callable] = {}

    @abstractmethod
    def register(self, name: str, component: Any, **kwargs) -> None:
        """Register a component with the registry."""
        pass

    @abstractmethod
    def get(self, name: str) -> Any:
        """Retrieve a component from the registry."""
        pass

    @abstractmethod
    def list(self) -> List[str]:
        """List all registered components."""
        pass

    def validate(self, name: str, config: Dict[str, Any]) -> bool:
        """Validate configuration for a registered component."""
        if name not in self._validators:
            return True
        return self._validators[name](config)

    def get_metadata(self, name: str) -> Optional[Dict[str, Any]]:
        """Get metadata for a registered component."""
        return self._metadata.get(name)

    def discover_plugins(self, plugin_dir: Path) -> List[str]:
        """Discover and load plugins from a directory."""
        discovered = []
        if not plugin_dir.exists():
            return discovered

        for plugin_file in plugin_dir.glob("*.py"):
            if plugin_file.name.startswith("_"):
                continue

            try:
                module_name = f"{plugin_dir.name}.{plugin_file.stem}"
                module = importlib.import_module(module_name)
                discovered.extend(self._load_from_module(module))
            except Exception as e:
                logger.warning(f"Failed to load plugin {plugin_file}: {e}")

        return discovered

    def _load_from_module(self, module) -> List[str]:
        """Load components from a module."""
        loaded = []
        for name, obj in inspect.getmembers(module):
            if self._is_component(obj):
                try:
                    self.register(name, obj)
                    loaded.append(name)
                except Exception as e:
                    logger.warning(f"Failed to register {name}: {e}")
        return loaded

    @abstractmethod
    def _is_component(self, obj: Any) -> bool:
        """Check if an object is a valid component for this registry."""
        pass
```

#### 2. EffectRegistry

**Purpose:** Registry for animation and visual effects

```python
from typing import Protocol, runtime_checkable
from moviepy.editor import VideoClip

@runtime_checkable
class EffectProtocol(Protocol):
    """Protocol for effect components."""

    def apply(self, clip: VideoClip, config: Dict[str, Any]) -> VideoClip:
        """Apply effect to a video clip."""
        ...

class EffectRegistry(RegistryBase):
    """Registry for animation and visual effects."""

    def __init__(self):
        super().__init__("effects")
        self._register_builtin_effects()

    def register(self, name: str, effect: EffectProtocol,
                validator: Optional[Callable] = None,
                metadata: Optional[Dict[str, Any]] = None) -> None:
        """Register an effect with the registry."""
        if not isinstance(effect, EffectProtocol):
            raise ValueError(f"Effect {name} must implement EffectProtocol")

        self._registry[name] = effect
        if validator:
            self._validators[name] = validator
        if metadata:
            self._metadata[name] = metadata

    def get(self, name: str) -> EffectProtocol:
        """Get an effect from the registry."""
        if name not in self._registry:
            raise KeyError(f"Effect '{name}' not found in registry")
        return self._registry[name]

    def list(self) -> List[str]:
        """List all registered effects."""
        return list(self._registry.keys())

    def apply_effect(self, name: str, clip: VideoClip,
                    config: Dict[str, Any]) -> VideoClip:
        """Apply a registered effect to a clip."""
        effect = self.get(name)
        if not self.validate(name, config):
            raise ValueError(f"Invalid configuration for effect '{name}'")
        return effect.apply(clip, config)

    def _is_component(self, obj: Any) -> bool:
        """Check if an object is a valid effect."""
        return isinstance(obj, EffectProtocol)

    def _register_builtin_effects(self):
        """Register built-in effects."""
        from .effects import KenBurnsEffect, SlideEffect, StaticEffect

        self.register("ken_burns", KenBurnsEffect())
        self.register("slide", SlideEffect())
        self.register("static", StaticEffect())
```

#### 3. TransitionRegistry

**Purpose:** Registry for scene transitions

```python
@runtime_checkable
class TransitionProtocol(Protocol):
    """Protocol for transition components."""

    def apply(self, clip1: VideoClip, clip2: VideoClip,
              config: Dict[str, Any]) -> VideoClip:
        """Apply transition between two clips."""
        ...

class TransitionRegistry(RegistryBase):
    """Registry for scene transitions."""

    def __init__(self):
        super().__init__("transitions")
        self._register_builtin_transitions()

    def register(self, name: str, transition: TransitionProtocol,
                validator: Optional[Callable] = None,
                metadata: Optional[Dict[str, Any]] = None) -> None:
        """Register a transition with the registry."""
        if not isinstance(transition, TransitionProtocol):
            raise ValueError(f"Transition {name} must implement TransitionProtocol")

        self._registry[name] = transition
        if validator:
            self._validators[name] = validator
        if metadata:
            self._metadata[name] = metadata

    def get(self, name: str) -> TransitionProtocol:
        """Get a transition from the registry."""
        if name not in self._registry:
            raise KeyError(f"Transition '{name}' not found in registry")
        return self._registry[name]

    def list(self) -> List[str]:
        """List all registered transitions."""
        return list(self._registry.keys())

    def apply_transition(self, name: str, clip1: VideoClip, clip2: VideoClip,
                        config: Dict[str, Any]) -> VideoClip:
        """Apply a registered transition between clips."""
        transition = self.get(name)
        if not self.validate(name, config):
            raise ValueError(f"Invalid configuration for transition '{name}'")
        return transition.apply(clip1, clip2, config)

    def _is_component(self, obj: Any) -> bool:
        """Check if an object is a valid transition."""
        return isinstance(obj, TransitionProtocol)

    def _register_builtin_transitions(self):
        """Register built-in transitions."""
        from .transitions import FadeTransition, CrossfadeTransition, SlideTransition

        self.register("fade", FadeTransition())
        self.register("crossfade", CrossfadeTransition())
        self.register("slide", SlideTransition())
```

#### 4. RegistryManager

**Purpose:** Central coordination for all registries

```python
class RegistryManager:
    """Central registry coordination and management."""

    def __init__(self):
        self._registries: Dict[str, RegistryBase] = {}
        self._plugin_dirs: Dict[str, Path] = {}
        self._initialize_registries()

    def _initialize_registries(self):
        """Initialize all registries."""
        self._registries["effects"] = EffectRegistry()
        self._registries["transitions"] = TransitionRegistry()
        # Future: audio_effects, text_effects, etc.

    def get_registry(self, name: str) -> RegistryBase:
        """Get a registry by name."""
        if name not in self._registries:
            raise KeyError(f"Registry '{name}' not found")
        return self._registries[name]

    def register_component(self, registry_name: str, component_name: str,
                          component: Any, **kwargs) -> None:
        """Register a component with a specific registry."""
        registry = self.get_registry(registry_name)
        registry.register(component_name, component, **kwargs)

    def get_component(self, registry_name: str, component_name: str) -> Any:
        """Get a component from a specific registry."""
        registry = self.get_registry(registry_name)
        return registry.get(component_name)

    def list_components(self, registry_name: str) -> List[str]:
        """List all components in a registry."""
        registry = self.get_registry(registry_name)
        return registry.list()

    def discover_plugins(self, registry_name: str, plugin_dir: Path) -> List[str]:
        """Discover plugins for a specific registry."""
        registry = self.get_registry(registry_name)
        self._plugin_dirs[registry_name] = plugin_dir
        return registry.discover_plugins(plugin_dir)

    def reload_plugins(self, registry_name: str) -> List[str]:
        """Reload plugins for a registry."""
        if registry_name not in self._plugin_dirs:
            return []

        registry = self.get_registry(registry_name)
        plugin_dir = self._plugin_dirs[registry_name]
        return registry.discover_plugins(plugin_dir)

    def validate_config(self, registry_name: str, component_name: str,
                       config: Dict[str, Any]) -> bool:
        """Validate configuration for a component."""
        registry = self.get_registry(registry_name)
        return registry.validate(component_name, config)

    def get_component_metadata(self, registry_name: str,
                              component_name: str) -> Optional[Dict[str, Any]]:
        """Get metadata for a component."""
        registry = self.get_registry(registry_name)
        return registry.get_metadata(component_name)
```

## Built-in Effects

### KenBurnsEffect

```python
class KenBurnsEffect:
    """Ken Burns effect for image animation."""

    def apply(self, clip: VideoClip, config: Dict[str, Any]) -> VideoClip:
        """Apply Ken Burns effect to a clip."""
        zoom_start = config.get("zoom_start", 1.0)
        zoom_end = config.get("zoom_end", 1.2)
        pan_x = config.get("pan_x", 0.0)
        pan_y = config.get("pan_y", 0.0)

        def ken_burns_transform(get_frame, t):
            # Calculate zoom and pan based on time
            progress = t / clip.duration
            current_zoom = zoom_start + (zoom_end - zoom_start) * progress
            current_pan_x = pan_x * progress
            current_pan_y = pan_y * progress

            # Apply transformation
            frame = get_frame(t)
            # Implementation details...
            return frame

        return clip.fl(ken_burns_transform)
```

### SlideEffect

```python
class SlideEffect:
    """Slide effect for image transitions."""

    def apply(self, clip: VideoClip, config: Dict[str, Any]) -> VideoClip:
        """Apply slide effect to a clip."""
        direction = config.get("direction", "left")
        distance = config.get("distance", 100)

        def slide_transform(get_frame, t):
            # Calculate slide position based on time
            progress = t / clip.duration
            offset_x = distance * progress if direction in ["left", "right"] else 0
            offset_y = distance * progress if direction in ["up", "down"] else 0

            # Apply transformation
            frame = get_frame(t)
            # Implementation details...
            return frame

        return clip.fl(slide_transform)
```

## Built-in Transitions

### FadeTransition

```python
class FadeTransition:
    """Fade transition between clips."""

    def apply(self, clip1: VideoClip, clip2: VideoClip,
              config: Dict[str, Any]) -> VideoClip:
        """Apply fade transition between clips."""
        duration = config.get("duration", 0.5)

        # Create fade out for clip1
        fade_out = clip1.fadeout(duration)

        # Create fade in for clip2
        fade_in = clip2.fadein(duration)

        # Composite the clips
        return CompositeVideoClip([fade_out, fade_in])
```

### CrossfadeTransition

```python
class CrossfadeTransition:
    """Crossfade transition between clips."""

    def apply(self, clip1: VideoClip, clip2: VideoClip,
              config: Dict[str, Any]) -> VideoClip:
        """Apply crossfade transition between clips."""
        duration = config.get("duration", 0.5)

        # Create crossfade
        return CompositeVideoClip([
            clip1.set_duration(clip1.duration + duration),
            clip2.set_start(clip1.duration - duration).fadein(duration)
        ])
```

## Plugin System

### Plugin Discovery

```python
def discover_plugins(plugin_dir: Path) -> Dict[str, List[str]]:
    """Discover plugins in a directory."""
    discovered = {}

    for registry_dir in plugin_dir.iterdir():
        if registry_dir.is_dir():
            registry_name = registry_dir.name
            discovered[registry_name] = []

            for plugin_file in registry_dir.glob("*.py"):
                if plugin_file.name.startswith("_"):
                    continue

                try:
                    # Load plugin module
                    module_name = f"{registry_name}.{plugin_file.stem}"
                    module = importlib.import_module(module_name)
                    discovered[registry_name].append(plugin_file.stem)
                except Exception as e:
                    logger.warning(f"Failed to load plugin {plugin_file}: {e}")

    return discovered
```

### Plugin Development

```python
# Example custom effect plugin
from vine.registry import EffectRegistry

class CustomZoomEffect:
    """Custom zoom effect plugin."""

    def apply(self, clip, config):
        scale = config.get("scale", 1.5)
        duration = config.get("duration", 2.0)

        def zoom_transform(get_frame, t):
            progress = t / duration
            current_scale = 1.0 + (scale - 1.0) * progress
            # Apply zoom transformation
            return get_frame(t)  # Simplified

        return clip.fl(zoom_transform)

# Register the plugin
EffectRegistry().register("custom_zoom", CustomZoomEffect())
```

## Configuration

### Registry Configuration

```python
from pydantic import BaseModel, Field
from typing import List
from pathlib import Path

class RegistryConfig(BaseModel):
    """Registry system configuration."""

    # Plugin directories
    plugin_dirs: List[Path] = Field(default_factory=list)

    # Discovery settings
    auto_discover: bool = True
    reload_on_change: bool = False

    # Validation settings
    strict_validation: bool = True
    allow_unknown_components: bool = False

    # Performance settings
    cache_size: int = 100
    enable_caching: bool = True
```

## Error Handling

### Registry Errors

```python
class RegistryError(Exception):
    """Base exception for registry errors."""
    pass

class ComponentNotFoundError(RegistryError):
    """Raised when a component is not found in registry."""
    pass

class InvalidComponentError(RegistryError):
    """Raised when a component is invalid for the registry."""
    pass

class ConfigurationError(RegistryError):
    """Raised when component configuration is invalid."""
    pass
```

## Performance Optimization

### Caching

```python
class RegistryCache:
    """Cache for registry components."""

    def __init__(self, max_size: int = 100):
        self._cache = {}
        self._max_size = max_size
        self._access_count = {}

    def get(self, key: str) -> Optional[Any]:
        """Get item from cache."""
        if key in self._cache:
            self._access_count[key] += 1
            return self._cache[key]
        return None

    def set(self, key: str, value: Any) -> None:
        """Set item in cache."""
        if len(self._cache) >= self._max_size:
            self._evict_least_used()

        self._cache[key] = value
        self._access_count[key] = 1

    def _evict_least_used(self):
        """Evict least used item from cache."""
        if not self._access_count:
            return

        least_used = min(self._access_count.items(), key=lambda x: x[1])
        del self._cache[least_used[0]]
        del self._access_count[least_used[0]]
```

## Testing Strategy

### Unit Tests

1. **Registry Registration**: Test component registration
2. **Component Retrieval**: Test component retrieval and error handling
3. **Validation**: Test configuration validation
4. **Plugin Discovery**: Test plugin loading and discovery
5. **Error Handling**: Test error scenarios and recovery

### Integration Tests

1. **Effect Application**: Test effect application to clips
2. **Transition Application**: Test transition application between clips
3. **Registry Manager**: Test registry coordination
4. **Plugin System**: Test end-to-end plugin loading

### Performance Tests

1. **Registration Performance**: Test registration speed
2. **Retrieval Performance**: Test component retrieval speed
3. **Memory Usage**: Test memory consumption
4. **Cache Performance**: Test caching effectiveness

## Documentation Requirements

1. **API Reference**: Complete API documentation
2. **Plugin Development Guide**: How to create custom plugins
3. **Built-in Components**: Documentation of all built-in effects/transitions
4. **Configuration Guide**: Registry configuration options
5. **Examples**: Usage examples and tutorials
