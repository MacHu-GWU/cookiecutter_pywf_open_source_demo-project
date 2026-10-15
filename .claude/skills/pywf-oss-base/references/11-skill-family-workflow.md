---
description: "The pywf-oss skills, what each one does, the typical flows that chain them, and the handoffs between them. Read when choosing which pywf-oss skill fits a job, or when one skill finishes and the next step is unclear."
---

# Family Workflow

How the `pywf-oss-*` skills fit together, and what each one hands to the next.

---

## 1. Skills

| Skill | Job | Hands off to |
| :--- | :--- | :--- |
| `pywf-oss-add-module` | Create a module or subpackage, with its test file, its `all.py`, and its `api.py` export | `pywf-oss-write-test` once the code exists |
| `pywf-oss-write-test` | Write or fix the tests for an existing module, and reach full coverage on it | `pywf-oss-write-doc` if the feature is user-facing |
| `pywf-oss-write-doc` | Write or update an `.rst` or `.ipynb` docs page | `pywf-oss-changelog` |
| `pywf-oss-changelog` | Write the target version's section of `release-history.rst` from git history | `pywf-oss-release` |
| `pywf-oss-release` | Bump the version, verify, then publish and tag, with the user's approval at each public step | `pywf-oss-write-pypi-skill` (optional) |
| `pywf-oss-write-pypi-skill` | Generate an Agent Skill that documents this library's public API and CLI | — |
| `pywf-oss-audit` | Check a repo against these conventions, and report what to fix and which skill fixes it | any of the above |

---

## 2. Typical flows

**New feature**

`add-module` → write the code → `write-test` → `write-doc` → `changelog` → `release`

**Bug fix**

Fix the code → `write-test` (add the regression test) → `changelog` → `release`

**Bring an older repo up to the current template**

`audit` → apply its findings, grouped by the skill that fixes each one → `audit` again until it is clean.

---

## 3. Handoffs

- After `add-module`, the module file exists with a docstring and the test file exists with a `run_cov_test` block, so `write-test` only fills in test functions.
- `write-test` is done when `.venv/bin/python tests/<...>/test_<...>.py` shows 100% for that module (or every missing line has a justified `# pragma: no cover`) and `mise run cov` passes.
- `changelog` reads `git log <last-tag>..HEAD`, so commit the code before running it.
- `release` refuses to publish if the changelog has no section for the `pyproject.toml` version.
