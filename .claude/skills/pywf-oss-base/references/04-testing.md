---
description: "The source-to-test path mapping, the test file template and its import order, the run_cov_test block, all.py per folder, how to run tests, and coverage rules with # pragma: no cover. Read when creating, moving, or writing tests, or when checking coverage."
---

# Testing

Tests use pytest and pytest-cov. Every source module has exactly one test file, and every test file can run on its own as a script to report the coverage of just its module.

---

## 1. Source-to-test mapping

The `tests/` tree mirrors the `<package>/` tree. Directory names stay the same, and each **file name is prefixed with its full directory path**:

| Source | Test |
| :--- | :--- |
| `<package>/api.py` | `tests/test_api.py` |
| `<package>/utils.py` | `tests/test_utils.py` |
| `<package>/core/copy.py` | `tests/core/test_core_copy.py` |
| `<package>/a/b/c.py` | `tests/a/b/test_a_b_c.py` |
| `<package>/a/_private.py` | `tests/a/test_a__private.py` |
| `<package>/a/b/` (subpackage) | `tests/a/b/all.py` |
| `<package>/` (whole package) | `tests/all.py` |

Why the prefix: pytest's default rootdir-based import mode needs test module basenames to be unique. Without the prefix, `tests/a/test_api.py` and `tests/b/test_api.py` collide, and the whole run fails with "import file mismatch".

The following get **no** test file: `__init__.py`, `paths.py`, `_version.py`, `cli.py`, and anything under `vendor/`, `tests/`, or `docs/`. They match the `.coveragerc` omit list.

`tests/` subfolders have no `__init__.py`.

Run `python ${CLAUDE_SKILL_DIR}/../pywf-oss-base/scripts/check_test_layout.py --project_root .` to:

- list missing test files,
- list orphan test files that map to no module,
- list `run_cov_test` calls whose module argument does not match their file.

Add `--source <package>/x/y.py` to print the expected test path for one file.

Occasional exceptions are fine, for example one test file covering two tiny modules. Leave a comment saying why.

---

## 2. Test file template

```python
# -*- coding: utf-8 -*-

from <package>.core.copy import copy_file
from <package>.core.copy import CopyResult

import pytest

from pathlib import Path

from <package>.paths import path_enum


def test_copy_file():
    result = copy_file(...)
    assert isinstance(result, CopyResult)


class TestCopyResult:
    def test_to_dict(self):
        ...


if __name__ == "__main__":
    from <package>.tests import run_cov_test

    run_cov_test(
        __file__,
        "<package>.core.copy",
        preview=False,
    )
```

Import order in test files is different from source files:

1. **The subject under test first.** These are the functions and classes from the module this file maps to, imported with an absolute import from that exact module. They are the protagonists of the file, so they go on top.
2. `import pytest` and `import typing as T`, if needed.
3. Standard library.
4. Third party.
5. Other modules of this package, as absolute imports (`from <package>.x import y`), plus helpers from `<package>.tests`.

Test files always use absolute imports, never relative ones.

### The `run_cov_test` block

- It always sits in `if __name__ == "__main__":`, with the import inside the block.
- **One argument per line**, with a trailing comma. That way the user can toggle `preview=False` to `preview=True` (open the HTML report in a browser) by editing a single line.
- The second argument is the dotted module path of the source file this test file maps to.

---

## 3. `all.py`: one per tested folder

Every `tests/` folder that mirrors a subpackage has an `all.py` that runs every test in that folder, with coverage measured on the whole subpackage:

```python
# -*- coding: utf-8 -*-

if __name__ == "__main__":
    from <package>.tests import run_cov_test

    run_cov_test(
        __file__,
        "<package>.a.b",
        is_folder=True,
        preview=False,
    )
```

- `is_folder=True` makes pytest collect the whole folder that `__file__` is in, instead of the single file.
- `tests/all.py` covers the whole package (`"<package>"`).
- `all.py` has no test functions. Its name does not start with `test_`, so the full suite never collects it.

---

## 4. Running tests

| Goal | Command |
| :--- | :--- |
| One module, with its coverage | `.venv/bin/python tests/core/test_core_copy.py` |
| One subpackage, with its coverage | `.venv/bin/python tests/core/all.py` |
| Everything, with coverage | `mise run cov` |
| Everything, fast | `mise run test` |
| Ad-hoc selection | `.venv/bin/pytest tests/core -k copy` |

While developing a module, run its own test file and aim for 100% on that module. Before finishing, run `mise run cov`.

---

## 5. Coverage

- `.coveragerc` omits `docs/`, `tests/`, `vendor/`, `_version.py`, `cli.py`, and `paths.py`. It also excludes the usual lines: `if __name__ == "__main__":`, `raise NotImplementedError`, `def __repr__`, and so on.
- Use `# pragma: no cover` on a line or block that cannot or should not run in the unit test environment:
  - platform-specific branches,
  - `if T.TYPE_CHECKING:`,
  - defensive code for impossible states,
  - code that only runs against real external services.
- Never use it to hide logic you simply have not tested.
- Coverage is uploaded to codecov.io from CI (see `09-ci-and-hosting.md`).

---

## 6. Writing good tests

- Name test functions after what they test: `test_<function>`, or `test_<function>_<case>`. Group the tests of one class in `class Test<ClassName>:`.
- A test docstring is one or two lines: what is verified, and why it matters. Skip it when the name says it all.
- Use `pytest.mark.parametrize` for tests that differ only in data, instead of near-duplicate functions.
- Tests never depend on the order they run in or on the current working directory. Use `path_enum` or `tmp_path` for files.
- Tests that need real external services go in `tests_int/`, not `tests/`. They follow the same mapping rules.
