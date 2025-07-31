#!/usr/bin/env python3
"""Run performance benchmarks and generate reports."""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def run_benchmarks(output_dir: Path = None) -> dict[str, Any]:
    """Run all benchmark tests and return results."""
    if output_dir is None:
        output_dir = Path("output/benchmarks")

    output_dir.mkdir(parents=True, exist_ok=True)

    # Run benchmarks with JSON output
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_file = output_dir / f"benchmark_results_{timestamp}.json"

    cmd = [
        "python",
        "-m",
        "pytest",
        "scripts/benchmarks/",
        "--benchmark-only",
        "--benchmark-json",
        str(json_file),
        "--benchmark-sort",
        "name",
        "--benchmark-min-rounds",
        "5",
        "--benchmark-max-time",
        "10.0",
        "-v",
    ]

    print("Running benchmarks...")
    print(f"Command: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("Benchmarks completed successfully!")

        # Load and process results
        with open(json_file) as f:
            benchmark_data = json.load(f)

        return {
            "timestamp": timestamp,
            "json_file": str(json_file),
            "data": benchmark_data,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }

    except subprocess.CalledProcessError as e:
        print(f"Benchmark run failed: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return {
            "timestamp": timestamp,
            "error": str(e),
            "stdout": e.stdout,
            "stderr": e.stderr,
        }


def generate_report(results: dict[str, Any], output_dir: Path) -> Path:
    """Generate a human-readable benchmark report."""
    if "error" in results:
        report_content = f"""
# Benchmark Report - {results['timestamp']}

## Error
Benchmark run failed: {results['error']}

## STDOUT
{results['stdout']}

## STDERR
{results['stderr']}
"""
    else:
        data = results["data"]
        benchmarks = data.get("benchmarks", [])

        # Group benchmarks by category
        categories = {}
        for bench in benchmarks:
            test_name = bench["name"]
            category = test_name.split("::")[0] if "::" in test_name else "Other"

            if category not in categories:
                categories[category] = []
            categories[category].append(bench)

        # Generate report content
        report_content = f"""# Benchmark Report - {results['timestamp']}

## Summary
- Total benchmarks: {len(benchmarks)}
- Categories: {len(categories)}
- Generated: {datetime.now().isoformat()}

## Performance Results by Category

"""

        for category, category_benchmarks in categories.items():
            report_content += f"### {category}\n\n"
            report_content += "| Test | Mean (ms) | Std Dev | Min | Max | Rounds |\n"
            report_content += "|------|-----------|---------|-----|-----|--------|\n"

            for bench in sorted(category_benchmarks, key=lambda x: x["stats"]["mean"]):
                stats = bench["stats"]
                report_content += (
                    f"| {bench['name'].split('::')[-1]} | "
                    f"{stats['mean']:.3f} | "
                    f"{stats['stddev']:.3f} | "
                    f"{stats['min']:.3f} | "
                    f"{stats['max']:.3f} | "
                    f"{stats['rounds']} |\n"
                )

            report_content += "\n"

        # Add performance insights
        report_content += "## Performance Insights\n\n"

        # Find fastest and slowest benchmarks
        if benchmarks:
            fastest = min(benchmarks, key=lambda x: x["stats"]["mean"])
            slowest = max(benchmarks, key=lambda x: x["stats"]["mean"])

            report_content += f"### Fastest: {fastest['name']}\n"
            report_content += f"- Mean time: {fastest['stats']['mean']:.3f} ms\n\n"

            report_content += f"### Slowest: {slowest['name']}\n"
            report_content += f"- Mean time: {slowest['stats']['mean']:.3f} ms\n\n"

            # Calculate performance ratios
            ratio = slowest["stats"]["mean"] / fastest["stats"]["mean"]
            report_content += "### Performance Range\n"
            report_content += f"- Fastest to slowest ratio: {ratio:.1f}x\n\n"

    # Write report
    report_file = output_dir / f"benchmark_report_{results['timestamp']}.md"
    with open(report_file, "w") as f:
        f.write(report_content)

    print(f"Report generated: {report_file}")
    return report_file


def compare_with_baseline(
    results: dict[str, Any], baseline_file: Path = None
) -> dict[str, Any]:
    """Compare current results with a baseline."""
    if baseline_file is None:
        baseline_file = Path("output/benchmarks/baseline.json")

    if not baseline_file.exists():
        print(f"No baseline file found at {baseline_file}")
        return {"error": "No baseline file found"}

    try:
        with open(baseline_file) as f:
            baseline_data = json.load(f)

        current_benchmarks = {b["name"]: b for b in results["data"]["benchmarks"]}
        baseline_benchmarks = {b["name"]: b for b in baseline_data["benchmarks"]}

        comparisons = {}
        for name in current_benchmarks:
            if name in baseline_benchmarks:
                current_mean = current_benchmarks[name]["stats"]["mean"]
                baseline_mean = baseline_benchmarks[name]["stats"]["mean"]
                change_pct = ((current_mean - baseline_mean) / baseline_mean) * 100

                comparisons[name] = {
                    "current": current_mean,
                    "baseline": baseline_mean,
                    "change_pct": change_pct,
                    "status": "faster" if change_pct < 0 else "slower",
                }

        return comparisons

    except Exception as e:
        return {"error": f"Failed to compare with baseline: {e}"}


def save_baseline(results: dict[str, Any], output_dir: Path) -> Path:
    """Save current results as baseline for future comparisons."""
    if "error" in results:
        print("Cannot save baseline due to benchmark errors")
        return None

    baseline_file = output_dir / "baseline.json"
    with open(baseline_file, "w") as f:
        json.dump(results["data"], f, indent=2)

    print(f"Baseline saved: {baseline_file}")
    return baseline_file


def main():
    """Main entry point."""
    output_dir = Path("output/benchmarks")

    # Parse command line arguments
    save_baseline_flag = "--save-baseline" in sys.argv
    compare_baseline_flag = "--compare-baseline" in sys.argv

    # Run benchmarks
    results = run_benchmarks(output_dir)

    # Generate report
    report_file = generate_report(results, output_dir)

    # Handle baseline operations
    if save_baseline_flag and "error" not in results:
        save_baseline(results, output_dir)

    if compare_baseline_flag:
        comparisons = compare_with_baseline(results)
        if "error" not in comparisons:
            print("\n## Baseline Comparison")
            for name, comp in comparisons.items():
                status_emoji = "🟢" if comp["status"] == "faster" else "🔴"
                print(
                    f"{status_emoji} {name}: {comp['change_pct']:+.1f}% ({comp['status']})"
                )
        else:
            print(f"Baseline comparison failed: {comparisons['error']}")

    print("\nBenchmark run completed!")
    print(f"Report: {report_file}")
    if "json_file" in results:
        print(f"JSON results: {results['json_file']}")


if __name__ == "__main__":
    main()
