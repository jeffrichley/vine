# 🤝 Contributing to Seedling

Thank you for your interest in contributing to the Seedling Python project template! This document provides guidelines and requirements for contributing to the template.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Development Setup](#development-setup)
- [Documentation](#documentation)
- [Quality Requirements](#quality-requirements)
- [Contribution Process](#contribution-process)
- [Code Style Guidelines](#code-style-guidelines)
- [Testing Requirements](#testing-requirements)
- [Review Process](#review-process)

## 📜 Code of Conduct

By participating in this project, you agree to maintain a respectful environment for everyone. We are committed to providing a welcoming and inspiring community for all.

## 🛠️ Development Setup

### Prerequisites

- **Python 3.11+**: Required for modern type hints and features
- **uv**: Fast Python package manager (recommended)
- **Git**: Version control system
- **Copier**: Template engine for testing

### Installation

```bash
# Clone the repository
git clone https://github.com/jeffrichley/seedling.git
cd seedling

# Install dependencies
uv sync
```

## 📚 Documentation

### Building Documentation

The Seedling template includes comprehensive documentation that can be built locally:

#### Prerequisites

- **uv**: Fast Python package manager
- **Sphinx**: Documentation generator

#### Quick Build

```bash
# Navigate to docs directory
cd docs

# Build documentation (creates virtual environment automatically)
./build-docs.sh
```

#### Manual Build

```bash
# Navigate to docs directory
cd docs

# Install dependencies
uv sync

# Build HTML documentation
make html

# Serve locally
make serve
```

The documentation will be available at http://localhost:8000

#### Documentation Structure

```
docs/
├── source/                    # Source files
│   ├── index.md              # Main documentation index
│   ├── quickstart.md         # Quick start guide
│   ├── installation.md       # Installation instructions
│   ├── configuration.md      # Configuration reference
│   ├── examples.md           # Examples and use cases
│   ├── contributing.md       # This file
│   ├── adr/                  # Architecture decisions
│   ├── features/             # Feature documentation
│   ├── advanced/             # Advanced usage
│   └── reference/            # Reference documentation
├── build/                    # Built documentation (generated)
├── pyproject.toml           # Documentation dependencies
├── Makefile                 # Build targets
└── build-docs.sh           # Build script
```

#### Adding New Documentation

1. **Create new files** in the appropriate directory under `docs/source/`
2. **Use Markdown** (`.md`) files with MyST extensions
3. **Update navigation** in `docs/source/index.md` if needed
4. **Build and test** your changes locally
5. **Follow the style** of existing documentation

#### Documentation Guidelines

- **Use clear headings** and structure
- **Include code examples** where helpful
- **Keep it concise** but comprehensive
- **Test all links** and references
- **Use consistent formatting**

### Testing Template Generation

When making changes to the template, test that it generates projects correctly:

```bash
# Test template generation
copier copy . /tmp/test-project --trust

# Navigate to generated project
cd /tmp/test-project

# Test that it builds and works
uv sync
uv run dev test
uv run dev checkit

# Clean up
cd ..
rm -rf /tmp/test-project
```

## 🎯 Quality Requirements

Seedling maintains strict quality standards. **All contributions must pass these quality gates:**

### Quality Gates

1. **🔍 Linting (Ruff)**: Code style and best practices
2. **🧠 Type Safety (MyPy)**: Strict type checking with zero errors
3. **📊 Coverage (≥80%)**: Comprehensive test coverage
4. **📈 Complexity (Xenon)**: Maintainable code complexity
5. **🧹 Dead Code (Vulture)**: No unused code or imports
6. **🔒 Security (pip-audit)**: No dependency vulnerabilities

### Pre-commit Checks

```bash
# Run all quality checks
uv run dev checkit

# Individual checks
uv run dev lint          # Ruff linting
uv run dev typecheck     # MyPy type checking
uv run dev test          # Pytest with coverage
uv run dev quality-gates # All quality gates
```

## 🔄 Contribution Process

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/YOUR_USERNAME/seedling.git
cd seedling

# Add upstream remote
git remote add upstream https://github.com/jeffrichley/seedling.git
```

### 2. Create a Feature Branch

```bash
# Create and switch to a new branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/your-bug-description
```

### 3. Make Your Changes

- **Follow the code style** guidelines below
- **Add tests** for new functionality
- **Update documentation** if needed
- **Test template generation** with your changes

### 4. Test Your Changes

```bash
# Run quality checks
uv run dev checkit

# Test template generation
copier copy . /tmp/test-project --trust
cd /tmp/test-project
uv sync
uv run dev test
cd ..
rm -rf /tmp/test-project

# Build documentation
cd docs
./build-docs.sh
cd ..
```

### 5. Commit Your Changes

```bash
# Stage your changes
git add .

# Commit with a descriptive message
git commit -m "feat: add new template feature"

# Push to your fork
git push origin feature/your-feature-name
```

### 6. Create a Pull Request

- **Describe your changes** clearly
- **Reference any issues** that are fixed
- **Include screenshots** if UI changes
- **Test the template** generation works

## 📝 Code Style Guidelines

### Python Code

- **Follow PEP 8** with Black formatting
- **Use type hints** for all functions
- **Write docstrings** for all public functions
- **Keep functions small** and focused
- **Use meaningful variable names**

### Template Files

- **Use descriptive variable names** in Jinja2 templates
- **Add comments** for complex template logic
- **Test template generation** with different configurations
- **Keep templates readable** and maintainable

### Documentation

- **Use clear, concise language**
- **Include code examples**
- **Test all links and references**
- **Follow the existing style**

## 🧪 Testing Requirements

### Template Testing

- **Test with different configurations**
- **Verify generated projects build**
- **Check that all tools work**
- **Test edge cases and error handling**

### Documentation Testing

- **Build documentation locally**
- **Check all links work**
- **Verify code examples run**
- **Test search functionality**

## 👀 Review Process

1. **Automated checks** must pass
2. **Template generation** must work
3. **Documentation** must be updated
4. **Code review** by maintainers
5. **Final testing** before merge

## 🆘 Getting Help

- **Check existing issues** on GitHub
- **Read the documentation** thoroughly
- **Ask questions** in discussions
- **Join the community** chat

## 📄 License

By contributing to Seedling, you agree that your contributions will be licensed under the MIT License.
