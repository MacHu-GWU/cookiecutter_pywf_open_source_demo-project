---
name: pywf-oss-setup-machine
description: "Walk the maintainer through setting up a Mac for pywf open-source Python libraries: global mise, uv and gh, shell activation, the home_secret.toml key paths, and the GitHub, Codecov, Read the Docs and PyPI tokens, then verify without printing any secret. Use when the user sets up a new machine, asks how the environment works, rotates a token, or a task fails because a tool or token is missing."
---

Get a machine from nothing to "every template repo runs `mise run inst`, and every setup task finds its token". Do it as a guided runbook: check, report, and let the user do every step that touches a secret.

Read ../pywf-oss-base/SKILL.md, then:
- ../pywf-oss-base/references/01-secrets.md
- ../pywf-oss-base/references/02-machine-setup.md

## Steps

1. **Check the tools.**
   - Run `mise --version`, `uv --version`, and `gh auth status`.
   - Check that `~/.zshrc` contains `mise activate`.
   - Report what is present and what is missing, in a short table.
2. **Install what is missing.** Show the `brew install ...` lines, and run them after the user's yes. `gh auth login` is interactive; run it only if the user asks.
3. **Secrets file.**
   - Check only that the file exists, and its permissions: `ls -l ~/home_secret.toml`. Never read its content.
   - If it is missing, list the key paths that `mise.toml` `[env]` uses (read them from `mise.toml`), say what each value is for, and show the `chmod 600` line.
4. **Tokens.** For each token, give the creation URL and the exact scopes. The user creates each token and writes it into the file. Never ask for a token in the chat.
5. **Verify.**
   - In a template repo, run `mise trust` if needed, then `mise run inst`.
   - Run the True/False check.
   - Report each variable as present or missing. For a missing one, name its key path from `mise.toml`.

## Boundaries

- Account-level settings, such as connecting GitHub in Read the Docs, are done by the user in the browser. Give the link and say what to click.

Next step for a new repo: `pywf-oss-setup-repo`.
