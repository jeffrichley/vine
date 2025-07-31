#!/usr/bin/env python3
"""
Quality Gates Runner for Vine Project

This script runs all quality gates and provides detailed reporting.
Can be used both locally and in CI environments.
"""

import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class QualityGateResult:
    """Result of a quality gate check."""

    name: str
    passed: bool
    output: str
    error_code: int
    duration: float


class QualityGatesRunner:
    """Runs quality gates and provides reporting."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.results: list[QualityGateResult] = []

    def run_command(self, cmd: list[str], name: str) -> QualityGateResult:
        """Run a command and capture its result."""
        print(f"🔍 Running {name}...")
        start_time = datetime.now()

        try:
            result = subprocess.run(
                cmd,
                check=False,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
            )
            duration = (datetime.now() - start_time).total_seconds()

            return QualityGateResult(
                name=name,
                passed=result.returncode == 0,
                output=result.stdout + result.stderr,
                error_code=result.returncode,
                duration=duration,
            )
        except subprocess.TimeoutExpired:
            duration = (datetime.now() - start_time).total_seconds()
            return QualityGateResult(
                name=name,
                passed=False,
                output=f"Timeout after {duration}s",
                error_code=-1,
                duration=duration,
            )
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            return QualityGateResult(
                name=name, passed=False, output=str(e), error_code=-2, duration=duration
            )

    def run_linting_gate(self) -> QualityGateResult:
        """Run linting quality gate."""
        return self.run_command(
            ["uv", "run", "ruff", "check", "src/", "tests/"], "Linting (Ruff)"
        )

    def run_type_safety_gate(self) -> QualityGateResult:
        """Run type safety quality gate."""
        return self.run_command(
            ["uv", "run", "mypy", "--config-file=pyproject.toml", "src/", "tests/"],
            "Type Safety (MyPy)",
        )

    def run_coverage_gate(self) -> QualityGateResult:
        """Run test coverage quality gate."""
        return self.run_command(
            [
                "uv",
                "run",
                "pytest",
                "tests/",
                "--cov=src/vine",
                "--cov-report=term-missing",
                "--cov-fail-under=80",
            ],
            "Test Coverage (≥80%)",
        )

    def run_complexity_gate(self) -> QualityGateResult:
        """Run code complexity quality gate."""
        return self.run_command(
            ["uv", "run", "xenon", "--max-absolute", "B", "--max-average", "A", "src/"],
            "Code Complexity (Xenon)",
        )

    def run_security_gate(self) -> QualityGateResult:
        """Run security audit quality gate."""
        return self.run_command(
            ["uv", "run", "pip-audit"], "Security Audit (pip-audit)"
        )

    def run_docs_gate(self) -> QualityGateResult:
        """Run documentation build quality gate."""
        return self.run_command(
            ["make", "html"], "Documentation Build", cwd=self.project_root / "docs"
        )

    def run_all_gates(self, include_docs: bool = True) -> list[QualityGateResult]:
        """Run all quality gates."""
        gates = [
            self.run_linting_gate,
            self.run_type_safety_gate,
            self.run_coverage_gate,
            self.run_complexity_gate,
            self.run_security_gate,
        ]

        if include_docs:
            gates.append(self.run_docs_gate)

        for gate_func in gates:
            result = gate_func()
            self.results.append(result)

            if result.passed:
                print(f"✅ {result.name} - PASSED ({result.duration:.1f}s)")
            else:
                print(f"❌ {result.name} - FAILED ({result.duration:.1f}s)")
                print(f"   Error: {result.output[:200]}...")

        return self.results

    def generate_report(self) -> str:
        """Generate a comprehensive quality gates report."""
        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)

        report = f"""
🎯 Quality Gates Report
======================

📊 Summary:
  ✅ Passed: {passed}/{total}
  ❌ Failed: {total - passed}/{total}
  📈 Success Rate: {(passed/total)*100:.1f}%

🔍 Detailed Results:
"""

        for result in self.results:
            status = "✅ PASS" if result.passed else "❌ FAIL"
            report += f"  {status} {result.name} ({result.duration:.1f}s)\n"

            if not result.passed and result.output:
                # Show first few lines of error output
                lines = result.output.strip().split("\n")[:3]
                for line in lines:
                    report += f"    {line}\n"
                output_lines = result.output.strip().split("\n")
                if len(output_lines) > 3:
                    report += f"    ... ({len(output_lines) - 3} more lines)\n"

        report += f"""
🚀 Quality Standards:
  • Code must pass all linting checks
  • Type safety must be enforced (MyPy strict mode)
  • Test coverage must be ≥80%
  • Code complexity must be within thresholds

  • No security vulnerabilities allowed
  • Documentation must build successfully

⏱️ Total Duration: {sum(r.duration for r in self.results):.1f}s
📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

        return report

    def save_report(self, output_file: Path | None = None) -> None:
        """Save the report to a file."""
        if output_file is None:
            output_file = self.project_root / "quality_gates_report.txt"

        report = self.generate_report()
        output_file.write_text(report)
        print(f"📄 Report saved to: {output_file}")


def main():
    """Main entry point."""
    project_root = Path(__file__).parent.parent
    runner = QualityGatesRunner(project_root)

    # Parse command line arguments
    include_docs = "--no-docs" not in sys.argv
    save_report = "--save-report" in sys.argv

    print("🚀 Running Quality Gates for Vine Project")
    print("=" * 50)

    try:
        results = runner.run_all_gates(include_docs=include_docs)

        # Generate and display report
        report = runner.generate_report()
        print(report)

        # Save report if requested
        if save_report:
            runner.save_report()

        # Exit with appropriate code
        failed_gates = [r for r in results if not r.passed]
        if failed_gates:
            print(f"❌ {len(failed_gates)} quality gate(s) failed!")
            sys.exit(1)
        else:
            print("🎉 All quality gates passed!")
            sys.exit(0)

    except KeyboardInterrupt:
        print("\n⏹️ Quality gates interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
