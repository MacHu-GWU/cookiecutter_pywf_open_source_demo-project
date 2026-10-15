---
description: "The supported Python policy (floor 3.11, every CPython not at end of life) and the five places a Python version number lives. Read when checking or changing where a Python version number is written, or when those numbers disagree."
---

# Python Versions

---

## 1. Policy

- **The floor is 3.11.** Code uses 3.11+ syntax.
- **The supported range is every CPython version not at end of life** (schedule: <https://devguide.python.org/versions/>). A few months' lag either way is fine.

---

## 2. Where each number lives

| Where | What it means |
| :--- | :--- |
| `pyproject.toml` `requires-python` | The supported range, for example `">=3.11,<4.0"` |
| `pyproject.toml` classifiers | One `Programming Language :: Python :: 3.x` per supported version |
| `.github/workflows/main.yml` `python-version` and `USING_COVERAGE` | Every supported version, tested in CI |
| `mise.toml` `[tools] python` | The one dev interpreter that creates `.venv`; must lie inside the range |
| `.readthedocs.yml` `build.tools.python` | The interpreter that builds the docs; must lie inside the range |

uv creates `.venv` from the mise interpreter, and resolves dependencies against `requires-python`.

When the range changes, change `requires-python`, the classifiers, and the CI matrix together, in one commit. Change the other two only if they fall outside the new range.
