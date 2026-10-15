# Secrets and Environment Variables

The maintainer runs hundreds of repos on one machine. Instead of a `.env` file per repo, every secret lives in one file, `$HOME/home_secret.toml`, read through the `home-secret-toml` CLI (`hst`).

---

## 1. How a repo gets a secret

`mise.toml` `[env]` resolves each variable when mise loads the project:

```toml
[env]
GITHUB_TOKEN = "{{ exec(command='uvx --from home-secret-toml hst get github.accounts.sh.users.sh.secrets.dev.value') }}"
PYPI_TOKEN = "{{ exec(command='uvx --from home-secret-toml hst get pypi.accounts.sh.token') }}"
```

mise tasks then read the plain environment variable, for example `os.environ["GITHUB_TOKEN"]`.

The template uses these variables:

| Variable | Used by |
| :--- | :--- |
| `GITHUB_TOKEN` | `release`, `setup-codecov`, `update-github-metadata` |
| `CODECOV_TOKEN` | `setup-codecov` (the Codecov **API** token, not the upload token) |
| `READTHEDOCS_TOKEN` | `setup-readthedocs` |
| `PYPI_TOKEN` | `publish` |

---

## 2. Hard rules for AI agents

- **Never read, open, cat, grep, copy, or summarize `$HOME/home_secret.toml`.** Not even to check whether a key exists.
- Never print secret values. That means: no `echo $PYPI_TOKEN`, no `env`, no `printenv`, no `mise env`, and no `hst get` outside of `mise.toml`.
- Never write a secret value into a file, commit, log, notebook cell, or URL.
- To add a new secret, add an `[env]` line to `mise.toml` with the `hst get <key.path>` command, and tell the user which key path to add to their `home_secret.toml`. The user fills in the value.
- If a task fails for a missing or invalid token, report the variable name and stop. Do not try to work around it.

---

## 3. CI is different

GitHub Actions does not use mise or `home_secret.toml`. It gets secrets from repository secrets (for example `secrets.CODECOV_TOKEN`), which the `setup-*` tasks create. See `ci-and-hosting.md`.
