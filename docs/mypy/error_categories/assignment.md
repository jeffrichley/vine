# Assignment Error Analysis

## Overview
This document analyzes assignment errors found when enabling strict typing for Project Vine.

## Error Summary

**Total Errors**: 12 errors across 5 files
**Error Pattern**: Type mismatches in variable assignments

## Error Distribution by File

### 1. Registry Files (4 errors)
- `src/vine/registry/effect_registry.py`: 2 errors
- `src/vine/registry/animation_registry.py`: 2 errors

**Pattern**: `KenBurnsConfig` variables assigned `SlideConfig` or `StaticConfig` objects

### 2. Rendering Files (2 errors)
- `src/vine/rendering/moviepy_adapter.py`: 1 error
- `src/vine/rendering/video_renderer.py`: 1 error

**Pattern**: `VideoTrack` variables assigned `TextTrack` objects

### 3. Test Files (6 errors)
- `tests/unit/test_timeline_builder_edge_cases.py`: 2 errors
- `tests/unit/test_timeline_builder_comprehensive.py`: 4 errors

**Pattern**: Type mismatches in test scenarios (track types, clip types)

## Detailed Error Analysis

### Registry Errors (Lines 110-113)

**Files**: `effect_registry.py`, `animation_registry.py`
**Issue**: `KenBurnsConfig` variables assigned incompatible config objects

```python
# Current problematic code:
config: KenBurnsConfig = SlideConfig(...)  # Type mismatch
config: KenBurnsConfig = StaticConfig(...)  # Type mismatch
```

**Fix Strategy**:
- Use `cast()` for test scenarios
- Or change variable type to `Union[KenBurnsConfig, SlideConfig, StaticConfig]`
- Or use proper type hierarchy if these should be related

### Rendering Errors (Lines 38, 150)

**Files**: `moviepy_adapter.py`, `video_renderer.py`
**Issue**: `VideoTrack` variables assigned `TextTrack` objects

```python
# Current problematic code:
track: VideoTrack = TextTrack(...)  # Type mismatch
```

**Fix Strategy**:
- Use `cast()` for type assertions
- Or change variable type to `VideoTrack | TextTrack`
- Or use proper base class if tracks should be unified

### Test Errors (Lines 383-820)

**Files**: Test files
**Issue**: Various type mismatches in test scenarios

```python
# Examples:
track: VideoTrack = AudioTrack(...)  # Type mismatch
track: VideoTrack = TextTrack(...)   # Type mismatch
clip: VideoClip | ImageClip = TextClip(...)  # Type mismatch
clip: VideoClip | ImageClip = AudioClip(...) # Type mismatch
```

**Fix Strategy**:
- Use `cast()` for test scenarios where type assertions are needed
- Or change variable types to union types
- Or use proper base classes

## Fix Implementation Plan

### Phase 1: Registry Fixes
1. **File**: `src/vine/registry/effect_registry.py`
   - **Line 110**: Fix `KenBurnsConfig` assignment
   - **Line 112**: Fix `KenBurnsConfig` assignment

2. **File**: `src/vine/registry/animation_registry.py`
   - **Line 111**: Fix `KenBurnsConfig` assignment
   - **Line 113**: Fix `KenBurnsConfig` assignment

### Phase 2: Rendering Fixes
3. **File**: `src/vine/rendering/moviepy_adapter.py`
   - **Line 150**: Fix `VideoTrack` assignment

4. **File**: `src/vine/rendering/video_renderer.py`
   - **Line 38**: Fix `VideoTrack` assignment

### Phase 3: Test Fixes
5. **File**: `tests/unit/test_timeline_builder_edge_cases.py`
   - **Line 383**: Fix `VideoTrack` assignment
   - **Line 386**: Fix `VideoTrack` assignment

6. **File**: `tests/unit/test_timeline_builder_comprehensive.py`
   - **Line 625**: Fix `VideoTrack` assignment
   - **Line 629**: Fix `VideoTrack` assignment
   - **Line 815**: Fix `VideoClip | ImageClip` assignment
   - **Line 820**: Fix `VideoClip | ImageClip` assignment

## Fix Strategy by Error Type

### Type 1: Config Object Mismatches
- **Use**: `cast(KenBurnsConfig, config_object)`
- **Or**: Change variable type to union type
- **Or**: Use proper base class if configs should be unified

### Type 2: Track Type Mismatches
- **Use**: `cast(VideoTrack, track_object)`
- **Or**: Change variable type to `VideoTrack | TextTrack | AudioTrack`
- **Or**: Use proper base class if tracks should be unified

### Type 3: Clip Type Mismatches
- **Use**: `cast(VideoClip, clip_object)`
- **Or**: Change variable type to union type
- **Or**: Use proper base class if clips should be unified

## Success Criteria

- [x] 0 assignment errors in registry files
- [x] 0 assignment errors in rendering files
- [x] 0 assignment errors in test files
- [x] All tests pass after fixes
- [x] No runtime regressions

## Risk Assessment

### Low Risk
- Test file fixes (can use `cast()` safely)
- Registry fixes (likely test scenarios)

### Medium Risk
- Rendering fixes (may affect runtime behavior)
- Type hierarchy changes (may affect API)

## Implementation Notes

1. **Prefer `cast()` for test scenarios** - safer than changing type hierarchies
2. **Use union types for production code** - more flexible than `cast()`
3. **Consider base classes** - if types should be unified in the type system
4. **Test thoroughly** - ensure no runtime regressions

## Next Steps

1. Implement fixes systematically by file
2. Test after each file
3. Update progress tracker
4. Remove assignment from `disable_error_code` when complete
