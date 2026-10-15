---
name: pywf-oss-write-test
description: "Write, extend, or fix the unit tests for a module of a pywf open-source Python library, following the source-to-test mapping and run_cov_test conventions, until that module is fully covered. Use when the user asks to add tests, raise coverage, or fix failing tests for a module or subpackage."
---

Write the tests for one module (or every module of one subpackage), so that its own test file reports full coverage and `mise run cov` passes.

Read ../pywf-oss-base/SKILL.md, then:
- ../pywf-oss-base/references/testing.md
- ../pywf-oss-base/references/code-style.md

## Steps

1. **Locate.** Read the source module. Get its test path from `python ${CLAUDE_SKILL_DIR}/../pywf-oss-base/scripts/check_test_layout.py --project_root . --source <file>`. If the test file is missing, create it from the template in `testing.md`. Do not invent another location.
2. **Baseline.** Run `.venv/bin/python tests/<...>/test_<...>.py` and note the missing lines in the `term-missing` report.
3. **Write the tests.**
   - Import the subject under test at the top of the file.
   - Use one `test_<name>` per behavior, or `class Test<Class>` for a class.
   - Use `pytest.mark.parametrize` for data variants, and `tmp_path` or `path_enum` for files.
   - Target behavior and edge cases, not lines. Coverage is the check, not the goal.
4. **Close the gaps.** Rerun until the module is at 100%. A line that truly cannot run in unit tests gets `# pragma: no cover` with a reason that is clear from context. Never add the pragma just to hide untested logic, and never change the source only to make it easier to cover without telling the user.
5. **Finish.**
   - Run `mise run cov`; the whole suite must pass.
   - Run the layout check with no `--source`; it must report 0 problems.
   - Run `uvx ruff format` and `uvx ruff check --select F401,F821,F841` on the touched files.

## Boundaries

- If a test reveals a bug in the source, stop and report it, with the failing test as evidence. Fix it only if the user agrees, or if the user asked for fixes.
- Do not edit `run_cov_test` blocks except to correct the module path. Keep one argument per line.
