# Phase 3: Argument & Assignment Typing Audit Report

## Overview
This document audits the errors that are currently suppressed by the `disable_error_code` section in `pyproject.toml` to plan their systematic removal.

## Error Summary

**Total Errors**: 1,269 errors across 16 files
**Error Categories**:
- `call-arg`: ~1,200+ errors (95% of total)
- `assignment`: ~10 errors
- `arg-type`: ~5 errors
- `return-value`: ~1 error

## Error Distribution by Category

### 1. `call-arg` Errors (~1,200+ errors)

**Primary Issue**: Missing required named arguments in constructor calls

#### Most Affected Files:
- `tests/unit/test_video_spec_tracks.py`: ~400+ errors
- `tests/unit/test_tracks.py`: ~50+ errors
- `tests/unit/test_transitions.py`: ~100+ errors
- `tests/unit/test_effects.py`: ~50+ errors
- `tests/unit/test_audio_config.py`: ~100+ errors
- `tests/unit/test_animation_config.py`: ~100+ errors
- `src/vine/builder/timeline_builder.py`: ~50+ errors
- `tests/unit/test_rendering.py`: ~50+ errors

#### Common Missing Arguments:
- **VideoSpec**: `description`, `author`, `width`, `height`, `fps`, `duration`, `voice_config`, `music_config`, `output_path`, `output_format`, `quality`, `background_color`, `enable_audio`, `enable_video`
- **VideoTrack**: `z_order`, `visible`
- **AudioTrack**: `volume`, `muted`
- **TextTrack**: `z_order`, `visible`
- **VideoClip**: `end_time`, `width`, `height`, `x_position`, `y_position`, `opacity`
- **AudioClip**: `end_time`, `volume`, `fade_in`, `fade_out`, `crossfade_duration`, `auto_crossfade`, `normalize_audio`, `volume_curve`, `voice_config`, `music_config`
- **TextClip**: `end_time`, `font_size`, `font_color`, `font_family`, `font_weight`, `x_position`, `y_position`, `alignment`, `opacity`
- **Transition**: `direction`, `easing`
- **KenBurnsConfig**: `duration`, `start_time`, `zoom_factor`, `pan_x`, `pan_y`, `easing`
- **VoiceConfig**: `fade_in`, `fade_out`, `start_time`, `end_time`, `pitch`
- **MusicConfig**: `fade_in`, `fade_out`, `start_time`, `end_time`, `duck_voice`, `duck_level`

### 2. `assignment` Errors (~10 errors)

**Primary Issue**: Type mismatches in variable assignments

#### Affected Files:
- `src/vine/rendering/moviepy_adapter.py`: 2 errors
- `tests/unit/test_timeline_builder_edge_cases.py`: 2 errors
- `tests/unit/test_timeline_builder_comprehensive.py`: 3 errors
- `src/vine/rendering/video_renderer.py`: 2 errors

#### Examples:
```python
# TextTrack assigned to VideoTrack variable
track: VideoTrack = TextTrack(...)

# AudioTrack assigned to VideoTrack variable
track: VideoTrack = AudioTrack(...)

# TextClip assigned to VideoClip variable
clip: VideoClip | ImageClip = TextClip(...)
```

### 3. `arg-type` Errors (~5 errors)

**Primary Issue**: Wrong argument types in function calls

#### Affected Files:
- `src/vine/builder/timeline_builder.py`: 2 errors
- `tests/unit/test_transitions.py`: 1 error
- `src/vine/rendering/moviepy_adapter.py`: 1 error

#### Examples:
```python
# String passed where Literal type expected
Transition(transition_type="fade")  # Should be Literal['fade', 'crossfade', ...]

# Wrong track type passed to adapter
adapt_text_track(video_track)  # Expected TextTrack, got VideoTrack
```

### 4. `return-value` Errors (~1 error)

**Primary Issue**: Wrong return type from function

#### Affected Files:
- `src/vine/models/video_spec.py`: 1 error

#### Example:
```python
# Function returns object but expected specific list type
def _get_tracks_by_type(self, track_type: str) -> List[VideoTrack | AudioTrack | TextTrack]:
    return object()  # Should return actual list
```

## Priority Fix Strategy

### Phase 1: High Impact, Low Complexity (Start Here)
1. **Fix `return-value` errors** (1 error) - Simple return type fixes
2. **Fix `assignment` errors** (~10 errors) - Type assertion or variable type fixes
3. **Fix `arg-type` errors** (~5 errors) - Literal type fixes and correct argument types

### Phase 2: Medium Impact, High Volume
4. **Fix `call-arg` errors systematically** (~1,200+ errors)
   - Start with test files (easier to fix)
   - Group by model type (VideoSpec, VideoTrack, etc.)
   - Add missing required arguments with sensible defaults

### Phase 3: Cleanup
5. **Remove `disable_error_code` section entirely**
6. **Verify no regressions**

## Implementation Plan

### Step 1: Fix Return Value Error
- File: `src/vine/models/video_spec.py:172`
- Fix: Update return type or implementation

### Step 2: Fix Assignment Errors
- Add type assertions or fix variable declarations
- Use `cast()` where appropriate for test scenarios

### Step 3: Fix Argument Type Errors
- Fix Literal type mismatches
- Correct function argument types

### Step 4: Fix Call Argument Errors (Batch Approach)
- **Batch 1**: Test files (easier, less critical)
- **Batch 2**: Source files (more critical)
- **Strategy**: Add missing arguments with sensible defaults

## Risk Assessment

### Low Risk
- Test file fixes (can be reverted easily)
- Return value fixes (straightforward)

### Medium Risk
- Assignment fixes (may require type system changes)
- Argument type fixes (may affect API)

### High Risk
- Source file `call-arg` fixes (may break existing code)
- TimelineBuilder fixes (core API)

## Success Criteria

- [ ] 0 `return-value` errors
- [ ] 0 `assignment` errors
- [ ] 0 `arg-type` errors
- [ ] 0 `call-arg` errors
- [ ] `disable_error_code` section removed
- [ ] All tests pass
- [ ] No runtime regressions

## Next Steps

1. Start with Phase 1 (return-value, assignment, arg-type)
2. Document each fix in progress tracker
3. Test after each batch
4. Remove suppressions only when all errors are fixed
