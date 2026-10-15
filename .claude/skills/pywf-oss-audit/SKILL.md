---
name: pywf-oss-audit
description: "Audit a pywf open-source Python library against the template conventions (layout, imports, typing, test mapping, run_cov_test blocks, docs, CI, Python versions) and report each deviation with the skill that fixes it. Changes nothing unless asked. Use when the user asks to check, audit, review, or upgrade a repo to the current template."
---

Compare one repo with the template conventions, and produce a prioritized list of deviations. This is a read-only job: change files only if the user then asks.

Read ../pywf-oss-base/SKILL.md, then every file in ../pywf-oss-base/references/.

## Checks

Run these, and record each finding with its file, the rule broken (reference file and section), and the fixing skill:

1. **Test layout.** Run `python ${CLAUDE_SKILL_DIR}/../pywf-oss-base/scripts/check_test_layout.py --project_root .`. It finds missing, orphan, and mismatched test files, and `all.py` without `is_folder=True`.
2. **Python versions.** Check that `requires-python`, the classifiers, the CI matrix, `USING_COVERAGE`, the mise `python`, and `.readthedocs.yml` agree with `01-toolchain.md` section 2 (floor 3.11, every non-end-of-life version, Windows plus Ubuntu).
3. **Lint.**
   - `uvx ruff check --select F401,F821,F841 <package> tests`
   - `uvx ruff format --check <package> tests`
   - `python ${CLAUDE_SKILL_DIR}/../pywf-oss-base/scripts/check_one_import_per_line.py --paths <package> tests .mise/tasks`
   - Check that `[tool.ruff]` exists in `pyproject.toml`.
4. **Code style**, sampled in about 10 source files and the touched areas:
   - the file header,
   - the five-group import order,
   - no absolute self-imports inside `<package>/`,
   - no `T.Optional` / `T.List` / `T.Union`,
   - `from __future__ import annotations` where annotations exist.
5. **Public API.**
   - `api.py` has one name per line and exports no `_private` names.
   - Every exported name has a docstring.
   - `tests/test_api.py` touches every exported name.
6. **Docs.**
   - Folders follow `NN-Title`.
   - Headings use 78-character underlines.
   - `mise run build-doc` reports no warnings.
   - Notebooks have committed outputs.
7. **Changelog.** The Backlog block is present, and the latest version section matches the `pyproject.toml` version or the last tag.

## Report

Group the findings by the fixing skill: `pywf-oss-write-test`, `pywf-oss-add-module`, `pywf-oss-write-doc`, `pywf-oss-changelog`, or "direct edit" for config and style. Within each group, list the findings in order of severity:

1. breaks CI or the release,
2. breaks a convention that tools rely on,
3. style.

End with counts per group, and ask which group to fix first.
