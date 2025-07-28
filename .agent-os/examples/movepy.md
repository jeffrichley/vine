========================
CODE SNIPPETS
========================
TITLE: Loading Resources with MoviePy
DESCRIPTION: Demonstrates the base clips that can be created with MoviePy for loading various resources like video files, images, and audio. This serves as a foundational example for starting video projects.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/user_guide/loading.rst#_snippet_0

LANGUAGE: python
CODE:
```
# This is a placeholder for the code that would be loaded from the specified file.
# The actual code content is not provided in the input text.
# Example: VideoFileClip, AudioFileClip, ImageSequenceClip, TextClip, ColorClip usage.
```

----------------------------------------

TITLE: Basic MoviePy Video Editing Example
DESCRIPTION: Demonstrates a typical MoviePy workflow: loading a video, modifying its volume, adding a title overlay for a duration, and rendering the result to a new file. This example requires the MoviePy library and FFmpeg to be installed.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/getting_started/quick_presentation.rst#_snippet_0

LANGUAGE: python
CODE:
```
from moviepy.editor import *

# Load a video file
clip = VideoFileClip("my_video.mp4")

# Lower the volume by 50%
clip = clip.volumex(0.5)

# Create a title clip that lasts for 10 seconds
txt_clip = TextClip("My Title", fontsize=70, color='white')
txt_clip = txt_clip.set_pos('center').set_duration(10)

# Overlay the title clip onto the video clip
video = CompositeVideoClip([clip, txt_clip])

# Write the result to a new file
video.write_videofile("my_video_edited.mp4")
```

----------------------------------------

TITLE: Lint MoviePy Code with Black (python)
DESCRIPTION: Formats the MoviePy codebase according to Black's style guide. This command should be run from the project's root directory.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/developer_guide/developers_install.rst#_snippet_5

LANGUAGE: python
CODE:
```
$ python -m black .
```

----------------------------------------

TITLE: Install MoviePy with Dependencies
DESCRIPTION: Installs the MoviePy library in editable mode with optional dependencies for documentation, testing, and linting within a virtual environment.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/developer_guide/contribution_guidelines.rst#_snippet_2

LANGUAGE: bash
CODE:
```
pip install -e ".[optional,doc,test,lint]"
```

----------------------------------------

TITLE: Install MoviePy
DESCRIPTION: Installs the MoviePy library using pip. This is a prerequisite for using MoviePy for video editing tasks.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/getting_started/moviepy_10_minutes.rst#_snippet_0

LANGUAGE: shell
CODE:
```
pip install moviepy
```

----------------------------------------

TITLE: Build MoviePy Documentation (python)
DESCRIPTION: Builds the MoviePy documentation after the necessary libraries have been installed. This command is executed from the project's root directory.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/developer_guide/developers_install.rst#_snippet_1

LANGUAGE: python
CODE:
```
$ python setup.py build_docs
```

----------------------------------------

TITLE: Install MoviePy Documentation Dependencies (bash)
DESCRIPTION: Installs the Python libraries required to build the MoviePy documentation. This command uses pip with an extra dependency set.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/developer_guide/developers_install.rst#_snippet_0

LANGUAGE: bash
CODE:
```
$ (sudo) pip install moviepy[doc]
```

----------------------------------------

TITLE: Install MoviePy with Dependencies
DESCRIPTION: Installs the MoviePy library in editable mode with optional dependencies for documentation, testing, and linting. It is recommended to perform this within a virtual environment.

SOURCE: https://github.com/zulko/moviepy/blob/master/CONTRIBUTING.md#_snippet_2

LANGUAGE: shell
CODE:
```
pip install -e ".[optional,doc,test,lint]"
```

----------------------------------------

TITLE: Install Pre-commit Hooks
DESCRIPTION: Configures and installs pre-commit hooks for the project, ensuring code quality checks are run automatically before commits.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/developer_guide/contribution_guidelines.rst#_snippet_3

LANGUAGE: bash
CODE:
```
pre-commit install
```

----------------------------------------

TITLE: Run MoviePy Tests (python)
DESCRIPTION: Executes the MoviePy test suite using the pytest framework. Ensure testing libraries are installed first.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/developer_guide/developers_install.rst#_snippet_4

LANGUAGE: python
CODE:
```
$ python -m pytest
```

----------------------------------------

TITLE: Run Moviepy Tests
DESCRIPTION: Executes the test suite for the Moviepy library using the pytest framework. Ensure all dependencies are installed before running this command.

SOURCE: https://github.com/zulko/moviepy/blob/master/tests/README.rst#_snippet_1

LANGUAGE: shell
CODE:
```
pytest
```

----------------------------------------

TITLE: Install Moviepy Testing Dependencies
DESCRIPTION: Installs the necessary dependencies for testing the Moviepy library using pip. This command ensures all required packages, including testing-specific ones, are available in your Python environment.

SOURCE: https://github.com/zulko/moviepy/blob/master/tests/README.rst#_snippet_0

LANGUAGE: shell
CODE:
```
pip install moviepy[test]
```

----------------------------------------

TITLE: Set FFplay Binary Path on Windows (Python)
DESCRIPTION: Demonstrates setting the FFPLAY_BINARY environment variable with a Windows-style path. This ensures MoviePy can find the ffplay executable on Windows systems.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/getting_started/install.rst#_snippet_4

LANGUAGE: python
CODE:
```
os.environ["FFPLAY_BINARY"] = r"C:\\Program Files\\ffmpeg\\ffplay.exe"
```

----------------------------------------

TITLE: Add Git Pre-commit Hooks (bash)
DESCRIPTION: Installs Git pre-commit hooks for the MoviePy project. This automates linting and formatting checks before commits.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/developer_guide/developers_install.rst#_snippet_7

LANGUAGE: bash
CODE:
```
$ pre-commit install
```

----------------------------------------

TITLE: Install MoviePy using pip (Bash)
DESCRIPTION: Installs the MoviePy library using the pip package manager. Requires pip to be installed. This command is executed in a terminal.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/getting_started/install.rst#_snippet_0

LANGUAGE: bash
CODE:
```
$ (sudo) pip install moviepy
```

----------------------------------------

TITLE: Lint MoviePy Code with Flake8 (python)
DESCRIPTION: Checks the MoviePy codebase for style guide violations using Flake8. This command includes verbose output and ignores specific error codes.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/developer_guide/developers_install.rst#_snippet_6

LANGUAGE: python
CODE:
```
$ python3 -m flake8 -v --show-source --ignore=E501 moviepy docs/conf.py examples tests
```

----------------------------------------

TITLE: Install MoviePy Testing Dependencies (bash)
DESCRIPTION: Installs the Python libraries required for running MoviePy's tests. This command uses pip with the 'test' extra dependency set.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/developer_guide/developers_install.rst#_snippet_2

LANGUAGE: bash
CODE:
```
$ (sudo) pip install moviepy[test]
```

----------------------------------------

TITLE: Install MoviePy Linting Dependencies (bash)
DESCRIPTION: Installs the Python libraries required for linting MoviePy's code. This command uses pip with the 'lint' extra dependency set.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/developer_guide/developers_install.rst#_snippet_3

LANGUAGE: bash
CODE:
```
$ (sudo) pip install moviepy[lint]
```

----------------------------------------

TITLE: Creating Video Clips from Functions
DESCRIPTION: Shows how to create custom animated video clips by defining a `frame_function(t)` that returns a NumPy array representing the frame at time `t`. This is useful for generating animations programmatically, such as the pulsating red circle example using Pillow.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/user_guide/loading.rst#_snippet_2

LANGUAGE: python
CODE:
```
# This is a placeholder for the code that would be loaded from the specified file.
# The actual code content is not provided in the input text.
# Example: `VideoClip(make_frame=my_frame_function, duration=5)`
```

----------------------------------------

TITLE: Install Pre-commit Hooks
DESCRIPTION: Configures the pre-commit framework to run code checks automatically before commits. This ensures code quality and adherence to project conventions like PEP8.

SOURCE: https://github.com/zulko/moviepy/blob/master/CONTRIBUTING.md#_snippet_3

LANGUAGE: shell
CODE:
```
pre-commit install
```

----------------------------------------

TITLE: Python Video Editing Example
DESCRIPTION: Demonstrates loading a video file, extracting a subclip, scaling audio volume, adding a text overlay, and writing the result to a new file using MoviePy.

SOURCE: https://github.com/zulko/moviepy/blob/master/README.md#_snippet_0

LANGUAGE: python
CODE:
```
from moviepy import VideoFileClip, TextClip, CompositeVideoClip

# Load file example.mp4 and keep only the subclip from 00:00:10 to 00:00:20
# Reduce the audio volume to 80% of its original volume

clip = (
    VideoFileClip("long_examples/example2.mp4")
    .subclipped(10, 20)
    .with_volume_scaled(0.8)
)

# Generate a text clip. You can customize the font, color, etc.
txt_clip = TextClip(
    font="Arial.ttf",
    text="Hello there!",
    font_size=70,
    color='white'
).with_duration(10).with_position('center')

# Overlay the text clip on the first video clip
final_video = CompositeVideoClip([clip, txt_clip])
final_video.write_videofile("result.mp4")
```

----------------------------------------

TITLE: Set Clip Start and End Times
DESCRIPTION: Specifies the start and end times for individual clips within the final composition. This is crucial for sequencing clips correctly and handling clips without inherent durations.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/getting_started/moviepy_10_minutes.rst#_snippet_6

LANGUAGE: python
CODE:
```
clip = clip.set_start(start_time).set_end(end_time)
```

----------------------------------------

TITLE: Check Moviepy Configuration
DESCRIPTION: The check function in moviepy.config is used to verify that the moviepy installation and its dependencies are correctly configured. It helps diagnose potential issues with the environment setup.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/reference/reference/moviepy.config.check.rst#_snippet_0

LANGUAGE: APIDOC
CODE:
```
moviepy.config.check()

  Verifies the moviepy configuration.

  This function checks for the presence and correctness of necessary external libraries and settings required for moviepy to function properly. It may print warnings or errors if issues are detected.

  Parameters:
    None

  Returns:
    None. The function performs checks and reports status via console output.
```

----------------------------------------

TITLE: Create ColorClip
DESCRIPTION: Shows how to create a ColorClip, which generates a clip displaying a single solid color. This is useful for compositing operations or as a background element.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/user_guide/loading.rst#_snippet_9

LANGUAGE: python
CODE:
```
from moviepy.editor import *

# Create a ColorClip with a specific size, duration, and color.
# The color can be specified as a string (e.g., 'red', 'blue') or an RGB tuple.
# The size is given as a tuple (width, height).
color_clip = ColorClip(size=(640, 480), color=(255, 0, 0), duration=5)

# This clip can be used in compositing or saved as a video file.
# For example:
# color_clip.write_videofile("red_background.mp4")
```

----------------------------------------

TITLE: Preview Video Clip
DESCRIPTION: Allows previewing a video clip directly within the script. Requires ffplay to be installed and accessible. The preview function can take an optional fps argument to control playback speed for performance.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/getting_started/moviepy_10_minutes.rst#_snippet_3

LANGUAGE: python
CODE:
```
# Preview the intro clip
# intro_clip.preview()

# Preview the bird clip
# bird_clip.preview()

# Preview the pigs clip
# pigs_clip.preview()

# Preview the final clip
# final_clip.preview()
```

----------------------------------------

TITLE: Load VideoFileClip
DESCRIPTION: Demonstrates loading a video clip from a file using VideoFileClip. These clips automatically have 'fps' and 'duration' attributes, useful for rendering operations.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/user_guide/loading.rst#_snippet_3

LANGUAGE: python
CODE:
```
from moviepy.editor import VideoFileClip

clip = VideoFileClip("my_video.mp4")
# clip is a VideoFileClip object
```

----------------------------------------

TITLE: Changing Clip Start and End Times in Composition
DESCRIPTION: Demonstrates how to control the playback timing of individual clips within a composition. Each clip can have its start and end times defined using the 'start' and 'end' attributes.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/user_guide/compositing.rst#_snippet_3

LANGUAGE: python
CODE:
```
from moviepy.editor import *

clip1 = VideoFileClip("my_video.mp4").subclip(0, 10)
clip2 = VideoFileClip("my_video.mp4").subclip(0, 8)
clip3 = VideoFileClip("my_video.mp4").subclip(0, 12)

# Clip1 plays for the first 6 seconds
clip1 = clip1.set_start(0).set_end(6)

# Clip2 starts playing 5 seconds into the video
clip2 = clip2.set_start(5)

# Clip3 starts playing after clip2 ends (at 5 + 8 = 13 seconds)
clip3 = clip3.set_start(clip2.start + clip2.duration)

final_clip = CompositeVideoClip([clip1, clip2, clip3])

final_clip.write_videofile("timed_composition.mp4")
```

----------------------------------------

TITLE: Preview Clip as Video
DESCRIPTION: Preview a clip as a video using the `preview` function. This requires `ffplay` to be installed and accessible. Performance may vary based on system resources; consider adjusting clip properties like FPS or resolution for smoother playback.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/user_guide/rendering.rst#_snippet_0

LANGUAGE: python
CODE:
```
from moviepy.editor import *

clip = VideoFileClip("my_video.mp4").subclip(10, 20)
clip.preview()
# or
# clip.preview(fps=24, audio_fps=44100, method="pygame")
```

----------------------------------------

TITLE: Compose Multiple Clips
DESCRIPTION: Assembles multiple timed clips into a single video using `CompositeVideoClip`. This class plays clips on top of each other according to their set start and end points.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/getting_started/moviepy_10_minutes.rst#_snippet_7

LANGUAGE: python
CODE:
```
final_clip = CompositeVideoClip([clip1, clip2, clip3], size=(width, height))
```

----------------------------------------

TITLE: Verify MoviePy Binary Configuration (Python)
DESCRIPTION: Checks if MoviePy can locate the necessary FFmpeg and FFplay binaries. This is done by calling the `check()` function from `moviepy.config`. It helps diagnose issues with external dependencies.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/getting_started/install.rst#_snippet_3

LANGUAGE: python
CODE:
```
from moviepy.config import check
check()
```

----------------------------------------

TITLE: Load Audio File with AudioFileClip
DESCRIPTION: Explains how to load an audio file into MoviePy using the AudioFileClip class. This is the primary method for working with existing audio files.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/user_guide/loading.rst#_snippet_12

LANGUAGE: python
CODE:
```
from moviepy.editor import *

# Load an audio file (e.g., MP3, WAV).
# Pass the path to the audio file to the AudioFileClip constructor.
# MoviePy handles various audio formats.
audio_file_clip = AudioFileClip("my_audio_file.mp3")

# You can then manipulate this audio clip, for example:
# - Get its duration: audio_file_clip.duration
# - Cut a subclip: sub_audio = audio_file_clip.subclip(10, 20)
# - Change volume: louder_audio = audio_file_clip.volumex(1.5)
# - Concatenate with other audio clips: final_audio = concatenate_audioclips([audio_file_clip, another_audio_clip])

# For more details, refer to the AudioFileClip documentation.
# You can write the processed audio to a new file:
# audio_file_clip.write_audiofile("processed_audio.wav")
```

----------------------------------------

TITLE: Run MoviePy Script in New Docker Container (Two Steps)
DESCRIPTION: Starts a new MoviePy Docker container, enters its bash shell, and then executes a Python script. This is a two-step process.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/getting_started/docker.rst#_snippet_3

LANGUAGE: shell
CODE:
```
docker run -it moviepy bash
python myscript.py
```

----------------------------------------

TITLE: Create AudioClip from a Function
DESCRIPTION: Demonstrates how to create an AudioClip by defining a function that generates audio frames based on time. The function should return a NumPy array representing mono (Nx1) or stereo (Nx2) audio.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/user_guide/loading.rst#_snippet_11

LANGUAGE: python
CODE:
```
from moviepy.editor import *
import numpy as np

# Define a function that generates audio data at a given time t.
# This function should return a numpy array. For mono, it's Nx1; for stereo, it's Nx2.
# Here, we create a simple sine wave.
def audio_function(t):
    # Generate 1 second of audio data (e.g., 44100 samples per second)
    sample_rate = 44100
    frequency = 440 # A4 note
    amplitude = 0.5

    # Create a time vector for one second
    t_vec = np.linspace(t, t + 1, sample_rate, endpoint=False)

    # Generate sine wave for mono audio
    audio_data = amplitude * np.sin(2 * np.pi * frequency * t_vec)

    # For stereo, you would return a shape (sample_rate, 2) array
    # audio_data = np.vstack((audio_data, audio_data)).T # Simple stereo copy

    return audio_data.reshape(-1, 1) # Return as Nx1 for mono

# Create an AudioClip from the function.
# You need to specify the duration and the sampling rate.
# The duration is in seconds.
audio_clip = AudioClip(audio_function, duration=5, fps=44100)

# For more details, refer to the AudioClip documentation.
# You can then write this audio clip to a file:
# audio_clip.write_audiofile("sine_wave.wav")
```

----------------------------------------

TITLE: Load ImageSequenceClip
DESCRIPTION: Shows how to create a clip from a sequence of images. The sequence can be a list of image file names, a folder name (processed in alphanumerical order), or a list of NumPy arrays. All images must be of the same dimensions.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/user_guide/loading.rst#_snippet_4

LANGUAGE: python
CODE:
```
from moviepy.editor import ImageSequenceClip

# Sequence of image file names
clip = ImageSequenceClip(["frame001.png", "frame002.png", "frame003.png"], fps=24)

# Sequence from a folder
# clip = ImageSequenceClip("my_image_folder", fps=24)

# Sequence of numpy arrays
# clip = ImageSequenceClip([frame1_array, frame2_array], fps=24)
```

----------------------------------------

TITLE: Configure FFmpeg/FFplay Paths in Python
DESCRIPTION: Sets environment variables in Python to specify custom paths for FFmpeg and FFplay binaries. This is useful for using specific versions of these tools. Requires the `os` module.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/getting_started/install.rst#_snippet_1

LANGUAGE: python
CODE:
```
import os
os.environ["FFMPEG_BINARY"] = "/path/to/custom/ffmpeg"
os.environ["FFPLAY_BINARY"] = "/path/to/custom/ffplay"
```

----------------------------------------

TITLE: Create AudioClip from NumPy Array
DESCRIPTION: Demonstrates how to convert a NumPy array representing audio data into an AudioClip using AudioArrayClip. This is useful when audio is generated or processed by other libraries.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/user_guide/loading.rst#_snippet_13

LANGUAGE: python
CODE:
```
from moviepy.editor import *
import numpy as np

# Assume you have a NumPy array containing audio data.
# The array should have shape (N, 1) for mono or (N, 2) for stereo, where N is the number of samples.
# Let's create a sample array (e.g., 2 seconds of silence at 44100 Hz)
sample_rate = 44100
duration = 2
num_samples = int(sample_rate * duration)

# Create a mono audio array (all zeros for silence)
audio_array = np.zeros((num_samples, 1))

# For stereo, you would create an array like:
# audio_array = np.zeros((num_samples, 2))

# Create an AudioArrayClip from the NumPy array.
# You need to provide the array and the sampling rate (fps).
# The fps parameter indicates how fast the array should be played.
audio_array_clip = AudioArrayClip(audio_array, fps=sample_rate)

# For more details, refer to the AudioArrayClip documentation.
# You can write this clip to a file:
# audio_array_clip.write_audiofile("array_audio.wav")
```

----------------------------------------

TITLE: ffplay_audiopreview: Preview Audio with FFplay
DESCRIPTION: This function previews an audio clip using the ffplay executable. It requires ffplay to be installed and accessible in the system's PATH. The function takes an audio clip object and optional parameters like FPS and buffer size.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/reference/reference/moviepy.audio.io.ffplay_audiopreviewer.ffplay_audiopreview.rst#_snippet_0

LANGUAGE: APIDOC
CODE:
```
ffplay_audiopreview(audio, fps=44100, bufsize=1024, audiolib='ffplay', **kwargs)

  Previews an audio clip using the ffplay executable.

  Parameters:
    audio: The audio clip to preview.
    fps (int): Frames per second for audio playback. Defaults to 44100.
    bufsize (int): Buffer size for audio playback. Defaults to 1024.
    audiolib (str): The audio library to use. Defaults to 'ffplay'.
    **kwargs: Additional keyword arguments to pass to the underlying function.

  Dependencies:
    - ffplay executable must be installed and in the system's PATH.

  Returns:
    None. Plays the audio clip directly.
```

----------------------------------------

TITLE: Create TextClip with OpenType Font
DESCRIPTION: Demonstrates how to create a TextClip using an OpenType font by providing the path to the font file. It also highlights the 'method' parameter for text overflow handling ('label' or 'caption').

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/user_guide/loading.rst#_snippet_8

LANGUAGE: python
CODE:
```
from moviepy.editor import *

# Example usage of TextClip
# The font must be an OpenType font.
# The path to the font file is passed to the TextClip constructor.
# The 'method' parameter can be 'label' (text overflows) or 'caption' (text breaks lines).
text_clip = TextClip("Hello MoviePy!", fontsize=70, color='white', font='Arial-Bold', method='caption', size=(640,480))

# To use a specific font file:
# text_clip = TextClip("Hello MoviePy!", font='/path/to/your/font.ttf', method='caption')

# For more details on parameters, refer to the TextClip documentation.

# Example of how to use it in a video (requires a duration)
# video = text_clip.set_duration(5)
# video.write_videofile("text_example.mp4")
```

----------------------------------------

TITLE: Run MoviePy Script in Docker (One Command)
DESCRIPTION: Starts a new MoviePy Docker container, mounts the current directory to /code, and executes a Python script in a single command.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/getting_started/docker.rst#_snippet_4

LANGUAGE: shell
CODE:
```
docker run -it -v `pwd`:/code moviepy python myscript.py
```

----------------------------------------

TITLE: Load DataVideoClip
DESCRIPTION: Creates a video clip from a list of datasets and a callback function. Each frame is generated by iterating through the dataset and invoking the callback with the current data. This is an advanced usage, typically for data-driven animations.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/user_guide/loading.rst#_snippet_5

LANGUAGE: python
CODE:
```
from moviepy.editor import DataVideoClip

def my_callback(data):
    # Create a frame based on the 'data' entry
    pass

data_list = [data1, data2, data3]
clip = DataVideoClip(data_list, my_callback, fps=24)
```

----------------------------------------

TITLE: Load ImageClip
DESCRIPTION: Creates a static image clip, which is the base class for unanimated clips. It displays a single image throughout its duration. You must define its duration and FPS if operations require them.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/user_guide/loading.rst#_snippet_7

LANGUAGE: python
CODE:
```
from moviepy.editor import ImageClip

# From a file
clip = ImageClip("my_image.png")

# With a specific duration and FPS
# clip = ImageClip("my_image.png", duration=5, fps=24)
```

----------------------------------------

TITLE: Export a Single Frame of a Clip
DESCRIPTION: Provides an example of how to export a single frame from a video clip, useful for creating preview images or thumbnails. The function allows specifying the time point and output filename.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/user_guide/rendering.rst#_snippet_5

LANGUAGE: python
CODE:
```
from moviepy.editor import VideoFileClip

clip = VideoFileClip("my_video.mp4")

# Save a frame at 10 seconds (10.0) to a JPG file
clip.save_frame("preview.jpg", t=10.0)
```

----------------------------------------

TITLE: Create and Use Mask Clips
DESCRIPTION: Illustrates the creation and application of mask clips in MoviePy. Masks are greyscale clips with a single color channel (0-1) that control pixel visibility. They can be attached to other clips using `with_mask`.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/user_guide/loading.rst#_snippet_10

LANGUAGE: python
CODE:
```
from moviepy.editor import *

# Create a base video clip (e.g., from a file or another generator)
# base_clip = VideoFileClip("my_video.mp4")

# Create a mask clip. This example uses a simple gradient.
# Masks have one component per pixel, between 0 and 1.
# A value of 1 means fully visible, 0 means fully transparent.
mask_clip = ColorClip(size=(640, 480), color=(0,0,0), is_mask=True).set_duration(5)
# You can also create masks from images or other video clips.
# For example, to use an image as a mask:
# mask_clip = ImageClip("my_mask.png", is_mask=True).set_duration(5)

# Attach the mask to the base clip.
# The mask determines which parts of the base_clip are visible.
# masked_clip = base_clip.with_mask(mask_clip)

# Masks can be converted to RGB using to_RGB()
# rgb_mask = mask_clip.to_RGB()

# Any clip can be converted to a mask using to_mask()
# mask_from_clip = base_clip.to_mask()

# Note: Images with alpha layers are automatically used as masks unless transparent=False is passed.
# If a clip is not already black and white, it will be converted automatically when used as a mask.
```

----------------------------------------

TITLE: Create Custom MoviePy Effect
DESCRIPTION: Demonstrates how to create a custom effect by inheriting from `moviepy.Effect.Effect`. This example shows how to define an effect with parameters and implement the `apply` method to modify a clip, such as adding a progress bar.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/user_guide/create_effects.rst#_snippet_0

LANGUAGE: python
CODE:
```
from moviepy.editor import VideoFileClip, TextClip
from moviepy.video.fx.all import crop
from moviepy.Effect import Effect

class ProgressBarEffect(Effect):
    def __init__(self, color=(255, 255, 255), height=5, opacity=0.5):
        # Effect parameters are stored in self.params
        self.params = {'color': color, 'height': height, 'opacity': opacity}

    def apply(self, clip):
        # The apply method receives the clip to modify
        # It must return the modified clip

        # We use clip.set_pos to position the progress bar
        # We use clip.set_duration to get the total duration
        # We use clip.fl to apply a function to each frame

        def make_frame(t, frame):
            # Calculate progress
            progress = t / clip.duration

            # Get clip dimensions
            width, height = clip.size

            # Create progress bar
            bar_width = int(width * progress)

            # Create a colored rectangle for the progress bar
            # Using TextClip for simplicity to create a colored rectangle
            # In a real scenario, you might use numpy or Pillow directly
            progress_bar = TextClip(
                '',
                color='white',
                bg_color=self.params['color'],
                size=(bar_width, self.params['height']),
                method='caption'
            ).set_opacity(self.params['opacity'])

            # Overlay the progress bar onto the frame
            # Position it at the bottom center
            overlayed_frame = CompositeVideoClip([
                clip.get_frame(t),
                progress_bar.set_position(('center', 'bottom'))
            ])
            return overlayed_frame

        # Apply the frame modification function to the clip
        return clip.fl(make_frame)

# Example Usage:
# clip = VideoFileClip("my_video.mp4")
# progress_bar_clip = clip.with_effects(ProgressBarEffect(color=(0, 255, 0), height=10))
# progress_bar_clip.write_videofile("output_video.mp4")

```

----------------------------------------

TITLE: Configure FFmpeg/FFplay Paths using .env (INI)
DESCRIPTION: Defines custom paths for FFmpeg and FFplay binaries in a `.env` file. MoviePy automatically reads this file to configure external tools. This method is an alternative to setting environment variables directly in Python.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/getting_started/install.rst#_snippet_2

LANGUAGE: ini
CODE:
```
FFMPEG_BINARY=/path/to/custom/ffmpeg
FFPLAY_BINARY=/path/to/custom/ffplay
```

----------------------------------------

TITLE: Closing Clips and Releasing Resources
DESCRIPTION: Illustrates the proper way to release resources (like subprocesses and file locks) by calling the `close()` method on MoviePy clip instances. It emphasizes using clips as context managers with `with` statements for automatic cleanup, especially important for `VideoFileClip` and `AudioFileClip`.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/user_guide/loading.rst#_snippet_1

LANGUAGE: python
CODE:
```
# This is a placeholder for the code that would be loaded from the specified file.
# The actual code content is not provided in the input text.
# Example: Using `with VideoFileClip(...) as clip:` or `clip.close()`.
```

----------------------------------------

TITLE: Extract Scenes using Subclip
DESCRIPTION: Extracts specific segments from a video clip using the subclip method. This allows for selecting parts of the video based on start and end times, which can be in seconds or HH:MM:SS.µS format.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/getting_started/moviepy_10_minutes.rst#_snippet_2

LANGUAGE: python
CODE:
```
# Extract the intro scene
intro_clip = clip.subclip(5, 10)

# Extract the scene with the bird
bird_clip = clip.subclip(10, 15)

# Extract the scene with the pigs
pigs_clip = clip.subclip(15, 20)

# Extract the final scene
final_clip = clip.subclip(20, 25)
```

----------------------------------------

TITLE: Write Video with FFmpeg
DESCRIPTION: This function is used to write a video clip to a file using the FFmpeg tool. It handles various video codecs, formats, and quality settings. Ensure FFmpeg is installed and accessible in your system's PATH.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/reference/reference/moviepy.video.io.ffmpeg_writer.ffmpeg_write_video.rst#_snippet_0

LANGUAGE: Python
CODE:
```
from moviepy.editor import VideoFileClip
from moviepy.video.io.ffmpeg_writer import ffmpeg_write_video

# Load a video clip
clip = VideoFileClip("my_video.mp4")

# Write the clip to a new file using FFmpeg
# You can specify codec, bitrate, fps, etc.
ffmpeg_write_video(clip, "output.mp4", fps=clip.fps, codec="libx264", bitrate="5000k")

# Close the clip
clip.close()
```

----------------------------------------

TITLE: Load UpdatedVideoClip
DESCRIPTION: Creates a video clip where frame generation depends on an external 'world' object that needs updating. The world object must have 'clip_t', 'update()', and 'to_frame()' methods. Useful for simulations or real-time external contexts.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/user_guide/loading.rst#_snippet_6

LANGUAGE: python
CODE:
```
from moviepy.editor import UpdatedVideoClip

class MyWorld:
    def __init__(self):
        self.clip_t = 0

    def update(self):
        # Update world state and increment self.clip_t
        pass

    def to_frame(self):
        # Render frame based on current world state
        pass

world = MyWorld()
clip = UpdatedVideoClip(world, fps=24)
```

----------------------------------------

TITLE: Merge Video and Audio with FFmpeg
DESCRIPTION: This function merges a video file with an audio file using FFmpeg. It requires FFmpeg to be installed and accessible in the system's PATH. The function takes paths to the video and audio files as input and outputs a merged video file.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/reference/reference/moviepy.video.io.ffmpeg_tools.ffmpeg_merge_video_audio.rst#_snippet_0

LANGUAGE: APIDOC
CODE:
```
moviepy.video.io.ffmpeg_tools.ffmpeg_merge_video_audio(video_input, audio_input, output,
                                                                remove_intermediates=True,
                                                                verbose=True,
                                                                ffmpeg_params=None,
                                                                method='auto')

  Merges a video file with an audio file using FFmpeg.

  Parameters:
    video_input (str): Path to the video file.
    audio_input (str): Path to the audio file.
    output (str): Path for the merged output file.
    remove_intermediates (bool, optional): If True, delete intermediate files. Defaults to True.
    verbose (bool, optional): If True, print FFmpeg output. Defaults to True.
    ffmpeg_params (list, optional): List of FFmpeg parameters to pass. Defaults to None.
    method (str, optional): The merging method. Defaults to 'auto'.

  Returns:
    None

  Example:
    ffmpeg_merge_video_audio('my_video.mp4', 'my_audio.mp3', 'output.mp4')

  Related:
    ffmpeg_extract_audio, ffmpeg_extract_subclip, ffmpeg_write_audio, ffmpeg_write_video
```

----------------------------------------

TITLE: moviepy color_gradient function
DESCRIPTION: This snippet documents the color_gradient function from the moviepy library. It is used for generating color gradients within video clips. Specific parameters, return types, and usage examples are not provided in the input text, but this function is part of the drawing tools.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/reference/reference/moviepy.video.tools.drawing.color_gradient.rst#_snippet_0

LANGUAGE: Python
CODE:
```
moviepy.video.tools.drawing.color_gradient
```

----------------------------------------

TITLE: Remove Part of a Clip
DESCRIPTION: Modifies a clip by removing a portion between specified start and end times using the `with_effects` method. This method returns a new clip and does not modify the original.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/getting_started/moviepy_10_minutes.rst#_snippet_4

LANGUAGE: python
CODE:
```
clip = clip.with_effects([
    vfx.time_slicer(start_time=600, end_time=1000)
])
```

----------------------------------------

TITLE: Get Cross-Platform Popen Parameters (Python)
DESCRIPTION: This function generates parameters suitable for `subprocess.Popen` to ensure cross-platform compatibility. It helps in executing external commands consistently across different operating systems like Windows, macOS, and Linux. The function likely returns a list or tuple of arguments that can be directly passed to `subprocess.Popen`.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/reference/reference/moviepy.tools.cross_platform_popen_params.rst#_snippet_0

LANGUAGE: python
CODE:
```
from moviepy.tools import cross_platform_popen_params

# Example usage (assuming the function returns a list of arguments):
# command = ['ffmpeg', '-i', 'input.mp4', 'output.avi']
# params = cross_platform_popen_params(command)
# print(params)

# The actual implementation details of cross_platform_popen_params are not provided in the input text,
# but it's intended to abstract away OS-specific differences in how commands and arguments are handled by subprocess.Popen.
```

----------------------------------------

TITLE: Create Text and Image Clips
DESCRIPTION: Demonstrates creating `TextClip` for text overlays and `ImageClip` for logo overlays. It involves specifying text content, font, size, color, and resizing image clips.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/getting_started/moviepy_10_minutes.rst#_snippet_5

LANGUAGE: python
CODE:
```
txt_clip = TextClip("Hello World", fontsize=50, color='white')
logo_clip = ImageClip("logo.png").set_duration(2).resize(height=50)
```

----------------------------------------

TITLE: Import MoviePy and Load Video
DESCRIPTION: Imports necessary MoviePy modules and loads a video file into a clip object. MoviePy handles various media types beyond video, including images, audio, and text.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/getting_started/moviepy_10_minutes.rst#_snippet_1

LANGUAGE: python
CODE:
```
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.config import change_settings

# change_settings({"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick-7.1.0-Q16-HDRI\\magick.exe"}) # Example for Windows

# Load the video clip
clip = VideoFileClip("trailer_bbb.mp4")
```

----------------------------------------

TITLE: moviepy.video.tools.drawing.blit Function
DESCRIPTION: The blit function is part of moviepy's drawing utilities, designed for compositing video clips. It is typically used to overlay one clip onto another. Specific parameters, return values, and usage examples are detailed in the full documentation generated by the tool.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/reference/reference/moviepy.video.tools.drawing.blit.rst#_snippet_0

LANGUAGE: python
CODE:
```
from moviepy.video.tools.drawing import blit

# Example usage (signature and parameters inferred from context):
# blit(surface, clip, pos, size=None, mask=None, transparent=0.0, method='blend')

# The actual implementation and detailed docstring would be generated by Sphinx's autofunction directive.
```

----------------------------------------

TITLE: Find Audio Period in MoviePy
DESCRIPTION: This function is part of the moviepy.audio.tools.cuts module and is designed to identify the periodic characteristics of an audio signal. Specific parameters, return values, and usage examples are not detailed in the provided documentation excerpt, but it is intended for audio analysis tasks.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/reference/reference/moviepy.audio.tools.cuts.rst#_snippet_0

LANGUAGE: python
CODE:
```
def find_audio_period(clip, fps=44100, nsamples=1000, verbose=False):
    """Finds the period of the audio signal of a clip.

    Parameters
    ----------
    clip : AudioClip
        The audio clip to analyze.
    fps : int, optional
        The number of samples per second. Default is 44100.
    nsamples : int, optional
        The number of samples to consider for the analysis. Default is 1000.
    verbose : bool, optional
        If True, prints information during the process. Default is False.

    Returns
    -------
    float
        The period of the audio signal in seconds.
    """
    # Implementation details are not provided in the source text.
    pass
```

----------------------------------------

TITLE: FFPLAY_VideoPreviewer Class Documentation
DESCRIPTION: Provides documentation for the FFPLAY_VideoPreviewer class, detailing its methods and attributes for video previewing. This class relies on the ffplay executable being available in the system's PATH.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/reference/reference/moviepy.video.io.ffplay_previewer.FFPLAY_VideoPreviewer.rst#_snippet_0

LANGUAGE: APIDOC
CODE:
```
moviepy.video.io.ffplay_previewer.FFPLAY_VideoPreviewer
=========================================================

.. currentmodule:: moviepy.video.io.ffplay_previewer

.. autoclass:: FFPLAY_VideoPreviewer
   :members:

   This class is responsible for previewing video clips using the external ffplay command-line tool. It handles the process of launching ffplay, feeding it the video data, and managing the playback window.

   Dependencies:
     - ffplay executable must be installed and accessible in the system's PATH.

   Usage:
     Instances of this class are typically created internally by moviepy when a preview function is called on a clip.

   Example:
     (Internal usage, not directly instantiated by end-users for simple previews)

   Note:
     The specific methods and attributes documented by `:members:` will be listed here, but the provided text only indicates the class itself. A full documentation would list methods like `__init__`, `play`, `close`, etc., with their respective parameters and return values.
```

----------------------------------------

TITLE: Adding Transitions and Effects in MoviePy
DESCRIPTION: Shows how to apply visual and audio effects to clips using the 'with_effects' method. This is used for creating transitions like fade-in/out and cross-fades, and for modifying clip properties.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/getting_started/moviepy_10_minutes.rst#_snippet_9

LANGUAGE: python
CODE:
```
from moviepy.editor import *
from moviepy.video.fx.all import *
from moviepy.audio.fx.all import *

# Example: Applying fade-in and fade-out effects
clip = clip.with_effects([fadein(1), fadeout(1)])

# Example: Applying a speed change effect
rambo_clip = rambo_clip.with_effects([vfx.speedx(0.5)])
```

----------------------------------------

TITLE: Positioning Clips in MoviePy
DESCRIPTION: Demonstrates how to set the position of video clips within a composition using the 'with_position' method. Positions can be specified in pixels, strings (like 'top', 'center'), or relative percentages.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/getting_started/moviepy_10_minutes.rst#_snippet_8

LANGUAGE: python
CODE:
```
clip.with_position("center")
clip.with_position((100, 50))
clip.with_position(x=0.5, y=0.5, relative=True)
```

----------------------------------------

TITLE: CompositeAudioClip Class Documentation
DESCRIPTION: Documents the CompositeAudioClip class from moviepy.audio.AudioClip. This entry provides a high-level overview and indicates that all members of the class are documented. Specific method signatures, parameters, and return values are not detailed in this input snippet but are implied by the autoclass directive.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/reference/reference/moviepy.audio.AudioClip.CompositeAudioClip.rst#_snippet_0

LANGUAGE: APIDOC
CODE:
```
moviepy.audio.AudioClip.CompositeAudioClip
==========================================

.. currentmodule:: moviepy.audio.AudioClip

.. autoclass:: CompositeAudioClip
   :members:

This documentation entry represents the structure for documenting the CompositeAudioClip class. The `autoclass` directive with `:members:` instructs the documentation generator to include all public methods and attributes of the class. Detailed API specifications for each member (parameters, return types, usage) would typically follow this declaration but are not present in the provided input text.
```

----------------------------------------

TITLE: Run MoviePy Test Suite
DESCRIPTION: Executes the project's test suite using pytest to verify the functionality of your changes and ensure no regressions have been introduced.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/developer_guide/contribution_guidelines.rst#_snippet_7

LANGUAGE: bash
CODE:
```
pytest
```

----------------------------------------

TITLE: Documenting DataVideoClip Class
DESCRIPTION: This snippet illustrates how to use Sphinx directives to document the DataVideoClip class and its members. It specifies the current module and requests all members to be documented.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/reference/reference/moviepy.video.VideoClip.DataVideoClip.rst#_snippet_0

LANGUAGE: APIDOC
CODE:
```
.. currentmodule:: moviepy.video.VideoClip

.. autoclass:: DataVideoClip
   :members:
```

----------------------------------------

TITLE: Run Test Suite
DESCRIPTION: Executes the MoviePy test suite to verify that your changes have not introduced regressions or bugs. This should be run before submitting a pull request.

SOURCE: https://github.com/zulko/moviepy/blob/master/CONTRIBUTING.md#_snippet_7

LANGUAGE: shell
CODE:
```
pytest
```

----------------------------------------

TITLE: Stage CHANGELOG.md and pyproject.toml
DESCRIPTION: Stages the changelog and project configuration files for commit. This prepares the necessary files for the release.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/developer_guide/maintainers_publish.rst#_snippet_0

LANGUAGE: shell
CODE:
```
git add CHANGELOG.md pyproject.toml
```

----------------------------------------

TITLE: Clone MoviePy Repository
DESCRIPTION: Clones the official MoviePy repository to your local machine using Git. Obtain the URL from your GitHub fork.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/developer_guide/contribution_guidelines.rst#_snippet_0

LANGUAGE: bash
CODE:
```
git clone URL_TO_YOUR_FORK
```

----------------------------------------

TITLE: Moviepy Documentation Generation Directives
DESCRIPTION: This snippet outlines the Sphinx directives and Jinja templating used to structure the documentation generation process for the moviepy project. It includes logic for handling abstract classes and conditional inclusion of modules.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/_templates/custom_autosummary/module.rst#_snippet_0

LANGUAGE: APIDOC
CODE:
```
.. custom module to enable complete documentation of every function
   see https://stackoverflow.com/a/62613202

{{ fullname | escape | underline}}

{% if fullname in ['moviepy.Effect'] or '.fx.' in fullname %} {# Fix for autosummary to document abstract class #}
.. automodule:: {{ fullname }}
   :inherited-members:
{% else %}
.. automodule:: {{ fullname }}
{% endif %}


   {% block classes %}
   {% if classes %}
   .. rubric:: {{ _('Classes') }}

   .. autosummary::
      :toctree:
      :template: custom_autosummary/class.rst
   {% for item in classes %}
      {{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}


   {% block functions %}
   {% if functions %}
   .. rubric:: {{ _('Functions') }}

   .. autosummary::
      :toctree:
   {% for item in functions %}
      {{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}


   {% block exceptions %}
   {% if exceptions %}
   .. rubric:: {{ _('Exceptions') }}

   .. autosummary::
   {% for item in exceptions %}
      {{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}

{% block modules %}
{% if modules %}
.. rubric:: Modules

.. autosummary::
   :toctree:
   :template: custom_autosummary/module.rst
   :recursive:
{% for item in modules %}
{% if not item in ['moviepy.version'] %}
   {{ item }}
{% endif %}
{%- endfor %}
{% endif %}
{% endblock %}
```

----------------------------------------

TITLE: Simplified MoviePy Imports (v2.0+)
DESCRIPTION: MoviePy v2.0 removes the `moviepy.editor` namespace. Imports should now be done directly from the `moviepy` package. Using `from moviepy import *` is recommended for simplicity, as it loads only essential components.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/getting_started/updating_to_v2.rst#_snippet_0

LANGUAGE: python
CODE:
```
from moviepy import *
from moviepy import VideoFileClip
```

----------------------------------------

TITLE: Extract Subclip with FFmpeg
DESCRIPTION: Extracts a subclip from a video file using FFmpeg. This function is part of the moviepy library and leverages FFmpeg for efficient video processing. Detailed parameters, return values, and usage examples are typically found in the full function signature, which is referenced here.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/reference/reference/moviepy.video.io.ffmpeg_tools.ffmpeg_extract_subclip.rst#_snippet_0

LANGUAGE: python
CODE:
```
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

# Example usage (parameters would be defined here):
# ffmpeg_extract_subclip("my_video.mp4", "output_subclip.mp4", start_time, end_time)
```

----------------------------------------

TITLE: Clone MoviePy Repository
DESCRIPTION: Clones the MoviePy repository from a specified URL to your local machine. This is typically done after forking the official repository to your GitHub account.

SOURCE: https://github.com/zulko/moviepy/blob/master/CONTRIBUTING.md#_snippet_0

LANGUAGE: shell
CODE:
```
git clone URL_TO_YOUR_FORK
```

----------------------------------------

TITLE: Build MoviePy Docker Image
DESCRIPTION: Builds the MoviePy Docker image using the specified Dockerfile. Ensure you are in the moviepy root directory before executing this command.

SOURCE: https://github.com/zulko/moviepy/blob/master/docs/getting_started/docker.rst#_snippet_0

LANGUAGE: shell
CODE:
```
docker build -t moviepy -f Dockerfile .
```
