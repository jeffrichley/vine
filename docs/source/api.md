# Template Reference

This section provides comprehensive documentation for the Seedling template system.

## Template Variables

Seedling uses Jinja2 templating with the following variables:

### Core Variables

- **`project_name`**: The name of your project (e.g., "My Awesome Library")
- **`project_slug`**: The Python package name (e.g., "my_awesome_library")
- **`github_username`**: Your GitHub username
- **`python_versions`**: Supported Python versions (comma-separated)
- **`license`**: License type (MIT, Apache-2.0, etc.)

### Optional Variables

- **`description`**: Project description
- **`keywords`**: Project keywords for PyPI
- **`author_name`**: Author name
- **`author_email`**: Author email
- **`include_cli`**: Whether to include CLI functionality
- **`include_docs`**: Whether to include documentation setup
- **`include_ci`**: Whether to include CI/CD configuration

## Template Structure

The Seedling template generates the following structure:

```
{{ project_slug }}/
├── src/
│   └── {{ project_slug }}/
│       ├── __init__.py
│       └── py.typed
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── docs/
├── pyproject.toml
├── README.md
└── .github/
    └── workflows/
```

## Configuration Examples

### Basic Configuration

```yaml
# copier.yml
project_name: My Awesome Library
project_slug: my_awesome_library
github_username: myusername
python_versions: "3.11, 3.12"
license: MIT
description: A fantastic Python library
```

### CLI Application

```yaml
# copier.yml
project_name: My CLI Tool
project_slug: my_cli_tool
github_username: myusername
python_versions: "3.11, 3.12"
license: MIT
include_cli: true
description: A command-line interface tool
```

### Enterprise Library

```yaml
# copier.yml
project_name: Enterprise Library
project_slug: enterprise_library
github_username: myusername
python_versions: "3.11, 3.12"
license: Apache-2.0
include_docs: true
include_ci: true
description: Enterprise-grade Python library
```

## Generated Files

### Core Files

- **`pyproject.toml`**: Project configuration with all dependencies
- **`README.md`**: Project documentation with badges
- **`src/{{ project_slug }}/__init__.py`**: Package initialization
- **`tests/`**: Complete test structure

### Optional Files

- **`docs/`**: Sphinx documentation setup (if `include_docs: true`)
- **`.github/workflows/`**: CI/CD workflows (if `include_ci: true`)
- **`src/{{ project_slug }}/cli.py`**: CLI interface (if `include_cli: true`)

## Customization

### Adding Custom Variables

To add custom variables to your template:

1. Add the variable to `copier.yml`
2. Use `{{ variable_name }}` in your template files
3. Provide a default value or make it required

### Template Extensions

You can extend the template by:

1. Adding new directories to the template
2. Creating conditional sections with `{% if variable %}` blocks
3. Using Jinja2 filters and functions

## Best Practices

1. **Use descriptive variable names**
2. **Provide sensible defaults**
3. **Validate input with copier.yml schema**
4. **Test template generation with different configurations**
5. **Document all template variables**

## Examples

For usage examples, see the [Examples](examples.md) section.

## Contributing

To add new template features, follow these guidelines:

1. Add variables to `copier.yml`
2. Update template files with new variables
3. Add documentation for new features
4. Test with various configurations

For more information, see the [Contributing Guide](contributing.md).
