#!/usr/bin/env python3
"""Script to fix missing imports for type annotations."""

import re
from pathlib import Path


def fix_imports_in_file(file_path: Path) -> tuple[int, list[str]]:
    """Fix missing imports for type annotations in a file.

    Returns:
        Tuple of (number of imports added, list of import names)
    """
    with open(file_path) as f:
        content = f.read()

    original_content = content
    imports_added = []

    # Check if we need to add Any import
    needs_any = "-> Any" in content or ": Any" in content
    has_any_import = "from typing import Any" in content or "import Any" in content

    # Check if we need to add MagicMock import
    needs_magicmock = ": MagicMock" in content
    has_magicmock_import = "from unittest.mock import MagicMock" in content

    if needs_any and not has_any_import:
        imports_added.append("Any")

        # Find the typing import line or create one
        typing_pattern = r"from typing import ([^,\n]+)"
        typing_match = re.search(typing_pattern, content)

        if typing_match:
            # Add Any to existing typing import
            existing_imports = typing_match.group(1)
            if "Any" not in existing_imports:
                new_imports = f"{existing_imports}, Any"
                content = re.sub(
                    typing_pattern, f"from typing import {new_imports}", content
                )
        else:
            # Create new typing import
            content = "from typing import Any\n" + content

    if needs_magicmock and not has_magicmock_import:
        imports_added.append("MagicMock")

        # Find the unittest.mock import line or create one
        mock_pattern = r"from unittest\.mock import ([^,\n]+)"
        mock_match = re.search(mock_pattern, content)

        if mock_match:
            # Add MagicMock to existing unittest.mock import
            existing_imports = mock_match.group(1)
            if "MagicMock" not in existing_imports:
                new_imports = f"{existing_imports}, MagicMock"
                content = re.sub(
                    mock_pattern, f"from unittest.mock import {new_imports}", content
                )
        else:
            # Create new unittest.mock import
            content = "from unittest.mock import MagicMock\n" + content

    if content != original_content:
        # Create backup
        backup_path = file_path.with_suffix(file_path.suffix + ".import_backup")
        with open(backup_path, "w") as f:
            f.write(original_content)

        # Write modified content
        with open(file_path, "w") as f:
            f.write(content)

        return len(imports_added), imports_added

    return 0, []


def main() -> None:
    """Process all test files for missing imports."""
    test_dir = Path("tests")
    total_files_modified = 0
    total_imports_added = 0

    print("Fixing missing imports for type annotations...")
    print("=" * 50)

    for py_file in sorted(test_dir.rglob("*.py")):
        if py_file.name.startswith("test_") or "test" in py_file.name:
            if py_file.suffix in [
                ".backup",
                ".fixture_backup",
                ".mock_backup",
                ".import_backup",
            ]:
                continue  # Skip backup files

            imports_added, import_names = fix_imports_in_file(py_file)

            if imports_added > 0:
                total_files_modified += 1
                total_imports_added += imports_added
                print(f"✓ {py_file}: Added {imports_added} imports")
                for import_name in import_names:
                    print(f"  - {import_name}")
            else:
                print(f"- {py_file}: No import fixes needed")

    print("=" * 50)
    print(
        f"Summary: Added {total_imports_added} imports in {total_files_modified} files"
    )

    if total_files_modified > 0:
        print("\nBackup files created with .import_backup extension")
        print("Run tests to verify functionality is preserved")


if __name__ == "__main__":
    main()
