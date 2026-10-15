---
description: "The mise tasks, the Python version policy (3.11+ and where each version number lives), uv dependencies and extras, the format and lint tasks (ruff), and python-fire CLIs. Read when setting up or installing the repo, running any task, adding a dependency, changing supported Python versions, or adding a command line interface."
---

# Toolchain

mise runs everything, uv manages packages, ruff lints and formats, and `.venv/` is the only environment. You never call `pip`, and you rarely call `uv` directly.

In every reference file, `<package>` means the import package directory, such as `cookiecutter_pywf_open_source_demo`.

---

## 1. mise: tools, tasks, env vars

`mise.toml` is the single entry point for three things:

- `[tools]`: the dev Python, `uv`, `claude`, `pandoc`. mise installs each version once per machine and shares it across repos.
- `[tasks.*]`: every workflow command. List them with `mise tasks ls`. Each task's `description` says what it does.
- `[env]`: secrets, loaded through `home-secret-toml`. See `08-secrets.md`.

Run a task with `mise run <task>`. Prefer a task over the raw command it wraps, because tasks carry dependencies (for example, `cov` depends on `inst`).

| Task | What it does |
| :--- | :--- |
| `inst` | Create `.venv` and `uv sync --all-extras` |
| `format` / `lint` | ruff format everything / ruff check plus the one-import-per-statement check |
| `cov` | Run the full test suite with coverage, writing `htmlcov/` |
| `test` | Run the full test suite without coverage |
| `build-doc` / `view-doc` | Build Sphinx HTML into `docs/build/html` / open it |
| `notebook-to-markdown` | Convert docs notebooks to Markdown for AI reading |
| `export` | Regenerate `requirements*.txt` from `uv.lock` |
| `build` / `publish` | Build wheel and sdist / upload to PyPI |
| `release` | Create the GitHub tag and release for the current version |
| `setup-codecov` / `setup-readthedocs` / `update-github-metadata` | One-time project setup (see `09-ci-and-hosting.md`) |

`publish`, `release`, and the `setup-*` tasks act on external services. Never run them without the user's explicit go-ahead.

---

## 2. Python versions: four numbers, one rule

| Where | What it means |
| :--- | :--- |
| `pyproject.toml` `requires-python` | The supported range. The floor is **3.11**, and the range covers every CPython version that is not end-of-life. |
| `pyproject.toml` classifiers | One `Programming Language :: Python :: 3.x` per supported version. |
| `.github/workflows/main.yml` `python-version` and `USING_COVERAGE` | Every supported version, tested in CI. |
| `mise.toml` `[tools] python` | The single dev interpreter used to create `.venv`. It must lie inside `requires-python`. |
| `.readthedocs.yml` `build.tools.python` | The interpreter used to build the docs. It must also lie inside the range. |

`.venv` follows `pyproject.toml`: uv creates it from the mise interpreter and resolves against `requires-python`. When you add or drop a Python version, change the range, the classifiers, and the CI matrix together. Check the other two values only if they fall outside the new range.

---

## 3. uv: dependencies

- Dependencies live in `pyproject.toml`: `dependencies` for runtime, and `[project.optional-dependencies]` extras for everything else.
  - `dev`: local tools such as `rich` and `ipykernel`.
  - `test`: `pytest` and `pytest-cov`.
  - `doc`: Sphinx, furo, nbsphinx, docfly, and related packages.
  - `mise`: libraries used by `.mise/tasks/*.py`.
- Every pin is a bounded range with a trailing comment saying why the package is there: `"pytest>=9.0.3,<10.0.0", # Testing framework`.
- To add a dependency, edit `pyproject.toml`, then run `mise run inst`. That updates `uv.lock` and `.venv`. Run `mise run export` afterwards if the `requirements*.txt` files must stay in sync.
- `uv.lock` and `requirements*.txt` are generated files. Never edit them by hand.
- Run Python through the venv: `.venv/bin/python`, `.venv/bin/pytest`.

---

## 4. ruff: format and lint

```bash
mise run format   # uvx ruff format <package> tests .mise/tasks .claude/skills
mise run lint     # uvx ruff check --select F401,F821,F841 on the same paths, plus check_one_import_per_line.py
```

- The configuration lives in `pyproject.toml` under `[tool.ruff]`.
  - Excluded: `<package>/vendor`, and the skill `assets/` (templates with `<package>` placeholders).
  - `__init__.py` and `api.py` may have unused imports, because those imports are the re-exports.
- Run `format`, then `lint`, before you finish any change to Python code.
- The lint set is deliberately small: unused imports, undefined names, unused variables. Style is the formatter's job, and line length is not linted.
- `# fmt: off` / `# fmt: on` keeps hand-written layout: one field per line in declarative models, aligned tables. See `03-code-style.md` section 6.

---

## 5. Command line interface (only if the package has one)

- Use [python-fire](https://github.com/google/python-fire). Put the CLI in `<package>/cli.py`, with a class whose public methods are the subcommands, and a `main()` that calls `fire.Fire(<TheClass>)`.
- Register the console script in `[project.scripts]`, for example `<cli-name> = "<package>.cli:main"`, and add `fire` to `dependencies`.
- Keep `cli.py` thin. It parses arguments and calls functions that live in normal modules, so the logic stays covered by tests. `.coveragerc` omits `cli.py`.
