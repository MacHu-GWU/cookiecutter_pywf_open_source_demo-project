---
description: "How the pywf-oss skills themselves are written and maintained: the base and invoker split, reference numbering and the backward-only citation rule, one concern per file, the frontmatter and heading format, generic placeholders instead of project-specific examples, script conventions, and the checks to run after any change. Read before adding, splitting, renaming, or editing any pywf-oss skill, reference, script, or asset."
---

# Authoring the pywf-oss Skills

---

## 1. The family

- **`pywf-oss-base`** holds knowledge only: `references/`, `scripts/`, and `assets/`. It is not bound to any one action. It can be loaded on its own to answer a question about a convention, or to pick the right invoker.
- **Each invoker `pywf-oss-<action>`** does one job. Its body says "Read ../pywf-oss-base/SKILL.md, then:" and lists the base files it needs. After that comes only what is its own: the steps, what it asks the user, when it stops for the user's yes, and what it reports.
- **A shared fact lives in exactly one reference.** Invokers point to it and never restate it. If an invoker needs a fact to be different, change the reference.
- **Every skill is an ordinary, model-invocable skill.** None of them sets `disable-model-invocation`. A skill that changes an external service protects it by asking for the user's yes before each such step, not by blocking invocation.

---

## 2. Reference files

- **Name** each file `NN-slug.md`: two digits, then a kebab-case slug.
- **Order** follows the project lifecycle. Authoring (00) comes first, then secrets and the machine, the toolchain, layout and code, tests, docs, CI and hosting, release, maintenance, and last the skill workflow.
- **Cite backward only.** A reference may cite lower-numbered references. It does not cite a higher-numbered one. When a reference needs something from later in the lifecycle, either move that fact down into the earlier file, or state it as a plain fact without a citation. SKILL.md files may cite any reference.
- **One concern per file.** Split a file when two of its parts can change independently:
  - different tools in the same area: Sphinx, its theme, and each extension get their own file;
  - structure and style: where tests live, versus how tests are written.
  A topic that a job needs only sometimes gets its own file, so an invoker can load it on demand.
- **Shape:**
  - YAML frontmatter with only `description`,
  - then one H1,
  - then numbered H2 sections separated by `---`.
- **`description`** is one double-quoted string in two parts: first what the file contains, then "Read when ...". It contains no double quotes. `scripts/update_skill_index.py` copies it into the base SKILL.md index.
- **Citations** look like `` `NN-slug.md` ``, optionally followed by "section N". Prefer citing the whole file; section numbers move.

---

## 3. Generic content

- Write in English.
- **Use placeholders, never a real project's names.** The skills must work when copied into any repo.

  | Placeholder | Meaning |
  | :--- | :--- |
  | `<package_name>` | The import package directory. It is always snake_case and equals `[project].name` in `pyproject.toml`. |
  | `<owner>`, `<repo>` | GitHub owner and repository name. Repositories are named `<package_name>-project`. |
  | `module_name`, `subpackage`, `ClassName`, `method_name`, `func_name`, `CONSTANT_NAME`, `attr_name` | Code names in examples |
  | `third_party_lib`, `sibling_lib` | An ordinary third-party distribution, and a close-relative distribution |

- Name the tools of the template stack (mise, uv, ruff, pytest, pytest-cov, Sphinx, furo, docfly, nbsphinx, sphinx-design, sphinx-jinja, home-secret-toml, GitHub Actions, Codecov, Read the Docs). They are the conventions themselves.
- Name any other library only when a rule is about it, as in "one field per line in pydantic models".
- When a rule needs a working demonstration, point to the sample docs pages in `docs/source/` of a template repo. Do not copy a project's code into the reference.
- **Approval wording:** "the user's yes", and "one yes covers one step".

---

## 4. Scripts and assets

- Every script under `scripts/` is a stdlib-only command line tool:
  - a `_main()` that holds the logic, and a `main(argv)` that only parses arguments;
  - `--arg_name` flags only, no positional arguments;
  - exit code 0 for success, 1 for a failure found, 2 for a usage error.
- **File header:** `#!/usr/bin/env python3` on line 1, then `# -*- coding: utf-8 -*-` on line 2.
- **How to call a script:**
  - from the base skill: `python ${CLAUDE_SKILL_DIR}/scripts/<name>.py`;
  - from an invoker: `python ${CLAUDE_SKILL_DIR}/../pywf-oss-base/scripts/<name>.py`;
  - from a mise task: by its repo path, `python3 .claude/skills/pywf-oss-base/scripts/<name>.py`.
- `assets/` holds templates with placeholders. They are not valid Python, so ruff excludes them.

---

## 5. After any change to the family

1. Run `python ${CLAUDE_SKILL_DIR}/scripts/update_skill_index.py`. It regenerates the references index in SKILL.md.
2. Keep three places in agreement:
   - the "Which skill to use" table in the base SKILL.md, especially its "Reads from this base" column;
   - each invoker's "Read" list;
   - the handoff table in the skill-family workflow reference.
   For a new or renamed skill, also update the skills table in `CLAUDE.md`.
3. Run `python ${CLAUDE_SKILL_DIR}/scripts/check_skill_family.py --skills_dir .claude/skills`, adding `--forbid <name>` for each project name that must not appear (for example, the demo package of the seed repo). It checks that:
   - every skill's frontmatter is well formed;
   - every `../pywf-oss-base/...` path resolves;
   - every cited reference exists;
   - no reference cites a later one;
   - no forbidden name appears.
4. Run `mise run lint`.
