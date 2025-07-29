"""
Typed YAML utilities for safe and consistent YAML operations.

This module provides typed wrapper functions around PyYAML to ensure
type safety and consistent return types across the codebase.
"""

from pathlib import Path
from typing import Any, Dict, Union

import yaml  # noqa: TID251


def load_yaml_from_path(path: Union[str, Path]) -> Any:
    """
    Load YAML data from a file path with type safety.

    Args:
        path: Path to the YAML file

    Returns:
        Parsed YAML data (typically Dict[str, Any] but could be other types)

    Raises:
        FileNotFoundError: If the file doesn't exist
        yaml.YAMLError: If the YAML is malformed
    """
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_yaml_from_string(content: str) -> Any:
    """
    Load YAML data from a string with type safety.

    Args:
        content: YAML content as a string

    Returns:
        Parsed YAML data (typically Dict[str, Any] but could be other types)

    Raises:
        yaml.YAMLError: If the YAML is malformed
    """
    return yaml.safe_load(content)


def dump_yaml_to_path(data: Dict[str, Any], path: Union[str, Path]) -> None:
    """
    Dump data to a YAML file with type safety.

    Args:
        data: Dictionary to serialize to YAML
        path: Path where the YAML file should be written

    Raises:
        OSError: If the file cannot be written
        yaml.YAMLError: If the data cannot be serialized
    """
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, default_flow_style=False, sort_keys=False)


def dump_yaml_to_string(data: Dict[str, Any]) -> str:
    """
    Dump data to a YAML string with type safety.

    Args:
        data: Dictionary to serialize to YAML

    Returns:
        YAML content as a string

    Raises:
        yaml.YAMLError: If the data cannot be serialized
    """
    return yaml.safe_dump(data, default_flow_style=False, sort_keys=False)


def validate_yaml_schema(data: Dict[str, Any], required_keys: list[str]) -> bool:
    """
    Validate that a YAML dictionary contains required keys.

    Args:
        data: Dictionary loaded from YAML
        required_keys: List of keys that must be present

    Returns:
        True if all required keys are present, False otherwise
    """
    return all(key in data for key in required_keys)
