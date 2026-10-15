---
name: pywf-oss-write-test
description: "Write, extend, or fix the unit tests for a module of a pywf open-source Python library, following the source-to-test mapping and run_cov_test conventions, until that module is fully covered. Use when the user asks to add tests, raise coverage, or fix failing tests for a module or subpackage."
---

Write the tests for one module (or every module of one subpackage), so that its own test file reports full coverage and `mise run cov` passes.

Read ../pywf-oss-base/SKILL.md, then:
- ../pywf-oss-base/references/09-code-style.md
- ../pywf-oss-base/references/10-test-layout.md
- ../pywf-oss-base/references/11-test-writing.md
- ../pywf-oss-base/references/12-coverage.md

## Steps

1. **Locate.**
   - Read the source module.
   - Get its test path from `python ${CLAUDE_SKILL_DIR}/../pywf-oss-base/scripts/check_test_layout.py --project_root . --source <file>`.
   - If the test file is missing, create it from the template. Do not invent another location.
2. **Baseline.** Run `.venv/bin/python tests/<...>/test_<...>.py`, and note the missing lines in the `term-missing` report.
3. **Write the tests,** following the test-writing reference.
4. **Close the gaps.**
   - Rerun until the module is at 100%.
   - A line that truly cannot run in unit tests may get `# pragma: no cover`, only under the coverage reference's rules.
   - Never change the source just to make it easier to cover without telling the user.
5. **Finish.**
   - `mise run cov` passes.
   - The layout check with no `--source` reports 0 problems.
   - `mise run format`, then `mise run lint`, reports nothing.

## Boundaries

- If a test reveals a bug in the source, stop and report it, with the failing test as evidence. Fix the source only after the user's yes, or if the user asked for fixes.
- Edit a `run_cov_test` block only to correct its module path. Keep one argument per line.
- Next step: `pywf-oss-write-doc` if the feature is user-facing, otherwise `pywf-oss-changelog`.
