#!/usr/bin/env python3
"""
Fix Important Test Errors Script

This script helps identify and fix the remaining important mypy errors in tests.
Focuses on high-signal errors that could indicate real bugs:
- assignment: Type mismatches in variable assignments
- index: Index access issues
- arg-type: Wrong argument types being passed
- unreachable: Dead code that can never execute

Usage:
    python scripts/fix_important_test_errors.py
"""

import re
import subprocess


def run_mypy_on_tests() -> str:
    """Run mypy on tests and return the output."""
    try:
        result = subprocess.run(
            [
                "python",
                "-m",
                "mypy",
                "tests/",
                "--show-error-codes",
                "--no-error-summary",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.stdout


def parse_mypy_output(output: str) -> dict[str, list[tuple[str, int, str]]]:
    """Parse mypy output and group errors by type."""
    errors: dict[str, list[tuple[str, int, str]]] = {
        "assignment": [],
        "index": [],
        "arg-type": [],
        "unreachable": [],
        "other": [],
    }

    # Pattern to match mypy error lines
    pattern = r"([^:]+):(\d+):(\d+): error: ([^[]+)\[([^\]]+)\]"

    for line in output.strip().split("\n"):
        if not line.strip():
            continue

        match = re.match(pattern, line)
        if match:
            file_path, line_num, col_num, message, error_code = match.groups()
            line_num = int(line_num)

            if error_code in errors:
                errors[error_code].append((file_path, line_num, message.strip()))
            else:
                errors["other"].append((file_path, line_num, message.strip()))

    return errors


def analyze_errors(errors: dict[str, list[tuple[str, int, str]]]) -> None:
    """Analyze and display error statistics."""
    print("🔍 MyPy Test Error Analysis")
    print("=" * 50)

    total_errors = sum(len(error_list) for error_list in errors.values())
    print(f"Total remaining errors: {total_errors}")
    print()

    # Show important errors first
    important_codes = ["assignment", "index", "arg-type", "unreachable"]

    for error_code in important_codes:
        if errors[error_code]:
            print(f"🚨 {error_code.upper()} ({len(errors[error_code])} errors):")
            for file_path, line_num, message in errors[error_code][:5]:  # Show first 5
                print(f"   {file_path}:{line_num} - {message}")
            if len(errors[error_code]) > 5:
                print(f"   ... and {len(errors[error_code]) - 5} more")
            print()

    # Show other errors
    if errors["other"]:
        print(f"📝 Other errors ({len(errors['other'])}):")
        for file_path, line_num, message in errors["other"][:3]:  # Show first 3
            print(f"   {file_path}:{line_num} - {message}")
        if len(errors["other"]) > 3:
            print(f"   ... and {len(errors['other']) - 3} more")
        print()


def get_file_content(file_path: str, line_num: int, context_lines: int = 3) -> str:
    """Get file content around the specified line."""
    try:
        with open(file_path) as f:
            lines = f.readlines()

        start = max(0, line_num - context_lines - 1)
        end = min(len(lines), line_num + context_lines)

        content = []
        for i in range(start, end):
            prefix = ">>> " if i == line_num - 1 else "    "
            content.append(f"{prefix}{i+1:4d}: {lines[i].rstrip()}")

        return "\n".join(content)
    except Exception as e:
        return f"Error reading file: {e}"


def suggest_fixes(errors: dict[str, list[tuple[str, int, str]]]) -> None:
    """Suggest fixes for the important errors."""
    print("🔧 Suggested Fixes")
    print("=" * 50)

    important_codes = ["assignment", "index", "arg-type", "unreachable"]

    for error_code in important_codes:
        if not errors[error_code]:
            continue

        print(f"\n📋 {error_code.upper()} ERRORS:")
        print("-" * 30)

        for file_path, line_num, message in errors[error_code][:3]:  # Show first 3
            print(f"\nFile: {file_path}:{line_num}")
            print(f"Error: {message}")
            print("Context:")
            print(get_file_content(file_path, line_num))
            print()

            # Suggest specific fixes based on error type
            if error_code == "assignment":
                print(
                    "💡 Suggestion: Check variable type annotations or add type casting"
                )
            elif error_code == "index":
                print("💡 Suggestion: Add bounds checking or fix index type")
            elif error_code == "arg-type":
                print("💡 Suggestion: Fix argument type or add proper type annotation")
            elif error_code == "unreachable":
                print("💡 Suggestion: Remove dead code or fix logic flow")
            print()


def main():
    """Main function."""
    print("🔍 Running MyPy on tests...")
    output = run_mypy_on_tests()

    if not output.strip():
        print("✅ No mypy errors found in tests!")
        return

    errors = parse_mypy_output(output)
    analyze_errors(errors)

    # Check if there are important errors to fix
    important_errors = sum(
        len(errors[code]) for code in ["assignment", "index", "arg-type", "unreachable"]
    )

    if important_errors > 0:
        suggest_fixes(errors)
        print("\n🎯 Next Steps:")
        print(f"   - Fix {important_errors} important errors manually")
        print("   - Focus on assignment, index, arg-type, and unreachable errors")
        print("   - These could indicate real bugs in your test logic")
    else:
        print("✅ No important errors to fix!")


if __name__ == "__main__":
    main()
