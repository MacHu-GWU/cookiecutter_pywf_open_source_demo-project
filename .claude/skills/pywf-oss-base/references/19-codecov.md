---
description: "Codecov for a template repo: codecov.yml versus .coveragerc, how the per-repo upload token reaches GitHub through the setup-codecov task, the upload step in CI, and how to fix a failed or wrong upload. Read when setting up coverage reporting for a repo, or when the Codecov upload fails or its numbers look wrong."
---

# Codecov

---

## 1. Configuration

- `codecov.yml` holds the report settings on the Codecov side.
- What gets measured is set by `.coveragerc` (`12-coverage.md`).

---

## 2. Upload token

- `mise run setup-codecov` uses `CODECOV_TOKEN`, the account **API** token (`01-secrets.md`), to fetch the repo's own upload token. It then stores that upload token as the `CODECOV_TOKEN` Actions secret of the GitHub repo.
- The task is idempotent, and it changes an external service, so it runs only after the user's yes (`03-mise.md`).

---

## 3. Upload in CI

The last step of the workflow (`18-github-actions.md`) uploads `coverage.xml` with `codecov/codecov-action`. The report path goes in the `files:` input; the old `file:` input was removed.

---

## 4. Diagnosing

| Symptom | Fix |
| :--- | :--- |
| "Upload coverage to Codecov" fails | The `CODECOV_TOKEN` Actions secret is missing or stale. Check with `gh secret list` (it shows names only), then rerun `mise run setup-codecov`. |
| The upload succeeds, but the numbers look wrong | Compare `.coveragerc` `omit` with the `--cov=<package_name>` target, and check that the step before produced `coverage.xml`. |
