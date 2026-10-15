---
description: "How secrets reach a repo: one $HOME/home_secret.toml file read by the home-secret-toml CLI through mise [env], which environment variables the template uses, the hard rules that forbid an AI from reading or printing secrets, and why CI gets its secrets differently. Read before running anything that needs a token, adding a new secret, or debugging an authentication failure."
---

# Secrets

The maintainer runs hundreds of repos on one machine. Instead of a `.env` file per repo, every secret lives in one file, `$HOME/home_secret.toml`, read by the [home-secret-toml](https://github.com/MacHu-GWU/home_secret_toml-project) CLI (`hst`).

---

## 1. How a repo gets a secret

- `$HOME/home_secret.toml` is one flat TOML file. Each line is a full dotted key path and its value.
- The `[env]` block of each repo's `mise.toml` turns key paths into environment variables when mise loads the project:

  ```toml
  [env]
  GITHUB_TOKEN = "{{ exec(command='uvx --from home-secret-toml hst get github.accounts.sh.users.sh.secrets.dev.value') }}"
  PYPI_TOKEN = "{{ exec(command='uvx --from home-secret-toml hst get pypi.accounts.sh.token') }}"
  ```

- Scripts then read a plain environment variable, for example `os.environ["GITHUB_TOKEN"]`.

The template uses these variables:

| Variable | Key path in `home_secret.toml` | What it is for |
| :--- | :--- | :--- |
| `GITHUB_TOKEN` | `github.accounts.sh.users.sh.secrets.dev.value` | GitHub API: repo metadata, Actions secrets, tags and releases |
| `CODECOV_TOKEN` | `codecov_io.accounts.sh.users.sh.secrets.dev.value` | The Codecov **API** token, used to fetch each repo's upload token |
| `READTHEDOCS_TOKEN` | `readthedocs.accounts.sh.users.sh.secrets.dev.value` | Read the Docs API |
| `PYPI_TOKEN` | `pypi.accounts.sh.token` | Uploading to PyPI |

---

## 2. Hard rules for an AI

- **Never read, open, cat, grep, copy, or summarize `$HOME/home_secret.toml`.** Not even to check whether a key exists.
- **Never print a secret value.** That means: no `echo $PYPI_TOKEN`, no `env`, no `printenv`, no `mise env`, and no `hst get` outside of `mise.toml`.
- Never write a secret into a file, a commit, a log, a notebook cell, a URL, or the chat.
- **To check which variables are loaded**, print only True or False. Run this from a repo root:

  ```bash
  mise exec -- python3 -c "import os; print({k: bool(os.environ.get(k)) for k in ['GITHUB_TOKEN', 'CODECOV_TOKEN', 'READTHEDOCS_TOKEN', 'PYPI_TOKEN']})"
  ```

- **To add a new secret**, add an `[env]` line with the `hst get <key.path>` command to `mise.toml`, and tell the user which key path to add to their file. The user writes the value.
- **When a task fails for a missing or rejected token**, report the variable name and stop. Do not work around it.
- **A user who pastes a secret into the chat** should rotate it, because it is now in the transcript. Do not use it.

---

## 3. CI is different

GitHub Actions does not use mise or `home_secret.toml`. It reads repository secrets, such as `secrets.CODECOV_TOKEN`, which one-time setup tasks store on the GitHub repo.
