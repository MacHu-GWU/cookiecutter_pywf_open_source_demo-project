# -*- coding: utf-8 -*-

"""
Virtualenv management related automation.
"""

import typing as T
import shutil
import subprocess
import dataclasses

from .vendor.emoji import Emoji
from .vendor.better_pathlib import temp_cwd
from .logger import logger
from .helpers import print_command

if T.TYPE_CHECKING:  # pragma: no cover
    from .define import PyWf


@dataclasses.dataclass
class PyWfVenv:
    """
    Namespace class for Virtualenv management related automation.

    :param python_version: example "3.7", "3.8", ...
    """

    python_version: str = dataclasses.field()

    def _validate_python_version(self: "PyWf"):
        value_error = ValueError(
            f"'python_version' has to be in format of '3.7', '3.8', ..."
        )
        if self.python_version[0] not in ["3"]:
            raise value_error
        if self.python_version[1] != ".":
            raise value_error
        if not self.python_version[2:].isdigit():
            raise value_error
        if int(self.python_version[2:]) < 7:
            raise ValueError("python_version has to be >= 3.7")

    @logger.emoji_block(
        msg="Create Virtual Environment",
        emoji=Emoji.python,
    )
    def _create_virtualenv(
        self: "PyWf",
        real_run: bool = True,
        quiet: bool = False,
    ) -> bool:
        """
        Run:

        .. code-block:: bash

            $ virtualenv -p python${X}.${Y} ./.venv

        :return: a boolean flat to indicate whether a creation is performed.
        """
        if self.dir_venv.exists():
            logger.info(f"{self.dir_venv} already exists, do nothing.")
            return False
        else:
            # Ref: https://python-poetry.org/docs/managing-environments/
            args = [
                f"{self.path_bin_poetry}",
                "config",
                "virtualenvs.in-project",
                "true",
            ]
            if quiet:
                args.append("--quiet")
            print_command(args)
            if real_run is True:
                subprocess.run(args, check=True)

            args = [
                f"{self.path_bin_poetry}",
                "env",
                "use",
                f"python{self.python_version}",
            ]
            if quiet:
                args.append("--quiet")
            print_command(args)
            if real_run is True:
                with temp_cwd(self.dir_project_root):
                    subprocess.run(args, check=True)
            logger.info("done")
            return True

    def create_virtualenv(
        self: "PyWf",
        real_run: bool = True,
        verbose: bool = False,
    ) -> bool:  # pragma: no cover
        with logger.disabled(not verbose):
            return self._create_virtualenv(
                real_run=real_run,
                quiet=not verbose,
            )

    @logger.emoji_block(
        msg="Remove Virtual Environment",
        emoji=Emoji.python,
    )
    def _remove_virtualenv(
        self: "PyWf",
        real_run: bool = True,
        quiet: bool = False,
    ) -> bool:
        """
        Run:

        .. code-block:: bash

            $ rm -r /path/to/.venv

        :return: a boolean flat to indicate whether a deletion is performed.
        """
        if self.dir_venv.exists():
            args = [
                "rm",
                "-r",
                f"{self.dir_venv}",
            ]
            print_command(args)
            if real_run:
                shutil.rmtree(f"{self.dir_venv}", ignore_errors=True)
            logger.info(f"done! {self.dir_venv} is removed.")
            return True
        else:
            logger.info(f"{self.dir_venv} doesn't exists, do nothing.")
            return False

    def remove_virtualenv(
        self: "PyWf",
        real_run: bool = True,
        verbose: bool = False,
    ):  # pragma: no cover
        with logger.disabled(not verbose):
            return self._remove_virtualenv(
                real_run=real_run,
                quiet=not verbose,
            )
