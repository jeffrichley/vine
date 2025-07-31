#!/usr/bin/env python3
"""Script to add return type annotations to pytest fixtures."""

import re
from pathlib import Path


def add_fixture_return_types_to_file(file_path: Path) -> tuple[int, list[str]]:
    """Add return type annotations to pytest fixtures in a file.

    Returns:
        Tuple of (number of fixtures modified, list of fixture names)
    """
    with open(file_path) as f:
        content = f.read()

    original_content = content
    modified_fixtures = []

    # Pattern to match pytest fixture definitions without return types
    # This pattern looks for @pytest.fixture followed by def fixture_name():
    pattern = r"^(\s*@pytest\.fixture[^\n]*\n\s*def\s+(\w+)\s*\([^)]*\)\s*):(\s*)$"

    def replace_fixture(match):
        full_match = match.group(0)
        fixture_name = match.group(2)
        trailing = match.group(3)

        modified_fixtures.append(fixture_name)

        # Add -> Any return type (since fixtures can return various types)
        return f"{full_match.rstrip()[:-1]} -> Any:{trailing}"

    new_content = re.sub(pattern, replace_fixture, content, flags=re.MULTILINE)

    if new_content != original_content:
        # Create backup
        backup_path = file_path.with_suffix(file_path.suffix + ".fixture_backup")
        with open(backup_path, "w") as f:
            f.write(original_content)

        # Write modified content
        with open(file_path, "w") as f:
            f.write(new_content)

        return len(modified_fixtures), modified_fixtures

    return 0, []


def main() -> None:
    """Process all test files for fixture return types."""
    test_dir = Path("tests")
    total_files_modified = 0
    total_fixtures_modified = 0

    print("Adding return type annotations to pytest fixtures...")
    print("=" * 50)

    for py_file in sorted(test_dir.rglob("*.py")):
        if py_file.name.startswith("test_") or "test" in py_file.name:
            if py_file.suffix in [".backup", ".fixture_backup"]:
                continue  # Skip backup files

            fixtures_modified, fixture_names = add_fixture_return_types_to_file(py_file)

            if fixtures_modified > 0:
                total_files_modified += 1
                total_fixtures_modified += fixtures_modified
                print(f"✓ {py_file}: {fixtures_modified} fixtures modified")
                for fixture_name in fixture_names:
                    print(f"  - {fixture_name}")
            else:
                print(f"- {py_file}: No fixture changes needed")

    print("=" * 50)
    print(
        f"Summary: Modified {total_fixtures_modified} fixtures in {total_files_modified} files"
    )

    if total_files_modified > 0:
        print("\nBackup files created with .fixture_backup extension")
        print("Run tests to verify functionality is preserved")


if __name__ == "__main__":
    main()
