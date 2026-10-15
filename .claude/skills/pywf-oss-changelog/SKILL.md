---
name: pywf-oss-changelog
description: "Write or correct the section for the upcoming version in release-history.rst of a pywf open-source Python library, based on git history since the last tag. Use when the user wants to prepare release notes, update the changelog, or is about to publish or tag a new version."
---

Keep the target version's section of `release-history.rst` accurate and complete, based on git history. Never touch the `x.y.z (Backlog)` section.

Read ../pywf-oss-base/SKILL.md, then:
- ../pywf-oss-base/references/10-release.md (section 2 has the format and the rules)

## Step 1: Gather state

```bash
git describe --tags --abbrev=0   # last published tag: the baseline
grep '^version' pyproject.toml   # target version: the source of truth
```

## Step 2: Read the changes

```bash
git log {LAST_TAG}..HEAD --oneline
git diff {LAST_TAG}..HEAD --stat
git diff {LAST_TAG}..HEAD -- '*.py'
```

These outputs are the ground truth. Pay special attention to `api.py` diffs: added names are features, and removed or renamed names are breaking changes.

## Step 3: Read the current file

`head -100 release-history.rst`, to see the exact formatting this repo uses. Read the Backlog content as reference only, to understand what the maintainer plans. Never copy it or move it.

## Step 4: Write

- **The section exists**: compare it with git history. Add what is missing, remove what git does not support, and sharpen vague entries.
- **The section is missing**: insert `VERSION (YYYY-MM-DD)` (today's date) directly below the Backlog block, using the format and category order in `10-release.md`. Omit empty categories.

Edit the file directly. It is tracked by git, so no confirmation is needed.

## Rules

- Never touch `x.y.z (Backlog)`: not its header, not its content, not its blank lines.
- Entries are user-facing and concise: what changed and why it matters, not implementation details.
- Name public API with `:class:` / `:func:` / `:meth:` roles, so the entries link into the docs.

When you are done, tell the user the section is ready, and that `pywf-oss-release` is the next step.
