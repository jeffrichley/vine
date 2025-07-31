Dependency Groups
================

Project Vine uses dependency groups for modular installation, allowing you to install only the dependencies you need for your specific use case.

Overview
--------

Dependency groups are defined in ``pyproject.toml`` and provide a clean way to manage different types of dependencies:

- **Runtime dependencies**: Core functionality required to use the library
- **Development dependencies**: Tools for development, testing, and quality assurance
- **Documentation dependencies**: Tools for building documentation
- **Type checking dependencies**: Tools for static type analysis
- **Security dependencies**: Tools for security scanning

Available Groups
---------------

Core Runtime
~~~~~~~~~~~

The core runtime dependencies are installed by default:

.. code-block:: bash

   uv pip install -e .

This includes:
- **moviepy**: Video processing and editing
- **pydantic**: Data validation and settings management
- **pyyaml**: YAML configuration parsing
- **pillow**: Image processing
- **numpy**: Numerical computing
- **rich**: Rich text and beautiful formatting

Development
~~~~~~~~~~~

Development dependencies for coding, testing, and quality assurance:

.. code-block:: bash

   uv pip install -e ".[dev]"

This includes:
- **black**: Code formatting
- **ruff**: Linting and import sorting
- **pre-commit**: Git hooks for quality checks
- **pytest**: Testing framework
- **pytest-cov**: Coverage reporting
- **mypy**: Type checking
- **hypothesis**: Property-based testing
- **monkeytype**: Automatic type annotation generation
- **vulture**: Dead code detection
- **radon**: Code complexity analysis
- **xenon**: Complexity monitoring

- **validate-pyproject**: Configuration validation
- **toml-sort**: TOML file formatting

Documentation
~~~~~~~~~~~~~

Documentation building tools:

.. code-block:: bash

   uv pip install -e ".[docs]"

This includes:
- **sphinx**: Documentation generator
- **sphinx-rtd-theme**: Read the Docs theme
- **sphinx-autodoc-typehints**: Type hint documentation
- **sphinx-copybutton**: Copy button for code blocks
- **myst-parser**: Markdown support for Sphinx

Type Checking
~~~~~~~~~~~~~

Type checking tools:

.. code-block:: bash

   uv pip install -e ".[typecheck]"

This includes:
- **mypy**: Static type checker

Security
~~~~~~~~

Security scanning tools:

.. code-block:: bash

   uv pip install -e ".[security]"

This includes:
- **pip-audit**: Dependency vulnerability scanning

Testing
~~~~~~~

Testing tools (separate from dev group):

.. code-block:: bash

   uv pip install -e ".[test]"

This includes:
- **hypothesis**: Property-based testing
- **pytest-benchmark**: Performance benchmarking
- **psutil**: System and process utilities

Installation Examples
--------------------

Full Development Setup
~~~~~~~~~~~~~~~~~~~~~

For complete development environment:

.. code-block:: bash

   uv pip install -e ".[dev,docs,typecheck,security]"

This installs all development, documentation, type checking, and security tools.

Minimal Development Setup
~~~~~~~~~~~~~~~~~~~~~~~~~

For basic development without documentation:

.. code-block:: bash

   uv pip install -e ".[dev]"

This installs core development tools for coding and testing.

Documentation Only
~~~~~~~~~~~~~~~~~~

For building documentation:

.. code-block:: bash

   uv pip install -e ".[docs]"

This installs only the tools needed to build documentation.

Production Deployment
~~~~~~~~~~~~~~~~~~~~~

For production deployment, install only runtime dependencies:

.. code-block:: bash

   uv pip install -e .
   # or
   uv pip install vine

This installs only the core functionality without development tools.

Usage in CI/CD
-------------

Dependency groups are particularly useful in CI/CD pipelines:

.. code-block:: yaml

   # Example GitHub Actions workflow
   - name: Install dependencies
     run: |
       uv pip install -e ".[dev,test]"

   - name: Run tests
     run: |
       uv run dev test

   - name: Build documentation
     run: |
       uv pip install -e ".[docs]"
       make docs

Benefits
--------

- **Reduced installation time**: Install only what you need
- **Smaller environments**: Keep development environments lean
- **Clear separation**: Distinguish between runtime and development dependencies
- **CI/CD optimization**: Use specific groups for different pipeline stages
- **Security**: Separate security tools from development tools

Best Practices
-------------

1. **Use specific groups**: Install only the groups you need
2. **Document requirements**: Update this documentation when adding new groups
3. **Test installations**: Verify that each group installs correctly
4. **Keep groups focused**: Each group should have a clear, single purpose
5. **Update CI/CD**: Use appropriate groups in your CI/CD pipelines
