#!/usr/bin/env python3
"""
Script to fix mock typing issues in test files.

This script addresses Phase 2.1 of the MyPy cleanup plan by:
1. Replacing untyped mock assignments with properly typed ones
2. Adding proper type annotations to mock variables
3. Using the new typed mock protocols from conftest.py
"""

import re
import sys
from pathlib import Path


def fix_mock_typing_in_file(file_path: Path) -> list[str]:
    """Fix mock typing issues in a single test file."""
    changes = []

    with open(file_path, encoding="utf-8") as f:
        content = f.read()

    original_content = content

    # Pattern 1: Fix MockRenderer.return_value assignments
    # Before: mock_renderer = MockRenderer.return_value
    # After: mock_renderer: MockVideoRenderer = MockRenderer.return_value
    pattern1 = r"(mock_renderer)\s*=\s*(MockRenderer\.return_value)"
    replacement1 = r"\1: MockVideoRenderer = \2"
    content = re.sub(pattern1, replacement1, content)

    # Pattern 2: Fix MockClip.return_value assignments
    # Before: mock_clip = MockClip.return_value
    # After: mock_clip: MockAudioFileClip = MockClip.return_value
    pattern2 = r"(mock_clip)\s*=\s*(MockClip\.return_value)"
    replacement2 = r"\1: MockAudioFileClip = \2"
    content = re.sub(pattern2, replacement2, content)

    # Pattern 3: Fix MagicMock() assignments with proper typing
    # Before: mock_clip = MagicMock()
    # After: mock_clip: MockVideoClip = MagicMock()
    pattern3 = r"(mock_clip)\s*=\s*MagicMock\(\)"
    replacement3 = r"\1: MockVideoClip = MagicMock()"
    content = re.sub(pattern3, replacement3, content)

    # Pattern 4: Fix mock_audio assignments
    # Before: mock_audio = MagicMock()
    # After: mock_audio: MockAudioClip = MagicMock()
    pattern4 = r"(mock_audio)\s*=\s*MagicMock\(\)"
    replacement4 = r"\1: MockAudioClip = MagicMock()"
    content = re.sub(pattern4, replacement4, content)

    # Pattern 5: Fix mock_factory assignments
    # Before: mock_factory = MagicMock()
    # After: mock_factory: MockClipFactory = MagicMock()
    pattern5 = r"(mock_factory)\s*=\s*MagicMock\(\)"
    replacement5 = r"\1: MockClipFactory = MagicMock()"
    content = re.sub(pattern5, replacement5, content)

    # Add imports if needed
    if (
        "MockVideoRenderer" in content
        and "from tests.conftest import MockVideoRenderer" not in content
    ):
        # Find the import section and add our imports
        import_pattern = r"(from unittest\.mock import.*?)(\n)"
        import_replacement = r"\1, MockVideoRenderer, MockAudioFileClip, MockVideoClip, MockAudioClip, MockClipFactory\2"
        content = re.sub(import_pattern, import_replacement, content, flags=re.DOTALL)

        # If no unittest.mock import, add a new import line
        if "from unittest.mock import" not in content:
            # Add after existing imports
            content = re.sub(
                r"(import pytest\n)",
                r"\1from tests.conftest import MockVideoRenderer, MockAudioFileClip, MockVideoClip, MockAudioClip, MockClipFactory\n",
                content,
            )

    if content != original_content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        changes.append(f"Fixed mock typing in {file_path}")

    return changes


def main() -> None:
    """Main function to fix mock typing across all test files."""
    test_dir = Path("tests")

    if not test_dir.exists():
        print("Error: tests directory not found")
        sys.exit(1)

    # Find all Python test files
    test_files = list(test_dir.rglob("*.py"))

    all_changes = []

    for test_file in test_files:
        if test_file.name.startswith("__"):
            continue

        try:
            changes = fix_mock_typing_in_file(test_file)
            all_changes.extend(changes)
        except Exception as e:
            print(f"Error processing {test_file}: {e}")

    # Print summary
    print(f"Fixed mock typing in {len(all_changes)} files:")
    for change in all_changes:
        print(f"  - {change}")

    if all_changes:
        print("\nMock typing fixes completed successfully!")
    else:
        print("\nNo mock typing issues found.")


if __name__ == "__main__":
    main()
