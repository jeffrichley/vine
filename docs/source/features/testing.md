# 🧪 Testing

Seedling includes a comprehensive testing framework with modern Python testing tools.

## Overview

The template provides:
- **pytest**: Modern Python testing framework
- **Coverage**: Test coverage measurement
- **Hypothesis**: Property-based testing
- **Mocking**: Built-in mocking capabilities
- **Test organization**: Clear test structure

## Test Structure

```
tests/
├── unit/                    # Unit tests
│   ├── __init__.py
│   └── test_example.py
├── integration/             # Integration tests
│   └── __init__.py
└── e2e/                     # End-to-end tests
    └── __init__.py
```

## Running Tests

### Basic Testing

```bash
# Run all tests
uv run dev test

# Run with coverage
uv run dev test --cov

# Run specific test file
uv run dev test tests/unit/test_example.py

# Run specific test function
uv run dev test tests/unit/test_example.py::test_specific_function
```

### Test Categories

```bash
# Run only unit tests
uv run dev test tests/unit/

# Run only integration tests
uv run dev test tests/integration/

# Run only e2e tests
uv run dev test tests/e2e/
```

### Coverage Testing

```bash
# Run with coverage report
uv run dev test --cov --cov-report=term-missing

# Generate HTML coverage report
uv run dev test --cov --cov-report=html

# Check coverage threshold
uv run dev test --cov --cov-fail-under=80
```

## Writing Tests

### Unit Tests

```python
# tests/unit/test_example.py
import pytest
from your_package.example import main_function


def test_main_function():
    """Test the main function with valid input."""
    result = main_function("test input")
    assert result == "Processed: test input"


def test_main_function_with_empty_input():
    """Test the main function with empty input."""
    result = main_function("")
    assert result == "Processed: "


def test_main_function_with_invalid_input():
    """Test the main function with invalid input."""
    with pytest.raises(ValueError, match="Input cannot be None"):
        main_function(None)
```

### Property-Based Testing

```python
# tests/unit/test_property_based.py
from hypothesis import given, strategies as st
from your_package.example import main_function


@given(st.text())
def test_main_function_properties(input_text):
    """Test main function properties with any text input."""
    result = main_function(input_text)
    
    # Property 1: Result is always a string
    assert isinstance(result, str)
    
    # Property 2: Result always starts with "Processed: "
    assert result.startswith("Processed: ")
    
    # Property 3: Result length is predictable
    assert len(result) == len("Processed: ") + len(input_text)
```

### Integration Tests

```python
# tests/integration/test_integration.py
import pytest
from your_package.core import CoreClass
from your_package.config import Config


class TestIntegration:
    """Integration tests for core functionality."""
    
    def test_core_with_config(self):
        """Test core functionality with configuration."""
        config = Config(debug=True, timeout=30)
        core = CoreClass(config)
        
        result = core.process_data("test data")
        assert result.is_success
        assert result.data == "processed test data"
    
    def test_core_with_database(self, db_connection):
        """Test core functionality with database."""
        core = CoreClass(db_connection=db_connection)
        
        result = core.save_data("test data")
        assert result.is_success
        
        # Verify data was saved
        saved_data = db_connection.get_data()
        assert "test data" in saved_data
```

### End-to-End Tests

```python
# tests/e2e/test_e2e.py
import pytest
from your_package.cli import main


class TestEndToEnd:
    """End-to-end tests for CLI functionality."""
    
    def test_cli_basic_workflow(self, capsys):
        """Test basic CLI workflow."""
        # Simulate CLI input
        with pytest.MonkeyPatch().context() as m:
            m.setattr('sys.argv', ['your_package', 'process', 'test.txt'])
            
            main()
            
            captured = capsys.readouterr()
            assert "Processing test.txt" in captured.out
            assert "Success" in captured.out
    
    def test_cli_error_handling(self, capsys):
        """Test CLI error handling."""
        with pytest.MonkeyPatch().context() as m:
            m.setattr('sys.argv', ['your_package', 'process', 'nonexistent.txt'])
            
            main()
            
            captured = capsys.readouterr()
            assert "Error" in captured.err
            assert "File not found" in captured.err
```

## Test Configuration

### pytest Configuration

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--strict-config",
    "--verbose",
    "--tb=short",
]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "e2e: marks tests as end-to-end tests",
]
```

### Coverage Configuration

```toml
# pyproject.toml
[tool.coverage.run]
source = ["src"]
omit = [
    "*/tests/*",
    "*/test_*",
    "*/__pycache__/*",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if self.debug:",
    "if settings.DEBUG",
    "raise AssertionError",
    "raise NotImplementedError",
    "if 0:",
    "if __name__ == .__main__.:",
    "class .*\\bProtocol\\):",
    "@(abc\\.)?abstractmethod",
]
```

## Test Fixtures

### Common Fixtures

```python
# tests/conftest.py
import pytest
from your_package.config import Config
from your_package.database import Database


@pytest.fixture
def config():
    """Provide test configuration."""
    return Config(debug=True, timeout=10)


@pytest.fixture
def db_connection():
    """Provide test database connection."""
    db = Database(":memory:")
    db.create_tables()
    yield db
    db.close()


@pytest.fixture
def sample_data():
    """Provide sample test data."""
    return {
        "users": [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"},
        ],
        "products": [
            {"id": 1, "name": "Product A", "price": 10.99},
            {"id": 2, "name": "Product B", "price": 20.99},
        ]
    }
```

## Best Practices

### Test Organization

1. **Group related tests** in classes
2. **Use descriptive test names** that explain the scenario
3. **Follow AAA pattern**: Arrange, Act, Assert
4. **Keep tests independent** and isolated
5. **Use fixtures** for common setup

### Test Quality

1. **Test the behavior**, not the implementation
2. **Write tests first** (TDD approach)
3. **Test edge cases** and error conditions
4. **Use property-based testing** for complex logic
5. **Mock external dependencies**

### Coverage Goals

1. **Aim for 80%+ coverage** overall
2. **100% coverage** for critical paths
3. **100% coverage** for new code
4. **Test error handling** paths
5. **Test boundary conditions**

## Advanced Testing

### Parameterized Tests

```python
import pytest


@pytest.mark.parametrize("input,expected", [
    ("hello", "Processed: hello"),
    ("world", "Processed: world"),
    ("", "Processed: "),
])
def test_main_function_parameterized(input, expected):
    """Test main function with multiple inputs."""
    result = main_function(input)
    assert result == expected
```

### Async Testing

```python
import pytest
import asyncio
from your_package.async_module import async_function


@pytest.mark.asyncio
async def test_async_function():
    """Test async function."""
    result = await async_function("test")
    assert result == "async processed: test"
```

### Performance Testing

```python
import pytest
from your_package.performance import slow_function


def test_performance():
    """Test function performance."""
    import time
    
    start_time = time.time()
    result = slow_function()
    end_time = time.time()
    
    assert result is not None
    assert end_time - start_time < 1.0  # Should complete in under 1 second
```

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/ci.yml
- name: Run Tests
  run: |
    uv run dev test --cov --cov-report=xml
    uv run dev test --cov --cov-fail-under=80

- name: Upload Coverage
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage.xml
```

## Troubleshooting

### Common Issues

#### Import Errors

```bash
# Check Python path
PYTHONPATH=src uv run pytest

# Install in editable mode
uv pip install -e .
```

#### Coverage Issues

```bash
# Check coverage configuration
uv run coverage run --source=src -m pytest
uv run coverage report

# Debug coverage
uv run coverage debug data
```

#### Slow Tests

```bash
# Run only fast tests
uv run dev test -m "not slow"

# Profile test performance
uv run dev test --durations=10
```

### Getting Help

- **pytest documentation**: https://docs.pytest.org/
- **Hypothesis documentation**: https://hypothesis.readthedocs.io/
- **Coverage documentation**: https://coverage.readthedocs.io/
- **pytest-cov documentation**: https://pytest-cov.readthedocs.io/

## Next Steps

- **Set up test databases** for integration tests
- **Configure test environments** for different scenarios
- **Add performance benchmarks** for critical functions
- **Set up test data factories** for complex test scenarios 