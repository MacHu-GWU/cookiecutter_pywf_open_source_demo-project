---
description: "The yearly Python routine: what to change when a new CPython is released, and when the oldest one reaches end of life, across the version locations, the CI matrix, dependency caps, and the changelog. Read when a Python version is released or retired, or when asked to add or drop a supported Python version."
---

# Following the Python Release Cycle

A new CPython is released every October, and the oldest supported one reaches end of life around the same time. The policy and its timing are in `04-python-versions.md`.

---

## 1. A new version is released

1. Add it to the CI matrix and to `USING_COVERAGE` (`18-github-actions.md`), and to the classifiers (`04-python-versions.md`).
2. Run the full CI. If a dependency does not support the new Python yet, do not add that Python to the matrix and the classifiers yet; wait until the dependency ships.
3. Raise the `requires-python` cap, only if one was set.
4. The change is recorded in the changelog by category, as in `21-versioning-and-changelog.md` (a newly supported Python is a Minor Improvement).

---

## 2. A version reaches end of life

1. Remove it from the CI matrix, `USING_COVERAGE`, and the classifiers.
2. Raise the `requires-python` floor.
3. Lift the dependency caps that existed only because of the old floor (`05-uv-dependencies.md` section 2), through the upgrade process in `23-dependency-upgrades.md`.
4. Make sure the `mise.toml` dev Python and `.readthedocs.yml` are still inside the range (`04-python-versions.md`).
5. The change is recorded in the changelog as a Breaking Change (`21-versioning-and-changelog.md`): users on that Python no longer get new releases.
