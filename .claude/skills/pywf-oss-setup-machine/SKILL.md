---
name: pywf-oss-setup-machine
description: "Walk the maintainer through setting up a Mac for pywf open-source Python libraries: global mise and uv, shell activation, the home_secret.toml key paths, and the GitHub, Codecov, Read the Docs and PyPI tokens, then verify without printing any secret. Use when the user sets up a new machine, asks how the environment works, rotates a token, or a mise task fails because a tool or token is missing."
---

Get a machine from nothing to "every template repo runs `mise run inst` and every setup task finds its token". Do this as a guided runbook: check, report, and let the user do the steps that involve secrets.

Read ../pywf-oss-base/SKILL.md, then:
- ../pywf-oss-base/references/00-machine-setup.md
- ../pywf-oss-base/references/08-secrets.md

## Steps

1. **Check the tools.** Run `mise --version`, `uv --version`, `gh auth status`, and check that `~/.zshrc` contains `mise activate`. Report what is present and what is missing, in a short table.
2. **Install what is missing.** Show the `brew install ...` lines from `00-machine-setup.md` section 1, and run them only on the user's yes. Run `gh auth login` yourself only if the user asks; it is interactive.
3. **Secrets file.**
   - Check only whether the file exists and what its permissions are: `ls -l ~/home_secret.toml`. Never read its content.
   - If it is missing, show the key-path skeleton from section 2 for the user to fill in, and remind them to run `chmod 600 ~/home_secret.toml`.
4. **Tokens.** For each token, give the user the creation URL and the exact scopes from section 3. The user creates the tokens and pastes them into the file. Never ask for a token in the chat, and never write one anywhere.
5. **Verify.**
   - In a template repo, run `mise trust` if needed, then `mise run inst`.
   - Run the True/False check from section 4.
   - Report each variable as present or missing. For a missing one, name the expected key path.

## Boundaries

- A user who pastes a secret into the chat should be told to rotate that token, because it is now in the transcript. Do not use it.
- Account-level settings, such as connecting GitHub in Read the Docs, are done by the user in the browser. Give the link and what to click.
- When the machine is ready, the next step for a new repo is `pywf-oss-setup-repo`.
