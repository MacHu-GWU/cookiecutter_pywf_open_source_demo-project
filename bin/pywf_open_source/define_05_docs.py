# -*- coding: utf-8 -*-

"""
Document Build and Deploy Automation for Python Projects.
"""

import typing as T
import shutil
import dataclasses
import subprocess

from .vendor.emoji import Emoji
from .vendor.os_platform import OPEN_COMMAND

from .helpers import print_command
from .logger import logger

if T.TYPE_CHECKING:  # pragma: no cover
    from .define import PyWf


@dataclasses.dataclass
class PyWfDocs:
    """
    Namespace class for document related automation.
    """

    @logger.emoji_block(
        msg="Build Documentation Site Locally",
        emoji=Emoji.doc,
    )
    def _build_doc(
        self: "PyWf",
        real_run: bool = True,
        quiet: bool = False,
    ):
        """
        Use sphinx doc to build documentation site locally. It set the
        necessary environment variables so that the ``make html`` command
        can build the HTML successfully.
        """
        if real_run:
            shutil.rmtree(
                f"{self.dir_sphinx_doc_build}",
                ignore_errors=True,
            )
            shutil.rmtree(
                f"{self.dir_sphinx_doc_source_python_lib}",
                ignore_errors=True,
            )

        args = [
            f"{self.path_venv_bin_sphinx_build}",
            "-M",
            "html",
            f"{self.dir_sphinx_doc_source}",
            f"{self.dir_sphinx_doc_build}",
        ]
        print_command(args)
        if real_run:
            subprocess.run(args, check=True)

    def build_doc(
        self: "PyWf",
        real_run: bool = True,
        verbose: bool = True,
    ):  # pragma: no cover
        with logger.disabled(not verbose):
            return self._build_doc(
                real_run=real_run,
                quiet=not verbose,
            )

    @logger.emoji_block(
        msg="View Documentation Site Locally",
        emoji=Emoji.doc,
    )
    def _view_doc(
        self: "PyWf",
        real_run: bool = True,
        quiet: bool = False,
    ):
        """
        View documentation site built locally in web browser.

        It is usually at the ``${dir_project_root}/build/html/index.html``
        """
        args = [OPEN_COMMAND, f"{self.path_sphinx_doc_build_index_html}"]
        print_command(args)
        if real_run:
            subprocess.run(args)

    def view_doc(
        self: "PyWf",
        real_run: bool = True,
        verbose: bool = True,
    ):  # pragma: no cover
        with logger.disabled(not verbose):
            return self._view_doc(
                real_run=real_run,
                quiet=not verbose,
            )

    @logger.emoji_block(
        msg="Deploy Documentation Site To S3 as Versioned Doc",
        emoji=Emoji.doc,
    )
    def _deploy_versioned_doc(
        self: "PyWf",
        bucket: T.Optional[str] = None,
        prefix: str = "projects/",
        aws_profile: T.Optional[str] = None,
        real_run: bool = True,
        quiet: bool = False,
    ) -> bool:
        """
        Deploy versioned document to AWS S3.

        The S3 bucket has to enable static website hosting. The document site
        will be uploaded to ``s3://${bucket}/${prefix}${package_name}/${package_version}/``
        """
        if bool(self.doc_host_s3_bucket) is False:
            logger.info(f"{Emoji.red_circle} doc_host_s3_bucket is not set, skip.")
            return False
        if bucket is None:
            bucket = self.doc_host_s3_bucket
        if aws_profile is None:
            aws_profile = self.doc_host_aws_profile
        args = [
            f"{self.path_bin_aws}",
            "s3",
            "sync",
            f"{self.dir_sphinx_doc_build_html}",
            f"s3://{bucket}/{prefix}{self.package_name}/{self.package_version}/",
        ]
        if aws_profile:
            args.extend(["--profile", aws_profile])
        print_command(args)
        if real_run:
            subprocess.run(args, check=True)
        return real_run

    def deploy_versioned_doc(
        self: "PyWf",
        bucket: T.Optional[str] = None,
        prefix: str = "projects/",
        aws_profile: T.Optional[str] = None,
        real_run: bool = True,
        verbose: bool = True,
    ) -> bool:  # pragma: no cover
        with logger.disabled(not verbose):
            return self._deploy_versioned_doc(
                bucket=bucket,
                prefix=prefix,
                aws_profile=aws_profile,
                real_run=real_run,
                quiet=not verbose,
            )

    @logger.emoji_block(
        msg="Deploy Documentation Site To S3 as Latest Doc",
        emoji=Emoji.doc,
    )
    def _deploy_latest_doc(
        self: "PyWf",
        bucket: T.Optional[str] = None,
        prefix: str = "projects/",
        aws_profile: T.Optional[str] = None,
        real_run: bool = True,
        quiet: bool = False,
    ) -> bool:
        """
        Deploy the latest document to AWS S3.

        The S3 bucket has to enable static website hosting. The document site
        will be uploaded to ``s3://${bucket}/${prefix}${package_name}/latest/``
        """
        if bool(self.doc_host_s3_bucket) is False:
            logger.info(f"{Emoji.red_circle} doc_host_s3_bucket is not set, skip.")
            return False
        if bucket is None:
            bucket = self.doc_host_s3_bucket
        if aws_profile is None:
            aws_profile = self.doc_host_aws_profile
        args = [
            f"{self.path_bin_aws}",
            "s3",
            "sync",
            f"{self.dir_sphinx_doc_build_html}",
            f"s3://{bucket}/{prefix}{self.package_name}/latest/",
        ]
        if aws_profile:
            args.extend(["--profile", aws_profile])
        print_command(args)
        if real_run:
            subprocess.run(args, check=True)
        return real_run

    def deploy_latest_doc(
        self: "PyWf",
        bucket: T.Optional[str] = None,
        prefix: str = "projects/",
        aws_profile: T.Optional[str] = None,
        real_run: bool = True,
        verbose: bool = True,
    ) -> bool:  # pragma: no cover
        with logger.disabled(not verbose):
            return self._deploy_latest_doc(
                bucket=bucket,
                prefix=prefix,
                aws_profile=aws_profile,
                real_run=real_run,
                quiet=not verbose,
            )

    @logger.emoji_block(
        msg="View Latest Doc on AWS S3",
        emoji=Emoji.doc,
    )
    def _view_latest_doc(
        self: "PyWf",
        bucket: T.Optional[str] = None,
        prefix: str = "projects/",
        real_run: bool = True,
        quiet: bool = False,
    ):
        """
        Open the latest document that hosted on AWS S3 in web browser.

        Here's a sample document site url
        https://my-bucket.s3.amazonaws.com/my-prefix/my_package/latest/index.html
        """
        if bool(self.doc_host_s3_bucket) is False:
            logger.info(f"{Emoji.red_circle} doc_host_s3_bucket is not set, skip.")
            return False
        if bucket is None:
            bucket = self.doc_host_s3_bucket
        url = (
            f"https://{bucket}.s3.amazonaws.com/{prefix}{self.package_name}"
            f"/latest/{self.path_sphinx_doc_build_index_html.name}"
        )
        args = [OPEN_COMMAND, url]
        print_command(args)
        if real_run:
            subprocess.run(args, check=True)

    def view_latest_doc(
        self: "PyWf",
        bucket: T.Optional[str] = None,
        prefix: str = "projects/",
        real_run: bool = True,
        verbose: bool = True,
    ):
        """
        Open the latest document that hosted on AWS S3 in web browser.

        Here's a sample document site url
        https://my-bucket.s3.amazonaws.com/my-prefix/my_package/latest/index.html
        """
        with logger.disabled(not verbose):
            return self._view_latest_doc(
                bucket=bucket,
                prefix=prefix,
                real_run=real_run,
                quiet=not verbose,
            )
