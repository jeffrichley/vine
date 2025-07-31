#!/usr/bin/env python3
"""
Fix Test Imports Script

This script removes old wrapper imports from test files since we no longer
have wrapper functions in tests/utils.py.

Usage:
    python scripts/fix_test_imports.py
"""

import re
from pathlib import Path


def find_test_files() -> list[Path]:
    """Find all Python test files."""
    test_dir = Path("tests")
    return [
        py_file
        for py_file in test_dir.rglob("*.py")
        if py_file.name.startswith("test_") or py_file.name.endswith("_test.py")
    ]


def fix_imports_in_file(file_path: Path) -> tuple[int, list[str]]:
    """Fix imports in a single file."""
    with open(file_path) as f:
        content = f.read()

    original_content = content
    changes_made = []

    # Remove old wrapper imports
    import_patterns = [
        r"from tests\.utils import unit_test\n",
        r"from tests\.utils import slow_test\n",
        r"from tests\.utils import integration_test\n",
        r"from tests\.utils import asyncio_test\n",
        r"from tests\.utils import property_test\n",
        r"from tests\.utils import unit_property_test\n",
        r"from tests\.utils import unit_test, slow_test\n",
        r"from tests\.utils import unit_test, integration_test\n",
        r"from tests\.utils import unit_test, asyncio_test\n",
        r"from tests\.utils import unit_test, property_test\n",
        r"from tests\.utils import unit_test, unit_property_test\n",
    ]

    for pattern in import_patterns:
        if re.search(pattern, content):
            content = re.sub(pattern, "", content)
            changes_made.append(f"Removed import: {pattern.strip()}")

    # Clean up empty import lines
    content = re.sub(r"\n\s*\n\s*\n", "\n\n", content)  # Remove multiple empty lines
    content = re.sub(
        r"^\s*\n", "", content, flags=re.MULTILINE
    )  # Remove leading empty lines

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
        changes_count, changes = fix_imports_in_file(file_path)

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
        print("\n✅ No changes needed - all imports are already clean!")


if __name__ == "__main__":
    main()
