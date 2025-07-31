"""Factory pattern for creating MoviePy clips from Project Vine models."""

from moviepy import AudioFileClip, ImageClip, TextClip, VideoFileClip
from moviepy.audio.fx import AudioFadeIn, AudioFadeOut, AudioNormalize

from vine.models.tracks import AudioClip as VineAudioClip
from vine.models.tracks import ImageClip as VineImageClip
from vine.models.tracks import TextClip as VineTextClip

# Type alias for audio effects
AudioEffect = AudioFadeIn | AudioFadeOut | AudioNormalize


class ClipFactory:
    """Factory for creating MoviePy clips from Project Vine models.

    Implements the Factory pattern to centralize clip creation logic
    and provide a consistent interface for converting our Pydantic models
    to MoviePy clip objects.
    """

    @staticmethod
    def create_video_clip(video_clip: "VideoFileClip") -> VideoFileClip:
        """Create a MoviePy VideoFileClip from a Project Vine VideoClip.

        Args:
            video_clip: Project Vine VideoClip model

        Returns:
            MoviePy VideoFileClip object
        """
        # This would be used for actual video files
        # For now, we'll focus on ImageClip conversion
        raise NotImplementedError("VideoFileClip conversion not yet implemented")

    @staticmethod
    def create_image_clip(image_clip: VineImageClip) -> ImageClip:
        """Create a MoviePy ImageClip from a Project Vine ImageClip."""
        moviepy_clip: ImageClip = ImageClip(str(image_clip.path))

        if image_clip.duration is not None:
            moviepy_clip = moviepy_clip.with_duration(image_clip.duration)
        if image_clip.x_position != 0.0 or image_clip.y_position != 0.0:
            moviepy_clip = moviepy_clip.with_position(
                (image_clip.x_position, image_clip.y_position)
            )
        if image_clip.opacity != 1.0:
            moviepy_clip = moviepy_clip.with_opacity(image_clip.opacity)
        if image_clip.width is not None and image_clip.height is not None:
            moviepy_clip = moviepy_clip.resize((image_clip.width, image_clip.height))

        return moviepy_clip

    @staticmethod
    def _apply_audio_effects(
        moviepy_clip: AudioFileClip, audio_clip: VineAudioClip
    ) -> AudioFileClip:
        """Apply audio effects to the MoviePy clip."""
        if audio_clip.fade_in > 0.0:
            fade_in_effect: AudioEffect = AudioFadeIn(duration=audio_clip.fade_in)
            moviepy_clip = moviepy_clip.with_effects([fade_in_effect])  # type: ignore[misc]

        if audio_clip.fade_out > 0.0:
            fade_out_effect: AudioEffect = AudioFadeOut(duration=audio_clip.fade_out)
            moviepy_clip = moviepy_clip.with_effects([fade_out_effect])  # type: ignore[misc]

        if audio_clip.normalize_audio:
            normalize_effect: AudioEffect = AudioNormalize()
            moviepy_clip = moviepy_clip.with_effects([normalize_effect])  # type: ignore[misc]

        return moviepy_clip

    @staticmethod
    def _apply_volume_curve(
        moviepy_clip: AudioFileClip, audio_clip: VineAudioClip
    ) -> AudioFileClip:
        """Apply custom volume curve to the MoviePy clip."""
        if audio_clip.volume_curve is None:
            return moviepy_clip

        curve = audio_clip.volume_curve

        def volume_function(t: float) -> float:
            # Find the appropriate volume for the given time
            for i, (time, volume) in enumerate(curve):
                if t <= time:
                    if i == 0:
                        return volume
                    # Interpolate between points
                    prev_time, prev_volume = curve[i - 1]
                    ratio = (t - prev_time) / (time - prev_time)
                    return prev_volume + (volume - prev_volume) * ratio
            # If beyond the curve, use the last volume
            return curve[-1][1]

        return moviepy_clip.with_volume_function(volume_function)

    @staticmethod
    def create_audio_clip(audio_clip: VineAudioClip) -> AudioFileClip:
        """Create a MoviePy AudioFileClip from a Project Vine AudioClip."""
        moviepy_clip: AudioFileClip = AudioFileClip(str(audio_clip.path))

        if audio_clip.duration is not None:
            moviepy_clip = moviepy_clip.with_duration(audio_clip.duration)

        if audio_clip.volume != 1.0:
            moviepy_clip = moviepy_clip.with_volume_scaled(audio_clip.volume)

        moviepy_clip = ClipFactory._apply_audio_effects(moviepy_clip, audio_clip)
        moviepy_clip = ClipFactory._apply_volume_curve(moviepy_clip, audio_clip)

        return moviepy_clip

    @staticmethod
    def create_text_clip(text_clip: VineTextClip) -> TextClip:
        """Create a MoviePy TextClip from a Project Vine TextClip."""
        moviepy_clip: TextClip = TextClip(
            text=text_clip.content,
            font_size=text_clip.font_size,
            color=text_clip.font_color,
            method="caption",
            size=(800, 600),  # Default size for caption method
        )

        if text_clip.duration is not None:
            moviepy_clip = moviepy_clip.with_duration(text_clip.duration)
        if text_clip.x_position != 0.0 or text_clip.y_position != 0.0:
            moviepy_clip = moviepy_clip.with_position(
                (text_clip.x_position, text_clip.y_position)
            )
        if text_clip.opacity != 1.0:
            moviepy_clip = moviepy_clip.with_opacity(text_clip.opacity)

        return moviepy_clip
