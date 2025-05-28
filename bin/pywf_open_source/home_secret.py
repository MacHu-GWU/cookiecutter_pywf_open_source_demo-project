# -*- coding: utf-8 -*-

"""
Home Secrets Management Module

This module provides a flexible and secure mechanism for loading secrets from a JSON file.

The secret file is expected to be located in one of two places:

1. In the current directory (source of truth)
2. In the user's home directory (runtime location)

The module supports:

- Lazy loading of secrets
- Hierarchical secret referencing
- Automatic synchronization between source and home directories
- Robust error handling for missing or malformed secrets

Folder Structure:

.. code-block::

    ${HOME}/home_secret.json
    ${DIR_HERE}/home_secret.json
    ${DIR_HERE}/home_secret.py
"""

import typing as T
import json
import dataclasses
from pathlib import Path
from functools import cached_property

# The filename to look for in the current directory and home directory.
filename = "home_secret.json"
# The local path to the secret file in the current directory considered
# as source of truth and don't check in this to code version control.
p_here_secret = Path(filename)
# The home directory path where the secret file will be copied to and
# where secret been load from for the application.
p_home_secret = Path.home() / filename


def _deep_get(
    dct: dict,
    path: str,
) -> T.Union[
    str,
    int,
    list[str],
    list[int],
    dict[str, T.Any],
]:
    """
    Retrieve a nested value from a dictionary using dot-separated path.
    """
    value = dct
    for part in path.split("."):
        if part in value:
            value = value[part]
        else:
            raise KeyError(f"Key '{part}' not found in the provided data.")
    return value


@dataclasses.dataclass
class Token:
    """
    Tokens are placeholders for values that aren’t know when the token object
    is defined. The value will be loaded lazily when you call the :meth:`value` property.
    """

    data: dict[str, T.Any] = dataclasses.field()
    path: str = dataclasses.field()

    @property
    def v(self):
        """
        Lazily load and return the secret value.
        """
        return _deep_get(dct=self.data, path=self.path)


@dataclasses.dataclass
class HomeSecret:
    """ """

    @cached_property
    def data(self) -> dict[str, T.Any]:
        """
        Load the secret data from the `${HOME}/home_secret.json` file.
        """
        # This copy logic will only be used when you want to edit the source of truth
        if p_here_secret.exists():
            p_home_secret.write_text(
                p_here_secret.read_text(encoding="utf-8"),
                encoding="utf-8",
            )
        if not p_home_secret.exists():
            raise FileNotFoundError(f"Secret file not found at {p_home_secret}")
        return json.loads(p_home_secret.read_text(encoding="utf-8"))

    def v(self, path: str):
        """
        Shortcut to get the value of a secret by its path.
        V stands for Value.
        """
        return _deep_get(dct=self.data, path=path)

    def t(self, path: str) -> Token:
        """
        Create a Token object for the given path.
        T stands for Token.
        """
        return Token(
            data=self.data,
            path=path,
        )


hs = HomeSecret()


class Secret:
    """
    Hierarchical secret reference class.

    Provides a type-safe, easy-to-navigate structure for accessing secrets.
    Designed to mirror the structure of the home_secret.json file.
    """

    # fmt: off
    class example_provider:
        class accounts:
            class example_account:
                _p = "providers.example_provider.accounts.example_account"
                account_id = hs.t(f"{_p}.account_id")
                admin_email = hs.t(f"{_p}.admin_email")

                class secrets:
                    example_account_secret = hs.t(
                        "providers.example_provider.accounts.example_account.secrets.example_account_secret.value")

                class users:
                    class example_user:
                        email = hs.t("providers.example_provider.accounts.example_account.users.example_user.email")

                        class secrets:
                            example_user_secret = hs.t(
                                "providers.example_provider.accounts.example_account.users.example_user.secrets.example_user_secret.value")

    class atlassian:
        class accounts:
            class sh:
                _p = "providers.atlassian.accounts.sh"
                admin_email = hs.t(f"{_p}.admin_email")
                site_url = hs.t(f"{_p}.site_url")

                class users:
                    class sh:
                        email = hs.t(f"providers.atlassian.accounts.sh.users.sh.email")

                        class secrets:
                            sync_page = hs.t(f"providers.atlassian.accounts.sh.users.sh.secrets.sync_page.value")

            class sh_esc:
                _p = "providers.atlassian.accounts.sh_esc"
                admin_email = hs.t(f"{_p}.admin_email")
                site_url = hs.t(f"{_p}.site_url")

                class users:
                    class sh_esc:
                        email = hs.t("providers.atlassian.accounts.sh_esc.users.sh_esc.email")

                        class secrets:
                            sync_page = hs.t("providers.atlassian.accounts.sh_esc.users.sh_esc.secrets.sync_page.value")

    class cloudflare:
        class accounts:
            class esc:
                _p = "providers.cloudflare.accounts.esc"
                account_id = hs.t(f"{_p}.account_id")
                admin_email = hs.t(f"{_p}.admin_email")
                global_api_key = hs.t(f"{_p}.global_api_key")

                class secrets:
                    class read_and_write_all_r2_bucket:
                        _p = "providers.cloudflare.accounts.esc.secrets.read_and_write_all_r2_bucket"
                        token = hs.t(f"{_p}.value")
                        access_key = hs.t(f"{_p}.creds.access_key")
                        secret_key = hs.t(f"{_p}.creds.secret_key")
                        endpoint = hs.t(f"{_p}.creds.endpoint")

                    read_all_resources = hs.t("providers.cloudflare.accounts.esc.secrets.read_all_resources.value")

                class users:
                    class sh_esc:
                        email = hs.t("providers.cloudflare.accounts.esc.users.sh_esc.email")

                        class secrets:
                            _p = "providers.cloudflare.accounts.esc.users.sh_esc.secrets"
                            read_only = hs.t(f"{_p}.read_only.value")
                            cloudflare_pages_upload = hs.t(f"{_p}.cloudflare_pages_upload.value")

    class codecov_io:
        class accounts:
            class sh:
                class users:
                    class sh:
                        class secrets:
                            dev = hs.t("providers.codecov_io.accounts.sh.users.sh.secrets.dev.value")

            class sh_esc:
                class users:
                    class sh_esc:
                        class secrets:
                            dev = hs.t("providers.codecov_io.accounts.sh_esc.users.sh_esc.secrets.dev.value")

    class github:
        class accounts:
            class sh:
                account_id = hs.t("providers.github.accounts.sh.account_id")

                class users:
                    class sh:
                        user_id = hs.t("providers.github.accounts.sh.users.sh.user_id")

                        class secrets:
                            full_repo_access = hs.t(
                                "providers.github.accounts.sh.users.sh.secrets.full_repo_access.value")

            class sh_esc:
                account_id = hs.t("providers.github.accounts.sh_esc.account_id")

                class users:
                    class sh_esc:
                        user_id = hs.t("providers.github.accounts.sh_esc.users.sh_esc.user_id")

                        class secrets:
                            list_repo = hs.t("providers.github.accounts.sh_esc.users.sh_esc.secrets.list_repo.value")
                            dev = hs.t("providers.github.accounts.sh_esc.users.sh_esc.secrets.dev.value")

    class neon_tech:
        class accounts:
            class esc:
                admin_email = hs.t("providers.neon_tech.accounts.esc.admin_email")

                class projects:
                    class esc:
                        class branches:
                            dev = hs.t("providers.neon_tech.accounts.esc.projects.esc.branches.development")
                            prod = hs.t("providers.neon_tech.accounts.esc.projects.esc.branches.production")

    class readthedocs:
        class accounts:
            class sh:
                class users:
                    class sh:
                        class secrets:
                            dev = hs.t("providers.readthedocs.accounts.sh.users.sh.secrets.dev.value")

    class short_io:
        class accounts:
            class sh_esc:
                account_id = hs.t("providers.short_io.accounts.sh_esc.account_id")
                admin_email = hs.t("providers.short_io.accounts.sh_esc.admin_email")

                class users:
                    class sh_esc:
                        email = hs.t("providers.short_io.accounts.sh_esc.users.sh_esc.email")

                        class secrets:
                            dev = hs.t("providers.short_io.accounts.sh_esc.users.sh_esc.secrets.dev.value")

            class esc:
                account_id = hs.t("providers.short_io.accounts.esc.account_id")
                admin_email = hs.t("providers.short_io.accounts.esc.admin_email")

                class users:
                    class admin:
                        email = hs.t("providers.short_io.accounts.esc.users.admin.email")

                        class secrets:
                            link_esc = hs.t("providers.short_io.accounts.esc.users.admin.secrets.link_esc.value")
    # fmt: on


def _validate_secrets():
    """
    Validate secret loading by attempting to retrieve all defined secrets.
    """
    print("--- Validating secrets ---")
    # fmt: off
    print(f"{Secret.example_provider.accounts.example_account.account_id.v = }")
    print(f"{Secret.example_provider.accounts.example_account.admin_email.v = }")
    print(f"{Secret.example_provider.accounts.example_account.users.example_user.email.v = }")
    print(f"{Secret.example_provider.accounts.example_account.users.example_user.secrets.example_user_secret.v = }")
    print(f"{Secret.atlassian.accounts.sh.site_url.v = }")
    print(f"{Secret.atlassian.accounts.sh.admin_email.v = }")
    print(f"{Secret.atlassian.accounts.sh.users.sh.email.v = }")
    print(f"{Secret.atlassian.accounts.sh.users.sh.secrets.sync_page.v = }")
    print(f"{Secret.atlassian.accounts.sh_esc.site_url.v = }")
    print(f"{Secret.atlassian.accounts.sh_esc.admin_email.v = }")
    print(f"{Secret.atlassian.accounts.sh_esc.users.sh_esc.email.v = }")
    print(f"{Secret.atlassian.accounts.sh_esc.users.sh_esc.secrets.sync_page.v = }")
    print(f"{Secret.cloudflare.accounts.esc.account_id.v = }")
    print(f"{Secret.cloudflare.accounts.esc.admin_email.v = }")
    print(f"{Secret.cloudflare.accounts.esc.global_api_key.v = }")
    print(f"{Secret.cloudflare.accounts.esc.secrets.read_and_write_all_r2_bucket.token.v = }")
    print(f"{Secret.cloudflare.accounts.esc.secrets.read_and_write_all_r2_bucket.access_key.v = }")
    print(f"{Secret.cloudflare.accounts.esc.secrets.read_and_write_all_r2_bucket.secret_key.v = }")
    print(f"{Secret.cloudflare.accounts.esc.secrets.read_and_write_all_r2_bucket.endpoint.v = }")
    print(f"{Secret.cloudflare.accounts.esc.secrets.read_all_resources.v = }")
    print(f"{Secret.cloudflare.accounts.esc.users.sh_esc.secrets.read_only.v = }")
    print(f"{Secret.cloudflare.accounts.esc.users.sh_esc.secrets.cloudflare_pages_upload.v = }")
    print(f"{Secret.codecov_io.accounts.sh.users.sh.secrets.dev.v = }")
    print(f"{Secret.codecov_io.accounts.sh_esc.users.sh_esc.secrets.dev.v = }")
    print(f"{Secret.github.accounts.sh.account_id.v = }")
    print(f"{Secret.github.accounts.sh.users.sh.user_id.v = }")
    print(f"{Secret.github.accounts.sh.users.sh.secrets.full_repo_access.v = }")
    print(f"{Secret.github.accounts.sh_esc.account_id.v = }")
    print(f"{Secret.github.accounts.sh_esc.users.sh_esc.user_id.v = }")
    print(f"{Secret.github.accounts.sh_esc.users.sh_esc.secrets.list_repo.v = }")
    print(f"{Secret.github.accounts.sh_esc.users.sh_esc.secrets.dev.v = }")
    print(f"{Secret.neon_tech.accounts.esc.admin_email.v = }")
    print(f"{Secret.neon_tech.accounts.esc.projects.esc.branches.dev.v = }")
    print(f"{Secret.neon_tech.accounts.esc.projects.esc.branches.prod.v = }")
    print(f"{Secret.readthedocs.accounts.sh.users.sh.secrets.dev.v = }")
    print(f"{Secret.short_io.accounts.sh_esc.admin_email.v = }")
    print(f"{Secret.short_io.accounts.sh_esc.users.sh_esc.secrets.dev.v = }")
    print(f"{Secret.short_io.accounts.esc.users.admin.email.v = }")
    print(f"{Secret.short_io.accounts.esc.users.admin.secrets.link_esc.v = }")
    # fmt: on


if __name__ == "__main__":
    _validate_secrets()
