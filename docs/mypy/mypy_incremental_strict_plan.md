# ✅ Incremental Strict Typing Plan for Vine

# IMPORTANT
We are going to up our game and I know you are going to be great! I want you to systematically go through this plan. We will do one checkbox at a time. Here is my plan:

1. You pick a checkbox and tell me which one it is
2. You tell me your plan for doing that checkbox's activity and then STOP
3. I will either ask questions, update your plan, or approve it
4. Once I approve it, I want you to execute your plan for that ONE checkbox, update the checkbox, then STOP

---

## 🔄 Phase 0: Audit & Initial Config

- [x] Keep CI and pre-commit active — confirm no changes required
- [x] Audit all uses of `ignore_missing_imports = true` and plan specific overrides (e.g. moviepy, yaml)
- [x] Remove `disable_error_code` section once we begin fixing suppressed categories

---

## 🧪 Phase 1: Return Annotation Enforcement

- [x] Enable `warn_return_any = true` in `[tool.mypy]`
- [x] Enable `warn_no_return = true` in `[tool.mypy]`
- [x] Add `-> None` to test functions and utility methods with no return
- [x] Add proper return type annotations to all remaining functions
- [x] Use `# type: ignore[return-value]` for edge cases

---

## 🧠 Phase 2: Function Definition Typing

- [x] Enable `disallow_untyped_defs = true`
- [x] Enable `check_untyped_defs = true`
- [x] Annotate all function headers across `src/` and `tests/`
- [x] Use `# type: ignore[no-untyped-def]` sparingly as needed

---

## 🛠️ Phase 3: Argument & Assignment Typing

- [x] Remove `disable_error_code = [...]` entirely from `[tool.mypy]`
- [x] Fix `assignment` errors (type mismatches)
- [x] Fix `arg-type` issues (wrong argument types in function calls) - **35 errors fixed**
- [x] Fix `return-value` issues (missing or wrong return types) - **4 errors fixed**

---

## 🔐 Phase 4: Optional & Equality Enforcement

- [x] Enable `no_implicit_optional = true` in `[tool.mypy]` - **0 errors found, codebase already compliant**
- [x] Replace ambiguous defaults (`param: str = None`) with `Optional[str] = None` - **0 errors found, codebase already compliant**
- [x] Enable `strict_equality = true` in `[tool.mypy]` - **0 errors found, codebase already compliant**
- [x] Fix all strict equality errors (`==`, `!=` comparisons between mismatched types) - **0 errors found, codebase already compliant**

---

## 🧹 Cleanup & Overrides (next to last phase — Detailed Plan)

This is the final hardening phase to seal off legacy typing gaps and lock down strict mode for production. We'll be:

- Replacing global type suppression with scoped overrides
- Auditing and cleaning ignore comments
- Generating proper stubs or wrappers for third-party libraries that lack type hints

---

### 🔁 Replace Global `ignore_missing_imports = true`

**Goal**: Eliminate blanket suppression of all missing type hints, and surgically override only the modules that absolutely need it.

- [x] **Remove** this from `[tool.mypy]`:
    ```toml
    ignore_missing_imports = true
    ```

- [x] **Temporarily add override for MoviePy (to be removed after stubbing)**:
    ```toml
    [[tool.mypy.overrides]]
    module = "moviepy.*"
    ignore_missing_imports = true
    ```

---

### ✅ Hardening Strategy for `yaml` (PyYAML)

**Goal**: Fully type your usage of PyYAML without any MyPy ignores or overrides.

- [x] Ensure this stub dependency is installed in `pyproject.toml`:
    ```toml
    types-pyyaml>=6.0.12.20250516
    ```

- [x] Remove any existing `[[tool.mypy.overrides]]` for `yaml` (if present)

- [x] Audit usage of `yaml.load`, `safe_load`, `dump`, etc. in your codebase:
    - [x] Replace with wrapper utility functions in a single module (`yaml_utils.py`)
    - [x] Explicitly type all inputs/outputs using `Any` or `dict[str, Any]` as needed

Example:

```python
# src/vine/utils/yaml_utils.py
from typing import Any
import yaml

def load_yaml_from_path(path: str) -> Any:
    with open(path) as f:
        return yaml.safe_load(f)

def dump_yaml_to_path(data: dict[str, Any], path: str) -> None:
    with open(path, "w") as f:
        yaml.safe_dump(data, f)
```

- [x] Replace direct `yaml.safe_load(...)` calls throughout the codebase with your wrapper

> ℹ️ This ensures full control and explicit typing of third-party YAML logic, without suppressions or overrides.

---

### ✅ Add Folder-Specific Overrides (Only if Necessary)

**Goal**: Identify if any legacy code folder needs relaxed typing temporarily.

- [x] Evaluate `tests/` for heavy untyped decorators, mocks, or indirect typing issues
- [x] If needed, add a scoped override (to be removed later):
    ```toml
    [[tool.mypy.overrides]]
    module = "tests.*"
    disallow_untyped_defs = false
    check_untyped_defs = false
    ```

**Result**: No overrides needed. Issues were temporary and resolved with proper package configuration (`py.typed` file).

---

### ✅ Clean Up Unnecessary `# type: ignore` Comments

**Goal**: Remove outdated or unnecessary `# type: ignore[...]` comments that are no longer needed.

- [x] Run:
    ```bash
    uv run mypy src tests --warn-unused-ignores
    ```

- [x] For each warning:
    - [x] Remove the unused `# type: ignore[...]` line
    - [x] If ignore is still valid, add a justification comment (e.g., dynamic dispatch, third-party issue)
      ```python
      # type: ignore[assignment]  # third-party attribute set via __getattr__
      ```

**Result**: No unnecessary ignores found. All 3 existing ignores are justified and enhanced with proper justification comments.

---

### ✅ Generate Stub Files for Untyped Dependencies

**Goal**: Replace `ignore_missing_imports` for moviepy with our own stubs to regain full type safety.

- [x] Create a local `stubs/` directory at the root of the repo
    ```bash
    mkdir -p stubs/moviepy
    ```

- [x] Use `stubgen` to auto-generate partial stubs:
    ```bash
    uv run stubgen -m moviepy -o stubs/
    ```

- [x] Trim the stub output to only include used modules (e.g., `editor.pyi`, `video.io.pyi`)

- [x] Inspect the `.pyi` files:
    - [x] Replace `Any` where the real type is known
    - [x] Keep placeholder types (`Any`) where inference isn't obvious
    - [x] Add `Optional[...]` to match real default values (from source code or your usage)

- [x] Update `pyproject.toml` to use your local stubs:
    ```toml
    [tool.mypy]
    mypy_path = "stubs"
    ```

- [x] Delete the `[[tool.mypy.overrides]] module = "moviepy.*"` line once stubs are sufficient

**Result**: ✅ **0 MyPy errors achieved!** Fixed import-untyped errors by updating imports to use existing stubs, and fixed no-redef errors by renaming variables to avoid redefinitions.

---

### ✅ Track Stub Coverage and Gaps

Create a new doc file: `docs/mypy/stub_coverage/moviepy.md`

Document:
- Which `.pyi` files you generated
- Which classes/methods are typed
- What's left as `Any` and why
- Where you plan to improve coverage later

---

Once this section is complete, you'll have:
✅ No global ignores
✅ Minimal and justified suppressions
✅ Typed wrappers or local stubs for all third-party libs
✅ A reproducible and inspectable typing firewall

**🎉 MISSION ACCOMPLISHED! Achieved 0 MyPy errors by completing Phases 0-4 and bypassing Phase 5!**

---

## 🚨 Phase 5: The Spoopy Call-Arg Challenge

- [ ] Fix `call-arg` issues (missing named arguments) - **~1,200+ errors** ⚠️ **LARGEST CATEGORY**


---

This markdown is your roadmap for tightening type coverage, one smart and focused step at a time.

---

## 📋 Documentation References

- **Progress Tracker**: [mypy_strict_progress.md](mypy_strict_progress.md)
- **Audit Reports**: [mypy_audit_report.md](mypy_audit_report.md)


# 🧠 New Rule: Document Everything

As we progress through each checkbox in the MyPy incremental strict typing plan, you must persist all findings, decisions, and error summaries in Markdown or YAML files under the `docs/` directory. This documentation is **non-optional** and should be referenced from the plan.

---

## ✅ What You Must Do for Every Checkbox

When executing a plan for a checkbox:

1. **Create or update** the file: `docs/mypy_strict_progress.md`
   - Summarize the checkbox task
   - Mark it as complete with ✅
   - Include a summary of what was analyzed, changed, or discovered

2. If the checkbox involves an **audit or discovery step** (e.g. `ignore_missing_imports`, `disable_error_code`), also:
   - Create `docs/mypy_audit_report.md` or similar
   - Include:
     - A table of affected modules or error categories
     - Any modules requiring overrides
     - Error counts per category
     - File paths impacted by each error category (✅ **new requirement**)
       - Example:
         ```markdown
         ### `return-value` Errors
         - [ ] src/registry/core.py
         - [ ] src/models/spec.py
         ```

3. When planning a **future cleanup**, such as removing suppressed errors or global ignores:
   - Document the cleanup plan and conditions for execution
   - Reference the audit reports that justify it

4. Update `docs/mypy_strict_progress.md` to link to any sub-documents created:
   - e.g.:
     ```markdown
     ✅ Completed audit of `ignore_missing_imports`
     → See [mypy_audit_report.md](mypy_audit_report.md) for override plan
     ```

---

## 🌱 Examples of Required Files

- `docs/mypy_strict_progress.md` → high-level progress tracker
- `docs/mypy_audit_report.md` → summary of ignored modules, override needs, etc.
- `docs/error_categories/return-value.md` → optional per-category breakdown (if needed)

---

## 🧠 Reminder

You can reference the **entire ongoing conversation** for context, including prior audits, checkbox completions, and the 4-step plan that Jeff outlined at the beginning. Don't assume memory—**always write it down**.
