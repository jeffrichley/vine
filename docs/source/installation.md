# 📦 Installation Guide

Learn how to install and set up the Seedling template system.

## Prerequisites

Before using Seedling, ensure you have the following installed:

### Required Software

- **Python 3.11+**: Required for modern features and type hints
- **Git**: For version control and template cloning
- **Copier**: Template engine (we'll install this)

### Recommended Software

- **uv**: Fast Python package manager (used by generated projects)
- **Nox**: Task automation tool (used by generated projects)
- **Just**: Command runner for development shortcuts (optional but recommended)

### Optional Software

- **pyenv**: Python version management
- **GitHub CLI**: For repository management

## Installing Required Tools

### 1. Install uv (Recommended)

uv is the recommended Python package manager used by generated projects:

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Using pip
pip install uv
```

### 2. Install Copier

Copier is required to generate projects from the template:

```bash
# Using uv (recommended)
uv pip install copier

# Using pip
pip install copier

# Using pipx (isolated installation)
pipx install copier
```

### 3. Install Nox (Recommended)

Nox is used by generated projects for task automation:

```bash
# Using uv (recommended)
uv pip install nox

# Using pip
pip install nox

# Using pipx
pipx install nox
```

### 4. Install Just (Optional but Recommended)

Just provides convenient shortcuts for development tasks:

```bash
# macOS
brew install just

# Linux
# Download from https://github.com/casey/just/releases
# or use your package manager

# Windows
# Download from https://github.com/casey/just/releases
# or use Chocolatey: choco install just
```

## What the Template Provides

When you generate a project with Seedling, it includes:

### ✅ **Automatically Included (No Installation Required)**

- **All Python dependencies** via `pyproject.toml`:
  - Black (code formatting)
  - Ruff (linting)
  - MyPy (type checking)
  - pytest (testing)
  - Hypothesis (property-based testing)
  - Sphinx (documentation)
  - And many more...

- **Development tools configuration**:
  - Pre-commit hooks
  - Nox automation tasks
  - Just development shortcuts
  - GitHub Actions workflows

### 🔧 **Tools You Need to Install**

- **Copier**: To generate projects from the template
- **uv**: For dependency management in generated projects
- **Nox**: For running development tasks
- **Just**: For development shortcuts (optional)

## Verifying Installation

Check that all tools are installed correctly:

```bash
# Check Copier
copier --version

# Check uv
uv --version

# Check Nox
nox --version

# Check Just (if installed)
just --version
```

You should see output like:
```
Copier 7.0.0
uv 0.1.0
nox 2024.1.1
just 1.20.0
```

## Quick Installation Script

For convenience, we provide an installation script that installs all recommended tools:

```bash
# Download and run the installation script
curl -LsSf https://raw.githubusercontent.com/jeffrichley/seedling/main/scripts/install-tools.sh | bash

# Or clone the repository and run locally
git clone https://github.com/jeffrichley/seedling.git
cd seedling
./scripts/install-tools.sh
```

The script will:
- Install uv (Python package manager)
- Install Copier (template engine)
- Install Nox (task automation)
- Install Just (development shortcuts)
- Check for existing installations
- Provide colored output and error handling
- Show next steps after installation

## Development Environment Setup

### 1. Clone the Template Repository

```bash
git clone https://github.com/jeffrichley/seedling.git
cd seedling
```

### 2. Set Up Python Environment

```bash
# Using pyenv (if installed)
pyenv install 3.11.0
pyenv local 3.11.0

# Using uv
uv sync
```

### 3. Install Development Dependencies

```bash
# Using uv (recommended)
uv sync --all-extras

# Using pip
pip install -e ".[dev]"
```

### 4. Install Pre-commit Hooks

```bash
pre-commit install
```

## Testing the Installation

### 1. Generate a Test Project

```bash
# Create a test project
copier copy . /tmp/test-project --trust

# Navigate to the project
cd /tmp/test-project
```

### 2. Verify the Generated Project

```bash
# Check the project structure
ls -la

# Install dependencies
uv sync

# Run tests using Nox
nox -s tests

# Run tests using Just
just test

# Run quality checks
just quality
```

### 3. Clean Up

```bash
# Remove test project
rm -rf /tmp/test-project
```

## Troubleshooting

### Common Issues

#### Copier Not Found

```bash
# Check if copier is in PATH
which copier

# If not found, try reinstalling
pip uninstall copier
pip install copier
```

#### uv Installation Issues

```bash
# Check uv installation
uv --version

# If not found, try the installation again
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Nox Not Found

```bash
# Check Nox installation
nox --version

# If not found, try reinstalling
pip uninstall nox
pip install nox
```

#### Just Not Found

```bash
# Check Just installation
just --version

# If not found, install using your package manager
# macOS: brew install just
# Linux: Download from GitHub releases
# Windows: Download from GitHub releases or use Chocolatey
```

#### Python Version Issues

```bash
# Check Python version
python --version

# Should be 3.11 or higher
# If not, install a newer version using pyenv or your system package manager
```

#### Permission Issues

```bash
# If you get permission errors, try using --user flag
pip install --user copier nox

# Or use a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install copier nox
```

### Getting Help

- Check the {doc}`advanced/troubleshooting` guide
- Visit the [Copier documentation](https://copier.readthedocs.io/)
- Visit the [uv documentation](https://docs.astral.sh/uv/)
- Visit the [Nox documentation](https://nox.thea.codes/)
- Visit the [Just documentation](https://just.systems/)
- Open an issue on [GitHub](https://github.com/jeffrichley/seedling/issues)

## Next Steps

Now that you have Seedling installed, you can:

1. **Generate your first project**: See the {doc}`quickstart` guide
2. **Learn about configuration**: Check the {doc}`configuration` guide
3. **Explore examples**: Browse the {doc}`examples` page
4. **Customize the template**: Read the {doc}`advanced/customization` guide 