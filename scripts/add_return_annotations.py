#!/usr/bin/env python3
"""Script to add -> None return annotations to test functions."""

import re
import sys
from pathlib import Path


def add_return_annotations_to_file(file_path: Path) -> int:
    """Add -> None to test functions that don't have return annotations."""
    with open(file_path) as f:
        content = f.read()

    # Pattern to match test function definitions without return annotations
    # Matches: def test_something(...): or def test_something(...) -> something:
    pattern = r"def (test_\w+)\(([^)]*)\):(?!\s*->)"

    def replacement(match):
        func_name = match.group(1)
        params = match.group(2)
        return f"def {func_name}({params}) -> None:"

    new_content = re.sub(pattern, replacement, content)

    if new_content != content:
        with open(file_path, "w") as f:
            f.write(new_content)
        return 1
    return 0


def main():
    """Process all test files."""
    test_dir = Path("tests")
    if not test_dir.exists():
        print("Tests directory not found")
        sys.exit(1)

    files_updated = 0
    total_files = 0

    for py_file in test_dir.rglob("*.py"):
        total_files += 1
        if add_return_annotations_to_file(py_file):
            files_updated += 1
            print(f"Updated: {py_file}")

    print(f"\nSummary: Updated {files_updated} out of {total_files} test files")


if __name__ == "__main__":
    main()
