# -*- coding: utf-8 -*-

"""
Setup SaaS services for your Open Source Python project.
"""

import typing as T
import dataclasses
from functools import cached_property


try:
    import requests
    from github import Github
except ImportError:  # pragma: no cover
    pass

from .vendor.emoji import Emoji

from .logger import logger
from .helpers import raise_http_response_error

if T.TYPE_CHECKING:  # pragma: no cover
    from .define import PyWf


@dataclasses.dataclass
class PyWfSaas:  # pragma: no cover
    """
    Namespace class for SaaS service setup automation.
    """

    @cached_property
    def github_token(self: "PyWf") -> str:
        if self.path_github_token_file.exists():
            return self.path_github_token_file.read_text(encoding="utf-8").strip()
        else:  # pragma: no cover
            message = (
                f"{Emoji.error} Cannot find GitHub token file at "
                f"{self.path_github_token_file}!\n"
                f"{self.__class__.path_github_token_file.__doc__}"
            )
            raise FileNotFoundError(message)

    @cached_property
    def codecov_token(self: "PyWf") -> str:
        if self.path_codecov_token_file.exists():
            return self.path_codecov_token_file.read_text(encoding="utf-8").strip()
        else:  # pragma: no cover
            message = (
                f"{Emoji.error} Cannot find Codecov token file at "
                f"{self.path_codecov_token_file}!\n"
                f"{self.__class__.path_codecov_token_file.__doc__}"
            )
            raise FileNotFoundError(message)

    @cached_property
    def readthedocs_token(self: "PyWf") -> str:
        if self.path_readthedocs_token_file.exists():
            return self.path_readthedocs_token_file.read_text(encoding="utf-8").strip()
        else:
            message = (
                f"{Emoji.error} Cannot find Readthedocs token file at "
                f"{self.path_readthedocs_token_file}!\n"
                f"{self.__class__.path_readthedocs_token_file.__doc__}"
            )
            raise FileNotFoundError(message)

    def get_codecov_io_upload_token(
        self: "PyWf",
        real_run: bool = True,
    ) -> T.Optional[str]:
        """
        Get the upload token for codecov io for your GitHub repo.

        Ref:

        - https://docs.codecov.com/reference/repos_retrieve
        - https://docs.codecov.com/reference/repos_config_retrieve

        :returns: the upload token for codecov.io.
        """
        logger.info("Getting codecov.io upload token...")
        url = f"https://app.codecov.io/gh/{self.github_account}/{self.git_repo_name}/settings"
        with logger.indent():
            logger.info(f"preview at {url}")
        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {self.codecov_token}",
        }
        endpoint = "https://api.codecov.io/api/v2"
        url = f"{endpoint}/github/{self.github_account}/repos/{self.git_repo_name}/"
        if real_run:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            is_private = response.json()["private"]
            if is_private is True:
                raise ValueError("You cannot use codecov.io for private repositories.")

        url = f"{endpoint}/github/{self.github_account}/repos/{self.git_repo_name}/config/"
        if real_run:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            upload_token = response.json()["upload_token"]
            return upload_token
        else:
            return None

    @logger.emoji_block(
        msg="Setup codecov.io Upload Token on GitHub",
        emoji=Emoji.test,
    )
    def _setup_codecov_io_upload_token_on_github(
        self: "PyWf",
        real_run: bool = True,
    ):
        """
        Apply the codecov upload token to GitHub Action secrets in your GitHub repository.

        Ref:

        - https://docs.codecov.com/reference/repos_retrieve
        - https://docs.codecov.com/reference/repos_config_retrieve
        - https://pygithub.readthedocs.io/en/latest/examples/Repository.html

        :returns: a boolean flag to indicate whether the operation is performed.
        """
        codecov_io_upload_token = self.get_codecov_io_upload_token(real_run=real_run)

        logger.info("Setting up codecov.io upload token on GitHub...")
        with logger.indent():
            logger.info(f"preview at {self.github_actions_secrets_settings_url}")
        gh = Github(self.github_token)
        repo = gh.get_repo(self.github_repo_fullname)
        if real_run:
            repo.create_secret(
                secret_name="CODECOV_TOKEN",
                unencrypted_value=codecov_io_upload_token,
                secret_type="actions",
            )
        return real_run

    def setup_codecov_io_upload_token_on_github(
        self: "PyWf",
        real_run: bool = True,
        verbose: bool = True,
    ):
        with logger.disabled(not verbose):
            return self._setup_codecov_io_upload_token_on_github(
                real_run=real_run,
            )

    setup_codecov_io_upload_token_on_github.__doc__ = (
        _setup_codecov_io_upload_token_on_github.__doc__
    )

    @logger.emoji_block(
        msg="Setup readthedocs.org Project",
        emoji=Emoji.doc,
    )
    def _setup_readthedocs_project(
        self: "PyWf",
        real_run: bool = True,
    ) -> bool:
        """
        Create a project on readthedocs.org.

        Ref:

        - https://docs.readthedocs.io/en/stable/api/v3.html#get--api-v3-projects-(string-project_slug)-
        - https://docs.readthedocs.io/en/stable/api/v3.html#post--api-v3-projects-

        :returns: a boolean flag to indicate whether the operation is performed.
        """
        logger.info("Setting up readthedocs project...")
        readthedocs_project_name_slug = self.readthedocs_project_name.replace("_", "-")
        url = f"https://app.readthedocs.org/dashboard/{readthedocs_project_name_slug}/edit/"
        with logger.indent():
            logger.info(f"preview at {url}")
        headers = {
            "accept": "application/json",
            "Authorization": f"Token {self.readthedocs_token}",
        }
        endpoint = "https://readthedocs.org/api/v3"

        url = f"{endpoint}/projects/{readthedocs_project_name_slug}/"
        if real_run:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                url = f"https://app.readthedocs.org/projects/{readthedocs_project_name_slug}/"
                logger.info(
                    f"Project already exists on readthedocs.org, "
                    f"please view it at: {url}"
                )
                return True
            elif response.status_code == 404:
                logger.info("Project does not exist on readthedocs.org, creating it...")
            else:
                raise_http_response_error(response)

        url = f"{endpoint}/projects/"
        data = {
            "name": self.readthedocs_project_name,
            "repository": {"url": self.github_repo_url, "type": "git"},
            "homepage": f"http://{readthedocs_project_name_slug}.readthedocs.io/",
            "programming_language": "py",
            "language": "en",
            "privacy_level": "public",
            "external_builds_privacy_level": "public",
            "versioning_scheme": "multiple_versions_with_translations",
            "tags": [],
        }
        if real_run:
            response = requests.post(
                url,
                headers=headers,
                json=data,
            )
            if response.status_code < 200 or response.status_code >= 300:
                raise_http_response_error(response)
        return real_run

    def setup_readthedocs_project(
        self: "PyWf",
        real_run: bool = True,
        verbose: bool = True,
    ):
        with logger.disabled(not verbose):
            return self._setup_readthedocs_project(
                real_run=real_run,
            )

    setup_readthedocs_project.__doc__ = _setup_readthedocs_project.__doc__
