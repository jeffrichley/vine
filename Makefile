.PHONY: help docs docs-clean docs-serve docs-linkcheck format lint test test-cov test-cov-check build install-dev checkit v vulture demo render-test validate-specs benchmark benchmark-report benchmark-baseline interrogate interrogate

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install-dev:  ## Install development dependencies
	uv pip install -e ".[dev,docs]"

format:  ## Format code with black and ruff
	uv run black src/ tests/
	uv run ruff check src/ tests/ --fix

lint:  ## Lint code with ruff
	uv run ruff check src/ tests/

test:  ## Run tests
	uv run pytest tests/ -v

test-cov:  ## Run tests with coverage
	uv run pytest tests/ --cov=src/vine --cov-report=html --cov-report=term --cov-report=xml

test-cov-check:  ## Run tests with coverage and fail if below 80%
	uv run pytest tests/ --cov=src/vine --cov-report=term-missing --cov-fail-under=80

ftest:  ## Run tests with full parallel power (fastest execution)
	uv run pytest tests/ -n auto --dist loadscope --tb=short --durations=10

ftest-cov:  ## Run tests with coverage using full parallel power
	uv run pytest tests/ -n auto --dist loadscope --cov=src/vine --cov-report=term-missing --cov-report=html --cov-report=xml --tb=short --durations=10

ftest-verbose:  ## Run tests with full parallel power and verbose output
	uv run pytest tests/ -n auto --dist loadscope -v --durations=10

vulture:  ## Find dead code with vulture
	uv run vulture src/ tests/ --min-confidence 80

vulture-all:  ## Find all potential dead code with vulture (lower confidence)
	uv run vulture src/ tests/ --min-confidence 60

docs:  ## Build documentation
	cd docs && make html

docs-clean:  ## Clean documentation build
	cd docs && make clean

docs-serve:  ## Serve documentation locally
	cd docs && python -m http.server 8000 --directory build/html

docs-linkcheck:  ## Check documentation links
	cd docs && make linkcheck

docs-watch:  ## Watch for changes and rebuild documentation
	cd docs && sphinx-autobuild source build/html --port 8001 --open-browser

build:  ## Build the package
	uv build

# Documentation shortcuts
docs-build: docs  ## Alias for docs
docs-view: docs-serve  ## Alias for docs-serve

checkit:
	uv run mypy --config-file=pyproject.toml src/ tests/
	pre-commit run --all-files
	$(MAKE) test-cov-check

quality-gates:  ## Run all quality gates with detailed reporting
	python scripts/quality_gates.py --save-report

quality-gates-no-docs:  ## Run quality gates without documentation check
	python scripts/quality_gates.py --no-docs --save-report

precommit-autofix:
	pre-commit run --all-files
	git add .

# 🚀 PERFORMANCE BENCHMARKS (MANUAL ONLY - NOT RUN WITH REGULAR TESTS)
benchmark:  ## Run performance benchmarks (manual only)
	uv run python scripts/run_benchmarks.py

benchmark-report:  ## Run benchmarks and generate detailed report (manual only)
	uv run python scripts/run_benchmarks.py --compare-baseline

benchmark-baseline:  ## Run benchmarks and save as new baseline (manual only)
	uv run python scripts/run_benchmarks.py --save-baseline

benchmark-quick:  ## Run quick benchmarks (fewer rounds) (manual only)
	uv run pytest scripts/benchmarks/ --benchmark-only --benchmark-min-rounds=3 --benchmark-max-time=5.0

interrogate:  ## Check documentation coverage with interrogate
	uv run interrogate src/ tests/ scripts/ --fail-under=50 --generate-badge docs/assets/interrogate_badge.svg -v -m

audit:  ## Run security audit with pip-audit
	pip-audit --desc

validate-config:  ## Validate pyproject.toml structure
	uv run validate-pyproject pyproject.toml

sort-toml:  ## Sort and format pyproject.toml
	uv run toml-sort --in-place pyproject.toml
