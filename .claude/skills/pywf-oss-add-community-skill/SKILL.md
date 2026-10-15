---
name: pywf-oss-add-community-skill
description: "Install an optional community Agent Skill into this repo's .claude/skills/ from the pinned catalog, after a security review, or add or update a catalog entry from a GitHub link. Use when the user asks which community skills are available, wants to install one, or gives a GitHub link to a skill to catalog or pin."
---

Install a community skill from the catalog, or add or update a catalog entry. Installation is done by a script; this skill picks the entry, reviews the downloaded content, and keeps the catalog correct.

Read ../pywf-oss-base/SKILL.md, then:
- ../pywf-oss-base/references/25-community-skills.md

Catalog: ../pywf-oss-base/assets/community-skills.toml

## Install a skill

1. **Pick.** Run `--list`. Match the user's need against each entry's `when_to_use`, and confirm the choice with the user.
2. **Stage.** Run the script with `--name <skill_name>`, without `--install`.
3. **Review.**
   - Follow the security review in `25-community-skills.md` section 4, on the staged folder.
   - Report what the skill does, its scripts and what each one touches, and anything risky.
4. **Install.** After the user's yes, rerun with `--install`. Report the installed path and its `.source.json`.
5. **Git.** The skill is git-ignored by default. Ask whether it should be committed with the repo; if yes, delete its line from `.gitignore`.

## Add or update a catalog entry

1. From the GitHub link the user gives, find the skill folder and pin it, as in `25-community-skills.md` section 2.
2. Show the new or changed entry, including a proposed `when_to_use`, and save it after the user's yes. For a new entry, also add its `.claude/skills/<skill_name>/` line to the community-skills block of `.gitignore`.
3. Optionally stage it once with the script, to prove that the URL works.

## Boundaries

- Never install a skill that has not been staged and reviewed.
- Never run any of a downloaded skill's scripts during the review.
- Never overwrite an installed skill without the user's yes (`--force`).
