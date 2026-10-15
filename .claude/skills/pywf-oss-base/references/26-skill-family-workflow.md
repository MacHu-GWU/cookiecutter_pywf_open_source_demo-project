---
description: "How the pywf-oss invoker skills chain together: who hands off to whom, the typical flows (new machine and repo, feature, bug fix, maintenance, template upgrade), and what each handoff guarantees to the next skill. Read when a skill finishes and the next step is unclear, or when planning a multi-step job."
---

# Skill Family Workflow

What each skill does, and when to use it, is in the "Which skill to use" table of the base `SKILL.md`. This file covers the order in which the skills run.

---

## 1. Handoffs

| Skill | Hands off to |
| :--- | :--- |
| `pywf-oss-setup-machine` | `pywf-oss-setup-repo`, for a new repo |
| `pywf-oss-setup-repo` | `pywf-oss-add-module` to start coding; `pywf-oss-release` for the first version; `pywf-oss-fix-ci` if a service stays red |
| `pywf-oss-add-module` | `pywf-oss-write-test`, once the logic is written |
| `pywf-oss-write-test` | `pywf-oss-write-doc`, if the feature is user-facing; otherwise `pywf-oss-changelog` |
| `pywf-oss-write-doc` | `pywf-oss-changelog` |
| `pywf-oss-changelog` | `pywf-oss-release` |
| `pywf-oss-release` | `pywf-oss-write-pypi-skill` (optional) |
| `pywf-oss-write-pypi-skill` | — |
| `pywf-oss-fix-ci` | `pywf-oss-upgrade-deps`, when the cause is a dependency |
| `pywf-oss-upgrade-deps` | `pywf-oss-changelog`, then `pywf-oss-release` |
| `pywf-oss-add-community-skill` | — |
| `pywf-oss-audit` | any of the above, per finding |

---

## 2. Typical flows

| Flow | Steps |
| :--- | :--- |
| New machine, then new repo | `setup-machine` (once per machine) → `setup-repo` (once per repo) → `release` for the first version |
| New feature | `add-module` → write the logic → `write-test` → `write-doc` → `changelog` → `release` |
| Bug fix | fix the code → `write-test` (add the regression test) → `changelog` → `release` |
| A service is red | `fix-ci` |
| Routine upgrades, every few months or on a security fix | `upgrade-deps` → `changelog` → `release` |
| Yearly Python cycle | `fix-ci` (Python versions) → `upgrade-deps` (caps for the old floor) → `changelog` → `release` |
| A job needs an optional community skill | `add-community-skill` (stage → review → install) |
| Bring an older repo up to the current template | `audit` → apply its findings, grouped by fixing skill → `audit` again until it is clean |

---

## 3. What each handoff guarantees

- **After `add-module`:** the module exists with docstrings, and its test file exists with a `run_cov_test` block. `write-test` only fills in test functions.
- **After `write-test`:** the module's own test file shows 100% (or every uncovered line has a justified pragma), and `mise run cov` passes.
- **Before `changelog`:** the change is committed. `changelog` reads `git log <last_tag>..HEAD`.
- **`release`** checks for a changelog section for the `pyproject.toml` version, and runs the `changelog` steps first if it is missing.
