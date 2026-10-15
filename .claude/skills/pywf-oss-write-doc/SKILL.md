---
name: pywf-oss-write-doc
description: "Write or update a Sphinx documentation page of a pywf open-source Python library, as reStructuredText or as a Jupyter notebook with raw reStructuredText cells for cross-references, then build and check it. Use when the user asks to document a feature, write a guide or tutorial page, add a notebook example, or fix the docs."
---

Write or update one docs page under `docs/source/`, so that it builds cleanly, appears in the sidebar, and links correctly to the API reference and to other pages.

Read ../pywf-oss-base/SKILL.md, then:
- ../pywf-oss-base/references/13-sphinx.md
- ../pywf-oss-base/references/14-docfly.md
- ../pywf-oss-base/references/15-furo.md (only when changing the look or the theme)
- ../pywf-oss-base/references/16-sphinx-design.md (only when the page needs layout or widgets: cards, tabs, dropdowns, badges, buttons)
- ../pywf-oss-base/references/17-nbsphinx.md (only for notebook pages)

Templates: ../pywf-oss-base/assets/notebook-page-template.ipynb and ../pywf-oss-base/assets/raw-rst-cell.json.

## Steps

1. **Pick the format and the place.**
   - Use a notebook for runnable usage guides, and `.rst` for concepts and design notes. If the user did not say, choose, and state your choice.
   - List the existing page folders. Then choose the `NN-Title` folder, so the page lands at the right position in the sidebar.
2. **Gather facts.** Read the public API (`api.py`) and the docstrings of what you document. Examples import from `<package_name>.api`, as users would.
3. **Write.**
   - Give the page a unique label and a title (in a notebook, both go in a raw reStructuredText cell).
   - Use cross-reference roles for API names, and `:ref:` for other pages.
   - Edit notebooks with `NotebookEdit` or `nbformat`.
4. **Run notebooks:** `.venv/bin/jupyter nbconvert --to notebook --execute --inplace <notebook_path>`. Every cell must succeed, and the outputs are committed.
5. **Build and check,** as in `13-sphinx.md` section 4:
   - the build passes with no new warnings;
   - `python ${CLAUDE_SKILL_DIR}/../pywf-oss-base/scripts/check_doc_xrefs.py` reports 0 unresolved;
   - the page is in the sidebar with the right title;
   - for layout work, run the visual check.

## Boundaries

- Never edit `docs/source/api/`. To improve the API pages, improve the docstrings, and say so.
- Keep `README.rst` short. Long material goes in a docs page that the README links to.

Next step: `pywf-oss-changelog`.
