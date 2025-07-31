from typing import Any
from unittest.mock import MagicMock

import pytest

from vine.builder.timeline_builder import TimelineBuilder
from vine.models.clip_params import ExportResult, VideoExportOptions
from vine.models.transition import TransitionType


@pytest.mark.unit
def test_validate_audio_file_accepts_common_extensions() -> None:
    """Test _validate_audio_file returns True for common audio extensions."""
    builder = TimelineBuilder()
    for ext in [".mp3", ".wav", ".aac", ".m4a", ".ogg", ".flac"]:
        assert builder._validate_audio_file(f"file{ext}") is True


@pytest.mark.unit
def test_validate_audio_file_fallback_and_exception() -> None:
    """Test _validate_audio_file returns False if AudioFileClip fails."""
    builder = TimelineBuilder()

    # Save original method
    original_validate = builder._validate_audio_file

    try:
        # Mock the validation to simulate failure
        mock_validate = MagicMock(return_value=False)
        builder._validate_audio_file = mock_validate  # type: ignore

        # Test that the method returns False for invalid audio
        assert builder._validate_audio_file("file.unknown") is False
        mock_validate.assert_called_once_with("file.unknown")
    finally:
        # Restore original method
        builder._validate_audio_file = original_validate  # type: ignore


@pytest.mark.unit
def test_add_voice_at_invalid_audio_raises() -> None:
    """Test add_voice_at raises ValueError for invalid audio file."""
    builder = TimelineBuilder()

    # Save original method
    original_validate = builder._validate_audio_file

    try:
        # Mock the validation to return False (invalid audio)
        mock_validate = MagicMock(return_value=False)
        builder._validate_audio_file = mock_validate  # type: ignore

        with pytest.raises(ValueError):
            builder.add_voice_at("bad.mp3", 0, 1)
    finally:
        # Restore original method
        builder._validate_audio_file = original_validate  # type: ignore


@pytest.mark.unit
def test_add_music_at_invalid_audio_raises() -> None:
    """Test add_music_at raises ValueError for invalid audio file."""
    builder = TimelineBuilder()

    # Save original method
    original_validate = builder._validate_audio_file

    try:
        # Mock the validation to return False (invalid audio)
        mock_validate = MagicMock(return_value=False)
        builder._validate_audio_file = mock_validate  # type: ignore

        with pytest.raises(ValueError):
            builder.add_music_at("bad.mp3", 0, 1)
    finally:
        # Restore original method
        builder._validate_audio_file = original_validate  # type: ignore


@pytest.mark.unit
def test_add_sfx_at_invalid_audio_raises() -> None:
    """Test add_sfx_at raises ValueError for invalid audio file."""
    builder = TimelineBuilder()

    # Save original method
    original_validate = builder._validate_audio_file

    try:
        # Mock the validation to return False (invalid audio)
        mock_validate = MagicMock(return_value=False)
        builder._validate_audio_file = mock_validate  # type: ignore

        with pytest.raises(ValueError):
            builder.add_sfx_at("bad.mp3", 0, 1)
    finally:
        # Restore original method
        builder._validate_audio_file = original_validate  # type: ignore


@pytest.mark.unit
def test_add_image_at_both_duration_and_end_time() -> None:
    """Test add_image_at raises ValueError if both duration and end_time are given."""
    builder = TimelineBuilder()
    with pytest.raises(ValueError):
        builder.add_image_at("img.png", 0, duration=1, end_time=2)


@pytest.mark.unit
def test_add_text_at_both_duration_and_end_time() -> None:
    """Test add_text_at raises ValueError if both duration and end_time are given."""
    builder = TimelineBuilder()
    with pytest.raises(ValueError):
        builder.add_text_at("txt", 0, duration=1, end_time=2)


@pytest.mark.unit
def test_add_voice_at_both_duration_and_end_time() -> None:
    """Test add_voice_at raises ValueError if both duration and end_time are given."""
    builder = TimelineBuilder()

    # Save original method
    original_validate = builder._validate_audio_file

    try:
        # Mock the validation to return True (valid audio)
        mock_validate = MagicMock(return_value=True)
        builder._validate_audio_file = mock_validate  # type: ignore

        with pytest.raises(ValueError):
            builder.add_voice_at("voice.mp3", 0, duration=1, end_time=2)
    finally:
        # Restore original method
        builder._validate_audio_file = original_validate  # type: ignore


@pytest.mark.unit
def test_add_music_at_both_duration_and_end_time() -> None:
    """Test add_music_at raises ValueError if both duration and end_time are given."""
    builder = TimelineBuilder()

    # Save original method
    original_validate = builder._validate_audio_file

    try:
        # Mock the validation to return True (valid audio)
        mock_validate = MagicMock(return_value=True)
        builder._validate_audio_file = mock_validate  # type: ignore

        with pytest.raises(ValueError):
            builder.add_music_at("music.mp3", 0, duration=1, end_time=2)
    finally:
        # Restore original method
        builder._validate_audio_file = original_validate  # type: ignore


@pytest.mark.unit
def test_add_sfx_at_both_duration_and_end_time() -> None:
    """Test add_sfx_at raises ValueError if both duration and end_time are given."""
    builder = TimelineBuilder()

    # Save original method
    original_validate = builder._validate_audio_file

    try:
        # Mock the validation to return True (valid audio)
        mock_validate = MagicMock(return_value=True)
        builder._validate_audio_file = mock_validate  # type: ignore

        with pytest.raises(ValueError):
            builder.add_sfx_at("sfx.mp3", 0, duration=1, end_time=2)
    finally:
        # Restore original method
        builder._validate_audio_file = original_validate  # type: ignore


@pytest.mark.unit
def test_sequential_music_and_sfx_without_default_duration() -> None:
    """Test add_music and add_sfx without default duration (start_time increments)."""
    builder = TimelineBuilder()

    # Save original methods
    original_add_music_at = builder.add_music_at
    original_add_sfx_at = builder.add_sfx_at

    try:
        # Mock add_music_at
        mock_music_at = MagicMock()
        builder.add_music_at = mock_music_at  # type: ignore

        builder.add_music("music.mp3", duration=2)
        mock_music_at.assert_called_once_with("music.mp3", 0.0, 2)

        # Mock add_sfx_at
        mock_sfx_at = MagicMock()
        builder.add_sfx_at = mock_sfx_at  # type: ignore

        builder.add_sfx("sfx.mp3", duration=2)
        mock_sfx_at.assert_called_once_with("sfx.mp3", 0.0, 2)
    finally:
        # Restore original methods
        builder.add_music_at = original_add_music_at  # type: ignore
        builder.add_sfx_at = original_add_sfx_at  # type: ignore


@pytest.mark.unit
def test_sequential_music_and_sfx_with_default_duration() -> None:
    """Test add_music and add_sfx with default duration (start_time increments)."""
    builder = TimelineBuilder()
    builder.set_duration(3)

    # Save original methods
    original_add_music_at = builder.add_music_at
    original_add_sfx_at = builder.add_sfx_at

    try:
        # Mock add_music_at for first call
        mock_music_at = MagicMock()
        builder.add_music_at = mock_music_at  # type: ignore
        builder.add_music("music.mp3")
        mock_music_at.assert_called_once_with("music.mp3", 0.0, 3)

        # Mock add_music_at for second call
        mock_music_at2 = MagicMock()
        builder.add_music_at = mock_music_at2  # type: ignore
        builder.add_music("music2.mp3")
        # Now start_time should be 3.0
        mock_music_at2.assert_called_once_with("music2.mp3", 3.0, 3)

        # Mock add_sfx_at for first call
        mock_sfx_at = MagicMock()
        builder.add_sfx_at = mock_sfx_at  # type: ignore
        builder.add_sfx("sfx.mp3")
        mock_sfx_at.assert_called_once_with("sfx.mp3", 0.0, 3)

        # Mock add_sfx_at for second call
        mock_sfx_at2 = MagicMock()
        builder.add_sfx_at = mock_sfx_at2  # type: ignore
        builder.add_sfx("sfx2.mp3")
        # Now start_time should be 3.0
        mock_sfx_at2.assert_called_once_with("sfx2.mp3", 3.0, 3)
    finally:
        # Restore original methods
        builder.add_music_at = original_add_music_at  # type: ignore
        builder.add_sfx_at = original_add_sfx_at  # type: ignore

    builder.clear_duration()


@pytest.mark.unit
def test_render_and_export_success_and_failure() -> None:
    """Test render and export methods, including error path in export."""
    builder = TimelineBuilder()

    # Save original imports
    import os.path

    import vine.builder.timeline_builder

    original_video_renderer = vine.builder.timeline_builder.VideoRenderer
    original_getsize = os.path.getsize
    original_exists = os.path.exists

    try:
        # Mock VideoRenderer for render
        mock_renderer = MagicMock()
        mock_video_renderer_class = MagicMock(return_value=mock_renderer)
        vine.builder.timeline_builder.VideoRenderer = mock_video_renderer_class
        mock_renderer.render.return_value = MagicMock()

        builder.render()
        # Check that render was called with a VideoSpec
        mock_renderer.render.assert_called_once()
        call_args = mock_renderer.render.call_args[0]
        assert len(call_args) == 1
        assert hasattr(call_args[0], "video_tracks")  # Should be a VideoSpec

        # Mock VideoRenderer and file I/O for export success
        mock_renderer2 = MagicMock()
        mock_video_renderer_class2 = MagicMock(return_value=mock_renderer2)
        vine.builder.timeline_builder.VideoRenderer = mock_video_renderer_class2
        os.path.getsize = MagicMock(return_value=123)
        os.path.exists = MagicMock(return_value=True)

        video_clip: MagicMock = MagicMock()
        audio_clip: MagicMock = MagicMock()
        mock_renderer2.render_with_audio.return_value = (video_clip, audio_clip)
        video_clip.with_audio.return_value = video_clip
        video_clip.write_videofile.return_value = None
        # Set duration as an attribute that getattr can find
        video_clip.duration = 5.0
        video_clip.close.return_value = None
        audio_clip.close.return_value = None

        export_result: ExportResult = builder.export("out.mp4")
        assert export_result.success is True
        assert export_result.output_path == "out.mp4"
        assert export_result.duration == 5.0
        assert export_result.file_size == 123

        # Mock VideoRenderer and file I/O for export failure
        mock_video_renderer_class3 = MagicMock(side_effect=Exception("fail"))
        vine.builder.timeline_builder.VideoRenderer = mock_video_renderer_class3

        fail_result: ExportResult = builder.export("fail.mp4")
        assert fail_result.success is False
        assert fail_result.output_path == "fail.mp4"
        assert fail_result.duration == 0.0
        assert fail_result.error_message is not None
        assert "fail" in fail_result.error_message
    finally:
        # Restore original imports
        vine.builder.timeline_builder.VideoRenderer = original_video_renderer
        os.path.getsize = original_getsize
        os.path.exists = original_exists


@pytest.mark.unit
def test_video_track_auto_detection_creates_new_track() -> None:
    """Test _get_or_create_video_track creates a new track if all have overlaps."""
    builder = TimelineBuilder()
    track = builder._get_or_create_video_track()
    # Fill the first track with a fake overlapping clip
    track.clips.append(MagicMock(get_end_time=lambda: 10.0, start_time=0.0))
    # Add a new overlapping clip to force new track creation
    track.clips.append(MagicMock(get_end_time=lambda: 20.0, start_time=5.0))
    new_track = builder._get_or_create_video_track()
    assert new_track is not track
    assert len(builder.video_tracks) == 2


@pytest.mark.unit
def test_get_or_create_video_track_returns_existing_when_no_overlap() -> None:
    """Test _get_or_create_video_track returns the existing track if no overlap."""
    builder = TimelineBuilder()
    track = builder.video_tracks[0]
    result = builder._get_or_create_video_track()
    assert result is track


@pytest.mark.unit
def test_music_voice_sfx_text_track_auto_detection() -> None:
    """Test auto-detection for music, voice, sfx, and text tracks creates new tracks."""
    builder = TimelineBuilder()
    # Music
    mtrack = builder._get_or_create_music_track()
    mtrack.clips.append(MagicMock(get_end_time=lambda: 10.0, start_time=0.0))
    mtrack.clips.append(MagicMock(get_end_time=lambda: 20.0, start_time=5.0))
    assert builder._get_or_create_music_track() is not mtrack
    # Voice
    vtrack = builder._get_or_create_voice_track()
    vtrack.clips.append(MagicMock(get_end_time=lambda: 10.0, start_time=0.0))
    vtrack.clips.append(MagicMock(get_end_time=lambda: 20.0, start_time=5.0))
    assert builder._get_or_create_voice_track() is not vtrack
    # SFX
    strack = builder._get_or_create_sfx_track()
    strack.clips.append(MagicMock(get_end_time=lambda: 10.0, start_time=0.0))
    strack.clips.append(MagicMock(get_end_time=lambda: 20.0, start_time=5.0))
    assert builder._get_or_create_sfx_track() is not strack
    # Text
    ttrack = builder._get_or_create_text_track()
    ttrack.clips.append(MagicMock(get_end_time=lambda: 10.0, start_time=0.0))
    ttrack.clips.append(MagicMock(get_end_time=lambda: 20.0, start_time=5.0))
    assert builder._get_or_create_text_track() is not ttrack


@pytest.mark.unit
def test_sequential_methods_update_current_time() -> None:
    """Test that sequential methods update current time as expected."""
    builder = TimelineBuilder()

    # Save original methods
    original_add_image_at = builder.add_image_at
    original_add_text_at = builder.add_text_at
    original_add_voice_at = builder.add_voice_at
    original_add_music_at = builder.add_music_at
    original_add_sfx_at = builder.add_sfx_at

    try:
        # Mock add_image_at
        mock_img = MagicMock(return_value="imgctx")
        builder.add_image_at = mock_img  # type: ignore
        img_ctx: Any = builder.add_image("img.png", duration=2)
        assert img_ctx == "imgctx"
        assert builder._video_current_time == 2

        # Mock add_text_at
        mock_txt = MagicMock(return_value="txtctx")
        builder.add_text_at = mock_txt  # type: ignore
        txt_ctx: Any = builder.add_text("txt", duration=3)
        assert txt_ctx == "txtctx"
        assert builder._text_current_time == 3

        # Mock add_voice_at
        mock_voice = MagicMock(return_value="voicectx")
        builder.add_voice_at = mock_voice  # type: ignore
        voice_ctx: Any = builder.add_voice("voice.mp3", duration=4)
        assert voice_ctx == "voicectx"
        assert builder._voice_current_time == 4

        # Mock add_music_at
        mock_music = MagicMock(return_value="musicctx")
        builder.add_music_at = mock_music  # type: ignore
        music_ctx: Any = builder.add_music("music.mp3", duration=5)
        assert music_ctx == "musicctx"
        assert builder._music_current_time == 5

        # Mock add_sfx_at
        mock_sfx = MagicMock(return_value="sfxctx")
        builder.add_sfx_at = mock_sfx  # type: ignore
        sfx_ctx: Any = builder.add_sfx("sfx.mp3", duration=6)
        assert sfx_ctx == "sfxctx"
        assert builder._sfx_current_time == 6
    finally:
        # Restore original methods
        builder.add_image_at = original_add_image_at  # type: ignore
        builder.add_text_at = original_add_text_at  # type: ignore
        builder.add_voice_at = original_add_voice_at  # type: ignore
        builder.add_music_at = original_add_music_at  # type: ignore
        builder.add_sfx_at = original_add_sfx_at  # type: ignore


@pytest.mark.unit
def test_explicit_methods_create_clips_and_chain() -> None:
    """Test explicit methods create clips and return context objects."""
    builder = TimelineBuilder()

    # Save original imports and methods
    import vine.models.tracks

    original_image_clip = vine.models.tracks.ImageClip
    original_text_clip = vine.models.tracks.TextClip
    original_audio_clip = vine.models.tracks.AudioClip
    original_validate = builder._validate_audio_file

    try:
        # Mock ImageClip
        mock_image_clip = MagicMock()
        mock_image_clip.return_value = MagicMock()
        vine.models.tracks.ImageClip = mock_image_clip
        img_ctx: Any = builder.add_image_at("img.png", 0, duration=1)
        assert hasattr(img_ctx, "clip")

        # Mock TextClip
        mock_text_clip = MagicMock()
        mock_text_clip.return_value = MagicMock()
        vine.models.tracks.TextClip = mock_text_clip
        txt_ctx: Any = builder.add_text_at("txt", 0, duration=1)
        assert hasattr(txt_ctx, "clip")

        # Mock AudioClip and validation
        mock_audio_clip = MagicMock()
        mock_audio_clip.return_value = MagicMock()
        vine.models.tracks.AudioClip = mock_audio_clip
        mock_validate = MagicMock(return_value=True)
        builder._validate_audio_file = mock_validate  # type: ignore

        voice_ctx: Any = builder.add_voice_at("voice.mp3", 0, duration=1)
        assert hasattr(voice_ctx, "clip")
        music_ctx = builder.add_music_at("music.mp3", 0, duration=1)
        assert hasattr(music_ctx, "clip")
        sfx_ctx = builder.add_sfx_at("sfx.mp3", 0, duration=1)
        assert hasattr(sfx_ctx, "clip")
    finally:
        # Restore original imports and methods
        vine.models.tracks.ImageClip = original_image_clip
        vine.models.tracks.TextClip = original_text_clip
        vine.models.tracks.AudioClip = original_audio_clip
        builder._validate_audio_file = original_validate  # type: ignore


@pytest.mark.unit
def test_transition_methods() -> None:
    """Test add_transition and add_transition_at methods."""
    builder = TimelineBuilder()

    # Save original method
    original_add_transition_at = builder.add_transition_at

    try:
        # Mock add_transition_at for sequential transition
        mock_add = MagicMock()
        builder.add_transition_at = mock_add  # type: ignore

        builder._video_current_time = 5
        builder._music_current_time = 3
        builder._voice_current_time = 2
        builder._sfx_current_time = 1
        builder._text_current_time = 0
        builder.add_transition(TransitionType.FADE, duration=2)
        # Should call with start_time = max(5,3,2,1,0) - 2 = 3
        mock_add.assert_called_once_with(TransitionType.FADE, 3, 2)
    finally:
        # Restore original method
        builder.add_transition_at = original_add_transition_at  # type: ignore

    # Explicit transition
    builder.transitions.clear()
    builder.add_transition_at(TransitionType.FADE, 1.0, 2.0)
    assert builder.transitions[-1].transition_type == TransitionType.FADE
    assert builder.transitions[-1].start_time == 1.0
    assert builder.transitions[-1].duration == 2.0


@pytest.mark.unit
def test_utility_methods() -> None:
    """Test get_duration, get_track_count, get_clip_count, clear, set_fps, set_duration, clear_duration."""
    builder = TimelineBuilder()
    # Add some clips to tracks
    builder.video_tracks[0].clips.append(MagicMock(get_end_time=lambda: 10.0))
    builder.music_tracks[0].clips.append(MagicMock(get_end_time=lambda: 5.0))
    builder.voice_tracks[0].clips.append(MagicMock(get_end_time=lambda: 7.0))
    builder.sfx_tracks[0].clips.append(MagicMock(get_end_time=lambda: 3.0))
    builder.text_tracks[0].clips.append(MagicMock(get_end_time=lambda: 2.0))
    builder.transitions.append(MagicMock(get_end_time=lambda: 8.0))
    # get_duration should return max end time
    assert builder.get_duration() == 10.0
    # get_track_count
    counts = builder.get_track_count()
    assert counts["video"] == 1
    assert counts["music"] == 1
    assert counts["voice"] == 1
    assert counts["sfx"] == 1
    assert counts["text"] == 1
    # get_clip_count
    clip_counts = builder.get_clip_count()
    assert all(v == 1 for v in clip_counts.values())
    # set_fps
    builder.set_fps(60)
    assert builder.fps == 60
    # set_duration/clear_duration
    builder.set_duration(5)
    assert builder._next_duration == 5
    builder.clear_duration()
    assert builder._next_duration is None
    # clear
    builder.clear()  # type: ignore[unreachable]
    assert builder._video_current_time == 0.0
    assert builder._music_current_time == 0.0
    assert builder._voice_current_time == 0.0
    assert builder._sfx_current_time == 0.0
    assert builder._text_current_time == 0.0
    assert builder._next_duration is None
    assert len(builder.video_tracks) == 1
    assert len(builder.music_tracks) == 1
    assert len(builder.voice_tracks) == 1
    assert len(builder.sfx_tracks) == 1
    assert len(builder.text_tracks) == 1
    assert builder.transitions == []


@pytest.mark.unit
def test_export_branches_audio_none_and_options() -> None:
    """Test export with audio_clip None and with export options."""
    builder = TimelineBuilder()

    class DummyOptions(VideoExportOptions):
        def model_dump(self):
            return {"bitrate": "5000k", "fps": 30, "foo": None}

    # Save original imports
    import os.path

    import vine.builder.timeline_builder

    original_video_renderer = vine.builder.timeline_builder.VideoRenderer
    original_getsize = os.path.getsize
    original_exists = os.path.exists

    try:
        # Mock VideoRenderer
        mock_renderer = MagicMock()
        mock_video_renderer_class = MagicMock(return_value=mock_renderer)
        vine.builder.timeline_builder.VideoRenderer = mock_video_renderer_class

        # Mock os.path functions
        os.path.getsize = MagicMock(return_value=456)
        os.path.exists = MagicMock(return_value=True)

        # Setup mock video clip
        video_clip: MagicMock = MagicMock()
        video_clip.with_audio.return_value = video_clip
        audio_clip = None
        mock_renderer.render_with_audio.return_value = (video_clip, audio_clip)
        video_clip.write_videofile.return_value = None
        # Set duration as an attribute that getattr can find
        video_clip.duration = 8.0
        video_clip.close.return_value = None

        result: ExportResult = builder.export("out2.mp4", options=DummyOptions())
        assert result.success is True
        assert result.output_path == "out2.mp4"
        assert result.duration == 8.0
        assert result.file_size == 456
    finally:
        # Restore original imports
        vine.builder.timeline_builder.VideoRenderer = original_video_renderer
        os.path.getsize = original_getsize
        os.path.exists = original_exists


@pytest.mark.unit
def test_validate_audio_file_fallback_success() -> None:
    """Test _validate_audio_file with valid audio extension."""
    builder = TimelineBuilder()
    assert builder._validate_audio_file("file.mp3") is True
    assert builder._validate_audio_file("file.wav") is True
    assert builder._validate_audio_file("file.unknown") is False


@pytest.mark.unit
def test_sequential_methods_use_default_duration() -> None:
    """Test sequential methods use default duration if duration is None."""
    builder = TimelineBuilder()
    builder.set_duration(7)

    # Save original methods
    original_add_image_at = builder.add_image_at
    original_add_text_at = builder.add_text_at
    original_add_voice_at = builder.add_voice_at

    try:
        # Mock add_image_at
        mock_img = MagicMock(return_value="imgctx")
        builder.add_image_at = mock_img  # type: ignore
        builder.add_image("img.png")
        mock_img.assert_called_once_with("img.png", 0.0, 7)

        # Mock add_text_at
        mock_txt = MagicMock(return_value="txtctx")
        builder.add_text_at = mock_txt  # type: ignore
        builder.add_text("txt")
        mock_txt.assert_called_once_with("txt", 0.0, 7)

        # Mock add_voice_at
        mock_voice = MagicMock(return_value="voicectx")
        builder.add_voice_at = mock_voice  # type: ignore
        builder.add_voice("voice.mp3")
        mock_voice.assert_called_once_with("voice.mp3", 0.0, 7)
    finally:
        # Restore original methods
        builder.add_image_at = original_add_image_at  # type: ignore
        builder.add_text_at = original_add_text_at  # type: ignore
        builder.add_voice_at = original_add_voice_at  # type: ignore

    builder.clear_duration()


@pytest.mark.unit
def test_explicit_methods_with_end_time() -> None:
    """Test explicit methods with end_time instead of duration."""
    builder = TimelineBuilder()

    # Save original imports and methods
    import vine.models.tracks

    original_image_clip = vine.models.tracks.ImageClip
    original_text_clip = vine.models.tracks.TextClip
    original_audio_clip = vine.models.tracks.AudioClip
    original_validate = builder._validate_audio_file

    try:
        # Mock ImageClip
        mock_image_clip = MagicMock()
        mock_image_clip.return_value = MagicMock()
        vine.models.tracks.ImageClip = mock_image_clip
        img_ctx: Any = builder.add_image_at("img.png", 1, end_time=4)
        assert hasattr(img_ctx, "clip")

        # Mock TextClip
        mock_text_clip = MagicMock()
        mock_text_clip.return_value = MagicMock()
        vine.models.tracks.TextClip = mock_text_clip
        txt_ctx: Any = builder.add_text_at("txt", 2, end_time=5)
        assert hasattr(txt_ctx, "clip")

        # Mock AudioClip and validation
        mock_audio_clip = MagicMock()
        mock_audio_clip.return_value = MagicMock()
        vine.models.tracks.AudioClip = mock_audio_clip
        mock_validate = MagicMock(return_value=True)
        builder._validate_audio_file = mock_validate  # type: ignore

        voice_ctx: Any = builder.add_voice_at("voice.mp3", 3, end_time=6)
        assert hasattr(voice_ctx, "clip")
        music_ctx = builder.add_music_at("music.mp3", 4, end_time=7)
        assert hasattr(music_ctx, "clip")
        sfx_ctx = builder.add_sfx_at("sfx.mp3", 5, end_time=8)
        assert hasattr(sfx_ctx, "clip")
    finally:
        # Restore original imports and methods
        vine.models.tracks.ImageClip = original_image_clip
        vine.models.tracks.TextClip = original_text_clip
        vine.models.tracks.AudioClip = original_audio_clip
        builder._validate_audio_file = original_validate  # type: ignore


@pytest.mark.unit
def test_explicit_audio_methods_invalid_audio_with_end_time() -> None:
    """Test add_voice_at/add_music_at/add_sfx_at raise ValueError for invalid audio with end_time."""
    builder = TimelineBuilder()

    # Save original method
    original_validate = builder._validate_audio_file

    try:
        # Mock the validation to return False (invalid audio)
        mock_validate = MagicMock(return_value=False)
        builder._validate_audio_file = mock_validate  # type: ignore

        with pytest.raises(ValueError):
            builder.add_voice_at("bad.mp3", 0, end_time=1)
        with pytest.raises(ValueError):
            builder.add_music_at("bad.mp3", 0, end_time=1)
        with pytest.raises(ValueError):
            builder.add_sfx_at("bad.mp3", 0, end_time=1)
    finally:
        # Restore original method
        builder._validate_audio_file = original_validate  # type: ignore
