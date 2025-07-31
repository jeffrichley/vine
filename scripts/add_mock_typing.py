#!/usr/bin/env python3
"""Script to add proper typing to mock objects and MagicMock instances."""

import re
from pathlib import Path


def add_mock_typing_to_file(file_path: Path) -> tuple[int, list[str]]:
    """Add proper typing to mock objects in a file.

    Returns:
        Tuple of (number of mocks modified, list of mock names)
    """
    with open(file_path) as f:
        content = f.read()

    original_content = content
    modified_mocks = []

    # Pattern to match MagicMock() assignments without type annotations
    # This pattern looks for variable = MagicMock() without type hints
    pattern = r"^(\s*)(\w+)\s*=\s*MagicMock\(\)(\s*)$"

    def replace_mock(match):
        indent = match.group(1)
        var_name = match.group(2)
        trailing = match.group(3)

        modified_mocks.append(var_name)

        # Add type annotation for MagicMock
        return f"{indent}{var_name}: MagicMock = MagicMock(){trailing}"

    new_content = re.sub(pattern, replace_mock, content, flags=re.MULTILINE)

    # Also handle patch decorators that create mocks
    # Pattern for @patch decorators that might need typing
    patch_pattern = r"^(\s*@patch\([^)]*\)\s*\n\s*def\s+(\w+)\s*\([^)]*\)\s*):(\s*)$"

    def replace_patch_function(match):
        full_match = match.group(0)
        trailing = match.group(3)

        # Add -> None return type to patch functions
        return f"{full_match.rstrip()[:-1]} -> None:{trailing}"

    new_content = re.sub(
        patch_pattern, replace_patch_function, new_content, flags=re.MULTILINE
    )

    if new_content != original_content:
        # Create backup
        backup_path = file_path.with_suffix(file_path.suffix + ".mock_backup")
        with open(backup_path, "w") as f:
            f.write(original_content)

        # Write modified content
        with open(file_path, "w") as f:
            f.write(new_content)

        return len(modified_mocks), modified_mocks

    return 0, []


def main() -> None:
    """Process all test files for mock typing."""
    test_dir = Path("tests")
    total_files_modified = 0
    total_mocks_modified = 0

    print("Adding proper typing to mock objects...")
    print("=" * 50)

    for py_file in sorted(test_dir.rglob("*.py")):
        if py_file.name.startswith("test_") or "test" in py_file.name:
            if py_file.suffix in [".backup", ".fixture_backup", ".mock_backup"]:
                continue  # Skip backup files

            mocks_modified, mock_names = add_mock_typing_to_file(py_file)

            if mocks_modified > 0:
                total_files_modified += 1
                total_mocks_modified += mocks_modified
                print(f"✓ {py_file}: {mocks_modified} mocks modified")
                for mock_name in mock_names[:5]:  # Show first 5 mock names
                    print(f"  - {mock_name}")
                if len(mock_names) > 5:
                    print(f"  ... and {len(mock_names) - 5} more")
            else:
                print(f"- {py_file}: No mock changes needed")

    print("=" * 50)
    print(
        f"Summary: Modified {total_mocks_modified} mocks in {total_files_modified} files"
    )

    if total_files_modified > 0:
        print("\nBackup files created with .mock_backup extension")
        print("Run tests to verify functionality is preserved")


if __name__ == "__main__":
    main()
