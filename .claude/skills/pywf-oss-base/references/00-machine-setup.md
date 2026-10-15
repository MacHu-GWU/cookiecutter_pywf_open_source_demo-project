---
description: "The one-time setup of a maintainer's Mac: global mise and uv, shell activation, the $HOME/home_secret.toml layout and key paths, the four service tokens (GitHub, Codecov, Read the Docs, PyPI) with their scopes, and a check that never prints a secret. Read when setting up a new machine, adding or rotating a token, or when mise tasks fail because a tool or token is missing."
---

# Machine Setup

Everything here is done **once per machine**, not once per repo. Every repo built from the template then works with `mise run inst`.

---

## 1. Global tools

| Tool | Install | Why global |
| :--- | :--- | :--- |
| mise | `brew install mise` | It manages every per-repo tool version (`mise.toml` `[tools]`) and runs the tasks. |
| uv | `brew install uv` | `uvx` (used by `mise run format` / `lint` and by `hst` in `mise.toml` `[env]`) keeps one global tool cache, shared by all repos. Each repo still pins its own uv version in `mise.toml`. |
| git, gh | `brew install git gh`, then `gh auth login` | `gh` is used to read CI runs and to manage the repo from the terminal. |

Activate mise in the shell. Add this line to `~/.zshrc`, then open a new terminal:

```bash
eval "$(mise activate zsh)"
```

Check the setup with `mise --version`, `uv --version`, and `gh auth status`. In a repo, also run `mise trust` once (mise asks for it the first time) and then `mise run inst`.

---

## 2. Secrets file: `$HOME/home_secret.toml`

- One flat TOML file holds every secret for every repo. Each line is a full dotted key path with its value.
- The [home-secret-toml](https://github.com/MacHu-GWU/home_secret_toml-project) CLI reads it: `uvx --from home-secret-toml hst get <key.path>`.
- Each repo's `mise.toml` `[env]` turns key paths into environment variables (see `08-secrets.md`).

The key paths the template uses are below. The user writes the values; the AI only tells them which keys must exist.

```toml
# Values are written by the user, never by an AI.
github.accounts.sh.users.sh.secrets.dev.value = "..."       # -> GITHUB_TOKEN
codecov_io.accounts.sh.users.sh.secrets.dev.value = "..."   # -> CODECOV_TOKEN
readthedocs.accounts.sh.users.sh.secrets.dev.value = "..."  # -> READTHEDOCS_TOKEN
pypi.accounts.sh.token = "..."                              # -> PYPI_TOKEN
```

Rules:

- Set the file permission to the owner only: `chmod 600 ~/home_secret.toml`. Never commit it, and never copy it into a repo.
- An AI never opens, reads, greps, or prints this file (see `08-secrets.md`). To check it, use section 4.

---

## 3. Tokens: where to create them, and which scopes

| Variable | Where to create it | Scope | Used by |
| :--- | :--- | :--- | :--- |
| `GITHUB_TOKEN` | <https://github.com/settings/tokens> | Classic token: `repo` and `workflow`. Or a fine-grained token on all repos with Administration, Contents, Secrets, and Actions set to read and write. | `update-github-metadata`, `setup-codecov` (writes an Actions secret), `release` (tags and releases) |
| `CODECOV_TOKEN` | codecov.io → Settings → Access → generate an **API** token | API access to your account. This is not a repo upload token. | `setup-codecov`, which fetches each repo's upload token |
| `READTHEDOCS_TOKEN` | <https://app.readthedocs.org/accounts/tokens/> | Account API token | `setup-readthedocs` |
| `PYPI_TOKEN` | <https://pypi.org/manage/account/token/> | "Entire account". A brand-new project cannot use a project-scoped token for its first upload. | `publish` |

Also, once per account:

- Connect GitHub in the Read the Docs account settings, so that new projects build on every push.
- Sign in to codecov.io with GitHub, so that repos appear there.

**Rotating a token:** create the new token, replace the value in `home_secret.toml` (the user does this), and run the check in section 4. A new GitHub or Codecov token does not change the upload secret already stored in each repo. Rerun `mise run setup-codecov` only for repos whose CI upload fails.

---

## 4. Check, without printing any secret

Run this from any repo built from the template. It prints only `True` or `False` for each variable:

```bash
mise exec -- python3 -c "import os; print({k: bool(os.environ.get(k)) for k in ['GITHUB_TOKEN', 'CODECOV_TOKEN', 'READTHEDOCS_TOKEN', 'PYPI_TOKEN']})"
```

- `False` means the key path is missing from `home_secret.toml`, or `mise.toml` points at the wrong path.
- If mise itself errors while loading the env, the `hst` command failed. Usually the file is missing or the key path does not exist.

A token that is present can still be expired or have too few scopes. The task that uses it will fail with HTTP 401 or 403; in that case, go back to section 3.
