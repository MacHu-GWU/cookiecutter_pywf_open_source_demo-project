# Versioning, Changelog, and Release

---

## 1. Version

- Use semantic versioning: `MAJOR.MINOR.PATCH`.
  - Breaking change to the public API (`api.py`): MAJOR.
  - New public name or behavior: MINOR.
  - Bug fix or internal change: PATCH.
- `pyproject.toml` `[project].version` is the single source of truth. If `<package>/_version.py` exists, its `__version__` must match.
- The last released version is the latest git tag: `git describe --tags --abbrev=0`.

---

## 2. Changelog: `release-history.rst`

The changelog is `release-history.rst` at the repo root, and `docs/source/release-history.rst` includes it. It is reStructuredText (not `CHANGELOG.md`) because it renders in the Sphinx docs, and every other doc in the project is reST.

```rst
.. _release_history:

Release and Version History
==============================================================================


x.y.z (Backlog)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


1.2.0 (2026-10-14)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Add :class:`~<package>.core.S3Path.sync` for one-way folder sync.

**Bugfixes**

- Fix ``read_text`` ignoring ``encoding`` on Windows.
```

Rules:

- `x.y.z (Backlog)` is the maintainer's planning area. AI never edits it.
- New versions go directly under the Backlog block, newest first, as `VERSION (YYYY-MM-DD)` with a 78-character `~` underline.
- The categories are, in order: **Breaking Changes**, **Features and Improvements**, **Minor Improvements**, **Bugfixes**, **Miscellaneous**. Omit any category that has no entries.
- Entries are user-facing: what changed and why it matters. They are based on git history, not guesses. Use `:class:` / `:func:` / `:meth:` roles for public API names.

---

## 3. Release sequence

| Step | Who | Command |
| :--- | :--- | :--- |
| 1. Bump `version` in `pyproject.toml` (and `_version.py`) | AI or user | edit |
| 2. Write the version section in `release-history.rst` | AI (`pywf-oss-changelog`) | edit |
| 3. Full tests and docs build pass | AI | `mise run cov`, `mise run build-doc` |
| 4. Commit and push to `main` | user approves | git |
| 5. Publish to PyPI | **user approves** | `mise run publish` (builds, then `uv publish`) |
| 6. GitHub tag and release | **user approves** | `mise run release` (idempotent) |

Steps 5 and 6 are irreversible and public. Always ask before running them, and never run them as a side effect of another task.
