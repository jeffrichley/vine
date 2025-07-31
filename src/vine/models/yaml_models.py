"""Typed data models for YAML and external data structures."""

from typing import Any

from pydantic import BaseModel, Field


class YamlMetadata(BaseModel):
    """Typed metadata structure for YAML data."""

    name: str | None = Field(None, description="Name identifier")
    description: str | None = Field(None, description="Description text")
    tags: list[str] = Field(default_factory=list, description="List of tags")
    priority: int | None = Field(None, description="Priority level")
    category: str | None = Field(None, description="Category classification")
    source: str | None = Field(None, description="Source information")
    custom_data: dict[str, str | int | float | bool | list[str]] = Field(
        default_factory=dict, description="Custom key-value data"
    )


class YamlNestedData(BaseModel):
    """Typed nested data structure for YAML."""

    key: str = Field(..., description="Nested key")
    value: str | int | float | bool | list[str] = Field(..., description="Nested value")


class YamlItemData(BaseModel):
    """Typed item data structure for YAML lists."""

    name: str = Field(..., description="Item name")
    value: str | int | float | bool = Field(..., description="Item value")
    metadata: YamlMetadata | None = Field(None, description="Item metadata")


class YamlDocument(BaseModel):
    """Typed document structure for YAML files."""

    name: str | None = Field(None, description="Document name")
    value: str | int | float | bool | None = Field(None, description="Document value")
    nested: YamlNestedData | None = Field(None, description="Nested data")
    items: list[YamlItemData] = Field(default_factory=list, description="List of items")
    metadata: YamlMetadata = Field(
        default_factory=YamlMetadata, description="Document metadata"
    )


# Type alias for generic YAML data that can be any of our typed structures
YamlData = YamlDocument | YamlMetadata | YamlNestedData | YamlItemData | dict[str, Any]


class RegistryComponent(BaseModel):
    """Typed component structure for registry data."""

    name: str = Field(..., description="Component name")
    type: str = Field(..., description="Component type")
    config: dict[str, str | int | float | bool | list[str]] = Field(
        default_factory=dict, description="Component configuration"
    )
    metadata: YamlMetadata = Field(
        default_factory=YamlMetadata, description="Component metadata"
    )


class DefaultsData(BaseModel):
    """Typed defaults structure for configuration data."""

    width: int | None = Field(None, description="Default width")
    height: int | None = Field(None, description="Default height")
    fps: float | None = Field(None, description="Default FPS")
    duration: float | None = Field(None, description="Default duration")
    volume: float | None = Field(None, description="Default volume")
    custom_defaults: dict[str, str | int | float | bool] = Field(
        default_factory=dict, description="Custom default values"
    )
