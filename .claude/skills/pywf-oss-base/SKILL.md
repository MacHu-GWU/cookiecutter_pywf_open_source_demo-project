---
name: pywf-oss-base
description: "Shared conventions, scripts, and templates for the pywf-oss skills: how a pywf open-source Python library is laid out, styled, tested, documented, released, and wired to CI and hosting (mise, uv, ruff, pytest + run_cov_test, Sphinx + furo + docfly + nbsphinx, GitHub Actions, codecov.io, Read the Docs). Load it before creating or restructuring modules, tests, or docs in such a repo, or to answer questions about these conventions."
---

The conventions of the pywf open-source Python library template, shared by every `pywf-oss-*` skill. In all files, `<package>` is the import package directory (the `[project].name` of `pyproject.toml`, with `-` replaced by `_`).

## Files

| File | What it holds |
| :--- | :--- |
| `references/toolchain.md` | mise tasks, the Python version policy (3.11+), uv dependencies and extras, ruff and `# fmt: off`, python-fire CLIs |
| `references/repo-layout.md` | The repo tree; the special package files `api.py`, `paths.py`, `vendor/`, `<package>/tests/`, `<package>/docs/`; generated files |
| `references/code-style.md` | File header, the five-group import order and relative imports, 3.11+ type hints, privacy, docstrings |
| `references/testing.md` | The source-to-test path mapping, the test file template and its import order, the `run_cov_test` block, `all.py`, how to run tests, coverage and `# pragma: no cover` |
| `references/docs-sphinx.md` | The docs page tree, `.. autotoctree::`, reST heading and label rules, cross-reference roles, the docfly API reference, the doc build |
| `references/docs-notebook.md` | Notebook pages: raw reST cells for titles, cross-references, and directives; cell style; executing and committing outputs |
| `references/ci-and-hosting.md` | The GitHub Actions matrix, Codecov and Read the Docs setup tasks, the setup order for a new repo |
| `references/secrets.md` | `home_secret.toml` + `hst` through mise `[env]`, and the hard rules about never reading or printing secrets |
| `references/release.md` | Semantic versioning, the `release-history.rst` format, the release sequence and its approval gates |
| `references/workflow.md` | Which skill does what, the typical flows, and the handoffs between skills |
| `scripts/check_test_layout.py` | Lists missing, orphan, and mismatched test files; `--source <file>` prints the expected test path. Run: `python ${CLAUDE_SKILL_DIR}/scripts/check_test_layout.py --project_root .` (from an invoker: `${CLAUDE_SKILL_DIR}/../pywf-oss-base/scripts/...`) |
| `assets/raw-rst-cell.json` | A copy-ready raw reStructuredText notebook cell |
| `assets/notebook-page-template.ipynb` | A minimal notebook docs page: raw title cell, intro, code cell, cross-reference cell |

## Which skill for which job

| Skill | Reads from this base |
| :--- | :--- |
| `pywf-oss-add-module` | `repo-layout.md`, `code-style.md`, `testing.md`, `scripts/check_test_layout.py` |
| `pywf-oss-write-test` | `testing.md`, `code-style.md`, `scripts/check_test_layout.py` |
| `pywf-oss-write-doc` | `docs-sphinx.md`, `docs-notebook.md`, `assets/*` |
| `pywf-oss-changelog` | `release.md` |
| `pywf-oss-release` | `release.md`, `toolchain.md`, `ci-and-hosting.md`, `secrets.md` |
| `pywf-oss-write-pypi-skill` | `repo-layout.md` (section 2, `api.py`), `toolchain.md` (section 5, CLI) |
| `pywf-oss-audit` | all references, `scripts/check_test_layout.py` |

The flow between these skills is in `references/workflow.md`. For a question about a convention, read only the file that covers it.
