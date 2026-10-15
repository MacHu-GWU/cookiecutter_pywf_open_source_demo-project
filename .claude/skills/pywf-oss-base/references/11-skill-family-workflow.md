---
description: "The pywf-oss skills, what each one does, the typical flows that chain them, and the handoffs between them. Read when choosing which pywf-oss skill fits a job, or when one skill finishes and the next step is unclear."
---

# Family Workflow

How the `pywf-oss-*` skills fit together, and what each one hands to the next.

---

## 1. Handoffs

What each skill does, and when to use it, is in the "Which skill to use" table of `../SKILL.md`. This table only says who comes next.

| Skill | Hands off to |
| :--- | :--- |
| `pywf-oss-setup-machine` | `pywf-oss-setup-repo` for a new repo |
| `pywf-oss-setup-repo` | `pywf-oss-add-module` to start coding; `pywf-oss-fix-ci` if a service stays red |
| `pywf-oss-add-module` | `pywf-oss-write-test` once the code exists |
| `pywf-oss-write-test` | `pywf-oss-write-doc` if the feature is user-facing |
| `pywf-oss-write-doc` | `pywf-oss-changelog` |
| `pywf-oss-changelog` | `pywf-oss-release` |
| `pywf-oss-release` | `pywf-oss-write-pypi-skill` (optional) |
| `pywf-oss-write-pypi-skill` | — |
| `pywf-oss-fix-ci` | `pywf-oss-upgrade-deps` when the cause is a dependency |
| `pywf-oss-upgrade-deps` | `pywf-oss-changelog`, then `pywf-oss-release` |
| `pywf-oss-audit` | any of the above, per finding |

---

## 2. Typical flows

**New feature**

`add-module` → write the code → `write-test` → `write-doc` → `changelog` → `release`

**Bug fix**

Fix the code → `write-test` (add the regression test) → `changelog` → `release`

**New machine, then new repo**

`setup-machine` (once per machine) → `setup-repo` (once per repo) → `release` for the first version

**Maintenance**

- A service is red: `fix-ci`.
- Every few months, or when a security fix lands: `upgrade-deps` → `changelog` → `release`.
- Each October (new CPython, oldest one reaches end of life): `fix-ci` (Python version changes) → `upgrade-deps` (caps that existed only for the old floor) → `changelog` → `release`.

**Bring an older repo up to the current template**

`audit` → apply its findings, grouped by the skill that fixes each one → `audit` again until it is clean.

---

## 3. Handoffs

- After `add-module`, the module file exists with a docstring and the test file exists with a `run_cov_test` block, so `write-test` only fills in test functions.
- `write-test` is done when `.venv/bin/python tests/<...>/test_<...>.py` shows 100% for that module (or every missing line has a justified `# pragma: no cover`) and `mise run cov` passes.
- `changelog` reads `git log <last-tag>..HEAD`, so commit the code before running it.
- `release` refuses to publish if the changelog has no section for the `pyproject.toml` version.
