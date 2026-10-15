---
name: pywf-oss-audit
description: "Audit a pywf open-source Python library against the template conventions (layout, imports, typing, test mapping, run_cov_test blocks, docs, CI, Python versions) and report each deviation with the skill that fixes it. Changes nothing unless asked. Use when the user asks to check, audit, review, or upgrade a repo to the current template."
---

Compare one repo with the template conventions, and produce a prioritized list of deviations. This is a read-only job: change files only if the user then asks.

Read ../pywf-oss-base/SKILL.md, then every file in ../pywf-oss-base/references/.

## Checks

Run these, and record each finding with its file, the rule broken (reference file and section), and the fixing skill:

1. **Test layout.** Run `python ${CLAUDE_SKILL_DIR}/../pywf-oss-base/scripts/check_test_layout.py --project_root .`. It finds missing, orphan, and mismatched test files, and `all.py` without `is_folder=True`.
2. **Python versions and dependencies.**
   - Run `uv tree --outdated --depth 1` and list the outdated packages; the fix goes to `pywf-oss-upgrade-deps`.
   - Check that `requires-python`, the classifiers, the CI matrix, `USING_COVERAGE`, the mise `python`, and `.readthedocs.yml` agree with `01-toolchain.md` section 2 (floor 3.11, every non-end-of-life version, Windows plus Ubuntu); the fix goes to `pywf-oss-fix-ci`.
3. **Lint.**
   - Check that `mise.toml` has the `format` and `lint` tasks, and that `[tool.ruff]` exists in `pyproject.toml`. If they are missing, run the commands from `01-toolchain.md` section 4 directly.
   - `mise run lint`: ruff check plus the one-import-per-statement check.
   - `uvx ruff format --check <package> tests .mise/tasks`. This is read-only; do not run `mise run format` during an audit.
   - Declarative models (dataclass, pydantic, SQLAlchemy) keep one field per line inside `# fmt: off` / `# fmt: on`.
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
   - `python ${CLAUDE_SKILL_DIR}/../pywf-oss-base/scripts/check_doc_xrefs.py` reports 0 unresolved cross-references.
   - Notebooks have committed outputs.
7. **Changelog.** The Backlog block is present, and the latest version section matches the `pyproject.toml` version or the last tag.

## Report

Group the findings by the fixing skill: `pywf-oss-write-test`, `pywf-oss-add-module`, `pywf-oss-write-doc`, `pywf-oss-changelog`, `pywf-oss-fix-ci` (Python versions and CI config), `pywf-oss-upgrade-deps` (outdated or unmaintained dependencies), or "direct edit" for config and style. Within each group, list the findings in order of severity:

1. breaks CI or the release,
2. breaks a convention that tools rely on,
3. style.

End with counts per group, and ask which group to fix first.
