---
name: pywf-oss-upgrade-deps
description: "Upgrade, hold, or replace the dependencies of a pywf open-source Python library: list outdated and unmaintained packages, research changelogs and compatibility, update the version constraints and lock file, and prove the upgrade with tests, lint, a docs build, and a cross-reference scan. Use when the user asks to upgrade or update dependencies, asks whether a new version of a package is worth it, or wants to replace an unmaintained package."
---

Bring the dependencies up to date, with each change justified and verified.

Read ../pywf-oss-base/SKILL.md, then:
- ../pywf-oss-base/references/12-dependency-upgrades.md
- ../pywf-oss-base/references/01-toolchain.md (sections 2 and 3: Python versions and extras)

## Steps

1. **Inventory.** Run `uv tree --outdated --depth 1`, and check the last release date of each direct dependency. Show a table with these columns:
   - package,
   - extra,
   - locked version,
   - latest version,
   - last release date.
2. **Research.**
   - For each candidate, judge the upgrade as in `12-dependency-upgrades.md` section 3.
   - For more than two packages, delegate the changelog research to a subagent, and require cited sources.
   - Spot-check every version number against PyPI yourself.
   - Present the verdicts (upgrade / hold / replace) with the exact constraint strings.
3. **Decide.** The user picks which verdicts to apply. If the user asked to "just upgrade everything", apply all the upgrade verdicts, but still report the holds and replacements.
4. **Apply.** Follow section 4: edit the constraints, run `uv lock --upgrade-package`, `mise run inst`, and `mise run export`, and rename imports for replaced packages.
5. **Prove it.** Run every check in section 5:
   - tests,
   - lint,
   - the docs build,
   - `python ${CLAUDE_SKILL_DIR}/../pywf-oss-base/scripts/check_doc_xrefs.py`,
   - and, for doc-stack upgrades, a look at the three sample pages.

   Report each check as pass or fail. A failure goes back to step 2 for that package (hold it, or fix the code).
6. **Record.** Add a changelog line (see section 5). Do not commit unless the user asks.

## Boundaries

- Upgrade coupled packages together (Sphinx with its theme and extensions; pytest with pytest-cov).
- Never raise `requires-python` as a side effect of an upgrade. That is the user's decision; offer it as a separate question.
