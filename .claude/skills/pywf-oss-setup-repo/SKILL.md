---
name: pywf-oss-setup-repo
description: "Take a freshly generated pywf open-source Python library repo live: verify it locally, create and push the GitHub repo, set its metadata, connect Codecov and Read the Docs, enable CI, and confirm all three are green, asking for the user's yes before each external step. Use when the user has a new repo from the template and wants it on GitHub with CI, coverage, and hosted docs."
---

Turn a local repo generated from the template into a live project, with GitHub, CI, Codecov, and Read the Docs all green. Each external step waits for the user's yes; one yes covers one step.

Read ../pywf-oss-base/SKILL.md, then:
- ../pywf-oss-base/references/01-secrets.md
- ../pywf-oss-base/references/03-mise.md
- ../pywf-oss-base/references/18-github-actions.md
- ../pywf-oss-base/references/19-codecov.md
- ../pywf-oss-base/references/20-readthedocs.md

## Steps

1. **Preflight.**
   - Run the token True/False check. If any token is `False`, stop and hand off to `pywf-oss-setup-machine`.
   - Run `git remote -v`, and read `[project].name` from `pyproject.toml`.
   - Show the GitHub repo URL, the Read the Docs slug, and the docs URL that the tasks will use (`.mise/tasks/utils.py` derives them from these two values), and ask the user to confirm them.
2. **Local green.** Run `mise run inst`, `mise run cov`, `mise run lint`, and `mise run build-doc`. Fix any failure before going online. Template-fresh code should pass as it is.
3. **GitHub repo.** If no remote repo exists, propose `gh repo create <owner>/<repo> --public --source . --push`. The repo name must match the `git remote` URL. Run it after the user's yes.
4. **GitHub metadata.** `mise run update-github-metadata`, after the user's yes.
5. **Codecov.** `mise run setup-codecov`, after the user's yes. Then confirm the secret with `gh secret list`, which shows names only.
6. **Read the Docs.** `mise run setup-readthedocs`, after the user's yes.
7. **CI.**
   - Show the change that enables the `push` and `pull_request` triggers in `.github/workflows/main.yml`.
   - Commit and push it after the user's yes.
   - Watch the run with `gh run list` and `gh run view`.
8. **Confirm.** Report the CI run, the Codecov project, and the docs build as green or red. For anything red, diagnose it as in the matching reference, or hand off to `pywf-oss-fix-ci`.

## Boundaries

- Never change repo visibility, branch protection, or any repo setting not listed in these steps.
- Next steps: `pywf-oss-add-module` to start coding, and `pywf-oss-release` for the first version.
