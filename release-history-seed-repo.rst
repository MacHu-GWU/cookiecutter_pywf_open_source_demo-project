Seed Repo Release and Version History
==============================================================================
The changelog of this **seed repo** itself. The seed is a runnable project that `cookiecutter-pywf_open_source <https://github.com/MacHu-GWU/cookiecutter-pywf_open_source>`_ (the template repo) turns into a cookiecutter template, so every change here is a change to what newly generated projects get.

- The seed and the template repo share one version number. The source is ``version`` in this repo's ``pyproject.toml``; the template repo copies it and refuses to publish when the two differ.
- ``release-history.rst`` is template content: the starting changelog of every generated project. It never records the seed's own changes, and is never edited for a seed release.
- This file is excluded from the template. Each template release links to its section here.


x.y.z (Backlog)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


3.0.1 (2026-10-23)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Miscellaneous**

- No changes to what generated projects get; this version re-tags the seed after ``3.0.0``, so the tag includes this changelog.


3.0.0 (2026-10-23)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
First release recorded in this file. The version jumps from ``1.0.5`` to ``3.0.0`` because the seed and the template repo now share one version number, starting above both previous versions (seed ``1.0.5``, template ``2.1.0``). Nothing generated projects receive is incompatible with the previous release. This section describes everything a project generated from this seed gets.

**Features and Improvements**

- **Package layout:** ``api.py`` as the only public API, one re-export per line; ``paths.py`` with every project path as an absolute ``PathEnum`` attribute; private ``_`` modules; ``vendor/`` for copied third-party code; test helpers in ``<package_name>/tests/`` and docs data in ``<package_name>/docs/``, both excluded from the wheel
- **Sample code:** ``example_module_1`` and the subpackage ``example_package_1`` with its own ``api.py``, both exposed through the top-level ``api.py``
- **Tests:** ``tests/`` mirrors the package path (``<package_name>/a/b/c.py`` maps to ``tests/a/b/test_a_b_c.py``), one ``all.py`` per tested folder, a ``run_cov_test`` block per test file, and ``tests/test_api.py`` touching every exported name
- **Python:** 3.11+ (``requires-python = ">=3.11,<4.0"``), classifiers and the CI matrix for 3.11 to 3.14, one dev Python pinned in ``mise.toml``
- **Dependencies with uv:** runtime dependencies plus the ``dev``, ``test``, ``doc``, and ``mise`` extras, a ``>=floor,<next major`` constraint policy, a committed ``uv.lock``, and ``requirements*.txt`` exported from it
- **mise as the single entry point:** ``venv-create``, ``venv-remove``, ``inst``, ``format``, ``lint``, ``test``, ``cov``, ``view-cov``, ``build-doc``, ``view-doc``, ``notebook-to-markdown``, ``export``, ``build``, ``publish``, ``release``, ``update-github-metadata``, ``setup-codecov``, ``setup-readthedocs``
- **Secrets from** ``$HOME/home_secret.toml`` through the ``hst`` CLI in ``mise.toml`` ``[env]`` (``GITHUB_TOKEN``, ``CODECOV_TOKEN``, ``READTHEDOCS_TOKEN``, ``PYPI_TOKEN``); a secret that cannot be read becomes an empty string, so tasks that do not need it keep working
- **Lint and format:** ruff format, a small ruff rule set (F401, F821, F841), and a one-imported-name-per-statement check
- **Docs:** Sphinx with furo, docfly-generated API reference, nbsphinx notebooks, sphinx-design, sphinx-copybutton, sphinx-jinja; sample pages for reStructuredText, a Jupyter notebook, and a sphinx-design gallery; ``.claude/launch.json`` to preview the built HTML on port 8765
- **CI:** GitHub Actions on ``ubuntu-latest`` and ``windows-latest`` times every supported Python, a ``.venv`` cache keyed on the full Python version and ``uv.lock``, and a Codecov upload
- **Hosting:** Read the Docs built with uv and the ``mise.toml`` Python; Codecov; PyPI publish and GitHub release tasks; one-time setup tasks for GitHub metadata, Codecov, and Read the Docs
- **AI ready:** a ``CLAUDE.md`` with a project block and a shared template block, and the ``pywf-oss-*`` Claude Code skill family (setup machine and repo, add module, write test, write doc, changelog, release, write the PyPI API skill, write the maintenance skill family, fix CI, upgrade dependencies, add community skills, audit), backed by ``pywf-oss-base`` references and checker scripts
- **Knowledge channels:** user docs in Sphinx, the API in a ``pypi-<package_name>`` skill, and maintenance knowledge in a ``maintain-<package_name>-*`` skill family, never in a maintainer guide in the docs
- **Community skills:** a pinned catalog of optional third-party skills, installed only after a security review and git-ignored by default

**Miscellaneous**

- New ``release-history-seed-repo.rst`` (this file) and the seed-only ``pywf-oss-changelog-seed-repo`` skill that maintains it; both stay out of the template
