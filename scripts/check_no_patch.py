#!/usr/bin/env python3
"""Pre-commit hook to check for @patch usage in test files.

This script will fail if it finds any @patch decorators or with patch() statements
in test files, as these can interfere with coverage measurement.
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple


def find_patch_usage(file_path: Path) -> List[Tuple[int, str]]:
    """Find all @patch usage in a file.

    Args:
        file_path: Path to the file to check

    Returns:
        List of tuples (line_number, line_content) containing patch usage
    """
    violations = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for i, line in enumerate(lines, 1):
            line = line.strip()

            # Check for @patch decorators
            if line.startswith("@patch"):
                violations.append((i, line))

            # Check for with patch() statements
            if "with patch(" in line:
                violations.append((i, line))

            # Check for patch.object() statements
            if "patch.object(" in line:
                violations.append((i, line))

    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

    return violations


def check_test_files(directory: Path = Path("tests")) -> bool:
    """Check all test files for patch usage.

    Args:
        directory: Directory to check (default: tests/)

    Returns:
        True if no violations found, False otherwise
    """
    if not directory.exists():
        print(f"Directory {directory} does not exist")
        return True

    # Find all test files
    test_files = []
    for pattern in ["test_*.py", "*_test.py"]:
        test_files.extend(directory.rglob(pattern))

    violations_found = False

    for test_file in test_files:
        violations = find_patch_usage(test_file)

        if violations:
            violations_found = True
            print(f"\n❌ {test_file}:")
            for line_num, line_content in violations:
                print(f"  Line {line_num}: {line_content}")

    if violations_found:
        print(f"\n🚫 Found patch usage in test files!")
        print(f"Please replace @patch decorators and with patch() statements with:")
        print(f"  - Direct mock objects")
        print(f"  - Dependency injection")
        print(f"  - Real integration tests")
        print(f"  - Temporary module replacement (as done in test_contexts.py)")
        print(f"\nThis helps improve coverage measurement accuracy.")
        return False
    else:
        print(f"✅ No patch usage found in {len(test_files)} test files")
        return True


def main():
    """Main function for command line usage."""
    if len(sys.argv) > 1:
        directory = Path(sys.argv[1])
    else:
        directory = Path("tests")

    success = check_test_files(directory)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
