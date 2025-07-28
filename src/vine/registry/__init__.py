"""Registry module for Project Vine video composition framework."""

from vine.registry.animation_registry import AnimationRegistry
from vine.registry.effect_registry import EffectRegistry
from vine.registry.transition_registry import TransitionRegistry

__all__ = ["AnimationRegistry", "TransitionRegistry", "EffectRegistry"]
