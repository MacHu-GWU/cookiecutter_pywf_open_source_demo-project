---
name: pywf-oss-upgrade-deps
description: "Upgrade, hold, or replace the dependencies of a pywf open-source Python library: list outdated and unmaintained packages, research changelogs and compatibility, update the version constraints and lock file, and prove the upgrade with tests, lint, a docs build, and a cross-reference scan. Use when the user asks to upgrade or update dependencies, asks whether a new version of a package is worth it, or wants to replace an unmaintained package."
---

Bring the dependencies up to date, with every change justified and verified.

Read ../pywf-oss-base/SKILL.md, then:
- ../pywf-oss-base/references/04-python-versions.md
- ../pywf-oss-base/references/05-uv-dependencies.md
- ../pywf-oss-base/references/13-sphinx.md (section 2.2 and section 4: the cross-reference check and the visual check)
- ../pywf-oss-base/references/15-furo.md (only for a theme upgrade)
- ../pywf-oss-base/references/23-dependency-upgrades.md

## Steps

1. **Inventory.** Run `uv tree --outdated --depth 1`, and check the last release date of each direct dependency. Show a table with these columns:
   - package,
   - extra,
   - locked version,
   - latest version,
   - last release date.
2. **Research.** Judge each candidate as in `23-dependency-upgrades.md` section 2, including when to delegate the research to a subagent. Present each verdict (upgrade / hold / replace) with the exact constraint string.
3. **Decide.** The user picks which verdicts to apply. If the user said "just upgrade everything", apply every upgrade verdict, and still report the holds and replacements.
4. **Apply,** as in `23-dependency-upgrades.md` section 3.
5. **Prove it.** Run every regression check in `23-dependency-upgrades.md` section 4. Report each one as pass or fail. A failure sends that package back to step 2: hold it, or fix the code.
6. **Commit.** Commit the upgrade after the user's yes, so the changelog can see it in git history.

## Boundaries

- Upgrade the coupled packages listed in `23-dependency-upgrades.md` section 2 together.
- Never raise `requires-python` as a side effect of an upgrade. That is the user's decision; offer it as a separate question.

Next step: `pywf-oss-changelog`, then `pywf-oss-release`.
