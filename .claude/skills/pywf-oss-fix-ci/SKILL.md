---
name: pywf-oss-fix-ci
description: "Diagnose and fix a red GitHub Actions run, a failed Codecov upload, or a failed Read the Docs build of a pywf open-source Python library, and add or drop a supported Python version. Use when the user says CI, the tests on GitHub, coverage, Codecov, the docs build, or Read the Docs is failing or shows warnings, or asks to add or drop a Python version."
---

Find out from the logs why a hosted service is red, fix the cause in the repo, and confirm that it is green again. Also handle adding or dropping a Python version.

Read ../pywf-oss-base/SKILL.md, then:
- ../pywf-oss-base/references/04-python-versions.md
- ../pywf-oss-base/references/18-github-actions.md
- ../pywf-oss-base/references/19-codecov.md
- ../pywf-oss-base/references/20-readthedocs.md
- ../pywf-oss-base/references/24-python-release-cycle.md (only for adding or dropping a Python version)

## Steps

1. **Find which service is red, and get the log,** with the commands in the matching reference. Quote the decisive log lines to the user.
2. **Reproduce locally** where possible: `mise run cov` for tests, `mise run build-doc` for docs. If it passes locally, compare the environments:
   - OS and Python version;
   - which extras are installed (`uv sync --extra test` in CI, versus `--all-extras` locally);
   - the working directory.
3. **Fix the cause, not the symptom.**
   - Never skip, xfail, or delete a failing test to turn CI green without the user's yes.
   - Never narrow the matrix permanently to hide a failure.
4. **Verify.**
   - Rerun locally.
   - Then, after the user's yes, push the fix. Or, for an infrastructure flake, run `gh run rerun <id> --failed`.
   - Check the new run with `gh run view`.

## Boundaries

- Reading logs and runs is free. Pushing, rerunning, deleting caches, and rerunning setup tasks each need the user's yes.
- If the cause is a dependency, hand off to `pywf-oss-upgrade-deps`.
