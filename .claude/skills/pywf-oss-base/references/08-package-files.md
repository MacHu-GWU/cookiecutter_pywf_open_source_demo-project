---
description: "The special files inside the package: api.py as the only public API, paths.py with absolute paths, private _ modules, vendor/ for copied code, the test helpers in <package_name>/tests/, doc data in <package_name>/docs/, the optional _version.py, and a python-fire cli.py. Read when adding a public name, a path, a CLI, or anything that is not an ordinary module."
---

# Special Files in the Package

```text
<package_name>/
├── __init__.py      # minimal
├── api.py           # THE public API
├── paths.py         # every project path, absolute
├── _version.py      # optional: __version__ and metadata
├── cli.py           # optional: python-fire CLI
├── module_name.py   # ordinary modules
├── _module_name.py  # private modules
├── subpackage/      # may have its own api.py
├── vendor/          # copied third-party code
├── tests/           # test helpers (not tests)
└── docs/            # data for the docs
```

---

## 1. `api.py`: the public API

- Users import only through `api.py`. There are two canonical forms:

  ```python
  from <package_name>.api import ClassName
  import <package_name>.api as <package_name>  # then <package_name>.ClassName
  ```

- `api.py` holds only re-exports, one name per line, as relative imports:

  ```python
  # -*- coding: utf-8 -*-

  from .module_name import ClassName
  from .module_name import func_name
  from .module_name import CONSTANT_NAME
  from .subpackage import api as subpackage
  ```

- A subpackage that forms a coherent unit gets its own `subpackage/api.py`. The top-level `api.py` exposes it as a module, as in the last line above.
- **Anything not in `api.py` is internal**, and may change in any release.
- Adding a name to `api.py` is a feature; removing or renaming one is a breaking change.
- `tests/test_api.py` touches every exported name, so a broken re-export fails CI.

---

## 2. Private modules and names

- A module, function, or attribute whose name starts with `_` is private.
- Other modules of the package may use it, but `api.py` never exports it.

---

## 3. `paths.py`: absolute paths only

- `PathEnum` lists every directory and file that the code or the tests need, built from `Path(__file__)`. Nothing depends on the current working directory.
- Use `from .paths import path_enum`, then `path_enum.dir_project_root`, `path_enum.dir_htmlcov`, and so on.
- Need a new path? Add an attribute: `dir_*` for a directory, `path_*` for a file. Never build paths inline.

---

## 4. `vendor/`: copied third-party code

- Small, single-file utilities copied in, so the package does not take a dependency for them.
- Do not restyle a vendored file. Update it only by copying a newer upstream version.

---

## 5. `<package_name>/tests/` and `<package_name>/docs/`

- `<package_name>/tests/` holds test **helpers**, such as `run_cov_test` and shared fixtures, so that test files can import them. The tests themselves live in the top-level `tests/`.
- `<package_name>/docs/` holds `doc_data`, a dict that docs pages can render.
- Both are excluded from the wheel (`[tool.setuptools.packages.find] exclude` in `pyproject.toml`).

---

## 6. Version

- `pyproject.toml` `[project].version` is the single source of truth.
- If `_version.py` exists, its `__version__` must equal it. Change both together.

---

## 7. `cli.py` (only if the package has a command line interface)

- **Use [python-fire](https://github.com/google/python-fire).** `cli.py` has a class whose public methods are the subcommands, and a `main()` that calls `fire.Fire(TheClass)`.
- Register the command in `[project.scripts]`, for example `cli-name = "<package_name>.cli:main"`, and add `fire` to `dependencies`.
- Keep `cli.py` thin. It parses arguments and calls functions in ordinary modules, so the logic stays testable.

---

## 8. Excluded from coverage and from the API docs

`paths.py`, `_version.py`, `cli.py`, `vendor/`, `tests/`, and `docs/`. The test, coverage, and docs references rely on this list.
