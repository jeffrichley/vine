"""
Tests for YAML utilities module.
"""

import tempfile
from pathlib import Path
from typing import Any, cast

import pytest

from vine.utils.yaml_utils import (
    dump_yaml_to_path,
    dump_yaml_to_string,
    load_yaml_from_path,
    load_yaml_from_string,
    validate_yaml_schema,
)


class TestYAMLUtils:
    """Test cases for YAML utility functions."""

    @pytest.mark.unit
    def test_load_yaml_from_string(self) -> None:
        """Test loading YAML from a string."""
        yaml_content = """
        name: test
        value: 42
        nested:
          key: value
        """
        result = cast(dict[str, Any], load_yaml_from_string(yaml_content))
        assert result["name"] == "test"
        assert result["value"] == 42
        assert result["nested"]["key"] == "value"

    @pytest.mark.unit
    def test_dump_yaml_to_string(self) -> None:
        """Test dumping data to YAML string."""
        data = {"name": "test", "value": 42, "nested": {"key": "value"}}
        result = dump_yaml_to_string(data)
        # Should contain the expected content
        assert "name: test" in result
        assert "value: 42" in result
        assert "nested:" in result

    @pytest.mark.unit
    def test_load_yaml_from_path(self) -> None:
        """Test loading YAML from a file path."""
        data = {"name": "test", "value": 42, "nested": {"key": "value"}}
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            dump_yaml_to_path(data, f.name)
            temp_path = f.name
        try:
            result = cast(dict[str, Any], load_yaml_from_path(temp_path))
            assert result["name"] == "test"
            assert result["value"] == 42
            assert result["nested"]["key"] == "value"
        finally:
            Path(temp_path).unlink()

    @pytest.mark.unit
    def test_dump_yaml_to_path(self) -> None:
        """Test dumping data to a file path."""
        data = {"name": "test", "value": 42, "nested": {"key": "value"}}
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            temp_path = f.name
        try:
            dump_yaml_to_path(data, temp_path)
            # Verify the file was written correctly
            result = cast(dict[str, Any], load_yaml_from_path(temp_path))
            assert result["name"] == "test"
            assert result["value"] == 42
            assert result["nested"]["key"] == "value"
        finally:
            Path(temp_path).unlink()

    @pytest.mark.unit
    def test_validate_yaml_schema(self) -> None:
        """Test YAML schema validation."""
        data = {"name": "test", "value": 42, "optional": "present"}
        # Should pass with all required keys
        assert validate_yaml_schema(data, ["name", "value"])
        # Should fail with missing required key
        assert not validate_yaml_schema(data, ["name", "value", "missing"])

    @pytest.mark.unit
    def test_load_yaml_with_list(self) -> None:
        """Test loading YAML that contains lists."""
        yaml_content = """
        items:
          - name: item1
            value: 1
          - name: item2
            value: 2
        """
        result = cast(dict[str, Any], load_yaml_from_string(yaml_content))
        assert len(result["items"]) == 2
        assert result["items"][0]["name"] == "item1"
        assert result["items"][0]["value"] == 1
        assert result["items"][1]["name"] == "item2"
        assert result["items"][1]["value"] == 2
