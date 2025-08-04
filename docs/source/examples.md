# 📚 Examples

See Seedling in action with these real-world examples and configurations.

## Project Types

### Basic Python Package

Perfect for simple libraries and utilities.

```bash
copier copy https://github.com/jeffrichley/seedling.git my-package \
  --data project_name="My Package" \
  --data project_slug="my_package" \
  --data project_description="A simple Python package" \
  --data author_name="Your Name" \
  --data author_email="your.email@example.com" \
  --data github_username="yourusername" \
  --data license="MIT" \
  --data python_versions="3.11,3.12"
```

**Result**: A clean, minimal Python package with basic tooling.

### CLI Application

For command-line tools and utilities.

```bash
copier copy https://github.com/jeffrichley/seedling.git my-cli-app \
  --data project_name="My CLI App" \
  --data project_slug="my_cli_app" \
  --data project_description="A command-line interface application" \
  --data include_cli=true \
  --data license="Apache-2.0" \
  --data python_versions="3.12"
```

**Result**: A CLI application with argument parsing and command structure.

### Data Science Project

For machine learning and data analysis projects.

```bash
copier copy https://github.com/jeffrichley/seedling.git my-ml-project \
  --data project_name="ML Pipeline" \
  --data project_slug="ml_pipeline" \
  --data project_description="A machine learning pipeline for data analysis" \
  --data project_keywords="machine-learning,data-science,python,pipeline" \
  --data coverage_threshold=75 \
  --data license="MIT" \
  --data python_versions="3.11,3.12"
```

**Result**: A data science project with testing and documentation.

### Enterprise Library

For production-ready, enterprise-grade libraries.

```bash
copier copy https://github.com/jeffrichley/seedling.git enterprise-lib \
  --data project_name="Enterprise Library" \
  --data project_slug="enterprise_library" \
  --data project_description="A comprehensive enterprise-grade Python library" \
  --data project_keywords="enterprise,library,python,api,rest" \
  --data author_name="Your Full Name" \
  --data author_email="your.full.name@company.com" \
  --data github_username="yourusername" \
  --data copyright_year="2024" \
  --data version="1.0.0" \
  --data license="Apache-2.0" \
  --data python_versions="3.11,3.12,3.13" \
  --data coverage_threshold=95 \
  --data include_cli=true \
  --data enable_conda_fallback=true
```

**Result**: A production-ready library with strict quality standards.

## Configuration Files

### Minimal Configuration

```yaml
# minimal-config.yaml
project_name: "Minimal Project"
project_slug: "minimal_project"
project_description: "A minimal Python project"
author_name: "Your Name"
author_email: "your.email@example.com"
github_username: "yourusername"
license: "MIT"
python_versions: "3.11"
coverage_threshold: 80
```

Usage:
```bash
copier copy https://github.com/jeffrichley/seedling.git my-project --data-file minimal-config.yaml
```

### Full Configuration

```yaml
# full-config.yaml
project_name: "Enterprise Library"
project_slug: "enterprise_library"
project_description: "A comprehensive enterprise-grade Python library with full CI/CD, documentation, and quality tooling"
project_keywords: "enterprise,library,python,api,rest"
author_name: "Your Full Name"
author_email: "your.full.name@company.com"
github_username: "yourusername"
copyright_year: "2024"
version: "1.0.0"
license: "Apache-2.0"
python_versions: "3.11,3.12,3.13"
coverage_threshold: 95
include_cli: true
enable_conda_fallback: true
```

Usage:
```bash
copier copy https://github.com/jeffrichley/seedling.git my-project --data-file full-config.yaml
```

### Academic Project

```yaml
# academic-config.yaml
project_name: "Research Tool"
project_slug: "research_tool"
project_description: "A research tool for academic analysis"
project_keywords: "research,academic,python,analysis"
author_name: "Dr. Jane Smith"
author_email: "jane.smith@university.edu"
github_username: "janesmith"
copyright_year: "2024"
version: "0.1.0"
license: "MIT"
python_versions: "3.11,3.12"
coverage_threshold: 70
```

### Open Source Library

```yaml
# opensource-config.yaml
project_name: "Awesome Library"
project_slug: "awesome_library"
project_description: "An awesome open source Python library"
project_keywords: "python,library,open-source,awesome"
author_name: "Your Name"
author_email: "your.email@example.com"
github_username: "yourusername"
copyright_year: "2024"
version: "0.1.0"
license: "MIT"
python_versions: "3.11,3.12,3.13"
coverage_threshold: 90
include_cli: true
```

## Generated Project Examples

### Basic Package Structure

```
my-package/
├── src/my_package/
│   └── __init__.py
├── tests/
│   ├── unit/
│   │   └── test_example.py
│   ├── integration/
│   └── e2e/
├── docs/
│   ├── api.md
│   └── index.md
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── release.yml
├── pyproject.toml
├── .pre-commit-config.yaml
├── noxfile.py
├── README.md
└── LICENSE
```

### CLI Application Structure

```
my-cli-app/
├── src/my_cli_app/
│   ├── __init__.py
│   └── main.py          # CLI entry point
├── tests/
│   ├── unit/
│   │   └── test_main.py
│   ├── integration/
│   └── e2e/
├── docs/
├── .github/
├── pyproject.toml
├── .pre-commit-config.yaml
├── noxfile.py
├── README.md
└── LICENSE
```

## Post-Generation Examples

### Basic Development Workflow

```bash
cd my-project

# Set up development environment
uv sync
pre-commit install

# Run quality checks
uv run dev checkit

# Write some code
echo 'def hello_world(): return "Hello, World!"' > src/my_project/main.py

# Run tests
uv run dev test

# Format code
uv run dev format

# Build documentation
uv run dev docs
```

### CI/CD Pipeline

The generated project includes GitHub Actions workflows:

- **CI**: Runs on every push and PR
- **Release**: Automated releases with semantic versioning
- **Security**: Dependency scanning and vulnerability checks
- **Documentation**: Automatic documentation deployment

### Quality Gates

The template enforces quality standards:

- **Code formatting**: Black and isort
- **Linting**: Ruff for code quality
- **Type checking**: MyPy for type safety
- **Test coverage**: Minimum coverage threshold
- **Security**: pip-audit for vulnerabilities

## Customization Examples

### Adding Dependencies

```toml
# pyproject.toml
[project]
dependencies = [
    "requests>=2.28.0",
    "pandas>=1.5.0",
    "numpy>=1.24.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=23.0.0",
    # ... other dev dependencies
]
```

### Custom GitHub Actions

```yaml
# .github/workflows/custom.yml
name: Custom Workflow
on: [push, pull_request]
jobs:
  custom:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Custom step
        run: echo "Custom workflow"
```

### Custom Documentation

```markdown
# docs/custom.md
# Custom Documentation

Add your project-specific documentation here.
```

## Contributing Examples

Have a great example? Submit a pull request to add it here!

1. Create a new configuration file
2. Add a description of the use case
3. Include the generated project structure
4. Show post-generation setup steps 