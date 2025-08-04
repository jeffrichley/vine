# 📚 Documentation Development Guide

This guide covers how to develop, build, and maintain the Seedling documentation.

## Overview

The Seedling documentation uses:
- **Sphinx**: Documentation generator
- **MyST**: Markdown parser for Sphinx
- **Furo**: Modern, responsive theme
- **uv**: Fast Python package manager

## Quick Start

### Prerequisites

- **uv**: Fast Python package manager
- **Python 3.11+**: Required for Sphinx

### Building Documentation

```bash
# Navigate to docs directory
cd docs

# Quick build (recommended)
./build-docs.sh

# Or manual build
uv sync
make html
make serve
```

The documentation will be available at http://localhost:8000

## Documentation Structure

```
docs/
├── source/                    # Source files
│   ├── index.md              # Main documentation index
│   ├── quickstart.md         # Quick start guide
│   ├── installation.md       # Installation instructions
│   ├── configuration.md      # Configuration reference
│   ├── examples.md           # Examples and use cases
│   ├── contributing.md       # Contributing guide
│   ├── adr/                  # Architecture decisions
│   │   ├── index.md         # ADR index
│   │   ├── 0001-template-design.md
│   │   ├── 0002-technology-stack.md
│   │   └── 0003-architecture-decisions.md
│   ├── features/             # Feature documentation
│   │   ├── quality-tooling.md
│   │   ├── testing.md
│   │   ├── documentation.md
│   │   ├── ci-cd.md
│   │   └── development.md
│   ├── advanced/             # Advanced usage
│   │   ├── customization.md
│   │   ├── extending.md
│   │   └── troubleshooting.md
│   └── reference/            # Reference documentation
│       ├── configuration.md
│       ├── template-structure.md
│       ├── post-generation.md
│       └── architecture.md
├── build/                    # Built documentation (generated)
├── pyproject.toml           # Documentation dependencies
├── Makefile                 # Build targets
└── build-docs.sh           # Build script
```

## Writing Documentation

### File Format

- **Use Markdown** (`.md`) files with MyST extensions
- **Follow the existing style** and structure
- **Include code examples** where helpful

### MyST Extensions

The documentation supports these MyST extensions:

```markdown
# Basic extensions
- colon_fence: Code blocks with colons
- deflist: Definition lists
- dollarmath: LaTeX math
- fieldlist: Field lists
- html_admonition: HTML admonitions
- html_image: HTML images
- replacements: Text replacements
- smartquotes: Smart quotes
- strikethrough: Strikethrough text
- substitution: Variable substitution
- tasklist: Task lists
```

### Code Examples

```markdown
# Inline code
Use `copier copy` to generate a new project.

# Code blocks
```bash
copier copy https://github.com/jeffrichley/seedling.git my-project
```

# Syntax highlighting
```python
def hello_world():
    return "Hello, World!"
```
```

### Cross-References

```markdown
# Link to other documentation
See the {doc}`quickstart` guide for getting started.

# Link to external resources
Visit the [Copier documentation](https://copier.readthedocs.io/).

# Link to specific sections
See {ref}`configuration-examples` for examples.
```

### Admonitions

```markdown
```{note}
This is a note with important information.
```

```{warning}
This is a warning about potential issues.
```

```{tip}
This is a helpful tip for users.
```
```

## Adding New Documentation

### 1. Choose the Right Location

- **User guides**: Root of `source/`
- **Features**: `source/features/`
- **Advanced topics**: `source/advanced/`
- **Reference**: `source/reference/`
- **Architecture**: `source/adr/`

### 2. Create the File

```bash
# Create a new documentation file
touch docs/source/features/new-feature.md
```

### 3. Add Content

```markdown
# New Feature

Brief description of the new feature.

## Usage

How to use the feature.

## Configuration

Configuration options.

## Examples

```bash
# Example usage
example-command --option value
```
```

### 4. Update Navigation

Add your new file to the appropriate toctree in `docs/source/index.md`:

```markdown
```{toctree}
:maxdepth: 2
:caption: Features

features/quality-tooling
features/testing
features/new-feature
```
```

### 5. Build and Test

```bash
cd docs
./build-docs.sh
make serve
```

## Documentation Guidelines

### Writing Style

- **Be clear and concise**
- **Use active voice**
- **Write for the user's perspective**
- **Include practical examples**
- **Keep it scannable** with good headings

### Content Structure

- **Start with an overview**
- **Include prerequisites**
- **Provide step-by-step instructions**
- **Show examples**
- **Include troubleshooting**

### Code Examples

- **Use realistic examples**
- **Include expected output**
- **Test all code examples**
- **Use appropriate syntax highlighting**
- **Keep examples simple and focused**

### Links and References

- **Test all internal links**
- **Verify external links work**
- **Use descriptive link text**
- **Update links when files move**

## Building and Testing

### Local Development

```bash
# Start development server
cd docs
uv sync
make serve

# In another terminal, watch for changes
fswatch -o source/ | xargs -n1 -I{} make html
```

### Quality Checks

```bash
# Check for broken links
make linkcheck

# Check spelling
make spelling

# Check for dead links
make coverage
```

### Deployment

The documentation is configured for GitHub Pages deployment:

```yaml
# .github/workflows/docs.yml
name: Deploy Documentation
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build docs
        run: |
          cd docs
          ./build-docs.sh
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs/build/html
```

## Troubleshooting

### Common Issues

#### Build Errors

```bash
# Check Sphinx version
sphinx-build --version

# Check dependencies
uv pip list | grep sphinx

# Clean and rebuild
make clean
make html
```

#### Missing Dependencies

```bash
# Install missing dependencies
uv sync

# Or install specific packages
uv add sphinx furo myst-parser
```

#### Theme Issues

```bash
# Check theme installation
python -c "import furo; print(furo.__version__)"

# Reinstall theme
uv remove furo
uv add furo
```

### Getting Help

- **Check Sphinx documentation**: https://www.sphinx-doc.org/
- **MyST documentation**: https://myst-parser.readthedocs.io/
- **Furo theme**: https://pradyunsg.me/furo/
- **GitHub issues**: Report bugs and request features

## Contributing to Documentation

1. **Follow the style guide** above
2. **Test your changes** locally
3. **Update navigation** if needed
4. **Check all links** work
5. **Submit a pull request**

Thank you for contributing to the Seedling documentation! 📚 