# -*- coding: utf-8 -*-

"""
Enumeration of important paths on local file system.
"""

import typing as T
import dataclasses

import tomllib
from pathlib import Path

from .helpers import identify_py_major_and_minor_version

if T.TYPE_CHECKING:  # pragma: no cover
    from .define import PyWf


@dataclasses.dataclass
class PyWfToml:
    """
    Namespace class for accessing important paths.
    """

    @classmethod
    def from_pyproject_toml(cls: T.Type["PyWf"], path_pyproject_toml: Path):
        """
        Create the PyProjectOps instance from ``pyproject.toml`` file by reading
        the package name and python version information from it.

        It also compares the package version in the ``_version.py`` file with
        the version in ``pyproject.toml`` file, if they are not match, it will
        raise an error.
        """
        path_pyproject_toml = Path(path_pyproject_toml)
        toml_dict = tomllib.loads(path_pyproject_toml.read_text())
        package_name = toml_dict["tool"]["poetry"]["name"]
        package_version = toml_dict["tool"]["poetry"]["version"]
        python_version = toml_dict["tool"]["poetry"]["dependencies"]["python"]
        major, minor = identify_py_major_and_minor_version(python_version)
        pywf: "PyWf" = cls(
            dir_project_root=path_pyproject_toml.parent,
            package_name=package_name,
            python_version=f"{major}.{minor}",
        )
        if pywf.package_version != package_version:
            raise ValueError(
                f"The version in {pywf.path_version_py} is {pywf.package_version}, "
                f"and the version in {path_pyproject_toml} is {package_version}, "
                f"they has to be match!"
            )
        return pywf
