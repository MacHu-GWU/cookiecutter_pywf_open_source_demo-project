# -*- coding: utf-8 -*-

"""
The namespace for all the pyproject_ops automation methods.
"""

import typing as T
import tomllib
import dataclasses
from pathlib import Path

from .define_01_paths import PyWfPaths
from .define_02_logger import PyWfLogger
from .define_03_venv import PyWfVenv
from .define_04_toml import PyWfToml
from .define_05_deps import PyWfDeps
from .define_06_tests import PyWfTests
from .define_07_docs import PyWfDocs

# from .pyproject_build import PyProjectBuild
# from .pyproject_publish import PyProjectPublish


@dataclasses.dataclass
class PyWf(
    PyWfPaths,
    PyWfLogger,
    PyWfVenv,
    PyWfToml,
    PyWfDeps,
    PyWfTests,
    PyWfDocs,
    # PyProjectBuild,
    # PyProjectPublish,
):
    """
    The namespace for all the pyproject_ops automation methods.

    :param dir_project_root: The root directory of the project, it is usually
        the git root directory. It has to have a ``pyproject.toml`` file or
        ``setup.py`` in it.
    :param package_name: The name of the Python package you are working on.
        There has to be a folder with the same name under ``dir_project_root``,
        And it has to have a ``__init__.py`` file in it.
    """

    dir_project_root: Path = dataclasses.field()
    package_name: str = dataclasses.field()
    py_ver_major: int = dataclasses.field()
    py_ver_minor: int = dataclasses.field()
    py_ver_micro: int = dataclasses.field()
    doc_host_aws_profile: str = dataclasses.field(default="")
    doc_host_s3_bucket: str = dataclasses.field(default="")
    doc_host_s3_prefix: str = dataclasses.field(default="")

    def _validate_paths(self):
        if isinstance(self.dir_project_root, Path) is False:
            self.dir_project_root = Path(self.dir_project_root)

        if (self.dir_project_root.joinpath("pyproject.toml").exists() is False) and (
            self.dir_project_root.joinpath("setup.py").exists() is False
        ):
            raise ValueError(
                f"{self.dir_project_root} does not have a pyproject.toml or setup.py file "
                f"it might not be a valid project root directory."
            )
        dir_python_lib = self.dir_project_root.joinpath(self.package_name)
        if dir_python_lib.joinpath("__init__.py").exists() is False:
            raise ValueError(
                f"{dir_python_lib} does not have a __init__.py file, "
                f"the package name {self.package_name} might be invalid."
            )

    def _validate_python_version(self):
        if self.py_ver_major != 3:
            raise ValueError(
                f"Python major version has to be 3, but got {self.py_ver_major}."
            )

    def _sanitize_attrs(self):
        if self.doc_host_s3_prefix.endswith("/"):
            self.doc_host_s3_prefix = self.doc_host_s3_prefix[:-1]

    def __post_init__(self):
        self._validate_paths()
        self._validate_python_version()
        self._sanitize_attrs()

    @classmethod
    def from_pyproject_toml(
        cls,
        path_pyproject_toml: Path,
    ):
        """
        Create the PyProjectOps instance from ``pyproject.toml`` file by reading
        the package name and python version information from it.

        It also compares the package version in the ``_version.py`` file with
        the version in ``pyproject.toml`` file, if they are not match, it will
        raise an error.
        """
        path_pyproject_toml = Path(path_pyproject_toml)
        toml_dict = tomllib.loads(path_pyproject_toml.read_text())
        package_name = toml_dict["project"]["name"]
        python_version = toml_dict["tool"]["pywf"]["dev_python"]
        major, minor, micro = [int(ver) for ver in python_version.split(".")]
        doc_host_aws_profile = toml_dict["tool"]["pywf"]["doc_host_aws_profile"]
        doc_host_s3_bucket = toml_dict["tool"]["pywf"]["doc_host_s3_bucket"]
        doc_host_s3_prefix = toml_dict["tool"]["pywf"]["doc_host_s3_prefix"]
        return cls(
            dir_project_root=path_pyproject_toml.parent,
            package_name=package_name,
            py_ver_major=major,
            py_ver_minor=minor,
            py_ver_micro=micro,
            doc_host_aws_profile=doc_host_aws_profile,
            doc_host_s3_bucket=doc_host_s3_bucket,
            doc_host_s3_prefix=doc_host_s3_prefix,
        )
