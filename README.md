# 🌱 Seedling - Modern Python Project Template

A comprehensive Python project template with modern development tooling, automated CI/CD, and best practices built-in.

## 🚀 Quick Start

Generate a new Python project:

```bash
# Quick install all required tools
curl -LsSf https://raw.githubusercontent.com/jeffrichley/seedling/main/scripts/install-tools.sh | bash

# Or if you've cloned the repository
git clone https://github.com/jeffrichley/seedling.git
cd seedling
./scripts/install-tools.sh

# Or install manually
curl -LsSf https://astral.sh/uv/install.sh | sh
uv pip install copier
uv pip install nox
```

# Generate a new project
copier copy https://github.com/jeffrichley/seedling.git my-awesome-project
```

## ✨ Features

- **Modern Python Setup**: Python 3.11+, uv package manager, type hints
- **Quality Tooling**: Black, Ruff, MyPy, pre-commit hooks
- **Testing**: pytest with coverage, hypothesis for property-based testing
- **Documentation**: Sphinx with Furo theme, automatic API docs
- **CI/CD**: GitHub Actions with comprehensive checks
- **Security**: pip-audit, dependency scanning
- **Development**: Nox for task automation, comprehensive dev tools

## 🛠️ What You Need to Install

### Required
- **uv**: Fast Python package manager (see [installation](https://docs.astral.sh/uv/getting-started/installation/))
- **Copier**: Template engine (`uv pip install copier`)
- **Nox**: Task automation (`uv pip install nox`)

### Optional but Recommended
- **Just**: Command runner for shortcuts (see [installation](https://just.systems/man/en/))

## 🎯 What the Template Provides

When you generate a project, it includes:

### ✅ **Automatically Included (No Installation Required)**
- **All Python dependencies** (Black, Ruff, MyPy, pytest, Sphinx, etc.)
- **Pre-commit hooks** for code quality
- **Nox automation** for development tasks
- **Just shortcuts** for common commands
- **GitHub Actions** for CI/CD
- **Complete test structure** with unit, integration, and e2e tests
- **Documentation setup** with Sphinx and Furo theme

## 📚 Documentation

- **[Quick Start](docs/source/quickstart.md)** - Get started in 5 minutes
- **[Installation Guide](docs/source/installation.md)** - Detailed installation instructions
- **[Template Guide](docs/template-guide.md)** - Complete usage instructions
- **[Architecture Decisions](docs/adr/)** - Design decisions and rationale
- **[Contributing](docs/contributing.md)** - How to contribute to the template

### Building Documentation

To build and view the documentation locally:

```bash
# Build documentation
cd docs && ./build-docs.sh

# Serve locally
cd docs && make serve
```

The documentation will be available at http://localhost:8000

## 🛠️ Template Configuration

The template supports various configuration options:

- **Project metadata**: name, description, author, license
- **Python versions**: 3.11, 3.12, 3.13
- **Optional features**: CLI interface, conda fallback
- **Quality thresholds**: coverage, complexity limits

## 🎯 What You Get

A fully configured Python project with:

```
my-awesome-project/
├── src/my_awesome_project/     # Your package code
├── tests/                      # Test suite
│   ├── unit/                   # Unit tests
│   ├── integration/            # Integration tests
│   └── e2e/                    # End-to-end tests
├── docs/                       # Documentation
├── .github/                    # GitHub Actions workflows
├── pyproject.toml             # Modern Python configuration
├── .pre-commit-config.yaml    # Code quality hooks
├── noxfile.py                 # Development tasks
├── justfile                   # Development shortcuts
└── README.md                  # Project documentation
```

## 🤝 Contributing

See [CONTRIBUTING.md](docs/contributing.md) for details on contributing to the template.

## 📄 License

MIT License - see [LICENSE](LICENSE) for details. 