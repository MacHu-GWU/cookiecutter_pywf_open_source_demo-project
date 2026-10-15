---
description: "Semantic versioning rules tied to api.py, where the version lives, and the release-history.rst changelog: its format, the untouchable Backlog section, the category order, and how entries are written. Read when deciding a version number, or when writing or reviewing release notes."
---

# Versioning and Changelog

---

## 1. Version

- **Semantic versioning,** `MAJOR.MINOR.PATCH`, judged against the public API in `api.py` (`08-package-files.md`):
  - a breaking change to the public API: MAJOR;
  - a new public name or behavior: MINOR;
  - a bug fix or an internal change: PATCH.
- `pyproject.toml` `[project].version` is the single source of truth. After bumping it, run `mise run inst`, so `uv.lock` records the new version.
- The last released version is the latest git tag: `git describe --tags --abbrev=0`.

---

## 2. Changelog: `release-history.rst`

The changelog is `release-history.rst` at the repo root, and `docs/source/release-history.rst` includes it. It is reStructuredText, not `CHANGELOG.md`, because it renders in the Sphinx docs, and every other doc in the project is reStructuredText.

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

- Add :meth:`ClassName.method_name <<package_name>.module_name.ClassName.method_name>` to do one new thing.

**Bugfixes**

- Fix :func:`~<package_name>.module_name.func_name` ignoring ``encoding`` on Windows.
```

- **`x.y.z (Backlog)` is the maintainer's planning area.** An AI never edits it, and never copies or moves its content.
- **New versions go directly below the Backlog block,** newest first, as `VERSION (YYYY-MM-DD)` with a 78-character `~` underline.
- **Category order:** **Breaking Changes**, **Features and Improvements**, **Minor Improvements**, **Bugfixes**, **Miscellaneous**. Omit any category that has no entries.
- **Entries are user-facing:** what changed and why it matters. They are based on git history, not on guesses. Name public API with cross-reference roles (`13-sphinx.md`).

**Which category:**

| Change | Category |
| :--- | :--- |
| Removed or renamed public name; raised Python floor; new runtime dependency that users must accept | Breaking Changes |
| New public name or capability | Features and Improvements |
| Better behavior of an existing feature | Minor Improvements |
| Fixed wrong behavior | Bugfixes |
| Docs, CI, tooling, dev and test dependency upgrades | Miscellaneous |
