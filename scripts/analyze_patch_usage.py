#!/usr/bin/env python3
"""Script to analyze patch usage in test files and identify coverage interference."""

import re
from pathlib import Path
from typing import Dict, List, Tuple


def analyze_file(file_path: Path) -> Dict[str, List[str]]:
    """Analyze a test file for patch usage patterns."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    results = {
        "patch_decorators": [],
        "with_patch_statements": [],
        "patch_object_statements": [],
        "external_patches": [],
        "internal_patches": [],
    }

    lines = content.split("\n")

    for i, line in enumerate(lines, 1):
        line = line.strip()

        # Find @patch decorators
        if line.startswith("@patch"):
            results["patch_decorators"].append(f"Line {i}: {line}")

        # Find with patch() statements
        if "with patch(" in line:
            results["with_patch_statements"].append(f"Line {i}: {line}")

            # Check if it's patching external libraries
            if any(lib in line for lib in ["moviepy", "pydantic", "yaml", "numpy"]):
                results["external_patches"].append(f"Line {i}: {line}")
            else:
                results["internal_patches"].append(f"Line {i}: {line}")

        # Find patch.object statements
        if "patch.object(" in line:
            results["patch_object_statements"].append(f"Line {i}: {line}")

    return results


def find_test_files(directory: Path) -> List[Path]:
    """Find all test files in the directory."""
    test_files = []
    for pattern in ["test_*.py", "*_test.py"]:
        test_files.extend(directory.rglob(pattern))
    return test_files


def main():
    """Main function to analyze all test files."""
    test_dir = Path("tests")

    if not test_dir.exists():
        print(f"Test directory {test_dir} does not exist")
        return

    test_files = find_test_files(test_dir)
    print(f"Found {len(test_files)} test files")

    total_stats = {
        "patch_decorators": 0,
        "with_patch_statements": 0,
        "patch_object_statements": 0,
        "external_patches": 0,
        "internal_patches": 0,
    }

    problematic_files = []

    for test_file in test_files:
        results = analyze_file(test_file)

        # Count totals
        for key in total_stats:
            total_stats[key] += len(results[key])

        # Identify potentially problematic files
        external_count = len(results["external_patches"])
        if external_count > 0:
            problematic_files.append((test_file, external_count, results))

    print(f"\n=== PATCH USAGE SUMMARY ===")
    print(f"Total @patch decorators: {total_stats['patch_decorators']}")
    print(f"Total with patch() statements: {total_stats['with_patch_statements']}")
    print(f"Total patch.object() statements: {total_stats['patch_object_statements']}")
    print(f"External library patches: {total_stats['external_patches']}")
    print(f"Internal patches: {total_stats['internal_patches']}")

    print(f"\n=== FILES WITH EXTERNAL PATCHES (HIGHEST PRIORITY) ===")
    problematic_files.sort(key=lambda x: x[1], reverse=True)

    for file_path, count, results in problematic_files:
        print(f"\n{file_path} ({count} external patches):")
        for patch in results["external_patches"]:
            print(f"  {patch}")

    print(f"\n=== RECOMMENDATIONS ===")
    print(
        f"1. Focus on files with external patches first (most likely to interfere with coverage)"
    )
    print(f"2. Replace external patches with real integration tests where possible")
    print(f"3. Use dependency injection instead of patching internal methods")
    print(f"4. Consider using real objects instead of mocks for better coverage")


if __name__ == "__main__":
    main()
