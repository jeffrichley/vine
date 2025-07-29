# Return-Value Error Analysis

## Overview
Analysis of `return-value` errors found during MyPy strict typing enforcement.

## Current Status
- **Total Errors**: 4
- **Files Affected**: 2
- **Primary Issues**:
  - AnimationRegistry methods returning specific config types instead of base AnimationConfig
  - VideoSpec method returning object instead of proper list type

## Error Breakdown

### Source Files (4 errors)

#### `src/vine/registry/animation_registry.py` (3 errors)
- **Line 110**: `create_ken_burns()` returning `KenBurnsConfig` instead of `AnimationConfig`
- **Line 112**: `create_slide()` returning `SlideConfig` instead of `AnimationConfig`
- **Line 114**: `create_static()` returning `StaticConfig` instead of `AnimationConfig`

**Issue**: Registry methods are typed to return base `AnimationConfig` but return specific config types
**Fix Options**:
1. Change return type annotations to `Union[KenBurnsConfig, SlideConfig, StaticConfig]`
2. Change return type annotations to `AnimationConfig` (if these are truly base types)
3. Use `# type: ignore[return-value]` if the specific types are intentional

#### `src/vine/models/video_spec.py` (1 error)
- **Line 172**: `_get_tracks_by_type()` returning `object` instead of `List[VideoTrack | AudioTrack | TextTrack]`

**Issue**: Method returns `object` type instead of properly typed list
**Fix**: Update return type annotation to match actual return type

## Root Cause Analysis
1. **Registry Design**: AnimationRegistry methods return specific config types but are typed to return base type
2. **Type Inference**: MyPy cannot infer the correct return type for `_get_tracks_by_type()`
3. **API Consistency**: Registry pattern may need adjustment for proper typing

## Fix Strategy

### For AnimationRegistry
**Option 1**: Update return types to be more specific
```python
def create_ken_burns(self, **kwargs: Any) -> KenBurnsConfig:
def create_slide(self, **kwargs: Any) -> SlideConfig:
def create_static(self, **kwargs: Any) -> StaticConfig:
```

**Option 2**: Use Union type if base type is needed
```python
def create_ken_burns(self, **kwargs: Any) -> Union[KenBurnsConfig, AnimationConfig]:
```

### For VideoSpec
**Fix**: Update return type annotation
```python
def _get_tracks_by_type(self, track_type: type) -> List[VideoTrack | AudioTrack | TextTrack]:
```

## Impact Assessment
- **Low Risk**: Internal method changes
- **API Compatibility**: Registry changes may affect consumers
- **Type Safety**: Improved compile-time checking

## Files to Update
- [ ] `src/vine/registry/animation_registry.py`
- [ ] `src/vine/models/video_spec.py`

## Decision Points
1. **Registry Pattern**: Should registry methods return base types or specific types?
2. **Type Hierarchy**: Are KenBurnsConfig, SlideConfig, StaticConfig subtypes of AnimationConfig?
3. **API Design**: Should we maintain base type returns for consistency?
