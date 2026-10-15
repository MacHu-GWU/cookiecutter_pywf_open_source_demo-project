---
description: "How dependency versions are constrained in pyproject.toml, how to find outdated packages with uv, how to judge whether an upgrade is worth it, and the regression checks (tests, lint, docs build, cross-reference scan) that prove it worked. Read when upgrading any dependency, replacing an unmaintained package, or reviewing version constraints."
---

# Dependency Upgrades

---

## 1. Constraint policy

| Kind | Form | Example |
| :--- | :--- | :--- |
| Normal dependency | `>=<tested floor>,<<next major>` | `"pytest>=9.0.3,<10.0.0"` |
| Pre-1.0 package (minor = breaking) | `>=0.Y.Z,<1.0.0`, or `<0.(Y+1).0` when its minors break | `"nbsphinx>=0.9.8,<1.0.0"` |
| Visual theme (any release changes the look) | exact pin | `"furo==2025.12.19"` |
| Needs a fix or security patch | raise the floor to the fixed version | `"pytest>=9.0.3"` (CVE fix) |

- Every line keeps a trailing comment saying why the package is there.
- **Every dependency, including the extras, must support every Python version in `requires-python`.** When the newest release drops the floor version (for example, Sphinx 9.1 needs Python 3.12 or later while the floor is 3.11), cap the constraint below it, and record the reason in the comment.
- The floor is a version that was actually tested, normally the version in `uv.lock` after the upgrade.

---

## 2. Find what is outdated

```bash
uv tree --outdated --depth 1
```

This lists each direct dependency with its locked version and, if newer, `(latest: vX)`. The "latest" it shows already respects `requires-python`.

Unmaintained packages do not show up here. Every few upgrades, also check the last release date of each direct dependency on PyPI (`https://pypi.org/pypi/<name>/json`). A package with no release in about two years, whose maintainers point to a successor, should be replaced: for example, `httpx` was replaced by `httpx2`, which the pydantic team maintains.

---

## 3. Judge each upgrade

For each outdated package, read its changelog from the locked version to the latest, and answer these questions:

1. **Breaking changes that touch this repo.** Check them against how the repo actually uses the package: config, command-line flags, the APIs it imports.
2. **Requirements.** Python floor, and the minimum versions of shared dependencies (for example, furo needs a given Sphinx, and pytest-cov needs a given coverage).
3. **Gains.** Security fixes, bug fixes that affect this repo, and features worth adopting.
4. **Maintenance health.** Last release date, last commit date, whether issues get answered.

The verdict is one of: **upgrade** (with the new constraint), **hold** (and why), or **replace** (and with what). For a large batch, delegate the changelog research to a subagent. Ask for a cited source on every version number and breaking change, then spot-check the versions against PyPI yourself.

Upgrade coupled packages together: Sphinx with furo, sphinx-design, and nbsphinx; pytest with pytest-cov.

---

## 4. Apply

1. Edit the constraints in `pyproject.toml`.
2. `uv lock --upgrade-package <name>` for each package (or `uv lock --upgrade` for everything), then `mise run inst`.
3. `mise run export` to refresh the `requirements*.txt` files.
4. If a package was renamed or replaced, update every import and every mention: `.mise/tasks/*.py`, `mise.toml` task descriptions, the docs, and the skill references.

---

## 5. Regression checks

| Area | Check |
| :--- | :--- |
| Tests | `mise run cov` passes with no new deprecation warnings. Also run one test file directly (`.venv/bin/python tests/test_api.py`), to prove that `run_cov_test` still works. |
| Code | `mise run lint` |
| Docs build | `mise run build-doc` shows no new warnings |
| Docs links | `python ${CLAUDE_SKILL_DIR}/../pywf-oss-base/scripts/check_doc_xrefs.py --html_dir docs/build/html` reports 0 unresolved cross-references. Sphinx itself is silent about these. |
| Docs widgets | The three sample pages (`01` reST, `02` notebook, `03` sphinx-design gallery) render correctly: tabs switch, dropdowns open, the jinja table is filled, and notebook raw cells render. Check dark mode for theme upgrades. |
| CI | After pushing, the whole matrix (Ubuntu and Windows, every Python version) passes, and Codecov receives the report (see `09-ci-and-hosting.md`). |

Record the upgrade under **Miscellaneous** in `release-history.rst` (see `10-release.md`). Note a dependency change that affects users (a runtime dependency, or a new Python floor) under **Breaking Changes** or **Minor Improvements**.
