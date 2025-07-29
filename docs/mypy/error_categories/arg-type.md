# Arg-Type Error Analysis

## Overview
Analysis of `arg-type` errors found during MyPy strict typing enforcement.

## Current Status
- **Total Errors**: 35
- **Files Affected**: 7
- **Primary Issue**: String literals used where TransitionType enum expected

## Error Breakdown

### Test Files (35 errors)

#### `tests/unit/test_video_spec_tracks.py` (8 errors)
- **Lines**: 267, 316, 318, 381, 389, 398, 407
- **Issue**: `Transition(transition_type="fade")` using string instead of `TransitionType.FADE`
- **Fix**: Replace string literals with `TransitionType` enum values

#### `tests/unit/test_transitions.py` (12 errors)
- **Lines**: 57, 80, 93, 113, 137, 155, 165, 177, 203, 206, 209, 231, 245, 263
- **Issue**: `Transition(transition_type="fade")` using string instead of `TransitionType.FADE`
- **Fix**: Replace string literals with `TransitionType` enum values

#### `tests/unit/test_timeline_builder_tracks.py` (3 errors)
- **Lines**: 207, 220, 237
- **Issue**: `builder.add_transition("fade")` using string instead of `TransitionType.FADE`
- **Fix**: Replace string literals with `TransitionType` enum values

#### `tests/unit/test_timeline_builder_edge_cases.py` (3 errors)
- **Lines**: 74, 78, 82
- **Issue**: `builder.add_transition_at("fade", ...)` using string instead of `TransitionType.FADE`
- **Fix**: Replace string literals with `TransitionType` enum values

#### `tests/unit/test_timeline_builder_comprehensive.py` (9 errors)
- **Lines**: 247, 263, 276, 406, 431, 524, 593, 606
- **Issue**: `builder.add_transition("fade")` and `builder.add_transition_at("fade", ...)` using strings
- **Fix**: Replace string literals with `TransitionType` enum values

## Root Cause Analysis
The issue stems from:
1. **API Design**: TimelineBuilder methods accept `TransitionType` enum but tests use string literals
2. **Transition Constructor**: Expects `TransitionType` enum but tests pass string literals
3. **Test Data**: Test fixtures use string literals instead of enum values

## Fix Strategy
1. **Import TransitionType**: Add `from vine.models.transition import TransitionType` to test files
2. **Replace String Literals**:
   - `"fade"` → `TransitionType.FADE`
   - `"slide"` → `TransitionType.SLIDE`
   - `"zoom"` → `TransitionType.ZOOM`
3. **Update Test Fixtures**: Ensure all test data uses enum values

## Impact Assessment
- **Low Risk**: Test-only changes
- **No Breaking Changes**: API remains the same
- **Improved Type Safety**: Better compile-time checking

## Files to Update
- [ ] `tests/unit/test_video_spec_tracks.py`
- [ ] `tests/unit/test_transitions.py`
- [ ] `tests/unit/test_timeline_builder_tracks.py`
- [ ] `tests/unit/test_timeline_builder_edge_cases.py`
- [ ] `tests/unit/test_timeline_builder_comprehensive.py`
