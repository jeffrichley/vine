#!/usr/bin/env python3
"""
Remove Test Wrapper Decorators Script

This script replaces all test wrapper decorators with direct pytest and hypothesis decorators.
Since mypy is configured to ignore decorator-related errors in test files, we can use
the original decorators directly without wrappers.

Usage:
    python scripts/remove_test_wrappers.py
"""

import re
from pathlib import Path

# Mapping of wrapper decorators to their replacements
WRAPPER_REPLACEMENTS = {
    # Simple pytest wrappers
    r"@unit_test": "@pytest.mark.unit",
    r"@slow_test": "@pytest.mark.slow",
    r"@integration_test": "@pytest.mark.integration",
    r"@asyncio_test": "@pytest.mark.asyncio",
    # Property test wrappers (need special handling)
    r"@property_test\(([^)]+)\)": r"@given(\1)",
    r"@unit_property_test\(([^)]+)\)": r"@pytest.mark.unit\n    @given(\1)",
}


def find_test_files() -> list[Path]:
    """Find all Python test files."""
    test_dir = Path("tests")
    return [
        py_file
        for py_file in test_dir.rglob("*.py")
        if py_file.name.startswith("test_") or py_file.name.endswith("_test.py")
    ]


def replace_wrappers_in_file(file_path: Path) -> tuple[int, list[str]]:
    """Replace wrapper decorators in a single file."""
    with open(file_path) as f:
        content = f.read()

    original_content = content
    changes_made = []

    # Replace simple wrappers
    for pattern, replacement in WRAPPER_REPLACEMENTS.items():
        if re.search(pattern, content):
            new_content = re.sub(pattern, replacement, content)
            if new_content != content:
                content = new_content
                changes_made.append(f"Replaced {pattern} with {replacement}")

    # Special handling for unit_property_test with settings
    # This is more complex because we need to handle the settings part
    unit_property_pattern = r"@unit_property_test\(([^)]+)\)"
    unit_property_matches = re.finditer(unit_property_pattern, original_content)

    for match in unit_property_matches:
        args = match.group(1)
        # Split arguments to separate strategies from settings
        if "**" in args:
            # Has settings kwargs
            parts = args.split("**")
            strategies = parts[0].strip().rstrip(",")
            settings_kwargs = "**" + parts[1]

            replacement = f"@pytest.mark.unit\n    @given({strategies})\n    @settings({settings_kwargs})"
        else:
            # No settings kwargs
            replacement = f"@pytest.mark.unit\n    @given({args})"

        content = content.replace(match.group(0), replacement)
        changes_made.append(
            "Replaced unit_property_test with pytest.mark.unit + @given + @settings"
        )

    # Write back if changes were made
    if content != original_content:
        with open(file_path, "w") as f:
            f.write(content)
        return len(changes_made), changes_made

    return 0, []


def main():
    """Main function to process all test files."""
    print("🔍 Finding test files...")
    test_files = find_test_files()
    print(f"Found {len(test_files)} test files")

    total_changes = 0
    files_modified = 0

    for file_path in test_files:
        print(f"\n📝 Processing {file_path}...")
        changes_count, changes = replace_wrappers_in_file(file_path)

        if changes_count > 0:
            files_modified += 1
            total_changes += changes_count
            print(f"  ✅ Made {changes_count} changes:")
            for change in changes:
                print(f"    - {change}")
        else:
            print("  ⏭️  No changes needed")

    print("\n🎉 Summary:")
    print(f"  - Files processed: {len(test_files)}")
    print(f"  - Files modified: {files_modified}")
    print(f"  - Total changes: {total_changes}")

    if files_modified > 0:
        print("\n📋 Next steps:")
        print("  1. Run tests to ensure everything still works:")
        print("     python -m pytest tests/ -v")
        print("  2. Run mypy to verify no new errors:")
        print("     python -m mypy tests/")
        print("  3. Review the changes and commit if satisfied")
    else:
        print("\n✅ No changes needed - all files already use direct decorators!")


if __name__ == "__main__":
    main()
