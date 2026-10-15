---
description: "The one-time setup of a maintainer's Mac: global mise, uv, git and gh, shell activation, creating $HOME/home_secret.toml, where to create the GitHub, Codecov, Read the Docs and PyPI tokens and with which scopes, the account-level settings, and token rotation. Read when setting up a new machine, rotating a token, or when a tool or token is missing."
---

# Machine Setup

Everything here is done **once per machine**, not once per repo. After it, every repo built from the template works with `mise run inst`. Secrets follow `01-secrets.md`.

---

## 1. Global tools

| Tool | Install | Why it is global |
| :--- | :--- | :--- |
| mise | `brew install mise` | It installs every per-repo tool version once per machine and runs the tasks. |
| uv | `brew install uv` | `uvx` keeps one global tool cache, shared by all repos (for example for `hst` and `ruff`). Each repo still pins its own uv version. |
| git, gh | `brew install git gh`, then `gh auth login` | `gh` reads CI runs and manages GitHub repos from the terminal. |

Activate mise in the shell. Add this line to `~/.zshrc`, then open a new terminal:

```bash
eval "$(mise activate zsh)"
```

Check with `mise --version`, `uv --version`, and `gh auth status`. In each repo, run `mise trust` once (mise asks for it the first time), then `mise run inst`.

---

## 2. The secrets file

Create `$HOME/home_secret.toml` with the key paths listed in `01-secrets.md` section 1, then restrict it to the owner:

```bash
chmod 600 ~/home_secret.toml
```

- The user writes the values. An AI only says which key paths must exist.
- Never commit the file, and never copy it into a repo.

---

## 3. Tokens

| Variable | Where to create it | Scope |
| :--- | :--- | :--- |
| `GITHUB_TOKEN` | <https://github.com/settings/tokens> | Classic: `repo` and `workflow`. Or fine-grained, on all repos, with Administration, Contents, Secrets, and Actions set to read and write. |
| `CODECOV_TOKEN` | codecov.io → Settings → Access | An **API** token for your account. This is not a repo upload token. |
| `READTHEDOCS_TOKEN` | <https://app.readthedocs.org/accounts/tokens/> | Account API token |
| `PYPI_TOKEN` | <https://pypi.org/manage/account/token/> | "Entire account". A brand-new project cannot use a project-scoped token for its first upload. |

**Account settings, once each:**

- In Read the Docs, connect GitHub in the account settings, so that new projects build on every push.
- Sign in to codecov.io with GitHub, so that repos appear there.

**Rotating a token:**

1. Create the new token.
2. Replace the value in `home_secret.toml` (the user does this).
3. Run the True/False check in `01-secrets.md`.

A new Codecov API token does not change the upload secrets already stored in each GitHub repo.

---

## 4. Diagnosing a missing token

| What happens | Cause |
| :--- | :--- |
| The True/False check prints `False` | The key path is missing from `home_secret.toml`, or `mise.toml` points at the wrong path. |
| mise errors while loading the env | The `hst` command failed. Usually the file is missing, or the key path does not exist. |
| The token is present, but a task fails with HTTP 401 or 403 | The token has expired or has too few scopes. Go back to section 3. |
