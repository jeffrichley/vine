# 🚀 Quick Start Guide

Get up and running with Seedling in under 5 minutes!

## Prerequisites

- **Python 3.11+**: Required for modern features and type hints
- **Git**: For version control
- **Copier**: Template engine (we'll install this)
- **uv**: Fast Python package manager (recommended)
- **Nox**: Task automation tool (recommended)
- **Just**: Command runner for shortcuts (optional but recommended)

## Installation

### 1. Install Required Tools

```bash
# Quick install all tools (recommended)
curl -LsSf https://raw.githubusercontent.com/jeffrichley/seedling/main/scripts/install-tools.sh | bash

# Or install manually
curl -LsSf https://astral.sh/uv/install.sh | sh
uv pip install copier
uv pip install nox
# Just: macOS: brew install just, Linux: Download from releases
```

### 2. Generate Your First Project

```bash
# Generate a new project
copier copy https://github.com/jeffrichley/seedling.git my-awesome-project
```

You'll be prompted to configure your project:

```
project_name [My Awesome Project]: My Data Science Tool
project_slug [my_awesome_project]: my_data_science_tool
project_description [A modern Python project built with best practices and comprehensive tooling]: A powerful data science toolkit
author_name [Your Name]: Jane Doe
author_email [your.name@example.com]: jane.doe@example.com
github_username [yourusername]: janedoe
license (MIT, Apache-2.0, GPL-3.0, BSD-3-Clause) [MIT]: MIT
python_versions [3.11,3.12]: 3.11,3.12
coverage_threshold [80]: 85
```

### 3. Navigate to Your Project

```bash
cd my-awesome-project
```

### 4. Set Up Development Environment

```bash
# Install dependencies
uv sync

# Install pre-commit hooks
pre-commit install

# Run initial quality checks
just quality
```

### 5. Start Developing!

```bash
# Run tests using Nox
nox -s tests

# Run tests using Just
just test

# Format code
just lint

# Build documentation
just docs
```

## 🎯 What Just Happened?

1. **Project Structure**: A complete Python project structure was created
2. **Dependencies**: All necessary development tools were configured
3. **Quality Tools**: Pre-commit hooks, linting, and testing were set up
4. **CI/CD**: GitHub Actions workflows were configured
5. **Documentation**: Sphinx documentation was initialized

## 📁 Your New Project Structure

```
my-awesome-project/
├── src/my_data_science_tool/    # Your package code
├── tests/                       # Test suite
│   ├── unit/                    # Unit tests
│   ├── integration/             # Integration tests
│   └── e2e/                     # End-to-end tests
├── docs/                        # Documentation
├── .github/                     # GitHub Actions workflows
├── pyproject.toml              # Modern Python configuration
├── .pre-commit-config.yaml     # Code quality hooks
├── noxfile.py                  # Development tasks
├── justfile                    # Development shortcuts
└── README.md                   # Project documentation
```

## 🛠️ Available Commands

### Using Nox (Recommended)

```bash
# Run tests
nox -s tests

# Run linting
nox -s lint

# Run type checking
nox -s type_check

# Build documentation
nox -s docs

# Run all quality checks
nox -s lint type_check docs
```

### Using Just (Shortcuts)

```bash
# Run tests
just test

# Run linting
just lint

# Run type checking
just type-check

# Build documentation
just docs

# Run all quality checks
just quality
```

### Using uv (Direct)

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Format code
uv run black src tests
uv run ruff check src tests --fix

# Type check
uv run mypy src tests
```

## 🎯 What the Template Provides

The generated project includes:

### ✅ **Automatically Included**
- **All Python dependencies** (Black, Ruff, MyPy, pytest, Sphinx, etc.)
- **Pre-commit hooks** for code quality
- **Nox automation** for development tasks
- **Just shortcuts** for common commands
- **GitHub Actions** for CI/CD
- **Complete test structure** with unit, integration, and e2e tests
- **Documentation setup** with Sphinx and Furo theme

### 🔧 **What You Need to Install**
- **Copier**: To generate projects from the template
- **uv**: For dependency management
- **Nox**: For task automation
- **Just**: For development shortcuts (optional)

## Next Steps

- **Read the documentation**: Check the generated `docs/` directory
- **Customize your project**: Modify `pyproject.toml` and configuration files
- **Add your code**: Start coding in `src/my_data_science_tool/`
- **Write tests**: Add tests in the `tests/` directory
- **Deploy**: Push to GitHub and let CI/CD handle the rest!

For more detailed information, see the {doc}`installation` and {doc}`configuration` guides. 