---
description: "The dependency upgrade process: finding outdated and unmaintained packages with uv and PyPI, judging each upgrade (breaking changes, requirements, gains, maintenance health), which packages must move together, applying the change, and the regression checks across tests, lint, docs and CI that prove it worked. Read when upgrading or replacing any dependency, or when asked whether a new version is worth it."
---

# Dependency Upgrades

How constraints are written is in `05-uv-dependencies.md`. This file is about changing them.

---

## 1. Find what is outdated

```bash
uv tree --outdated --depth 1
```

This lists each direct dependency with its locked version and, when a newer one exists, `(latest: vX)`. The "latest" it shows already respects `requires-python`.

**Unmaintained packages do not show up here.** Every few upgrades, also check the last release date of each direct dependency on PyPI (`https://pypi.org/pypi/<dist_name>/json`). A package with no release in about two years, whose maintainers point to a successor, should be replaced by that successor.

---

## 2. Judge each upgrade

For each outdated package, read its changelog from the locked version to the latest, and answer four questions:

1. **Breaking changes that touch this repo.** Check them against how the repo actually uses the package: its config, its command-line flags, the APIs the repo imports.
2. **Requirements.** The package's Python floor, and the minimum versions of shared dependencies (a theme needs a given Sphinx; a pytest plugin needs a given pytest).
3. **Gains.** Security fixes, bug fixes that affect this repo, features worth adopting.
4. **Maintenance health.** Last release, last commit, whether issues get answered.

**The verdict is one of:**

- **upgrade**, with the new constraint;
- **hold**, with the reason;
- **replace**, with the successor.

**Research for more than two packages:** delegate the changelog reading to a subagent, and require a cited source for every version number and every breaking change. Spot-check the versions against PyPI yourself.

**Packages that must move together:**

- Sphinx with its theme and extensions (furo, sphinx-design, nbsphinx, sphinx-jinja, docfly);
- pytest with pytest-cov.

---

## 3. Apply

1. Edit the constraints in `pyproject.toml`, following `05-uv-dependencies.md`.
2. Run `uv lock --upgrade-package <dist_name>` for each package (or `uv lock --upgrade` for everything), then `mise run inst`.
3. Run `mise run export`, to refresh the `requirements*.txt` files.
4. If a package was renamed or replaced, update every import and every mention: `.mise/tasks/*.py`, `mise.toml` task descriptions, the docs, and the skill references.

---

## 4. Regression checks

| Area | Check |
| :--- | :--- |
| Tests | `mise run cov` passes, with no new deprecation warnings. Also run one test file directly, to prove that `run_cov_test` still works (`10-test-layout.md`). |
| Code | `mise run lint` |
| Docs build | `mise run build-doc` shows no new warnings, and the cross-reference check reports 0 unresolved (`13-sphinx.md`). |
| Docs look | The sample pages in `docs/source/` (reStructuredText, notebook, sphinx-design gallery) render correctly: tabs switch, dropdowns open, the jinja table is filled, notebook raw cells render. Use the visual check from `13-sphinx.md`. For a theme upgrade, also check both light and dark mode (`15-furo.md`). |
| CI | After pushing, the whole matrix passes, and Codecov receives the report (`18-github-actions.md`, `19-codecov.md`). |

The changelog entry for an upgrade follows the category table in `21-versioning-and-changelog.md`.
