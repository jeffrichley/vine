# Quality Gates System

## Overview

The Vine project implements a comprehensive automated quality gates system that enforces code quality standards throughout the development lifecycle. Quality gates are automated decision points that can block deployments, merges, or releases based on predefined quality thresholds.

## 🎯 Quality Gates Implemented

### 1. **Linting Gate** (Ruff)
- **Tool**: Ruff with flake8-tidy-imports
- **Purpose**: Enforce code style and import organization
- **Threshold**: Zero unfixable linting errors
- **Command**: `uv run ruff check src/ tests/`

### 2. **Type Safety Gate** (MyPy)
- **Tool**: MyPy with strict mode
- **Purpose**: Enforce type safety across the codebase
- **Threshold**: Zero type errors
- **Command**: `uv run mypy --config-file=pyproject.toml src/ tests/`

### 3. **Test Coverage Gate** (pytest-cov)
- **Tool**: pytest with coverage reporting
- **Purpose**: Ensure adequate test coverage
- **Threshold**: ≥80% coverage
- **Command**: `uv run pytest tests/ --cov=src/vine --cov-report=term-missing --cov-fail-under=80`

### 4. **Code Complexity Gate** (Xenon)
- **Tool**: Xenon with Radon backend
- **Purpose**: Maintain code complexity within acceptable limits
- **Threshold**:
  - Max absolute: B (no function exceeds B complexity)
  - Max average: A (average complexity is A or better)
- **Command**: `uv run xenon --max-absolute B --max-average A src/`

### 5. **Dead Code Detection Gate** (Vulture)
- **Tool**: Vulture
- **Purpose**: Identify and remove dead code
- **Threshold**: No dead code with ≥80% confidence
- **Command**: `uv run vulture src/ tests/ --min-confidence 80`

### 6. **Security Audit Gate** (pip-audit)
- **Tool**: pip-audit
- **Purpose**: Detect security vulnerabilities in dependencies
- **Threshold**: Zero known vulnerabilities
- **Command**: `uv run pip-audit`

### 7. **Documentation Build Gate** (Sphinx)
- **Tool**: Sphinx documentation builder
- **Purpose**: Ensure documentation builds successfully
- **Threshold**: Documentation builds without errors
- **Command**: `cd docs && make html`

## 🚀 Usage

### Local Development

Run all quality gates locally:

```bash
# Run all gates (including docs)
make quality-gates

# Run gates without documentation check
make quality-gates-no-docs

# Run the script directly
python scripts/quality_gates.py --save-report
```

### CI/CD Integration

Quality gates are automatically enforced in the CI pipeline:

- **Pull Requests**: All gates must pass before merge
- **Main Branch**: All gates must pass before deployment
- **Releases**: All gates must pass before release

## 📊 Quality Gate Reports

The quality gates system generates comprehensive reports including:

- **Summary**: Pass/fail counts and success rate
- **Detailed Results**: Individual gate results with timing
- **Error Details**: Specific issues found by each gate
- **Performance Metrics**: Execution time for each gate

### Report Example

```
🎯 Quality Gates Report
======================

📊 Summary:
  ✅ Passed: 1/6
  ❌ Failed: 5/6
  📈 Success Rate: 16.7%

🔍 Detailed Results:
  ❌ FAIL Linting (Ruff) (0.4s)
  ❌ FAIL Type Safety (MyPy) (16.9s)
  ❌ FAIL Test Coverage (≥80%) (3.1s)
  ❌ FAIL Code Complexity (Xenon) (0.6s)
  ❌ FAIL Dead Code Detection (Vulture) (0.5s)
  ✅ PASS Security Audit (pip-audit) (7.6s)
```

## ⚙️ Configuration

### Quality Gates Configuration

Quality gate thresholds are defined in `.github/quality-gates.yml`:

```yaml
quality_gates:
  coverage:
    minimum_percentage: 80
    fail_under: true

  complexity:
    max_absolute: "B"
    max_average: "A"
    max_modules: "A"

  dead_code:
    min_confidence: 80
```

### Enforcement Rules

Different quality gates are enforced based on the event:

- **Pull Request**: Core gates (coverage, complexity, type safety, linting, security)
- **Push to Main**: All gates including documentation
- **Release**: All gates including dead code detection

## 🔧 Troubleshooting

### Common Issues

1. **Linting Failures**
   - Run `uv run ruff check --fix src/ tests/` to auto-fix issues
   - Check import organization with `uv run ruff check --select I`

2. **Type Safety Failures**
   - Review MyPy errors and add proper type annotations
   - Use `# type: ignore` sparingly and document why

3. **Coverage Failures**
   - Add tests for uncovered code paths
   - Use `# pragma: no cover` for intentionally uncovered code

4. **Complexity Failures**
   - Refactor complex functions into smaller, simpler functions
   - Extract helper methods to reduce cyclomatic complexity

5. **Dead Code Detection**
   - Remove unused imports and functions
   - Use `# noqa: V104` for intentionally unused code

### Getting Help

- Check the quality gates report for specific error details
- Review the tool documentation for each quality gate
- Consult the project's coding standards and best practices

## 📈 Continuous Improvement

The quality gates system is designed to evolve with the project:

- **Thresholds**: Can be adjusted based on project maturity
- **New Gates**: Additional quality checks can be added
- **Tooling**: Tools can be upgraded or replaced as needed
- **Reporting**: Enhanced reporting and notifications can be added

## 🎉 Benefits

Implementing quality gates provides:

- **Consistent Quality**: Automated enforcement of quality standards
- **Early Detection**: Issues caught before they reach production
- **Team Alignment**: Clear expectations for code quality
- **Reduced Technical Debt**: Proactive identification of quality issues
- **Confidence**: Assurance that deployed code meets quality standards
