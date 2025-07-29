# 🎯 Call-Arg Error Fix Plan

## 📊 Error Analysis Summary

**Total Errors**: 1,228 call-arg errors across 17 files (reduced from 1,276 by removing unused enable_video/enable_audio fields)
**Main Categories**:
1. **VideoSpec** missing required fields (most errors)
2. **Track models** missing required fields
3. **Clip models** missing required fields
4. **Config models** missing required fields
5. **Transition/Effect models** missing required fields

## 🎯 Systematic Fix Strategy

### Phase 1: Add Sensible Defaults to Core Models

#### 1.1 VideoSpec Model (Priority: HIGH)
**File**: `src/vine/models/video_spec.py`
**Issue**: Many required fields missing sensible defaults
**Solution**: Add defaults for commonly omitted fields

**Fields to add defaults for**:
- `description`: `None` (already Optional)
- `author`: `None` (already Optional)
- `duration`: `None` (already Optional)
- `voice_config`: `None` (already Optional)
- `music_config`: `None` (already Optional)
- `output_path`: `None` (already Optional)

**Fields that need defaults**:
- `output_format`: `"mp4"`
- `quality`: `"high"`
- `background_color`: `"#000000"`

#### 1.2 Track Models (Priority: HIGH)
**File**: `src/vine/models/tracks.py`

**VideoTrack**:
- `z_order`: `0` (already has default)
- `visible`: `True` (already has default)

**AudioTrack**:
- `volume`: `1.0` (already has default)
- `muted`: `False` (already has default)

**TextTrack**:
- `z_order`: `0` (already has default)
- `visible`: `True` (already has default)

#### 1.3 Clip Models (Priority: HIGH)
**File**: `src/vine/models/tracks.py`

**VideoClip/ImageClip**:
- `end_time`: `None` (already Optional)
- `width`: `None` (already Optional)
- `height`: `None` (already Optional)
- `x_position`: `0.0` (already has default)
- `y_position`: `0.0` (already has default)
- `opacity`: `1.0` (already has default)

**TextClip**:
- `end_time`: `None` (already Optional)
- `font_size`: `48` (already has default)
- `font_color`: `"#FFFFFF"` (already has default)
- `font_family`: `"Arial"` (already has default)
- `font_weight`: `"normal"` (already has default)
- `x_position`: `0.0` (already has default)
- `y_position`: `0.0` (already has default)
- `alignment`: `"center"` (already has default)
- `opacity`: `1.0` (already has default)

**AudioClip**:
- `end_time`: `None` (already Optional)
- `volume`: `1.0` (already has default)
- `fade_in`: `0.0` (already has default)
- `fade_out`: `0.0` (already has default)
- `crossfade_duration`: `0.5` (already has default)
- `auto_crossfade`: `True` (already has default)
- `normalize_audio`: `False` (already has default)
- `volume_curve`: `None` (already Optional)
- `voice_config`: `None` (already Optional)
- `music_config`: `None` (already Optional)

### Phase 2: Fix Config Models

#### 2.1 Audio Config Models (Priority: MEDIUM)
**File**: `src/vine/models/audio_config.py`

**VoiceConfig**:
- `fade_out`: `None` (already Optional)
- `start_time`: `None` (already Optional)
- `end_time`: `None` (already Optional)
- `speed`: `1.0` (already has default)
- `pitch`: `1.0` (already has default)

**MusicConfig**:
- `fade_in`: `None` (already Optional)
- `fade_out`: `None` (already Optional)
- `start_time`: `None` (already Optional)
- `end_time`: `None` (already Optional)
- `loop`: `False` (already has default)
- `duck_voice`: `True` (already has default)
- `duck_level`: `0.3` (already has default)

#### 2.2 Animation Config Models (Priority: MEDIUM)
**File**: `src/vine/models/animation_config.py`

**AnimationConfig**:
- `duration`: `None` (already Optional)
- `easing`: `"ease_in_out"` (already has default)

**KenBurnsConfig**:
- `duration`: `None` (already Optional)
- `start_time`: `0.0` (already has default)
- `zoom_factor`: `1.2` (already has default)
- `pan_x`: `0.0` (already has default)
- `pan_y`: `0.0` (already has default)
- `easing`: `"ease_in_out"` (already has default)

### Phase 3: Fix Transition and Effect Models

#### 3.1 Transition Models (Priority: MEDIUM)
**File**: `src/vine/models/transition.py`

**Transition**:
- `direction`: `TransitionDirection.IN` (already has default)
- `easing`: `TransitionEasing.LINEAR` (already has default)

**File**: `src/vine/models/transitions.py`

**FadeConfig**:
- `duration`: `1.0` (already has default)
- `easing`: `"ease_in_out"` (already has default)
- `fade_type`: `"cross"` (already has default)

**CrossfadeConfig**:
- `duration`: `1.0` (already has default)
- `easing`: `"ease_in_out"` (already has default)
- `overlap`: `0.5` (already has default)

**SlideTransitionConfig**:
- `duration`: `1.0` (already has default)
- `easing`: `"ease_in_out"` (already has default)
- `direction`: `"left"` (already has default)
- `distance`: `100.0` (already has default)

#### 3.2 Effect Models (Priority: MEDIUM)
**File**: `src/vine/models/effects.py`

**KenBurnsConfig**:
- `duration`: `None` (already Optional)
- `start_time`: `0.0` (already has default)
- `zoom_factor`: `1.2` (already has default)
- `pan_x`: `0.0` (already has default)
- `pan_y`: `0.0` (already has default)
- `easing`: `"ease_in_out"` (already has default)

**SlideConfig**:
- `duration`: `None` (already Optional)
- `start_time`: `0.0` (already has default)
- `direction`: `"left"` (already has default)
- `distance`: `100.0` (already has default)
- `easing`: `"ease_in_out"` (already has default)

### Phase 4: Fix MoviePy Integration Issues

#### 4.1 Clip Factory Issues (Priority: HIGH)
**File**: `src/vine/rendering/clip_factory.py`
**Issues**:
- AudioFadeIn/AudioFadeOut/AudioNormalize missing `clip` argument
- AudioFileClip too many arguments
- TextClip unexpected keyword arguments

#### 4.2 Renderer Issues (Priority: HIGH)
**Files**:
- `src/vine/rendering/moviepy_adapter.py`
- `src/vine/rendering/audio_renderer.py`
- `src/vine/rendering/video_renderer.py`
- `src/vine/rendering/text_renderer.py`

**Issues**:
- CompositeVideoClip/CompositeAudioClip too many arguments
- ColorClip unexpected keyword arguments

## 🚀 Execution Plan

### Step 1: Fix Model Defaults
1. Update VideoSpec model with missing defaults
2. Verify all track and clip models have proper defaults
3. Update config models with missing defaults
4. Update transition and effect models with missing defaults

### Step 2: Fix MoviePy Integration
1. Fix clip_factory.py MoviePy function calls
2. Fix renderer MoviePy function calls
3. Update stubs if needed

### Step 3: Update Tests
1. Update test files to use proper defaults
2. Remove unnecessary explicit arguments where defaults are sufficient

### Step 4: Verify
1. Run MyPy to confirm errors are resolved
2. Run tests to ensure functionality is preserved

## 📈 Expected Results

After implementing this plan:
- **Reduction**: From 1,228 errors to ~0-50 errors
- **Remaining errors**: Likely only MoviePy stub issues
- **Maintainability**: Better default values for common use cases
- **Developer Experience**: Easier to create valid specs without remembering all defaults

## 🎯 Success Criteria

- [ ] MyPy shows 0 call-arg errors
- [ ] All tests pass
- [ ] No breaking changes to existing functionality
- [ ] Sensible defaults for common use cases
