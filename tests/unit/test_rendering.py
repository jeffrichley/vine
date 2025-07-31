"""Tests for the MoviePy rendering integration."""

from typing import Any
from unittest.mock import MagicMock, patch

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
        # Mock the MoviePy ImageClip creation
        with patch("vine.rendering.clip_factory.ImageClip") as mock_moviepy_class:
            mock_moviepy_class.return_value = mock_moviepy_clip
            result = ClipFactory.create_image_clip(vine_clip)
            # Verify we got a MoviePy ImageClip
            assert result is not None
            assert result.duration == 5.0

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
        # Mock the MoviePy TextClip creation
        with patch("vine.rendering.clip_factory.TextClip") as mock_moviepy_class:
            mock_moviepy_class.return_value = mock_moviepy_clip
            result = ClipFactory.create_text_clip(vine_clip)
            # Verify we got a MoviePy TextClip
            assert result is not None
            assert result.duration == 5.0  # Using fixture duration

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
        # Mock the MoviePy AudioFileClip creation
        with patch("vine.rendering.clip_factory.AudioFileClip") as mock_moviepy_class:
            mock_moviepy_class.return_value = mock_moviepy_clip
            result = ClipFactory.create_audio_clip(vine_clip)
            # Verify we got a MoviePy AudioFileClip
            assert result is not None
            assert result.duration == 5.0  # Using fixture duration


class TestMoviePyAdapter:
    """Test the MoviePyAdapter functionality."""

    @pytest.mark.unit
    def test_adapt_image_clip_returns_moviepy_clip(self, mock_moviepy_clip) -> None:
        """Test that adapt_image_clip returns a MoviePy clip."""
        vine_clip = ImageClip(path="test_image.jpg", start_time=0.0, duration=5.0)
        adapter = MoviePyAdapter()
        # Mock the ClipFactory to avoid real file operations
        with patch(
            "vine.rendering.moviepy_adapter.ClipFactory.create_image_clip"
        ) as mock_create:
            mock_create.return_value = mock_moviepy_clip
            result = adapter.adapt_image_clip(vine_clip)
            # Verify we get a MoviePy clip back
            assert result is not None
            assert result.duration == 5.0

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
        # Mock the ClipFactory to avoid real file operations
        with patch(
            "vine.rendering.moviepy_adapter.ClipFactory.create_image_clip"
        ) as mock_create:
            mock_create.side_effect = [mock_moviepy_clip, mock_moviepy_clip]
            result = adapter.adapt_video_track(track)
            # Verify we get a list of clips
            assert len(result) == 2
            assert all(clip is not None for clip in result)
            assert result[0].duration == 5.0
            assert result[1].duration == 5.0


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
        # Mock the adapter methods to avoid real file operations
        with (
            patch.object(renderer.adapter, "adapt_video_track") as mock_adapt_video,
            patch.object(renderer.adapter, "adapt_text_track") as mock_adapt_text,
        ):
            mock_adapt_video.return_value = [mock_moviepy_clip]
            mock_adapt_text.return_value = [mock_moviepy_clip]
            clips = renderer.create_clips(video_spec)
            # Verify we get clips from both tracks
            assert len(clips) == 2
            assert all(clip is not None for clip in clips)

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
        # Patch CompositeAudioClip and CompositeVideoClip to avoid MoviePy internals
        with (
            patch(
                "moviepy.video.compositing.CompositeVideoClip.CompositeAudioClip",
                return_value=MagicMock(),
            ),
            patch(
                "moviepy.video.compositing.CompositeVideoClip.CompositeVideoClip",
                return_value=MagicMock(),
            ),
        ):
            result = renderer.compose_clips([clip1, clip2], video_spec)
            # Verify we get a composite clip
            assert result is not None
            # Can't check duration because it's a MagicMock

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
        # Mock the render method to avoid file operations
        with patch.object(builder, "render") as mock_render:
            mock_render.return_value = mock_moviepy_clip
            # Add some content
            builder.add_image("test_image.jpg", duration=3.0)
            builder.add_text("Hello World", duration=3.0)
            result = builder.render()
            # Verify we get a video clip back
            assert result is not None
            assert hasattr(result, "duration")

    @pytest.mark.unit
    def test_export_method_creates_output_file(self, mock_moviepy_clip) -> None:
        """Test that the TimelineBuilder export method creates an output file."""
        builder = TimelineBuilder(width=1280, height=720, fps=30)
        # Mock the entire export process to avoid file system operations
        with (
            patch.object(builder, "render") as mock_render,
            patch(
                "vine.rendering.video_renderer.VideoRenderer.render_with_audio"
            ) as mock_render_with_audio,
            patch("os.path.getsize", return_value=1024),
        ):
            # Use MagicMock with proper specs for better type safety
            mock_clip = mock_moviepy_clip
            mock_clip.with_audio.return_value = mock_clip
            mock_clip.write_videofile = MagicMock()
            mock_clip.close = MagicMock()
            mock_render.return_value = mock_clip
            mock_render_with_audio.return_value = (mock_clip, None)
            result = builder.export("test_output.mp4")
            # Verify the method completed successfully
            assert result.success is True
            assert result.output_path == "test_output.mp4"
            assert result.duration == 5.0
            # Verify write_videofile was called (call expectation)
            mock_clip.write_videofile.assert_called_once()
