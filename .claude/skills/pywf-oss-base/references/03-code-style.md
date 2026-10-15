---
description: "The file header, one imported name per statement, the five-group import order with relative imports, Python 3.11+ type hints, privacy rules, and docstring and formatting conventions. Read before writing or reviewing any source code in the package."
---

# Code Style

These rules apply to source code under `<package>/`. Test files follow a different import order, described in `04-testing.md`.

---

## 1. File header

Every `.py` file starts with:

```python
# -*- coding: utf-8 -*-
```

A module docstring, if any, comes next. After that comes `from __future__ import annotations`, if needed (section 3).

---

## 2. Import order

Use five groups, in this order, with one blank line between groups:

1. **Special first**: `import typing as T`. This is the only way typing is imported.
2. **Standard library**: `import os`, `from pathlib import Path`, ...
3. **Third party**: `import boto3`, `from pydantic import BaseModel`, ...
4. **Close relatives**: distributions in the same ecosystem as this one, such as the author's other libraries this one is built on, or sibling distributions of one large project. Example: `from func_args.api import REQ`.
5. **This package, relative imports only**, ordered from farthest to nearest: `from ...x import`, then `from ..y import`, then `from .z import`. Distant modules are more like third-party code. The nearest ones are "my own" code and come last.

```python
# -*- coding: utf-8 -*-

"""
Module docstring.
"""

from __future__ import annotations

import typing as T
import json
from pathlib import Path

import httpx

from func_args.api import REQ

from ...utils import chunked
from ..exc import ParseError
from .model import Record

if T.TYPE_CHECKING:  # pragma: no cover
    from boto3 import S3Client
```

Rules:

- Inside `<package>/`, always use relative imports for the package's own modules. Never write `from <package>.x import y` there. That keeps the code tied to its position in the tree, not to the package name.
- **One imported name per statement**, everywhere: source, tests, `.mise/tasks`, and scripts.

  ```python
  # yes
  from .model import Record
  from .model import Field
  from github import Auth
  from github import Github

  # no
  from .model import Record, Field
  from github import (
      Auth,
      Github,
  )
  ```

  - Why: each line is one name, so diffs, `git blame`, and commenting a name in or out touch exactly one line, and `api.py` reads as a list of public names.
  - When a single long import is wrapped by `ruff format` into `from x import (\n    name,\n)`, that is still one name, and it is fine.
  - ruff cannot enforce this rule without also re-sorting imports and breaking the group order above. Check it, or split violations automatically, with `python ${CLAUDE_SKILL_DIR}/../pywf-oss-base/scripts/check_one_import_per_line.py --paths <package> tests [--fix]`.
- Put imports needed only for type hints under `if T.TYPE_CHECKING:  # pragma: no cover`, after all other imports.

---

## 3. Type hints (Python 3.11+)

- Use builtin generics and `|`: `list[str]`, `dict[str, int]`, `tuple[int, ...]`, `type[X]`, `X | None`, `A | B`.
- Never use `T.Optional`, `T.Union`, `T.List`, `T.Dict`, `T.Tuple`, `T.Set`, or `T.Type`.
- Use `T.` for names that only exist in `typing`: `T.Any`, `T.Callable`, `T.Iterable`, `T.Iterator`, `T.Literal`, `T.TypeVar`, `T.Self`, `T.TYPE_CHECKING`, `T.overload`.
- Every module with type annotations starts with `from __future__ import annotations`, so forward references need no quotes (`-> Node | None`). Pure re-export modules (`__init__.py`, `api.py`) do not need it.
- Annotate every public function and method, including the return type.

---

## 4. Naming and privacy

- A module, function, or attribute whose name starts with `_` is private. Other modules in the package may use it; `api.py` never exports it.
- Constants are `UPPER_CASE` at module level.

---

## 5. Docstrings and comments

- Docstrings use reStructuredText (Sphinx) fields: `:param name:`, `:returns:`, `:raises ExcType:`. They render through docfly and autodoc.
- Keep them thin. Say what the signature cannot say: behavior, side effects, raised errors, non-obvious constraints.
- Use `>>>` examples only when they show something non-obvious, and keep them runnable.
- Comments explain why, not what.
- Version history belongs in `release-history.rst`, not in code or comments. Use `.. versionadded:: x.y.z` or `.. versionchanged:: x.y.z` in a docstring when a public behavior changes.

---

## 6. Formatting

- `uvx ruff format` decides layout. Do not fight it, except with `# fmt: off` / `# fmt: on` around hand-aligned blocks (see `01-toolchain.md`).
- Prefer plain, explicit code: named temporaries, explicit `if` / `else`, bare `raise` to re-raise, `raise NewError(...) from e` to convert.
