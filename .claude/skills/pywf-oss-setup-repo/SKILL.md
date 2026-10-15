---
name: pywf-oss-setup-repo
description: "Take a freshly generated pywf open-source Python library repo live: verify it locally, create and push the GitHub repo, set its metadata, connect Codecov and Read the Docs, enable CI, and confirm all three are green, with the user's approval before each external step. Use when the user has a new repo from the template and wants it on GitHub with CI, coverage, and hosted docs."
disable-model-invocation: true
---

Turn a local repo generated from the template into a live project, with GitHub, CI, Codecov, and Read the Docs all green. Every external step waits for the user's yes.

Read ../pywf-oss-base/SKILL.md, then:
- ../pywf-oss-base/references/09-ci-and-hosting.md (section 4 is the order; section 5 is for when something is red)
- ../pywf-oss-base/references/00-machine-setup.md (section 4, the token check)
- ../pywf-oss-base/references/01-toolchain.md (section 1, the mise tasks)

## Steps

1. **Preflight.**
   - Run the token check. If any token is `False`, stop and hand off to `pywf-oss-setup-machine`.
   - Run `git remote -v`, and read `[project].name` from `pyproject.toml`.
   - Show the GitHub repo URL, the Read the Docs slug, and the docs URL that the tasks will use (`.mise/tasks/utils.py` derives them from these two values). Ask the user to confirm them.
2. **Local green.** Run `mise run inst`, `mise run cov`, `mise run lint`, and `mise run build-doc`. Fix any failure before going online. Template-fresh code should pass as it is.
3. **GitHub.**
   - If no remote repo exists, propose the `gh repo create ... --source . --push` command, and run it on yes.
   - Then run `mise run update-github-metadata` on yes.
4. **Codecov.** Run `mise run setup-codecov` on yes. Confirm the secret with `gh secret list`, which shows names only.
5. **Read the Docs.** Run `mise run setup-readthedocs` on yes.
6. **CI.**
   - Show the change that enables the `push` / `pull_request` triggers in `.github/workflows/main.yml`.
   - Commit and push on yes.
   - Watch the result with `gh run list` and `gh run view`.
7. **Confirm.** Report the CI run, the Codecov project page, and the docs build or URL as green or red. For anything red, follow `09-ci-and-hosting.md` section 5, or hand off to `pywf-oss-fix-ci`.

## Boundaries

- One yes covers one step.
- Never change repo visibility, branch protection, or other repo settings that are not in these steps.
- The first PyPI release is a separate job: `pywf-oss-release`.
