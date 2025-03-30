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
    # PyWfToml,
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
    toml_data: T.Dict[str, T.Any] = dataclasses.field()

    # --------------------------------------------------------------------------
    # [project]
    # --------------------------------------------------------------------------
    @property
    def package_name(self) -> str:
        return self.toml_data["project"]["name"]

    @property
    def package_version(self) -> str:
        return self.toml_data["project"]["version"]

    @property
    def package_license(self) -> str:
        return self.toml_data["project"]["license"]

    @property
    def package_description(self) -> str:
        return self.toml_data["project"]["description"]

    @property
    def package_author_name(self) -> str:
        return self.toml_data["project"]["authors"][0]["name"]

    @property
    def package_author_email(self) -> str:
        return self.toml_data["project"]["authors"][0]["email"]

    @property
    def package_maintainer_name(self) -> str:
        return self.toml_data["project"]["maintainers"][0]["name"]

    @property
    def package_maintainer_email(self) -> str:
        return self.toml_data["project"]["maintainers"][0]["email"]

    # --------------------------------------------------------------------------
    # [tool.pywf]
    # --------------------------------------------------------------------------
    @property
    def py_ver_major(self) -> int:
        return int(self.toml_data["tool"]["pywf"]["dev_python"].split(".")[0])

    @property
    def py_ver_minor(self) -> int:
        return int(self.toml_data["tool"]["pywf"]["dev_python"].split(".")[1])

    @property
    def py_ver_micro(self) -> int:
        return int(self.toml_data["tool"]["pywf"]["dev_python"].split(".")[2])

    @property
    def doc_host_aws_profile(self) -> str:
        return self.toml_data["tool"]["pywf"]["doc_host_aws_profile"]

    @property
    def doc_host_s3_bucket(self) -> str:
        return self.toml_data["tool"]["pywf"]["doc_host_s3_bucket"]

    @property
    def doc_host_s3_prefix(self) -> str:
        doc_host_s3_prefix = self.toml_data["tool"]["pywf"]["doc_host_s3_prefix"]
        if doc_host_s3_prefix.startswith("/"):
            doc_host_s3_prefix = doc_host_s3_prefix[1:]
        if doc_host_s3_prefix.endswith("/"):
            doc_host_s3_prefix = doc_host_s3_prefix[:-1]
        return doc_host_s3_prefix

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

    def _update_version_file(self):
        dir_here = Path(__file__).absolute().parent
        path_version_tpl = dir_here / "_version.tpl"
        content = path_version_tpl.read_text(encoding="utf-8").format(
            version=self.package_version,
            description=self.package_description,
            license=self.package_license,
            author=self.package_author_name,
            author_email=self.package_author_email,
            maintainer=self.package_maintainer_name,
            maintainer_email=self.package_maintainer_email,
        )
        self.path_version_py.write_text(content, encoding="utf-8")

    def __post_init__(self):
        self._validate_paths()
        self._validate_python_version()
        self._update_version_file()

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
        toml_data = tomllib.loads(path_pyproject_toml.read_text())
        return cls(
            dir_project_root=path_pyproject_toml.parent,
            toml_data=toml_data,
        )
