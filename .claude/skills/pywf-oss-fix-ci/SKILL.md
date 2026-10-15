---
name: pywf-oss-fix-ci
description: "Diagnose and fix a red GitHub Actions run, a failed Codecov upload, or a failed Read the Docs build of a pywf open-source Python library, and update the CI matrix when a Python version is released or reaches end of life. Use when the user says CI, tests on GitHub, coverage, codecov, the docs build, or Read the Docs is failing, or asks to add or drop a Python version."
---

Find out from the logs why a hosted service is red, fix the cause in the repo, and confirm it is green again. Also update the supported Python versions when the release cycle requires it.

Read ../pywf-oss-base/SKILL.md, then:
- ../pywf-oss-base/references/09-ci-and-hosting.md (section 5 for diagnosis, section 6 for Python versions)
- ../pywf-oss-base/references/01-toolchain.md (section 2, where each Python version number lives)
- ../pywf-oss-base/references/12-dependency-upgrades.md (when the cause is a dependency)

## Steps

1. **Identify which service is red, and get the log.**
   - GitHub Actions: `gh run list`, then `gh run view <id> --log-failed`.
   - Codecov: the "Upload coverage" step log, and `gh secret list`.
   - Read the Docs: the builds page, or the API status call in section 5.
   - Quote the decisive lines of the log to the user.
2. **Reproduce locally** when possible: `mise run cov` for tests, `mise run build-doc` for docs. If it passes locally, compare the environments: OS, Python version, extras installed (`uv sync --extra test` vs `--all-extras`), working directory.
3. **Fix the cause, not the symptom.**
   - Use the symptom table in section 5.
   - Never skip, xfail, or delete a failing test to turn CI green without the user's agreement.
   - Never narrow the matrix permanently to hide a failure.
4. **Verify.** Rerun locally. Then, on the user's yes, push the fix, or run `gh run rerun <id> --failed` for infrastructure flakes. Check the new run with `gh run view`.

## Python version changes

When asked to add or drop a Python version, change all the places listed in `09-ci-and-hosting.md` section 6 in one commit, run the full CI matrix, and add a changelog entry (dropping a version is a breaking change).

## Boundaries

- Reading logs and runs is free. Pushing, rerunning, deleting caches (`gh cache delete`), and rerunning setup tasks each need the user's yes.
- If the fix needs a dependency upgrade, hand off to `pywf-oss-upgrade-deps`.
