---
name: write-pypi-skill
description: A meta skill that reads the Python library at the current working directory and generates a reusable Agent Skill for it, named after the package, that documents the library's public API and, if present, its command line interface. The user invokes this when they want to turn a local Python library into a Claude skill so future sessions can use the library through its public surface without re-reading the source.
disable-model-invocation: true
---

# Write a pypi-package skill

Generate an Agent Skill that lets future Claude sessions use the local Python library through its public API, without re-loading the source.

## Where to write the output

Default to `~/.claude/skills/<package_name>/` (personal — usable in every project where the library is installed). If the user clearly wants project-only, use `.claude/skills/<package_name>/` instead.

If the target directory already exists, ask the user whether to overwrite before proceeding.

## Step 1 — Inspect the project

Read `pyproject.toml` at the working-directory root and extract:

- `[project].name` → becomes the skill's command name, `/<package_name>`. Use it verbatim (underscores stay underscores).
- `[project].version` → record for the skill header.
- `[project.scripts]` → if present, the library exposes a CLI. Note the entry point, e.g. `mycli = "package.cli:main"`. Remember the CLI executable name (the key on the left).

## Step 2 — Walk the public API

The library's stable public surface lives at `<package_name>/api.py`. Read it top to bottom; **one `from ... import X` per line == one public symbol**.

For each symbol, find where it actually lives, then:

- **Constant / function** — open its source. Record signature, docstring, and what it returns.
- **Class / dataclass** — also list its non-underscore methods and properties. For each: signature + one-line docstring summary. For dataclasses, list the fields too.
- **Sub-api module** (e.g. `import <package>.<sub>.api as <sub>`) — recurse into that subpackage's `api.py` and apply the same rules. Sub-api symbols are referenced as `<sub>.<symbol>` by the user.

Skip anything starting with `_` — that's internal and explicitly out of scope.

Users always import through `api.py`, never reach into internal modules. Document only these two canonical forms:

```python
from <package>.api import X
import <package>.api as <package>     # then <package>.X
```

## Step 3 — Pull usage examples from `tests/`

Grep `tests/` for each public symbol. The shortest passing test that exercises a symbol is usually the cleanest example — extract it for the docs (paraphrase / minimize; don't dump entire test files).

## Step 4 — Inspect the CLI (only when `[project.scripts]` exists)

Resolve the entry-point module from `[project.scripts]` and read it. Walk the command tree fully: every subcommand, every flag, every default. You'll need all of this for `ref/cli.md`.

## Step 5 — Write the skill

Create this layout under the chosen base directory:

```
<base>/<package_name>/
├── SKILL.md
└── ref/
    ├── public-api.md
    └── cli.md          # only if the library has a CLI
```

### SKILL.md — concise overview (always-loaded part)

Goal: be sufficient for common tasks **without** loading anything under `ref/`. Aim for ~50–150 lines.

Required sections:

- **Frontmatter `description`** — name the library, state what it does in one sentence, and name the top public symbols. The router uses this to surface the skill on matching queries.
- **One-paragraph purpose** — what the library is for.
- **Import** — the two canonical forms above. Nothing else.
- **Public API** — flat list, one entry per public symbol:
  - Function / method → typed signature + one-line summary.
  - Dataclass → fields + one-line summary; then method/property signatures, one per line.
  - Constant → value or type + one-line summary.
- **CLI** *(only when applicable)* — one short paragraph: command is typically `.venv/bin/<cli-name>`; run `<cli-name> -h` to discover subcommands; full args live in `ref/cli.md`. **Do not enumerate subcommands here.** Keep this section deliberately small — CLI use is infrequent, so lazy-load.
- **More detail** — pointers: "For full API docs see `ref/public-api.md`. For full CLI args see `ref/cli.md`."

### `ref/public-api.md` — full API reference (lazy-loaded)

Audience: an engineer **using** the library, not maintaining it.

For each public symbol:

- Full typed signature.
- Parameter and return semantics. State the *what*; state the *why* only when non-obvious (invariants, gotchas, design constraints the user must respect). Don't lecture on internals.
- A short usage example, preferably lifted (and trimmed) from `tests/`.

Skip line-by-line walkthroughs of internal code — the reader has the source if they want it.

### `ref/cli.md` — full CLI reference (lazy-loaded)

Audience needs to use the CLI **without** running `--help`. This file loads when the user mentions the CLI, so it must be complete:

- For each subcommand: short description, every flag with type and default, one short example.
- A small table per subcommand reads well.

Stay terse — complete ≠ verbose.

## Conciseness discipline

Every line in `SKILL.md` stays in the conversation once invoked — it is a recurring token cost. Prefer signatures, tables, and short examples over prose. The same discipline applies (less strictly) to `ref/*` since they are lazy-loaded.

## Verify before finishing

Sanity-check that documented symbols actually exist. For 2–3 representative symbols, run:

```bash
uv run python -c "from <package>.api import <symbol>"
```

If any import fails, the public API docs are wrong — fix them before reporting done.
