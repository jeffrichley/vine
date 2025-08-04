# 🚀 CI/CD

Seedling includes comprehensive CI/CD configuration for automated testing and deployment.

## Overview

The template provides:
- **GitHub Actions**: Automated workflows
- **Testing**: Automated test execution
- **Quality checks**: Automated code quality validation
- **Deployment**: Automated deployment to PyPI

## Workflows

### CI Workflow

The main CI workflow runs on every push and pull request:

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install uv
      uses: astral-sh/setup-uv@v1
    
    - name: Install dependencies
      run: uv sync
    
    - name: Run tests
      run: uv run dev test --cov
    
    - name: Run quality checks
      run: uv run dev checkit
```

### Release Workflow

Automated releases to PyPI:

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v4
      with:
        python-version: "3.11"
    
    - name: Install uv
      uses: astral-sh/setup-uv@v1
    
    - name: Build and publish
      run: |
        uv run build
        uv run twine upload dist/*
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
```

## Quality Gates

The CI pipeline enforces strict quality standards:

1. **Tests must pass** with 80%+ coverage
2. **Code quality checks** must pass (Ruff, MyPy)
3. **Security scans** must find no vulnerabilities
4. **Documentation** must build without errors

## Configuration

### GitHub Actions

All workflows are automatically configured based on template variables:

- **Python versions**: Uses `python_versions` from copier.yml
- **Package name**: Uses `project_slug` from copier.yml
- **Repository**: Uses `github_username` from copier.yml

### Secrets Required

For full functionality, set up these GitHub secrets:

- **`PYPI_API_TOKEN`**: For publishing to PyPI
- **`CODECOV_TOKEN`**: For coverage reporting

## Best Practices

1. **Run tests locally** before pushing
2. **Use feature branches** for development
3. **Write meaningful commit messages**
4. **Review CI results** before merging
5. **Keep dependencies updated**

## Next Steps

- **Set up deployment environments**
- **Configure branch protection rules**
- **Add performance testing**
- **Set up monitoring and alerting**
