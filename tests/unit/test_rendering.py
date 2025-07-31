"""Tests for the MoviePy rendering integration."""

from typing import Any
from unittest.mock import MagicMock

import pytest

from vine.builder.timeline_builder import TimelineBuilder
from vine.models.tracks import AudioClip, ImageClip, TextClip
from vine.rendering.clip_factory import ClipFactory
from vine.rendering.moviepy_adapter import MoviePyAdapter
from vine.rendering.video_renderer import VideoRenderer


@pytest.fixture
def mock_moviepy_clip() -> Any:
    """Create a mock MoviePy clip with proper method chaining."""
    mock_clip: MagicMock = MagicMock()
    mock_clip.duration = 5.0
    mock_clip.fps = 30.0
    mock_clip.size = (1920, 1080)
    mock_clip.layer_index = 0  # Add layer_index for CompositeVideoClip sorting
    mock_clip.end = 5.0  # Add end attribute for duration calculation
    # Mock audio properties
    mock_audio: MagicMock = MagicMock()
    mock_audio.nchannels = 2
    # ends must be a property returning a list of floats
    type(mock_audio).ends = property(lambda _: [5.0])
    mock_clip.audio = mock_audio
    # Mock method chaining - each method returns the same mock object
    mock_clip.with_duration.return_value = mock_clip
    mock_clip.with_position.return_value = mock_clip
    mock_clip.with_opacity.return_value = mock_clip
    mock_clip.with_volume_scaled.return_value = mock_clip
    mock_clip.with_volume_function.return_value = mock_clip
    mock_clip.with_effects.return_value = mock_clip
    mock_clip.resize.return_value = mock_clip
    return mock_clip


class TestClipFactory:
    """Test the ClipFactory functionality."""

    @pytest.mark.unit
    def test_create_image_clip_returns_moviepy_clip(self, mock_moviepy_clip) -> None:
        """Test that create_image_clip returns a MoviePy clip."""
        vine_clip = ImageClip(
            path="test_image.jpg",
            start_time=0.0,
            duration=5.0,
            x_position=100.0,
            y_position=200.0,
            opacity=0.8,
        )

        # Mock the MoviePy ImageClip class to return our mock clip
        from vine.rendering.clip_factory import ImageClip as MoviePyImageClip

        original_image_clip = MoviePyImageClip
        mock_image_clip_class = MagicMock()
        mock_image_clip_class.return_value = mock_moviepy_clip

        # Replace the MoviePy ImageClip class temporarily
        import vine.rendering.clip_factory

        vine.rendering.clip_factory.ImageClip = mock_image_clip_class

        try:
            result = ClipFactory.create_image_clip(vine_clip)

            # Verify WHAT the method should accomplish:
            # 1. It should return a MoviePy ImageClip
            assert result is not None
            assert result == mock_moviepy_clip

            # 2. It should create the ImageClip with the correct path
            mock_image_clip_class.assert_called_once_with("test_image.jpg")

            # 3. It should apply the duration from the vine clip
            mock_moviepy_clip.with_duration.assert_called_once_with(5.0)

            # 4. It should apply the position from the vine clip
            mock_moviepy_clip.with_position.assert_called_once_with((100.0, 200.0))

            # 5. It should apply the opacity from the vine clip
            mock_moviepy_clip.with_opacity.assert_called_once_with(0.8)

        finally:
            # Restore the original ImageClip class
            vine.rendering.clip_factory.ImageClip = original_image_clip

    @pytest.mark.unit
    def test_create_text_clip_returns_moviepy_clip(self, mock_moviepy_clip) -> None:
        """Test that create_text_clip returns a MoviePy clip with correct properties."""
        vine_clip = TextClip(
            content="Hello World",
            start_time=0.0,
            duration=3.0,
            font_size=48,
            font_color="#FFFFFF",
            font_family="Arial",
            x_position=50.0,
            y_position=100.0,
            opacity=0.9,
        )

        # Mock the MoviePy TextClip class to return our mock clip
        from vine.rendering.clip_factory import TextClip as MoviePyTextClip

        original_text_clip = MoviePyTextClip
        mock_text_clip_class = MagicMock()
        mock_text_clip_class.return_value = mock_moviepy_clip

        # Replace the MoviePy TextClip class temporarily
        import vine.rendering.clip_factory

        vine.rendering.clip_factory.TextClip = mock_text_clip_class

        try:
            result = ClipFactory.create_text_clip(vine_clip)

            # Verify WHAT the method should accomplish:
            # 1. It should return a MoviePy TextClip
            assert result is not None
            assert result == mock_moviepy_clip

            # 2. It should create the TextClip with the correct content and properties
            mock_text_clip_class.assert_called_once_with(
                text="Hello World",
                font_size=48,
                color="#FFFFFF",
                method="caption",
                size=(800, 600),
            )

            # 3. It should apply the duration from the vine clip
            mock_moviepy_clip.with_duration.assert_called_once_with(3.0)

            # 4. It should apply the position from the vine clip
            mock_moviepy_clip.with_position.assert_called_once_with((50.0, 100.0))

            # 5. It should apply the opacity from the vine clip
            mock_moviepy_clip.with_opacity.assert_called_once_with(0.9)

        finally:
            # Restore the original TextClip class
            vine.rendering.clip_factory.TextClip = original_text_clip

    @pytest.mark.unit
    def test_create_audio_clip_returns_moviepy_clip(self, mock_moviepy_clip) -> None:
        """Test that create_audio_clip returns a MoviePy clip with correct properties."""
        vine_clip = AudioClip(
            path="test_audio.mp3",
            start_time=0.0,
            duration=10.0,
            volume=0.8,
            fade_in=0.0,
            fade_out=0.0,
        )

        # Mock the MoviePy AudioFileClip class to return our mock clip
        from vine.rendering.clip_factory import AudioFileClip as MoviePyAudioFileClip

        original_audio_file_clip = MoviePyAudioFileClip
        mock_audio_file_clip_class = MagicMock()
        mock_audio_file_clip_class.return_value = mock_moviepy_clip

        # Replace the MoviePy AudioFileClip class temporarily
        import vine.rendering.clip_factory

        vine.rendering.clip_factory.AudioFileClip = mock_audio_file_clip_class

        try:
            result = ClipFactory.create_audio_clip(vine_clip)

            # Verify WHAT the method should accomplish:
            # 1. It should return a MoviePy AudioFileClip
            assert result is not None
            assert result == mock_moviepy_clip

            # 2. It should create the AudioFileClip with the correct path
            mock_audio_file_clip_class.assert_called_once_with("test_audio.mp3")

            # 3. It should apply the duration from the vine clip
            mock_moviepy_clip.with_duration.assert_called_once_with(10.0)

            # 4. It should apply the volume from the vine clip
            mock_moviepy_clip.with_volume_scaled.assert_called_once_with(0.8)

        finally:
            # Restore the original AudioFileClip class
            vine.rendering.clip_factory.AudioFileClip = original_audio_file_clip


class TestMoviePyAdapter:
    """Test the MoviePyAdapter functionality."""

    @pytest.mark.unit
    def test_adapt_image_clip_returns_moviepy_clip(self, mock_moviepy_clip) -> None:
        """Test that adapt_image_clip returns a MoviePy clip."""
        vine_clip = ImageClip(path="test_image.jpg", start_time=0.0, duration=5.0)
        adapter = MoviePyAdapter()

        # Mock the ClipFactory to return predictable results
        original_create_image_clip = adapter.clip_factory.create_image_clip
        mock_create_image_clip = MagicMock()
        mock_create_image_clip.return_value = mock_moviepy_clip
        adapter.clip_factory.create_image_clip = mock_create_image_clip  # type: ignore

        try:
            result = adapter.adapt_image_clip(vine_clip)

            # Verify WHAT the method should accomplish:
            # 1. It should return a MoviePy ImageClip
            assert result is not None
            assert result == mock_moviepy_clip

            # 2. It should delegate to the ClipFactory
            mock_create_image_clip.assert_called_once_with(vine_clip)

        finally:
            # Restore original method
            adapter.clip_factory.create_image_clip = original_create_image_clip  # type: ignore

    @pytest.mark.unit
    def test_adapt_video_track_returns_list_of_clips(self, mock_moviepy_clip) -> None:
        """Test that adapt_video_track returns a list of MoviePy clips."""
        from vine.models.tracks import VideoTrack

        track = VideoTrack(
            name="test_track",
            clips=[
                ImageClip(path="test_image1.jpg", start_time=0.0, duration=5.0),
                ImageClip(path="test_image2.jpg", start_time=5.0, duration=5.0),
            ],
        )
        adapter = MoviePyAdapter()

        # Mock the ClipFactory to return predictable results
        original_create_image_clip = adapter.clip_factory.create_image_clip
        mock_create_image_clip = MagicMock()
        mock_create_image_clip.side_effect = [mock_moviepy_clip, mock_moviepy_clip]
        adapter.clip_factory.create_image_clip = mock_create_image_clip  # type: ignore

        try:
            result = adapter.adapt_video_track(track)

            # Verify WHAT the method should accomplish:
            # 1. It should return a list of MoviePy clips
            assert isinstance(result, list)
            assert len(result) == 2
            assert all(clip is not None for clip in result)

            # 2. It should process each clip in the track
            assert mock_create_image_clip.call_count == 2

            # 3. It should call the factory for each ImageClip in the track
            mock_create_image_clip.assert_any_call(track.clips[0])
            mock_create_image_clip.assert_any_call(track.clips[1])

            # 4. It should return the clips in the correct order
            assert result[0] == mock_moviepy_clip
            assert result[1] == mock_moviepy_clip

        finally:
            # Restore original method
            adapter.clip_factory.create_image_clip = original_create_image_clip  # type: ignore


class TestVideoRenderer:
    """Test the VideoRenderer functionality."""

    @pytest.mark.unit
    def test_create_clips_returns_list_of_clips(self, mock_moviepy_clip) -> None:
        """Test that create_clips returns a list of MoviePy clips."""
        renderer = VideoRenderer()
        from vine.models.tracks import TextTrack, VideoTrack
        from vine.models.video_spec import VideoSpec

        video_spec = VideoSpec(
            title="Test Video",
            width=1920,
            height=1080,
            fps=30.0,
            video_tracks=[
                VideoTrack(
                    name="video_0",
                    clips=[
                        ImageClip(path="test_image.jpg", start_time=0.0, duration=5.0)
                    ],
                )
            ],
            text_tracks=[
                TextTrack(
                    name="text_0",
                    clips=[TextClip(content="Hello", start_time=0.0, duration=5.0)],
                )
            ],
        )

        # Mock the adapter methods to return predictable results
        original_adapt_video_track = renderer.adapter.adapt_video_track
        original_adapt_text_track = renderer.adapter.adapt_text_track

        mock_adapt_video_track = MagicMock()
        mock_adapt_video_track.return_value = [mock_moviepy_clip]
        renderer.adapter.adapt_video_track = mock_adapt_video_track  # type: ignore

        mock_adapt_text_track = MagicMock()
        mock_adapt_text_track.return_value = [mock_moviepy_clip]
        renderer.adapter.adapt_text_track = mock_adapt_text_track  # type: ignore

        try:
            clips = renderer.create_clips(video_spec)

            # Verify WHAT the method should accomplish:
            # 1. It should return a list of MoviePy clips
            assert isinstance(clips, list)
            assert len(clips) == 2
            assert all(clip is not None for clip in clips)

            # 2. It should process visible video tracks
            mock_adapt_video_track.assert_called_once()
            # Verify it was called with the video track from the spec
            call_args = mock_adapt_video_track.call_args
            assert call_args[0][0] == video_spec.video_tracks[0]

            # 3. It should process visible text tracks
            mock_adapt_text_track.assert_called_once()
            # Verify it was called with the text track from the spec
            call_args = mock_adapt_text_track.call_args
            assert call_args[0][0] == video_spec.text_tracks[0]

            # 4. It should combine clips from both track types
            assert clips[0] == mock_moviepy_clip  # From video track
            assert clips[1] == mock_moviepy_clip  # From text track

        finally:
            # Restore original methods
            renderer.adapter.adapt_video_track = original_adapt_video_track  # type: ignore
            renderer.adapter.adapt_text_track = original_adapt_text_track  # type: ignore

    @pytest.mark.unit
    def test_compose_clips_with_clips_returns_composite(
        self, mock_moviepy_clip
    ) -> None:
        """Test that compose_clips with clips returns a composite video."""
        renderer = VideoRenderer()
        from vine.models.video_spec import VideoSpec

        video_spec = VideoSpec(title="Test Video", width=1920, height=1080, fps=30.0)
        # Create mock clips with proper fps attribute
        clip1 = mock_moviepy_clip
        clip2 = mock_moviepy_clip

        # Mock the MoviePy CompositeVideoClip class
        from vine.rendering.video_renderer import CompositeVideoClip

        original_composite_video_clip = CompositeVideoClip
        mock_composite_video_clip_class = MagicMock()
        mock_composite_video_clip = MagicMock()
        mock_composite_video_clip_class.return_value = mock_composite_video_clip

        # Replace the CompositeVideoClip class temporarily
        import vine.rendering.video_renderer

        vine.rendering.video_renderer.CompositeVideoClip = (
            mock_composite_video_clip_class
        )

        try:
            result = renderer.compose_clips([clip1, clip2], video_spec)

            # Verify WHAT the method should accomplish:
            # 1. It should return a composite video clip
            assert result is not None
            assert result == mock_composite_video_clip

            # 2. It should create a CompositeVideoClip with the provided clips
            mock_composite_video_clip_class.assert_called_once_with(
                [clip1, clip2], size=(1920, 1080)
            )

            # 3. It should use the video spec dimensions for the composite
            call_args = mock_composite_video_clip_class.call_args
            assert call_args[1]["size"] == (1920, 1080)

        finally:
            # Restore the original CompositeVideoClip class
            vine.rendering.video_renderer.CompositeVideoClip = (
                original_composite_video_clip
            )

    @pytest.mark.unit
    def test_compose_clips_empty_list_returns_color_clip(self) -> None:
        """Test that empty clips list returns a color clip."""
        renderer = VideoRenderer()
        from vine.models.video_spec import VideoSpec

        video_spec = VideoSpec(title="Test Video", width=1920, height=1080, fps=30.0)
        result = renderer.compose_clips([], video_spec)
        # Verify we get a color clip
        assert result is not None
        # Color clips typically have a default duration or can be infinite
        assert hasattr(result, "duration")

    @pytest.mark.unit
    def test_finalize_with_default_background_color_completes_successfully(
        self, mock_moviepy_clip
    ) -> None:
        """Test that finalize with default background color completes without error."""
        renderer = VideoRenderer()
        from vine.models.video_spec import VideoSpec

        video_spec = VideoSpec(
            title="Test Video",
            width=1920,
            height=1080,
            fps=30.0,
            background_color="#000000",  # Default black
        )
        # This should complete without raising NotImplementedError
        result = renderer.finalize(mock_moviepy_clip, video_spec)
        # Verify the method completed successfully
        assert result is not None

    @pytest.mark.unit
    def test_finalize_with_custom_background_color_raises_error(
        self, mock_moviepy_clip
    ) -> None:
        """Test that finalize with custom background color raises NotImplementedError."""
        renderer = VideoRenderer()
        from vine.models.video_spec import VideoSpec

        video_spec = VideoSpec(
            title="Test Video",
            width=1920,
            height=1080,
            fps=30.0,
            background_color="#FF0000",  # Custom red background
        )
        # This should raise NotImplementedError
        with pytest.raises(
            NotImplementedError, match="Background color setting not yet implemented"
        ):
            renderer.finalize(mock_moviepy_clip, video_spec)

    @pytest.mark.unit
    def test_compose_clips_with_different_sizes(self) -> None:
        """Test compose_clips works with different video spec sizes."""
        renderer = VideoRenderer()
        from vine.models.video_spec import VideoSpec

        test_cases = [
            (1280, 720),  # HD
            (1920, 1080),  # Full HD
            (3840, 2160),  # 4K
            (640, 480),  # SD
        ]
        for width, height in test_cases:
            video_spec = VideoSpec(
                title="Test Video", width=width, height=height, fps=30.0
            )
            result = renderer.compose_clips([], video_spec)
            # Should create a clip with the specified dimensions
            assert result is not None
            assert hasattr(result, "size") or hasattr(
                result, "w"
            )  # MoviePy clips have size info


class TestTimelineBuilderIntegration:
    """Test the TimelineBuilder integration with rendering."""

    @pytest.mark.unit
    def test_render_method_returns_video_clip(self, mock_moviepy_clip) -> None:
        """Test that the TimelineBuilder render method returns a video clip."""
        builder = TimelineBuilder(width=1280, height=720, fps=30)

        # Add some content to make the render meaningful
        builder.add_image("test_image.jpg", duration=3.0)
        builder.add_text("Hello World", duration=3.0)

        # Mock the VideoRenderer.render method to return a predictable result
        from vine.rendering.video_renderer import VideoRenderer

        original_render = VideoRenderer.render
        mock_render = MagicMock()
        mock_render.return_value = mock_moviepy_clip
        VideoRenderer.render = mock_render  # type: ignore

        try:
            result = builder.render()

            # Verify WHAT the render method should accomplish:
            # 1. It should return a video clip
            assert result is not None
            assert result == mock_moviepy_clip

            # 2. It should delegate to the VideoRenderer
            mock_render.assert_called_once()

            # 3. It should pass a VideoSpec to the renderer
            call_args = mock_render.call_args
            video_spec = call_args[0][0]
            assert video_spec.title == "Generated Video"
            assert video_spec.width == 1280
            assert video_spec.height == 720
            assert video_spec.fps == 30.0

        finally:
            # Restore original method
            VideoRenderer.render = original_render  # type: ignore

    @pytest.mark.unit
    def test_export_method_creates_output_file(self, mock_moviepy_clip) -> None:
        """Test that the TimelineBuilder export method creates an output file."""
        builder = TimelineBuilder(width=1280, height=720, fps=30)

        # Add some content to make the export meaningful
        builder.add_image("test_image.jpg", duration=3.0)
        builder.add_text("Hello World", duration=3.0)

        # Mock the VideoRenderer.render_with_audio method to return a predictable result
        from vine.rendering.video_renderer import VideoRenderer

        original_render_with_audio = VideoRenderer.render_with_audio
        mock_render_with_audio = MagicMock()
        mock_render_with_audio.return_value = (mock_moviepy_clip, None)
        VideoRenderer.render_with_audio = mock_render_with_audio  # type: ignore

        # Mock os.path.getsize to simulate file creation
        import os.path

        original_getsize = os.path.getsize
        os.path.getsize = MagicMock(return_value=1024)

        # Mock os.path.exists to simulate file creation
        original_exists = os.path.exists
        os.path.exists = MagicMock(return_value=True)

        try:
            # Configure the mock clip to behave like a real MoviePy clip
            mock_moviepy_clip.with_audio.return_value = mock_moviepy_clip
            mock_moviepy_clip.write_videofile = MagicMock()
            mock_moviepy_clip.close = MagicMock()

            # Test the export functionality
            result = builder.export("test_output.mp4")

            # Verify WHAT the export method should accomplish:
            # 1. It should return a successful result
            assert result.success is True
            # 2. It should specify the correct output path
            assert result.output_path == "test_output.mp4"
            # 3. It should provide the video duration
            assert result.duration == 5.0  # From mock_moviepy_clip fixture
            # 4. It should provide file size information
            assert result.file_size == 1024
            # 5. It should not have an error message
            assert result.error_message is None

            # Verify the video was actually written (the core behavior)
            mock_moviepy_clip.write_videofile.assert_called_once()
            # Verify cleanup was performed
            mock_moviepy_clip.close.assert_called_once()

        finally:
            # Restore original methods
            VideoRenderer.render_with_audio = original_render_with_audio  # type: ignore
            os.path.getsize = original_getsize
            os.path.exists = original_exists
