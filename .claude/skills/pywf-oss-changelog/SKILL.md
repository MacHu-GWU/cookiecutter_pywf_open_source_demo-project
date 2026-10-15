---
name: pywf-oss-changelog
description: "Write or correct the section for the upcoming version in release-history.rst of a pywf open-source Python library, based on git history since the last tag. Use when the user wants to prepare release notes, update the changelog, record a change such as a dependency upgrade, or is about to publish or tag a new version."
---

Keep the target version's section of `release-history.rst` accurate and complete, based on git history. Never touch the `x.y.z (Backlog)` section.

Read ../pywf-oss-base/SKILL.md, then:
- ../pywf-oss-base/references/21-versioning-and-changelog.md

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

- These outputs are the ground truth.
- Pay special attention to the `api.py` diff: added names are features; removed or renamed names are breaking changes.
- Changes to `pyproject.toml` dependencies are classified with the category table in the reference.

## Step 3: Read the current file

Run `head -100 release-history.rst`, to see the exact formatting this repo uses. Read the Backlog content as reference only, to understand what the maintainer plans.

## Step 4: Write

- **The section exists:** compare it with git history. Add what is missing, remove what git does not support, and sharpen vague entries.
- **The section is missing:** insert `VERSION (YYYY-MM-DD)`, with today's date, directly below the Backlog block. Use the format and category order from the reference, and omit empty categories.

Edit the file directly. It is tracked by git, so it needs no confirmation.

Next step: `pywf-oss-release`.
