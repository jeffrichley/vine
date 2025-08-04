# Seedling Template Guide

A comprehensive guide for using the Seedling template to create world-class Python projects.

## 🌱 What is Seedling?

Seedling is a **Copier template** that generates modern Python projects with:

- **Complete CI/CD pipeline** with GitHub Actions
- **Quality assurance** with pre-commit-ci
- **Modern tooling** (uv, Nox, Just, Sphinx)
- **Professional documentation** with dark mode support
- **Enterprise-grade standards** and best practices

## 🚀 Quick Start

### Generate a New Project

```bash
# Generate a new project with interactive prompts
copier copy https://github.com/your-org/seedling my-new-project

# Or use a data file for non-interactive generation
copier copy https://github.com/your-org/seedling my-new-project --data-file project-data.yaml
```

### Example Data File (`project-data.yaml`)

```yaml
project_name: "My Awesome Project"
project_slug: "my_awesome_project"
project_description: "A modern Python project built with best practices"
author_name: "Your Name"
author_email: "your.email@example.com"
github_username: "yourusername"
license: "MIT"
python_versions: "3.11,3.12"
coverage_threshold: 80
```

## 📋 Configuration Options

### Project Information

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `project_name` | str | "My Awesome Project" | Human-readable project name |
| `project_slug` | str | "my_awesome_project" | Python package name (lowercase, underscores) |
| `project_description` | str | "A modern Python project..." | Brief project description |
| `project_keywords` | str | "python,modern,uv,nox,just" | Comma-separated PyPI keywords |
| `author_name` | str | "Your Name" | Your full name |
| `author_email` | str | "your.name@example.com" | Your email address |
| `github_username` | str | "yourusername" | Your GitHub username |
| `copyright_year` | str | "2024" | Copyright year |
| `version` | str | "0.1.0" | Initial version number |

### Features

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `license` | choice | "MIT" | Project license (MIT, Apache-2.0, GPL-3.0, BSD-3-Clause) |
| `python_versions` | str | "3.11,3.12" | Supported Python versions |
| `coverage_threshold` | int | 80 | Minimum test coverage percentage |



## 🛠️ Generated Project Structure

```
my-new-project/
├── src/
│   └── my_awesome_project/
│       └── __init__.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── docs/
│   ├── source/
│   │   ├── api.md
│   │   ├── contributing.md
│   │   └── index.md
│   └── build/
├── .github/
│   └── workflows/
│       ├── ci_nox.yml
│       ├── docs.yml
│       ├── release.yml
│       └── codeql.yml
├── pyproject.toml
├── noxfile.py
├── justfile
├── .pre-commit-config.yaml
└── README.md
```

## 🎯 Development Workflow

### Initial Setup

```bash
# Navigate to your new project
cd my-new-project

# Install dependencies (already done by copier)
uv sync --all-extras

# Verify installation
just test
```

### Daily Development

```bash
# Run quality checks
just quality

# Run tests
just test

# Format code
just format

# Build documentation
just docs

# Serve documentation locally
just docs-serve
```

### Available Commands

| Command | Description |
|---------|-------------|
| `just test` | Run tests with coverage |
| `just lint` | Run linting checks |
| `just type-check` | Run type checking |
| `just docs` | Build documentation |
| `just docs-serve` | Serve documentation locally |
| `just quality` | Run all quality checks |
| `just security` | Run security checks |
| `just complexity` | Run complexity analysis |

## 📚 Documentation

### Built-in Documentation

Every generated project includes:

- **API Reference**: Automatic API documentation
- **Contributing Guide**: Development guidelines
- **Dependency Groups**: Package management guide
- **Search Functionality**: Built-in search
- **Dark Mode Support**: Automatic theme switching

### Customizing Documentation

1. **Add API documentation** in `docs/source/api.md`
2. **Update contributing guide** in `docs/source/contributing.md`
3. **Add custom pages** in `docs/source/`
4. **Customize theme** in `docs/source/conf.py`

## 🔧 Customization

### Adding New Modules

1. **Create your module** in `src/your_project/`
2. **Add docstrings** with Google or NumPy style
3. **Include type hints** for all functions
4. **Update API docs** in `docs/source/api.md`

### Example: Adding a Core Module

```python
# src/your_project/core.py
"""Core functionality for the project."""

from typing import Any, Dict, List

def process_data(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Process input data and return results.
    
    Args:
        data: List of data dictionaries to process
        
    Returns:
        Processed results as a dictionary
    """
    # Your implementation here
    return {"processed": len(data)}
```

### Extending CI/CD

The generated project includes comprehensive CI/CD:

- **Multi-environment testing** (Python 3.11, 3.12)
- **Quality gates** (linting, type checking, coverage)
- **Security scanning** (CodeQL, pip-audit)
- **Documentation deployment** (GitHub Pages)
- **Automated releases** (PyPI publishing)

## 🚀 Deployment

### PyPI Publishing

```bash
# Build and publish to PyPI
just release

# Or manually
python -m build
python -m twine upload dist/*
```

### Documentation Deployment

Documentation is automatically deployed to GitHub Pages when you push to main.

## 🔍 Quality Standards

Every generated project enforces:

- **Type Safety**: Full MyPy integration
- **Code Quality**: Ruff linting with comprehensive rules
- **Test Coverage**: Minimum 80% coverage requirement
- **Documentation**: Comprehensive docstrings
- **Security**: Regular vulnerability scanning
- **Performance**: Code complexity analysis

## 🆘 Troubleshooting

### Common Issues

#### Pre-commit Hooks Failing

```bash
# Run pre-commit manually
pre-commit run --all-files

# Skip hooks temporarily (not recommended)
git commit --no-verify
```

#### Documentation Build Errors

```bash
# Check Sphinx configuration
just docs

# Verify dependencies
uv pip install -e ".[docs]"
```

#### Test Failures

```bash
# Run tests with verbose output
just test -- -v

# Run specific test file
just test -- tests/unit/test_specific.py
```

### Getting Help

- **Check the logs**: Look for error messages in CI/CD runs
- **Review documentation**: Generated projects include comprehensive docs
- **Community support**: Open an issue on the seedling repository

## 🔄 Updating Projects

### Template Updates

```bash
# Update your project with latest template
copier update

# Review changes before applying
copier update --vcs-ref HEAD~1
```

### Dependency Updates

```bash
# Update dependencies
uv lock --upgrade

# Update specific package
uv add package-name --upgrade
```

## 📖 Best Practices

### Code Organization

- **Use src/ layout**: Prevents import confusion
- **Follow naming conventions**: snake_case for modules, PascalCase for classes
- **Add type hints**: All public APIs should have type annotations
- **Write docstrings**: Use Google or NumPy style consistently

### Testing Strategy

- **Unit tests**: Fast, isolated tests for individual functions
- **Integration tests**: Tests for component interactions
- **End-to-end tests**: Full workflow testing
- **Property-based testing**: Use Hypothesis for edge cases

### Documentation

- **Keep docs updated**: Update documentation with code changes
- **Use examples**: Include usage examples in docstrings
- **Link related docs**: Cross-reference related documentation
- **Test documentation**: Ensure all code examples work

## 🎉 Success Stories

Projects built with Seedling include:

- **Enterprise applications** with strict quality requirements
- **Open source libraries** with comprehensive documentation
- **Research projects** requiring reproducible environments
- **CLI tools** with professional user experience

## 🤝 Contributing to Seedling

Want to improve the template?

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Test with multiple configurations**
5. **Submit a pull request**

See the [Contributing Guide](../CONTRIBUTING.md) for detailed instructions.

---

**Seedling** - Growing world-class Python projects from the ground up! 🌱
