---
description: "The GitHub Actions workflow and its Windows plus Ubuntu matrix, the Codecov and Read the Docs setup tasks, the setup order for a new repo, how to diagnose failures in CI, coverage upload and docs builds, and how to follow the Python release cycle. Read when wiring up a new repo, when CI, Codecov or Read the Docs is red, or when a Python version is released or reaches end of life."
---

# CI and Hosting

GitHub Actions runs the tests, codecov.io tracks coverage, and Read the Docs hosts the docs. mise tasks wire up all three for a new repo.

---

## 1. GitHub Actions (`.github/workflows/main.yml`)

- **Matrix**: `ubuntu-latest` and `windows-latest`, times every supported Python version (3.11 and up; see `01-toolchain.md` section 2). Libraries must pass on both Windows and Ubuntu. That is why code uses `pathlib` and `path_enum`, never hard-coded `/` paths or shell-only commands.
- **Steps**:
  1. checkout,
  2. setup-python,
  3. setup-uv, with its own cache turned off, because the next step caches the whole `.venv`,
  4. restore the cached `.venv` (keyed on OS + Python + `uv.lock`),
  5. `uv sync --extra test`,
  6. `uv run pytest tests --cov=<package> --cov-report=xml`,
  7. upload `coverage.xml` to Codecov for the versions listed in `USING_COVERAGE`.
- CI uses **uv, not mise**: the `[env]` block of `mise.toml` reads local secrets that do not exist on the runner.
- **Triggers** are set in the `on:` block. A template-fresh repo may only have `workflow_dispatch`. Enable `push` / `pull_request` on `main` once the repo is live.
- **Action versions**: keep every action on its latest major version. Old majors get warnings first (for example, a Node.js runtime deprecation, or removed inputs such as codecov's `file`, now `files`), and later they break. Use the floating major tag (`@v7`) where the action publishes one; setup-uv does not, so pin its full version (`@v10.3.0`). Check the run's Annotations panel after each change.
- **Quick debugging**: the workflow keeps commented-out single-OS and single-version lines. Swap them in temporarily, and never commit the narrowed matrix.

---

## 2. Codecov (codecov.io)

- `codecov.yml` holds the report settings. `.coveragerc` holds what is measured (see `04-testing.md`).
- One-time setup: run `mise run setup-codecov`. It uses `CODECOV_TOKEN` (the Codecov API token) to fetch the repo's upload token, and stores that upload token as the `CODECOV_TOKEN` secret of the GitHub repo.
- If CI fails at "Upload coverage to Codecov", the secret is missing or stale. Rerun the setup task; it is idempotent.

---

## 3. Read the Docs (readthedocs.org)

- `.readthedocs.yml` builds with uv: `uv sync --extra doc` into the Read the Docs virtualenv, then Sphinx with `docs/source/conf.py`.
- Read the Docs builds on every push to `main`. It has no secrets, so notebooks must ship with committed outputs (see `07-docs-notebook.md`).
- One-time setup:
  - `mise run setup-readthedocs` creates the Read the Docs project. It is idempotent.
  - `mise run update-github-metadata` sets the GitHub repo description (from `pyproject.toml`) and homepage (the docs URL).

---

## 4. Order for a brand-new repo

Prerequisite: the machine is set up (`00-machine-setup.md`), and all four tokens check `True`.

1. Make it green locally: `mise run inst`, `mise run cov`, `mise run lint`, and `mise run build-doc`.
2. Create the GitHub repo and push: `gh repo create <owner>/<repo>-project --public --source . --push`. The repo name must match the `git remote` URL that `.mise/tasks/utils.py` reads.
3. `mise run update-github-metadata`
4. `mise run setup-codecov`
5. `mise run setup-readthedocs`
6. Enable the `push` / `pull_request` triggers in `main.yml`, commit, push, and check that CI, Codecov, and the docs are all green (section 5).

All of these steps change external services. Run each one only with the user's go-ahead.

---

## 5. Diagnose a red service

Start from the evidence, never from a guess: read the failing log first.

### GitHub Actions

```bash
gh run list --limit 5                 # recent runs and their status
gh run view <run-id> --log-failed     # only the log lines of the failed steps
gh run rerun <run-id> --failed        # retry only the failed jobs (for flaky infrastructure)
gh workflow run main.yml              # start a run by hand (workflow_dispatch)
```

| Symptom | Usual cause | Fix |
| :--- | :--- | :--- |
| Fails only on `windows-latest` | Hard-coded `/` paths, shell-only commands, file encoding, or a file still open when it is deleted | Use `pathlib` / `path_enum`, `encoding="utf-8"`, and close files (`with`) |
| Fails only on the newest Python | A dependency has no wheel for it yet, or a deprecated stdlib API was removed | Check the dependency's release notes; cap or skip that version until it ships |
| `uv sync` fails | `uv.lock` is out of date with `pyproject.toml` | `uv lock` locally, then commit `uv.lock` |
| Passes locally, fails in CI | It depends on local state: a file in `tmp/`, an env var, the current working directory | Build the state inside the test (`tmp_path`, `path_enum`) |
| A stale `.venv` cache | The cache key is keyed on `uv.lock`, so a change outside the lock does not invalidate it | Delete the cache with `gh cache delete --all`, then rerun |

### Codecov

- "Upload coverage to Codecov" fails: the repo's `CODECOV_TOKEN` Actions secret is missing or stale. Check with `gh secret list` (it shows names only), then rerun `mise run setup-codecov`.
- The upload succeeds but the numbers look wrong: compare `.coveragerc` `omit` with the `--cov=<package>` target, and check that `coverage.xml` was produced in the step before.

### Read the Docs

- Build list and logs: `https://app.readthedocs.org/projects/<slug>/builds/` (`<slug>` is the project name with `_` replaced by `-`).
- Status from the terminal, without printing the token:

  ```bash
  mise exec -- sh -c 'curl -s -H "Authorization: Token $READTHEDOCS_TOKEN" "https://readthedocs.org/api/v3/projects/<slug>/builds/?limit=1"' | python3 -m json.tool
  ```

- Reproduce locally with `mise run build-doc`. Read the Docs uses the Python version in `.readthedocs.yml` and `uv sync --extra doc`, so a package that is missing from the `doc` extra (but present locally through another extra) fails only on Read the Docs.
- A notebook that needs credentials fails on Read the Docs. Commit its outputs and set `nbsphinx_execute = "never"` (see `07-docs-notebook.md`).

---

## 6. Following the Python release cycle

The release schedule is at <https://devguide.python.org/versions/>. A new CPython comes out every October, and the oldest version reaches end of life the same month.

- **New version released:** add it to the CI matrix, to `USING_COVERAGE`, and to the classifiers. Fix what fails. Then raise the `requires-python` cap only if one was set.
- **Version reaches end of life:** remove it from the matrix and the classifiers, and raise the `requires-python` floor. This is a user-visible change, so note it in the changelog under **Breaking Changes**. Then check the dependency caps that existed only because of the old floor (see `12-dependency-upgrades.md` section 1).
- Keep the `mise.toml` dev Python and `.readthedocs.yml` inside the supported range (see `01-toolchain.md` section 2).
