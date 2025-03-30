# -*- coding: utf-8 -*-

"""
Testing Automation for Python Projects.
"""

import typing as T
import subprocess
import dataclasses

from .vendor.emoji import Emoji
from .vendor.os_platform import OPEN_COMMAND
from .vendor.better_pathlib import temp_cwd

from .logger import logger
from .helpers import print_command

if T.TYPE_CHECKING:  # pragma: no cover
    from .define import PyWf


@dataclasses.dataclass
class PyWfTests:
    """
    Namespace class for testing related automation.
    """

    @logger.emoji_block(
        msg="Run Unit Test",
        emoji=Emoji.test,
    )
    def _run_unit_test(
        self: "PyWf",
        real_run: bool = True,
        quiet: bool = False,
    ):
        """
        A wrapper of ``pytest`` command to run unit test.
        """
        args = [
            f"{self.path_venv_bin_pytest}",
            f"{self.dir_tests}",
            "-s",
            f"--rootdir={self.dir_project_root}",
        ]
        if quiet:
            args.append("--quiet")
        print_command(args)
        if real_run:
            with temp_cwd(self.dir_project_root):
                subprocess.run(args, check=True)

    def run_unit_test(
        self: "PyWf",
        real_run: bool = True,
        verbose: bool = True,
    ):  # pragma: no cover
        with logger.disabled(not verbose):
            return self._run_unit_test(
                real_run=real_run,
                quiet=not verbose,
            )

    @logger.emoji_block(
        msg="Run Code Coverage Test",
        emoji=Emoji.test,
    )
    def _run_cov_test(
        self: "PyWf",
        real_run: bool = True,
        quiet: bool = False,
    ):
        """
        A wrapper of ``pytest`` command to run code coverage test.
        """
        args = [
            f"{self.path_venv_bin_pytest}",
            "-s",
            "--tb=native",
            f"--rootdir={self.dir_project_root}",
            f"--cov={self.package_name}",
            "--cov-report",
            "term-missing",
            "--cov-report",
            f"html:{self.dir_htmlcov}",
            f"{self.dir_tests}",
        ]
        if quiet:
            args.append("--quiet")
        print_command(args)
        if real_run:
            with temp_cwd(self.dir_project_root):
                subprocess.run(args, check=True)

    def run_cov_test(
        self: "PyWf",
        real_run: bool = True,
        verbose: bool = True,
    ):  # pragma: no cover
        with logger.disabled(not verbose):
            return self._run_cov_test(
                real_run=real_run,
                quiet=not verbose,
            )

    @logger.emoji_block(
        msg="View Code Coverage Test Result",
        emoji=Emoji.test,
    )
    def _view_cov(
        self: "PyWf",
        real_run: bool = True,
        quiet: bool = False,
    ):
        """
        View coverage test output html file locally in web browser.

        It is usually at the ``${dir_project_root}/htmlcov/index.html``
        """
        args = [OPEN_COMMAND, f"{self.path_htmlcov_index_html}"]
        if real_run:
            subprocess.run(args)

    def view_cov(
        self: "PyWf",
        real_run: bool = True,
        verbose: bool = True,
    ):  # pragma: no cover
        with logger.disabled(not verbose):
            return self._view_cov(
                real_run=real_run,
                quiet=not verbose,
            )

    @logger.emoji_block(
        msg="Run Integration Tests",
        emoji=Emoji.test,
    )
    def _run_int_test(
        self: "PyWf",
        real_run: bool = True,
        quiet: bool = False,
    ):
        """
        A wrapper of ``pytest`` command to run integration test.
        """
        args = [
            f"{self.path_venv_bin_pytest}",
            f"{self.dir_tests_int}",
            "-s",
            f"--rootdir={self.dir_project_root}",
        ]
        if quiet:
            args.append("--quiet")
        print_command(args)
        if real_run:
            with temp_cwd(self.dir_project_root):
                subprocess.run(args, check=True)

    def run_int_test(
        self: "PyWf",
        real_run: bool = True,
        verbose: bool = True,
    ):  # pragma: no cover
        with logger.disabled(not verbose):
            return self._run_int_test(
                real_run=real_run,
                quiet=not verbose,
            )

    @logger.emoji_block(
        msg="Run Load Test",
        emoji=Emoji.test,
    )
    def _run_load_test(
        self: "PyWf",
        real_run: bool = True,
        quiet: bool = False,
    ):
        """
        A wrapper of ``pytest`` command to run load test.
        """
        args = [
            f"{self.path_venv_bin_pytest}",
            f"{self.dir_tests_load}",
            "-s",
            f"--rootdir={self.dir_project_root}",
        ]
        if quiet:
            args.append("--quiet")
        print_command(args)
        if real_run:
            with temp_cwd(self.dir_project_root):
                subprocess.run(args, check=True)

    def run_load_test(
        self: "PyWf",
        real_run: bool = True,
        verbose: bool = True,
    ):  # pragma: no cover
        with logger.disabled(not verbose):
            return self._run_load_test(
                real_run=real_run,
                quiet=not verbose,
            )
