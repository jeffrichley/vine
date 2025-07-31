"""
Typed YAML utilities for safe and consistent YAML operations.

This module provides typed wrapper functions around PyYAML to ensure
type safety and consistent return types across the codebase.
"""

from pathlib import Path

import yaml  # noqa: TID251

from vine.models.yaml_models import YamlData


def load_yaml_from_path(path: str | Path) -> YamlData:
    """
    Load YAML data from a file path with type safety.

    Args:
        path: Path to the YAML file

    Returns:
        Parsed YAML data as typed YamlData

    Raises:
        FileNotFoundError: If the file doesn't exist
        yaml.YAMLError: If the YAML is malformed
    """
    with open(path, encoding="utf-8") as f:
        # Type ignore only at the boundary where we load from external source
        return yaml.safe_load(f)  # type: ignore[misc,no-any-return]


def load_yaml_from_string(content: str) -> YamlData:
    """
    Load YAML data from a string with type safety.

    Args:
        content: YAML content as a string

    Returns:
        Parsed YAML data as typed YamlData

    Raises:
        yaml.YAMLError: If the YAML is malformed
    """
    # Type ignore only at the boundary where we load from external source
    return yaml.safe_load(content)  # type: ignore[misc,no-any-return]


def dump_yaml_to_path(data: YamlData, path: str | Path) -> None:
    """
    Dump data to a YAML file with type safety.

    Args:
        data: Typed data to serialize to YAML
        path: Path where the YAML file should be written

    Raises:
        OSError: If the file cannot be written
        yaml.YAMLError: If the data cannot be serialized
    """
    with open(path, "w", encoding="utf-8") as f:
        # Type ignore only at the boundary where we dump to external format
        yaml.safe_dump(data, f, default_flow_style=False, sort_keys=False)


def dump_yaml_to_string(data: YamlData) -> str:
    """
    Dump data to a YAML string with type safety.

    Args:
        data: Typed data to serialize to YAML

    Returns:
        YAML content as a string

    Raises:
        yaml.YAMLError: If the data cannot be serialized
    """
    # Type ignore only at the boundary where we dump to external format
    return yaml.safe_dump(data, default_flow_style=False, sort_keys=False)


def validate_yaml_schema(data: YamlData, required_keys: list[str]) -> bool:
    """
    Validate that a YAML dictionary contains required keys.

    Args:
        data: Typed data loaded from YAML
        required_keys: List of keys that must be present

    Returns:
        True if all required keys are present, False otherwise
    """
    return all(key in data for key in required_keys)
