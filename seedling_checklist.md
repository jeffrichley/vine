# Seedling Copier Template — Ultra‑Detailed Build Checklist ✅

> **Audience**: Iris (project architect), Lily (implementation agent), and any contributor migrating *Vine* into the reusable **Seedling** template.
> **Goal**: Produce a world‑class, reproducible Copier template with automated CI/CD, docs, and development workflow.

---

## 📋 Legend

| Symbol | Meaning |
| ------ | ------- |
| ☐ | Task **not** started |
| 🛠 | Task **in progress** |
| ✅ | Task **done / verified** |
| 🔁 | Repeat for each matrix element / file |
| ⚠️ | Pay extra attention—common pitfalls |

Mark each checkbox as you finish. **Don’t** tick by “eyeballing”—run the command, verify output, then mark ✅.

---

## 0. Prerequisites

- ✅ **Developer environment**: macOS or Linux with **Python ≥ 3 .11**, **uv 0.1.34+**, **nox 2025.6+**, **just 1.25+**, **Copier 7.0+**, **Git 2.41+**, **GitHub CLI** (`gh`), and **Node ≥ 18** (only if you later add commitlint).
- ✅ **GitHub access**: admin rights to `vine` and the new `seedling` repos; ability to install GitHub Apps.
- ✅ **IDE**: VS Code, PyCharm, or Cursor with Ruff, MyPy, and Markdown plugins enabled.
- ✅ **Secrets**: `CODECOV_TOKEN` (project-level), `PYPI_API_TOKEN` (if you plan to publish), optional `GH_TOKEN` for release‑please PRs.

---

## 1. Snapshot & branch protection

1. ✅ **Clone Vine** fresh and create migration branch
   ```bash
   git clone git@github.com:your-org/vine.git
   cd vine
   git checkout -b migrate/seedling-template
   ```
2. ✅ Enable **branch protection** rules on `main`:
   - Require PR reviews (≥ 1)
   - Require status checks (CI, pre‑commit‑ci, CodeQL)
   - Dismiss stale approvals on push

---

## 2. Repo triage — prune dead weight

| Folder / file | Action | Command |
| --------------| ------ | ------- |
| `examples/`   | ⚠️ Drop entire folder (only keep empty dir placeholder) | `git rm -r examples && mkdir examples && touch examples/.gitkeep` |
| `output/`     | ⚠️ Drop (generated artefacts) | `git rm -r output` |
| `docs/_build/`| ⚠️ Drop HTML build | `git rm -r docs/_build` |
| Root `*.md` design notes | Move to `docs/adr/` | `mkdir -p docs/adr && git mv DESIGN.md docs/adr/0001-initial-spec.md` |
| `.venv/`, `.pytest_cache/`, `.coverage`, `htmlcov/` | Delete | manual |

---

## 3. Create template scaffold

1. ✅ **Scaffold directories**
   ```bash
   mkdir -p seedling/{docs,src/{{ project_slug }},tests/{unit,integration,e2e}}
   touch seedling/src/{{ project_slug }}/__init__.py
   touch seedling/tests/{unit,integration,e2e}/__init__.py
   ```
2. ✅ Copy over cleaned **noxfile.py**, **pyproject.toml**, **.pre-commit-config.yaml**—replace hard‑coded package name with Jinja tag `{{ project_slug }}`.
3. ✅ Add **LICENSE**, **CODE_OF_CONDUCT.md**, **SECURITY.md** (choose MIT license unless overwritten).

---

## 4. Draft `copier.yml`

> Located at template root.

- ✅ Define **metadata** block: `min_copier_version: "7.0.0"`, `_tasks`, `_exclude`, `_subdirectory`.
- ✅ Add **questions**: `project_name`, `project_slug`, `author_name`, `author_email`, `license`, `python_versions`, `coverage_threshold`, `include_cli`, `enable_conda_fallback`.
- ✅ For `python_versions`, add **validator** regex `^3\.\d{2?(,\s*3\.\d{2?})*$`.
- ✅ Add **conditional paths** in `_templates_suffix`: e.g., `{{ include_cli | ternary('.jinja', '.skip') }}`.

---

## 5. Post‑generation tasks

1. ✅ In `copier.yml` under `_tasks` add:
   ```yaml
   _tasks:
     - git init
     - pre-commit install
     - uv lock -p {{ python_versions.split(',')[0] }}
     {%- if enable_conda_fallback %}
     - uv mamba init
     {%- endif %}
   ```
2. ✅ Verify tasks by generating a **storybook** (`copier copy . /tmp/seedling-test --trust`).

---

## 6. Pre‑commit ecosystem

1. ☐ **Update** `.pre-commit-config.yaml`
   - Use Ruff `latest`, Black `24.1`, MyPy `1.10`, Commitizen `3.8`, pip‑audit `2024.x`, etc.
   - Add `repo: https://github.com/asottile/yesqa` to auto‑strip unused noqa comments.

2. ☐ Install and run once
   ```bash
   pre-commit install
   pre-commit run --all-files
   ```

---

## 7. Enable **pre‑commit‑ci**

1. ☐ **Install** GitHub App to org or repo.
2. ☐ In `.pre-commit-config.yaml` add the label hint:
   ```yaml
   ci:
     autoupdate_schedule: weekly
   ```
3. ☐ Push branch; confirm PR gets **auto-fix** commit when deliberately pushing poorly formatted file.

---

## 8. Commitizen

1. ☐ Add **pre-commit hook**
   ```yaml
   - repo: https://github.com/commitizen-tools/commitizen
     rev: v3.8.1
     hooks:
       - id: commitizen
         stages: [commit-msg]
   ```
2. ☐ Install **commitizen-action** workflow:
   ```yaml
   name: Commitizen bump
   on:
     push:
       branches: [main]
   jobs:
     bump:
       uses: commitizen-tools/commitizen-action@v2
   ```
3. ☐ Document **agent usage**: `cz commit -m "feat(api): add upload endpoint"`.

---

## 9. GitHub Actions workflows

### 9.1 CI (`ci.yml`)

| Job | Matrix | Key steps |
|-----|--------|-----------|
| **tests** | `python: [3.11,3.12]`, `mode: [minimal,full]` | uv cache → `nox -s tests -- --mode=${{matrix.mode}}` |
| **quality** | `python:3.12` only | `nox -s lint type_check docs_linkcheck` |
| **coverage** | depends on tests | Upload Codecov |

### 9.2 Docs (`docs.yml`)

1. Build with `nox -s docs`.
2. Deploy to GitHub Pages via `peaceiris/actions-gh-pages`.

### 9.3 CodeQL (`codeql.yml`)

- Language: python
- Autobuild: true
- Queries: security‑extended

### 9.4 Release (`release.yml`)

- Trigger: merge of PR authored by `release-please[bot]`.
- Steps: `actions/checkout`, `actions/setup-python`, `uv pip install build`, then `python -m build` and `pypa/gh-action-pypi-publish`.

---

## 10. Nox sessions

```python
PYTHON = ["3.11", "3.12"]
def _install(session, *extras):
    session.install(".", *extras, "-r", "requirements.txt")

@nox.session(python=PYTHON)
def tests(session):
    _install(session, ".[dev]")
    session.run("pytest", "--cov", "--mode", session.posargs or ["minimal"])

@nox.session
def docs(session):
    _install(session, ".[docs]")
    session.run("sphinx-build", "-b", "html", "docs", "docs/_build/html")

@nox.session
def docs_linkcheck(session):
    _install(session, ".[docs]")
    session.run("sphinx-build", "-b", "linkcheck", "docs", "docs/_build/linkcheck")
```

---

## 11. Justfile

```just
# Development shortcuts
test        := "nox -s tests"
lint        := "nox -s lint"
type-check  := "nox -s type_check"
docs        := "nox -s docs"
release     := "gh pr create -f --fill"
```

---

## 12. Optional Conda fallback

- ☐ Document activation: `uv mamba init`.
- ☐ Add note in README.
- ☐ When enabled, confirm that `uv pip install scipy==1.14.dev0` pulls Conda wheel.

---

## 13. Documentation polish

- ☐ Rewrite `docs/index.md` with template badges (`{{ project_slug }}` status‑shields).
- ☐ Add **ADR 0001** explaining design philosophy (Copier + uv + Nox + Just).
- ☐ Ensure Sphinx `conf.py` uses `importlib.metadata.version` with Jinja tag.

---

## 14. Smoke‑test template

1. ☐ Generate project into `/tmp/foo-bar` with defaults.
2. ☐ Run `just test`; ensure all sessions pass.
3. ☐ Simulate PR: `gh repo create tmp/foo-bar --private`, push, open PR, verify:
   - pre-commit-ci auto-fixes
   - CodeQL runs
   - CI matrix green
   - Release‑please **does not** run yet (needs Con‑Commits).

---

## 15. Publish Seedling

- ☐ Create new repo `seedling-template`.
- ☐ Push template content.
- ☐ Tag `v0.1.0`.
- ☐ Add GitHub description: “🌱 Copier template for world‑class Python projects (uv × Nox × Just × Sphinx × pre‑commit‑ci).”

---

*Created 2025‑08‑03 by Iris.*



make a setup for the git repos as a target or docs in readme
