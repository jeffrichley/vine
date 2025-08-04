# ⚙️ Configuration Guide

Learn how to configure your Seedling template project with all available options.

## Template Variables

Seedling uses Copier's template system with the following configuration variables:

### Project Metadata

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `project_name` | str | "My Awesome Project" | Human-readable project name |
| `project_slug` | str | "my_awesome_project" | Python package name (lowercase, underscores) |
| `project_description` | str | "A modern Python project..." | Brief project description |
| `project_keywords` | str | "python,modern,uv,nox,just" | Comma-separated keywords for PyPI |
| `version` | str | "0.1.0" | Initial version number |

### Author Information

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `author_name` | str | "Your Name" | Your full name |
| `author_email` | str | "your.name@example.com" | Your email address |
| `github_username` | str | "yourusername" | Your GitHub username |
| `copyright_year` | str | "2024" | Copyright year |

### Project Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `license` | choice | "MIT" | License type (MIT, Apache-2.0, GPL-3.0, BSD-3-Clause) |
| `python_versions` | str | "3.11,3.12" | Supported Python versions (comma-separated) |
| `coverage_threshold` | int | 80 | Minimum test coverage percentage (0-100) |

### Optional Features

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `include_cli` | bool | false | Include CLI interface |
| `enable_conda_fallback` | bool | false | Enable conda fallback for uv |

## Configuration Examples

### Basic Python Package

```yaml
project_name: "My Package"
project_slug: "my_package"
project_description: "A simple Python package"
author_name: "Your Name"
author_email: "your.email@example.com"
github_username: "yourusername"
license: "MIT"
python_versions: "3.11,3.12"
coverage_threshold: 80
```

### CLI Application

```yaml
project_name: "My CLI App"
project_slug: "my_cli_app"
project_description: "A command-line interface application"
author_name: "Your Name"
author_email: "your.email@example.com"
github_username: "yourusername"
license: "Apache-2.0"
python_versions: "3.12"
coverage_threshold: 85
include_cli: true
```

### Enterprise Library

```yaml
project_name: "Enterprise Library"
project_slug: "enterprise_library"
project_description: "A comprehensive enterprise-grade Python library"
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

## Using Configuration Files

### Method 1: Interactive Prompts

```bash
copier copy https://github.com/jeffrichley/seedling.git my-project
# Answer prompts interactively
```

### Method 2: Data File

Create a configuration file:

```yaml
# my-config.yaml
project_name: "My Project"
project_slug: "my_project"
project_description: "My awesome project"
author_name: "Your Name"
author_email: "your.email@example.com"
github_username: "yourusername"
license: "MIT"
python_versions: "3.11,3.12"
coverage_threshold: 85
```

Use the data file:

```bash
copier copy https://github.com/jeffrichley/seedling.git my-project --data-file my-config.yaml
```

### Method 3: Command Line Arguments

```bash
copier copy https://github.com/jeffrichley/seedling.git my-project \
  --data project_name="My Project" \
  --data project_slug="my_project" \
  --data author_name="Your Name" \
  --data license="MIT"
```

## Validation Rules

### Python Versions

- Must be comma-separated list
- Format: `3.11,3.12,3.13`
- Must be valid Python version numbers
- At least one version required

### Coverage Threshold

- Integer between 0 and 100
- Represents minimum test coverage percentage
- Used in CI/CD quality gates

### Project Slug

- Lowercase letters, numbers, and underscores only
- Must be a valid Python package name
- No spaces or special characters

## Post-Generation Configuration

After generating your project, you can:

### Update Template

```bash
cd my-project
copier update
```

### Override Settings

```bash
# Update specific settings
copier update --data coverage_threshold=90
```

### Skip Updates

```bash
# Skip specific files during update
copier update --skip .github/workflows/ci.yml
```

## Environment Variables

You can use environment variables for sensitive data:

```bash
export SEEDLING_AUTHOR_EMAIL="your.email@example.com"
export SEEDLING_GITHUB_USERNAME="yourusername"

copier copy https://github.com/jeffrichley/seedling.git my-project
```

## Best Practices

1. **Use descriptive names**: Make project names and descriptions clear
2. **Choose appropriate licenses**: Consider your project's needs
3. **Set realistic coverage**: Start with 80% and increase over time
4. **Use data files**: For reproducible configurations
5. **Version control**: Commit your configuration files

## Troubleshooting

### Common Issues

- **Invalid project slug**: Use only lowercase letters, numbers, and underscores
- **Python version format**: Use comma-separated list (e.g., "3.11,3.12")
- **Coverage threshold**: Must be integer between 0-100

### Getting Help

- Check the {doc}`troubleshooting` guide
- Review the {doc}`examples` for working configurations
- Visit the [Copier documentation](https://copier.readthedocs.io/) 