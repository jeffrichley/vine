# 🌱 Seedling - Modern Python Project Template

A comprehensive Python project template with modern development tooling, automated CI/CD, and best practices built-in.

## 🚀 Quick Start

Generate a new Python project in seconds:

```bash
# Install copier
pip install copier

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

## 📚 Documentation

```{toctree}
:maxdepth: 2
:caption: Getting Started

quickstart
installation
configuration
examples
```

```{toctree}
:maxdepth: 2
:caption: Template Features

features/quality-tooling
features/testing
features/documentation
features/ci-cd
features/development
```

```{toctree}
:maxdepth: 2
:caption: Advanced Usage

advanced/customization
advanced/extending
advanced/troubleshooting
advanced/documentation
```

```{toctree}
:maxdepth: 2
:caption: Reference

api
dependency-groups
reference/configuration
reference/template-structure
reference/post-generation
reference/architecture
```

```{toctree}
:maxdepth: 2
:caption: Contributing

contributing
adr/index
```

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
└── README.md                  # Project documentation
```

## 🛠️ Template Configuration

The template supports various configuration options:

- **Project metadata**: name, description, author, license
- **Python versions**: 3.11, 3.12, 3.13
- **Optional features**: CLI interface, conda fallback
- **Quality thresholds**: coverage, complexity limits

## 🤝 Contributing

See {doc}`contributing` for details on contributing to the template.

## 📄 License

MIT License - see the [LICENSE](https://github.com/jeffrichley/seedling/blob/main/LICENSE) file for details.
