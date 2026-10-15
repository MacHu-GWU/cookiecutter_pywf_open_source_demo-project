---
name: pywf-oss-add-module
description: "Create a new module or subpackage in a pywf open-source Python library, together with its mirrored test file, its all.py, and its api.py export. Use when the user asks to add a module, file, subpackage, or new feature area to the package."
---

Scaffold a new module or subpackage, so that it follows the template's layout, import, and test conventions before any real logic is written.

Read ../pywf-oss-base/SKILL.md, then:
- ../pywf-oss-base/references/08-package-files.md
- ../pywf-oss-base/references/09-code-style.md
- ../pywf-oss-base/references/10-test-layout.md
- ../pywf-oss-base/references/11-test-writing.md

## Steps

1. **Pin down the target.**
   - Get the dotted path (`<package_name>.subpackage.module_name`), whether it is a module or a subpackage, and whether its names are public.
   - If the user gave only a feature description, propose a path and confirm it before creating files.
2. **Create the source.**
   - A module gets the file header, a one-line module docstring, and the imports it needs.
   - A subpackage gets `__init__.py` (header only) and, if it exposes names, its own `api.py`.
   - Every public function and class gets at least a one-line docstring.
3. **Create the test files.** Get each expected path from the script, never by hand:

   ```bash
   python ${CLAUDE_SKILL_DIR}/../pywf-oss-base/scripts/check_test_layout.py --project_root . --source <package_name>/subpackage/module_name.py
   ```

   - For a module, write the test file from the template: subject import on top, a placeholder test, and the `run_cov_test` block.
   - For a new subpackage folder, also create its `all.py`.
4. **Export.**
   - If the names are public, add one line per name to the nearest `api.py`. If the user wants it, also expose a new subpackage's `api` from the parent `api.py`.
   - Add a touch for each new name to the matching `test_..._api.py`.
5. **Verify.**
   - Run the layout check with no `--source`; it must report 0 problems.
   - Run the new test file with `.venv/bin/python tests/<...>.py`.
   - Run `mise run format`, then `mise run lint`; lint must report nothing.

## Output

List the files you created, the `api.py` lines you added, and the layout-check result. Next step: `pywf-oss-write-test`, once the logic is written.
