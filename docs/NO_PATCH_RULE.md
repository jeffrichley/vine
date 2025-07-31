# No @patch Rule

## Overview

This project has a rule that **prohibits the use of `@patch` decorators and `with patch()` statements** in test files. This rule is enforced by a pre-commit hook that will fail if any patch usage is detected.

## Why This Rule Exists

The `@patch` decorator and `with patch()` context managers can interfere with coverage measurement tools, leading to:

- **Inaccurate coverage reports** - Some code paths may not be counted as covered
- **Coverage discrepancies** between local and CI environments
- **Difficulty in achieving consistent coverage targets**

## What Gets Checked

The pre-commit hook checks for:

- `@patch` decorators
- `with patch()` statements  
- `patch.object()` statements

## How to Replace @patch Usage

### 1. Direct Mock Objects

Instead of patching modules, create mock objects directly:

```python
# ❌ Before
@patch("vine.rendering.clip_factory.ImageClip")
def test_something(self, mock_image_clip):
    mock_image_clip.return_value = mock_clip
    # test code

# ✅ After
def test_something(self):
    mock_clip = MagicMock()
    # Store original and replace temporarily
    import vine.rendering.clip_factory
    original_image_clip = vine.rendering.clip_factory.ImageClip
    try:
        vine.rendering.clip_factory.ImageClip = MagicMock(return_value=mock_clip)
        # test code
    finally:
        vine.rendering.clip_factory.ImageClip = original_image_clip
```

### 2. Dependency Injection

Pass mock objects as parameters instead of patching:

```python
# ❌ Before
with patch.object(renderer, 'create_clips') as mock_create:
    renderer.create_clips()

# ✅ After
def test_with_mock_renderer(self, mock_renderer):
    mock_renderer.create_clips.return_value = []
    # test code
```

### 3. Real Integration Tests

Use real objects when possible:

```python
# ❌ Before
with patch("moviepy.audio.io.AudioFileClip.AudioFileClip"):
    # test code

# ✅ After
# Use real audio files or create minimal test files
def test_with_real_audio(self):
    # test with actual audio file
```

### 4. Temporary Module Replacement

For complex cases, temporarily replace modules (as done in `test_contexts.py`):

```python
# Store original module/class
original_class = module.ClassToMock
try:
    # Replace with mock
    module.ClassToMock = MockClass
    # test code
finally:
    # Restore original
    module.ClassToMock = original_class
```

## Running the Check

### Manual Check
```bash
make check-no-patch
```

### Pre-commit Hook
The check runs automatically on every commit. To run manually:
```bash
pre-commit run check-no-patch --all-files
```

### CI Integration
The check is also run in CI and will fail the build if any patch usage is found.

## Random Test Ordering

This project uses pytest-randomly to run tests in random order, which helps detect test interdependencies and ordering issues.

### Auto-Generated Seeds
- **Default behavior**: When running tests normally, pytest-randomly generates a new random seed each time
- **No fixed seed**: This ensures tests are truly randomized and can catch ordering-dependent bugs
- **Seed visibility**: The seed used is displayed in the test output for reproducibility

### Reproducible Seeds
- **For debugging**: Use `make test-seed SEED=12345` to run tests with a specific seed
- **For CI failures**: Use the displayed seed to reproduce failures locally
- **Direct usage**: `uv run pytest --randomly-seed=12345`

### Commands
```bash
# Run tests with auto-generated random seed (new seed each time)
make test-random
uv run pytest

# Run tests with specific seed for reproducibility
make test-seed SEED=12345
uv run pytest --randomly-seed=12345
```

## Examples of Successful Refactoring

See `tests/vine/models/test_contexts.py` for examples of how to replace `@patch` usage with the temporary module replacement pattern.

## Benefits

- **Accurate coverage measurement** - No interference with coverage tools
- **Consistent results** - Same coverage locally and in CI
- **Better test quality** - Forces more explicit mocking patterns
- **Easier debugging** - Clearer what's being mocked and how

## Migration Strategy

1. **Identify patch usage**: Run `make check-no-patch`
2. **Prioritize by impact**: Focus on external library patches first
3. **Refactor incrementally**: One file at a time
4. **Verify coverage**: Ensure coverage improves after refactoring
5. **Update tests**: Make sure all tests still pass

## Exceptions

In rare cases where `@patch` is absolutely necessary, you can temporarily disable the check by adding a comment:

```python
# noqa: patch-usage
@patch("some.module")
def test_something(self, mock_module):
    # test code
```

However, this should be avoided and used only as a last resort. 