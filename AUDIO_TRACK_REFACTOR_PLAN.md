# 🎵 Audio Track Refactor Implementation Plan

## 📋 Overview
Refactor TimelineBuilder to use separate audio tracks for music, voice, and SFX instead of generic audio tracks. This will provide better audio mixing control and clearer API intent.

---

## 🎯 Phase 1: Foundation & Defaults Setup

### ✅ 1.1 Update DefaultsManager
- [x] Add new default volume settings to `src/vine/defaults/defaults_manager.py`:
  ```python
  DEFAULT_MUSIC_VOLUME = 0.3    # Background music should be subtle
  DEFAULT_VOICE_VOLUME = 0.8    # Voice should be prominent
  DEFAULT_SFX_VOLUME = 0.5      # SFX should be noticeable but not overwhelming
  ```
- [x] Add method `get_audio_defaults()` that returns dict with all audio defaults
- [x] Add method `get_music_volume()`, `get_voice_volume()`, `get_sfx_volume()`

### ✅ 1.2 Update TimelineBuilder Constructor
- [x] Replace `self.audio_tracks` with separate track lists:
  ```python
  self.music_tracks: List[AudioTrack] = [AudioTrack(name="music_0")]
  self.voice_tracks: List[AudioTrack] = [AudioTrack(name="voice_0")]
  self.sfx_tracks: List[AudioTrack] = [AudioTrack(name="sfx_0")]
  ```
- [x] Add separate current time tracking:
  ```python
  self._music_current_time = 0.0
  self._voice_current_time = 0.0
  self._sfx_current_time = 0.0
  ```
- [x] Remove old `self.audio_tracks` and `self._audio_current_time`

### ✅ 1.3 Add Track Creation Methods
- [x] Create `_get_or_create_music_track()` method:
  ```python
  def _get_or_create_music_track(self) -> AudioTrack:
      """Get or create a music track for auto-detection."""
      for track in self.music_tracks:
          if not track.has_overlapping_clips():
              return track
      new_track = AudioTrack(name=f"music_{len(self.music_tracks)}")
      self.music_tracks.append(new_track)
      return new_track
  ```
- [x] Create `_get_or_create_voice_track()` method (same pattern)
- [x] Create `_get_or_create_sfx_track()` method (same pattern)

---

## 🎵 Phase 2: Core Audio Methods Implementation

### ✅ 2.1 Implement add_music_at()
- [x] Create method signature:
  ```python
  def add_music_at(
      self,
      music_path: Union[str, Path],
      start_time: float,
      duration: Optional[float] = None,
      end_time: Optional[float] = None,
      volume: Optional[float] = None,
      fade_in: float = 0.0,
      fade_out: float = 0.0,
      crossfade_duration: float = 0.5,
      auto_crossfade: bool = True,
      volume_curve: Optional[List[Tuple[float, float]]] = None,
      **kwargs,
  ) -> "TimelineBuilder":
  ```
- [x] Add file validation using MoviePy's audio file detection
- [x] Use `self.defaults.get_music_volume()` as default volume if none provided
- [x] Create AudioClip with professional controls and add to music track
- [x] Update `self._music_current_time`
- [x] Add comprehensive docstring with examples

### ✅ 2.2 Implement add_voice_at() (Updated)
- [x] Update existing method to use voice tracks instead of generic audio tracks
- [x] Change track selection from `_get_or_create_audio_track()` to `_get_or_create_voice_track()`
- [x] Use `self.defaults.get_voice_volume()` as default volume
- [x] Update `self._voice_current_time` instead of `self._audio_current_time`
- [x] Add professional controls to method signature:
  ```python
  def add_voice_at(
      self,
      voice_path: Union[str, Path],
      start_time: float,
      duration: Optional[float] = None,
      end_time: Optional[float] = None,
      volume: Optional[float] = None,
      fade_in: float = 0.0,
      fade_out: float = 0.0,
      crossfade_duration: float = 0.5,
      auto_crossfade: bool = True,
      volume_curve: Optional[List[Tuple[float, float]]] = None,
      **kwargs,
  ) -> "TimelineBuilder":
  ```

### ✅ 2.3 Implement add_sfx_at()
- [x] Create method signature:
  ```python
  def add_sfx_at(
      self,
      sfx_path: Union[str, Path],
      start_time: float,
      duration: Optional[float] = None,
      end_time: Optional[float] = None,
      volume: Optional[float] = None,
      fade_in: float = 0.0,
      fade_out: float = 0.0,
      crossfade_duration: float = 0.5,
      auto_crossfade: bool = True,
      volume_curve: Optional[List[Tuple[float, float]]] = None,
      **kwargs,
  ) -> "TimelineBuilder":
  ```
- [x] Add file validation using MoviePy's audio file detection
- [x] Use `self.defaults.get_sfx_volume()` as default volume
- [x] Create AudioClip with professional controls and add to sfx track
- [x] Update `self._sfx_current_time`
- [x] Add comprehensive docstring with examples

### ✅ 2.4 Add File Validation Helper
- [x] Create `_validate_audio_file(file_path: str) -> bool` method
- [x] Use MoviePy's `AudioFileClip` to test if file is valid audio
- [x] Return True if file can be loaded as audio, False otherwise
- [x] Add proper error handling for missing files, corrupted files, etc.

### ✅ 2.5 Implement Professional Audio Controls
- [x] Extend AudioClip model to support professional controls:
  ```python
  class AudioClip:
      fade_in: float = 0.0
      fade_out: float = 0.0
      crossfade_duration: float = 0.5
      auto_crossfade: bool = True
      normalize_audio: bool = False
      volume_curve: Optional[List[Tuple[float, float]]] = None
  ```
- [x] Add volume curve validation and processing
- [x] Implement fade effect application during rendering using MoviePy's AudioFadeIn/AudioFadeOut
- [x] Add audio normalization using MoviePy's AudioNormalize
- [x] Add custom volume curve support using MoviePy's with_volume_function

---

## 🔄 Phase 3: Sequential Methods Implementation

### ✅ 3.1 Implement add_music()
- [x] Create sequential version that appends to end of music track
- [x] Use `self._music_current_time` for start time
- [x] Update `self._music_current_time` after adding clip
- [x] Handle duration inheritance from `self._next_duration`

### ✅ 3.2 Update add_voice() (Existing)
- [x] Change to use voice tracks instead of generic audio tracks
- [x] Update to use `self._voice_current_time` instead of `self._audio_current_time`
- [x] Keep same method signature

### ✅ 3.3 Implement add_sfx()
- [x] Create sequential version that appends to end of sfx track
- [x] Use `self._sfx_current_time` for start time
- [x] Update `self._sfx_current_time` after adding clip
- [x] Handle duration inheritance from `self._next_duration`

---

## 📊 Phase 4: Track Management & Utilities

### ✅ 4.1 Update get_track_count()
- [x] Replace existing method to return new track types:
  ```python
  def get_track_count(self) -> Dict[str, int]:
      return {
          "video": len(self.video_tracks),
          "music": len(self.music_tracks),
          "voice": len(self.voice_tracks),
          "sfx": len(self.sfx_tracks),
          "text": len(self.text_tracks)
      }
  ```

### ✅ 4.2 Update get_clip_count()
- [x] Update to count clips across all new track types
- [x] Return dict with counts for each track type

### ✅ 4.3 Update get_duration()
- [x] Ensure method considers all new track types when calculating max duration
- [x] Update `_get_max_end_time_from_tracks()` to handle new track lists

### ✅ 4.4 Update clear() method
- [x] Reset all new track lists to initial state
- [x] Reset all new current times to 0.0
- [x] Remove old audio track references

---

## 🎬 Phase 5: Rendering Integration

### ✅ 5.1 Update build() method
- [x] Ensure VideoSpec creation includes all new track types
- [x] Verify all audio tracks are properly included in the spec
- [x] Test that spec contains correct track information

### ✅ 5.2 Update render() method
- [x] Ensure MoviePy integration works with new track structure
- [x] Verify audio mixing works correctly with separate tracks
- [x] Test that all audio types are properly combined

### ✅ 5.3 Update export() method
- [x] Ensure video export works with new audio track structure
- [x] Verify audio codec settings work correctly
- [x] Test that volume levels are preserved during export

---

## 🧪 Phase 6: Testing & Validation

### ✅ 6.1 Update Existing Tests
- [x] Update `test_timeline_builder_comprehensive.py` to test new methods
- [x] Update `test_timeline_builder_edge_cases.py` for new track behavior
- [x] Update `test_timeline_builder_tracks.py` for new track types
- [x] Ensure all existing tests pass with new implementation

### ✅ 6.2 Add New Test Cases
- [x] Test `add_music_at()` with various audio files
- [x] Test `add_sfx_at()` with short and long audio files
- [x] Test volume defaults are applied correctly
- [x] Test file validation rejects non-audio files
- [x] Test track creation and management
- [x] Test sequential methods work correctly

### ✅ 6.3 Integration Testing
- [x] Test complete video creation with all three audio types
- [x] Test audio mixing with multiple tracks of each type
- [x] Test volume control across different track types
- [x] Test export functionality with new track structure

---

## 📝 Phase 7: Documentation & Examples

### ✅ 7.1 Update API Documentation
- [x] Update TimelineBuilder docstring to reflect new audio methods
- [x] Add comprehensive docstrings for all new methods
- [x] Include usage examples for each audio type
- [x] Document volume defaults and track behavior

### ✅ 7.2 Update Framework Guide
- [x] Update `docs/VINE_FRAMEWORK_GUIDE.md` with new audio methods
- [x] Add examples showing music, voice, and SFX usage
- [x] Update Coffee Shop Dreams example to use new methods
- [x] Add section explaining audio track separation benefits

### ✅ 7.3 Update Examples
- [x] Update `examples/motivational_short.py` to use new methods
- [x] Update `examples/simple_shorts_video.py` to use new methods
- [x] Update `examples/create_shorts_video.py` to use new methods
- [x] Create new example showing all three audio types together

---

## 🔧 Phase 8: Adobe-Style Overlap Handling

### ✅ 8.1 Adobe-Style Track Behavior
- [x] Allow overlaps within same track type (music with music, voice with voice, SFX with SFX)
- [x] Different track types remain separate but mix in final output
- [x] Implementation: Modify `_get_or_create_*_track()` to allow overlaps on same track

### ✅ 8.2 Pure MoviePy Mixing Strategy
- [x] Let MoviePy handle all audio mixing automatically
- [x] No custom mixing algorithms needed
- [x] MoviePy handles volume mixing, clipping prevention, normalization
- [x] Implementation: Use MoviePy's `CompositeAudioClip` for final mixing

### ✅ 8.3 Custom Professional Controls
- [x] Add `fade_in` and `fade_out` parameters to audio methods
- [x] Add `crossfade_duration` for automatic crossfades between adjacent clips
- [x] Add `volume_curve` for custom volume envelopes
- [ ] Implementation: Extend AudioClip model with professional controls

### ✅ 8.4 Automatic Crossfade Detection
- [x] Detect adjacent clips on same track
- [x] Apply automatic crossfades based on overlap duration
- [x] Allow user to disable automatic crossfades
- [x] Implementation: Use MoviePy's CompositeAudioClip for automatic mixing and crossfades

### ✅ 8.5 Track Organization Strategy
- [x] Music tracks: Allow overlaps, MoviePy mixes
- [x] Voice tracks: Allow overlaps, MoviePy mixes
- [x] SFX tracks: Allow overlaps, MoviePy mixes
- [x] Cross-track: All audio types mix in final output via MoviePy

---

## 🚀 Phase 9: Final Integration

### ✅ 9.1 Remove Old Audio System
- [x] Remove `self.audio_tracks` completely
- [x] Remove `self._audio_current_time`
- [x] Remove old `_get_or_create_audio_track()` method
- [x] Clean up any remaining references to old audio system

### ✅ 9.2 Performance Testing
- [x] Test performance with large numbers of audio clips
- [x] Test memory usage with complex audio mixing
- [x] Ensure no performance regressions from new track system

### ✅ 9.3 Final Validation
- [x] Run all existing examples to ensure they work
- [x] Test with various audio file formats
- [x] Verify all documentation is accurate
- [x] Ensure no breaking changes to public API (except intended ones)

---

## 📋 Implementation Notes

### Adobe-Style Track Behavior
- Allow overlaps within same track type (music with music, voice with voice, SFX with SFX)
- Different track types remain separate but mix in final output
- MoviePy handles all audio mixing automatically
- Professional audio workflow with intuitive behavior

### File Validation Strategy
- Use MoviePy's `AudioFileClip` to test file validity
- Catch exceptions and provide clear error messages
- Support all MoviePy audio formats (mp3, wav, aac, etc.)

### Default Volumes
- Music: 0.3 (subtle background)
- Voice: 0.8 (prominent narration)
- SFX: 0.5 (noticeable effects)

### Professional Audio Controls
- `fade_in`: Duration of fade-in effect (default: 0.0)
- `fade_out`: Duration of fade-out effect (default: 0.0)
- `crossfade_duration`: Automatic crossfade with adjacent clips (default: 0.5)
- `volume_curve`: Custom volume envelope (advanced feature)
- `auto_crossfade`: Enable/disable automatic crossfades (default: True)

### Track Naming Convention
- Music: "music_0", "music_1", etc.
- Voice: "voice_0", "voice_1", etc.
- SFX: "sfx_0", "sfx_1", etc.

### Error Handling
- Clear error messages for invalid audio files
- Graceful handling of missing files
- Informative messages about track creation
- Professional error messages for audio mixing issues

---

## 🎯 Success Criteria

- [x] All existing examples work with new audio system
- [x] Adobe-style overlap behavior works correctly (same track type = mix, different = separate)
- [x] MoviePy handles all audio mixing automatically
- [x] Professional controls (fade_in, fade_out, crossfade_duration) work correctly
- [x] Default volumes are applied correctly per track type
- [x] File validation works for all supported audio formats
- [x] Track management is efficient and intuitive
- [x] Automatic crossfade detection works for adjacent clips
- [x] Documentation is comprehensive and accurate
- [x] No performance regressions
- [x] All tests pass

---

## ⚠️ Breaking Changes

- `add_voice_at()` now uses voice tracks instead of generic audio tracks
- `get_track_count()` returns different track types
- Old `audio_tracks` are completely removed
- Sequential audio methods now use track-specific current times

---

## 🚀 Next Steps

1. ✅ Start with Phase 1 (Foundation & Defaults) - COMPLETE
2. ✅ Implement phases sequentially - COMPLETE
3. ✅ Test thoroughly at each phase - COMPLETE
4. ✅ Update documentation as we go - COMPLETE
5. ✅ Final integration and validation - COMPLETE

**Estimated Timeline: 2-3 days for complete implementation**

## 📊 Current Status Summary

### ✅ **COMPLETED (95%)**
- **Phase 1**: Foundation & Defaults Setup - 100% Complete
- **Phase 2**: Core Audio Methods Implementation - 100% Complete
- **Phase 3**: Sequential Methods Implementation - 100% Complete
- **Phase 4**: Track Management & Utilities - 100% Complete
- **Phase 5**: Rendering Integration - 100% Complete
- **Phase 6**: Testing & Validation - 100% Complete
- **Phase 8**: Adobe-Style Overlap Handling - 100% Complete
- **Phase 9**: Final Integration - 100% Complete

### ✅ **COMPLETED (100%)**
- **Phase 7**: Documentation & Examples - 100% Complete

### 🎯 **MOVIEPY INTEGRATION HIGHLIGHTS**
1. **AudioFadeIn/AudioFadeOut**: Using MoviePy's built-in fade effects
2. **AudioNormalize**: Using MoviePy's audio normalization
3. **CompositeAudioClip**: Using MoviePy's automatic audio mixing and crossfades
4. **with_volume_function**: Using MoviePy's custom volume curve support
5. **with_effects**: Using MoviePy's effect chaining system

**Overall Progress: 100% Complete** 🎉
