---
name: pywf-oss-release
description: "Release a new version of a pywf open-source Python library: bump the version, check the changelog, tests, and docs, then publish to PyPI and create the GitHub release, with the user's approval before each public step. Use when the user asks to release, publish, ship, or cut a new version."
disable-model-invocation: true
---

Take the repo from "code is done" to "version is on PyPI and tagged on GitHub". Stop for approval before every step that cannot be undone.

Read ../pywf-oss-base/SKILL.md, then:
- ../pywf-oss-base/references/10-release.md
- ../pywf-oss-base/references/01-toolchain.md (section 1, mise tasks)
- ../pywf-oss-base/references/09-ci-and-hosting.md
- ../pywf-oss-base/references/08-secrets.md

## Steps

1. **Version.**
   - Show the last tag and the current `pyproject.toml` version.
   - If they are equal, propose a bump (PATCH, MINOR, or MAJOR, with a one-line reason based on the `api.py` diff) and apply it after the user agrees. Bump `_version.py` too if it exists.
2. **Changelog.** Check that `release-history.rst` has a section for the target version. If it is missing or stale, run the `pywf-oss-changelog` steps first.
3. **Checks.**
   - `mise run cov` and `mise run build-doc` must both pass.
   - `git status` must be clean, apart from the version and changelog edits.
   - Report any failure and stop.
4. **Commit and push.** Show the commit message. Commit and push to `main` only on the user's yes.
5. **Publish.** Ask: "Publish `<name>` `<version>` to PyPI?" On yes, run `mise run publish`.
6. **GitHub release.** Ask, then run `mise run release`.
7. **Report.** Give the PyPI URL (printed by `publish`) and the release URL.

## Boundaries

- One approval covers one step. A yes to publish is not a yes to release.
- If a token is missing or rejected, name the variable and stop. Never inspect `home_secret.toml` (see `08-secrets.md`).
- Never delete or move an existing tag or PyPI release. A bad release is fixed with a new PATCH version.
