# CI and Hosting

GitHub Actions runs the tests, codecov.io tracks coverage, and Read the Docs hosts the docs. mise tasks wire up all three for a new repo.

---

## 1. GitHub Actions (`.github/workflows/main.yml`)

- **Matrix**: `ubuntu-latest` and `windows-latest`, times every supported Python version (3.11 and up; see `toolchain.md` section 2). Libraries must pass on both Windows and Ubuntu. That is why code uses `pathlib` and `path_enum`, never hard-coded `/` paths or shell-only commands.
- **Steps**:
  1. checkout,
  2. setup-python,
  3. setup-uv,
  4. restore the cached `.venv` (keyed on OS + Python + `uv.lock`),
  5. `uv sync --extra test`,
  6. `uv run pytest tests --cov=<package> --cov-report=xml`,
  7. upload `coverage.xml` to Codecov for the versions listed in `USING_COVERAGE`.
- CI uses **uv, not mise**: the `[env]` block of `mise.toml` reads local secrets that do not exist on the runner.
- **Triggers** are set in the `on:` block. A template-fresh repo may only have `workflow_dispatch`. Enable `push` / `pull_request` on `main` once the repo is live.
- **Quick debugging**: the workflow keeps commented-out single-OS and single-version lines. Swap them in temporarily, and never commit the narrowed matrix.

---

## 2. Codecov (codecov.io)

- `codecov.yml` holds the report settings. `.coveragerc` holds what is measured (see `testing.md`).
- One-time setup: run `mise run setup-codecov`. It uses `CODECOV_TOKEN` (the Codecov API token) to fetch the repo's upload token, and stores that upload token as the `CODECOV_TOKEN` secret of the GitHub repo.
- If CI fails at "Upload coverage to Codecov", the secret is missing or stale. Rerun the setup task; it is idempotent.

---

## 3. Read the Docs (readthedocs.org)

- `.readthedocs.yml` builds with uv: `uv sync --extra doc` into the Read the Docs virtualenv, then Sphinx with `docs/source/conf.py`.
- Read the Docs builds on every push to `main`. It has no secrets, so notebooks must ship with committed outputs (see `docs-notebook.md`).
- One-time setup:
  - `mise run setup-readthedocs` creates the Read the Docs project. It is idempotent.
  - `mise run update-github-metadata` sets the GitHub repo description (from `pyproject.toml`) and homepage (the docs URL).

---

## 4. Order for a brand-new repo

1. Push the repo to GitHub.
2. `mise run update-github-metadata`
3. `mise run setup-codecov`
4. `mise run setup-readthedocs`
5. Enable the CI triggers, push, and check that CI, Codecov, and the docs are all green.

All of these tasks change external services. Run them only when the user asks.
