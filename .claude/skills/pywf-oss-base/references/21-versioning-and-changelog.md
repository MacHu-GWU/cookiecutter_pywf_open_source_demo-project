---
description: "Semantic versioning rules tied to api.py, where the version lives, and the release-history.rst changelog: its format, the untouchable Backlog section, the category order with a table of which change goes where, and plain-text entries. Read when deciding a version number, or when writing or reviewing release notes."
---

# Versioning and Changelog

---

## 1. Version

- **Semantic versioning,** `MAJOR.MINOR.PATCH`, judged against the public API in `api.py` (`08-package-files.md`):
  - a breaking change to the public API: MAJOR;
  - a new public name or behavior: MINOR;
  - a bug fix or an internal change: PATCH.
- The version lives only in `pyproject.toml` `[project].version` (`08-package-files.md` section 6). After bumping it, run `mise run inst`, so `uv.lock` records the new version. A version bump therefore changes exactly `pyproject.toml` and `uv.lock`.
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

- Add ``ClassName.method_name()`` to do one new thing.

**Bugfixes**

- Fix ``func_name()`` ignoring the ``encoding`` argument on Windows.
```

- **`x.y.z (Backlog)` is the maintainer's planning area.** An AI never edits it, and never copies or moves its content.
- **New versions go directly below the Backlog block,** newest first, as `VERSION (YYYY-MM-DD)` with a 78-character `~` underline.
- **Category order:** **Breaking Changes**, **Features and Improvements**, **Minor Improvements**, **Bugfixes**, **Miscellaneous**. Omit any category that has no entries.
- **Entries are user-facing:** what changed and why it matters. They are based on git history, not on guesses.
- **Entries are plain text.** Name code with inline literals (``` ``ClassName.method_name()`` ```), never with Sphinx cross-reference roles: the changelog outlives the API it describes, and a role that points at a removed or renamed name breaks in every later build.

**Which category:**

| Change | Category |
| :--- | :--- |
| Removed or renamed public name; raised Python floor (a Python reached end of life); new runtime dependency that users must accept | Breaking Changes |
| New public name or capability | Features and Improvements |
| Better behavior of an existing feature; newly supported Python version; runtime dependency floor raised or cap changed (Breaking Changes instead if users must change their code) | Minor Improvements |
| Fixed wrong behavior | Bugfixes |
| Docs, CI, tooling, dev and test dependency upgrades | Miscellaneous |
