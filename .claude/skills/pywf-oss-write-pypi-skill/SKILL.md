---
name: pywf-oss-write-pypi-skill
description: "Generate an Agent Skill, named after the package, that documents this library's public API and command line interface, so future sessions in other projects can use the library without re-reading its source. Use when the user asks to turn this library into a Claude skill, usually after a release."
---

Generate an Agent Skill that lets future sessions use this library through its public API, without loading the source.

Read ../pywf-oss-base/SKILL.md, then:
- ../pywf-oss-base/references/08-package-files.md (`api.py` defines the public API; `cli.py` is the python-fire CLI)

## Where to write the output

Default to `~/.claude/skills/<package_name>/` (personal: usable in every project where the library is installed). If the user clearly wants project-only, use `.claude/skills/<package_name>/` instead.

If the target directory already exists, ask the user whether to overwrite before proceeding.

## Step 1: Inspect the project

Read `pyproject.toml` at the working-directory root and extract:

- `[project].name` is `<package_name>`: the import package directory and the skill's name, `/<package_name>`.
- `[project].version`: record it for the skill header.
- `[project.scripts]`: if present, the library exposes a CLI. Note the entry point, for example `cli-name = "<package_name>.cli:main"`, and the executable name (the key on the left).

## Step 2: Walk the public API

The library's stable public surface lives at `<package_name>/api.py`. Read it top to bottom: **each `from ... import X` line is one public symbol**.

For each symbol, find where it actually lives, then:

- **Constant or function:** open its source. Record signature, docstring, and what it returns.
- **Class or dataclass:** also list its non-underscore methods and properties. For each: signature + one-line docstring summary. For dataclasses, list the fields too.
- **Subpackage API** (for example `from .subpackage import api as subpackage`): recurse into that subpackage's `api.py`, and apply the same rules. The user refers to its symbols as `subpackage.ClassName`.

Skip anything starting with `_`: it is internal and out of scope.

Users always import through `api.py`, and never reach into internal modules. Document only these two canonical forms:

```python
from <package_name>.api import X
import <package_name>.api as <package_name>     # then <package_name>.X
```

## Step 3: Pull usage examples from `tests/`

Grep `tests/` for each public symbol. The shortest passing test that exercises a symbol is usually the cleanest example. Extract it for the docs, trimmed to the essentials; never paste whole test files.

## Step 4: Inspect the CLI (only when `[project.scripts]` exists)

Resolve the entry-point module from `[project.scripts]` and read it. Walk the command tree fully: every subcommand, every flag, every default. You'll need all of this for `ref/cli.md`.

## Step 5: Write the skill

Create this layout under the chosen base directory:

```
<base>/<package_name>/
├── SKILL.md
└── ref/
    ├── public-api.md
    └── cli.md          # only if the library has a CLI
```

### SKILL.md: concise overview (always loaded)

Goal: be sufficient for common tasks **without** loading anything under `ref/`. Aim for 50 to 150 lines.

Required sections:

- **Frontmatter `description`:** name the library, state what it does in one sentence, and name the top public symbols. The router uses this to surface the skill on matching queries.
- **One-paragraph purpose:** what the library is for.
- **Import:** the two canonical forms above, nothing else.
- **Public API:** a flat list, one entry per public symbol:
  - Function or method: typed signature and a one-line summary.
  - Dataclass: fields and a one-line summary, then method and property signatures, one per line.
  - Constant: value or type, and a one-line summary.
- **CLI** (only when applicable): one short paragraph: command is typically `.venv/bin/<cli-name>`; run `<cli-name> -h` to discover subcommands; full args live in `ref/cli.md`. **Do not enumerate subcommands here.** Keep this section small: CLI use is infrequent, so its details load lazily.
- **More detail:** pointers: "For full API docs see `ref/public-api.md`. For full CLI args see `ref/cli.md`."

### `ref/public-api.md`: full API reference (loaded on demand)

Audience: an engineer **using** the library, not maintaining it.

For each public symbol:

- Full typed signature.
- Parameter and return semantics. State the *what*; state the *why* only when non-obvious (invariants, gotchas, design constraints the user must respect). Don't lecture on internals.
- A short usage example, preferably lifted (and trimmed) from `tests/`.

Skip line-by-line walkthroughs of internal code; the reader has the source.

### `ref/cli.md`: full CLI reference (loaded on demand)

Audience needs to use the CLI **without** running `--help`. This file loads when the user mentions the CLI, so it must be complete:

- For each subcommand: short description, every flag with type and default, one short example.
- A small table per subcommand reads well.

Stay terse: complete is not the same as verbose.

## Conciseness discipline

Every line in `SKILL.md` stays in the conversation once invoked, so it is a recurring token cost. Prefer signatures, tables, and short examples over prose. The same discipline applies (less strictly) to `ref/*` since they are lazy-loaded.

## Verify before finishing

Sanity-check that documented symbols actually exist. For 2–3 representative symbols, run:

```bash
.venv/bin/python -c "from <package_name>.api import ClassName"
```

If any import fails, the public API docs are wrong. Fix them before reporting done.
