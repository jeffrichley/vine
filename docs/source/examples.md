# Examples

## Basic Usage

```python
from vine.defaults import DefaultsManager

# Create a defaults manager
dm = DefaultsManager({"width": 1920, "height": 1080})

# Get a default value
width = dm.get("width")  # Returns 1920

# Set a new default
dm.set("fps", 30)

# Update multiple defaults
dm.update({"transition": "fade", "animation": "ken_burns"})
```

## Advanced Usage

```python
# Initialize with defaults
defaults = {
    "resolution": "1080x1920",
    "animation": "ken_burns",
    "transition": "crossfade",
    "font": "Montserrat-Bold"
}

dm = DefaultsManager(defaults)

# Get all defaults
all_defaults = dm.all

# Clear all defaults
dm.clear()
```
