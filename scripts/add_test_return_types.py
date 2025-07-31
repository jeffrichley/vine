#!/usr/bin/env python3
"""Script to automatically add -> None return types to test functions."""

import re
from pathlib import Path


def add_return_types_to_file(file_path: Path) -> tuple[int, list[str]]:
    """Add -> None return types to test functions in a file.

    Returns:
        Tuple of (number of functions modified, list of function names)
    """
    with open(file_path) as f:
        content = f.read()

    original_content = content
    modified_functions = []

    # Pattern to match test function definitions without return types
    # This pattern is conservative to avoid false positives
    pattern = r"^(\s*)(def\s+test_\w+\s*\([^)]*\)\s*):(\s*)$"

    def replace_function(match):
        indent = match.group(1)
        func_def = match.group(2)
        trailing = match.group(3)

        # Extract function name for logging
        func_name_match = re.search(r"def\s+(test_\w+)", func_def)
        if func_name_match:
            modified_functions.append(func_name_match.group(1))

        # Add -> None return type
        return f"{indent}{func_def} -> None:{trailing}"

    new_content = re.sub(pattern, replace_function, content, flags=re.MULTILINE)

    if new_content != original_content:
        # Create backup
        backup_path = file_path.with_suffix(file_path.suffix + ".backup")
        with open(backup_path, "w") as f:
            f.write(original_content)

        # Write modified content
        with open(file_path, "w") as f:
            f.write(new_content)

        return len(modified_functions), modified_functions

    return 0, []


def main() -> None:
    """Process all test files."""
    test_dir = Path("tests")
    total_files_modified = 0
    total_functions_modified = 0

    print("Adding -> None return types to test functions...")
    print("=" * 50)

    for py_file in sorted(test_dir.rglob("*.py")):
        if py_file.name.startswith("test_") or "test" in py_file.name:
            if py_file.suffix == ".backup":
                continue  # Skip backup files

            functions_modified, function_names = add_return_types_to_file(py_file)

            if functions_modified > 0:
                total_files_modified += 1
                total_functions_modified += functions_modified
                print(f"✓ {py_file}: {functions_modified} functions modified")
                for func_name in function_names[:5]:  # Show first 5 function names
                    print(f"  - {func_name}")
                if len(function_names) > 5:
                    print(f"  ... and {len(function_names) - 5} more")
            else:
                print(f"- {py_file}: No changes needed")

    print("=" * 50)
    print(
        f"Summary: Modified {total_functions_modified} functions in {total_files_modified} files"
    )

    if total_files_modified > 0:
        print("\nBackup files created with .backup extension")
        print("Run tests to verify functionality is preserved")


if __name__ == "__main__":
    main()
