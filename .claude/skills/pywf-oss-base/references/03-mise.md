---
description: "mise as the single entry point of a repo: the [tools], [tasks] and [env] blocks of mise.toml, the full task list and what each task runs, and which tasks change external services and need the user's yes. Read before running any project command, or when adding or changing a mise task."
---

# mise

mise runs everything in a repo. Prefer a mise task over the raw command it wraps, because tasks carry their dependencies: for example, `cov` runs `inst` first.

---

## 1. `mise.toml`

| Block | What it holds |
| :--- | :--- |
| `[tools]` | The dev Python, `uv`, `claude`, and `pandoc`. mise installs each version once per machine and shares it across repos. |
| `[tasks.*]` | Every workflow command. List them with `mise tasks ls`. Each task's `description` says what it does. Longer tasks are Python scripts in `.mise/tasks/`. |
| `[env]` | Secrets, loaded as described in `01-secrets.md`. |

Run a task with `mise run <task>`.

---

## 2. Tasks

| Task | What it does |
| :--- | :--- |
| `venv-create` / `venv-remove` | Create / delete `.venv` |
| `inst` | Create `.venv`, then `uv sync --all-extras` |
| `format` / `lint` | Format all Python code with ruff / check it with ruff and the one-import-per-statement check |
| `test` / `cov` | Run the test suite / run it with coverage, writing `htmlcov/` |
| `view-cov` | Open the coverage report |
| `build-doc` / `view-doc` | Build the Sphinx HTML into `docs/build/html` / open it |
| `notebook-to-markdown` | Convert the docs notebooks to Markdown, for AI reading |
| `export` | Regenerate `requirements*.txt` from `uv.lock` |
| `build` / `publish` | Build the wheel and sdist / upload them to PyPI |
| `release` | Create the GitHub tag and release for the current version |
| `update-github-metadata` / `setup-codecov` / `setup-readthedocs` | One-time setup of a new repo's GitHub, Codecov, and Read the Docs |

---

## 3. Tasks that change external services

`publish`, `release`, `update-github-metadata`, `setup-codecov`, and `setup-readthedocs` act on GitHub, PyPI, Codecov, or Read the Docs. Run each one only after the user's yes. One yes covers one task. Never run one as a side effect of another job.
