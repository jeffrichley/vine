.PHONY: audit build checkit docs docs-build docs-clean docs-linkcheck docs-serve docs-view docs-watch format help install-dev lint precommit-autofix sort-toml test test-cov test-cov-check validate-config vulture vulture-low

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

## 🎯 Code Quality

format:  ## Format code with black and ruff
	uv run black src/ tests/
	uv run ruff check src/ tests/ --fix

lint:  ## Lint code with ruff
	uv run ruff check src/ tests/

vulture:  ## Find dead code with vulture
	uv run vulture src/ tests/ --min-confidence 80

vulture-low:  ## Find all potential dead code with vulture (lower confidence)
	uv run vulture src/ tests/ --min-confidence 60

## 🧪 Testing

test:  ## Run tests
	uv run pytest tests/ -v

test-cov:  ## Run tests with coverage
	uv run pytest tests/ --cov=src/vine --cov-report=html --cov-report=term --cov-report=xml

test-cov-check:  ## Run tests with coverage and fail if below 80%
	uv run pytest tests/ --cov=src/vine --cov-report=term-missing --cov-fail-under=80

test-random:  ## Run tests with random seed (generates new seed each time)
	python scripts/run_tests_with_seed.py

test-seed:  ## Run tests with specific seed (usage: make test-seed SEED=12345)
	python scripts/run_tests_with_seed.py --seed $(SEED)

test-seed-show:  ## Show the last seed used
	python scripts/run_tests_with_seed.py --show-last-seed

check-no-patch:  ## Check for @patch usage in test files
	python scripts/check_no_patch.py

## 📚 Documentation

docs:  ## Build documentation
	cd docs && uv run make html

docs-build: docs  ## Alias for docs

docs-clean:  ## Clean documentation build
	cd docs && uv run make clean

docs-linkcheck:  ## Check documentation links
	cd docs && uv run make linkcheck

docs-serve:  ## Serve documentation locally
	cd docs && uv run python -m http.server 8000 --directory build/html

docs-view: docs-serve  ## Alias for docs-serve

docs-watch:  ## Watch for changes and rebuild documentation
	cd docs && uv run sphinx-autobuild source build/html --port 8001 --open-browser

## 📦 Build & Install

build:  ## Build the package
	uv build

install-dev:  ## Install development dependencies
	uv pip install -e ".[dev,docs]"

## ✅ Quality Gates

checkit:
	uv run mypy --config-file=pyproject.toml src/ tests/
	uv run xenon --max-absolute B --max-average A src/
	pre-commit run --all-files
	$(MAKE) test-cov-check

precommit-autofix:
	pre-commit run --all-files
	git add .

## 🧰 Utilities

audit:  ## Run security audit with pip-audit
	pip-audit --desc

sort-toml:  ## Sort and format pyproject.toml
	uv run toml-sort --in-place pyproject.toml

validate-config:  ## Validate pyproject.toml structure
	uv run validate-pyproject pyproject.toml
