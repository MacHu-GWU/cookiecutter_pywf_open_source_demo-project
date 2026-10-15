---
description: "Jupyter notebook docs pages under nbsphinx: raw reStructuredText cells for titles, cross-references and directives (with the exact cell JSON), the page skeleton, code cell style, and how to execute and commit outputs. Read when creating or editing a .ipynb docs page."
---

# Documentation: Jupyter Notebooks with nbsphinx

A docs page can be `index.ipynb` instead of `index.rst`. nbsphinx renders it, and docfly's `.. autotoctree::` picks it up like any other page. Read `05-docs-sphinx.md` first, because folder naming, labels, and cross-reference syntax are the same.

Use a notebook when the page teaches by running code and the reader benefits from seeing real output. Use `.rst` for concepts, design notes, and maintainer docs.

---

## 1. The three cell types

| Cell | Used for | Rendered as |
| :--- | :--- | :--- |
| `code` | Runnable examples, with committed outputs | Code plus its output |
| `markdown` | Ordinary prose, lists, links, images | Markdown |
| `raw` with `raw_mimetype: text/restructuredtext` | Anything that needs Sphinx: the labeled page title, `:ref:` / `:class:` / `:func:` cross-references, directives (`.. note::`, `.. code-block::`, sphinx-design grids) | reStructuredText, parsed by Sphinx |

Markdown cells cannot use Sphinx roles or directives. When you need one, write that piece as a raw reST cell. nbsphinx documents this at <https://nbsphinx.readthedocs.io/en/0.9.8/raw-cells.html>.

---

## 2. Raw reST cell: the exact JSON

In JupyterLab or PyCharm, you make one by setting the cell type to *Raw* and the *Raw NBConvert Format* to *reStructuredText*. On disk, the cell looks like this:

```json
{
  "cell_type": "raw",
  "id": "a1b2c3d4",
  "metadata": {
    "raw_mimetype": "text/restructuredtext"
  },
  "source": [
    ".. _getting-started:\n",
    "\n",
    "Getting Started\n",
    "==============================================================================\n"
  ]
}
```

- `metadata.raw_mimetype` must be exactly `text/restructuredtext`. Without it, nbsphinx drops the cell from the HTML.
- `source` is a list of lines, each ending in `\n` except possibly the last.
- `assets/raw-rst-cell.json` in this skill is a copy-ready template.

---

## 3. Page skeleton

1. **Cell 1: raw reST.** The page label and title, with a 78-character `=` underline (as above). This gives the page a `:ref:` target and the title the sidebar shows.
2. **Markdown cell.** One paragraph: what the page shows and who it is for.
3. **Alternating cells.** Use markdown cells (`##` section headings, explanations) and code cells. Use a raw reST cell wherever a cross-reference or directive is needed.

Example raw cell in the middle of a page:

```rst
Every path is an instance of :class:`~<package>.core.S3Path`; see :ref:`getting-started`
for how to create one.

.. note::

    Writes are not atomic.
```

With nbsphinx 0.9.8 (the template's version), a raw-cell title shows correctly in the sidebar and in `.. autotoctree::`. This was checked against `docs/source/02-Sample-Jupyter-Notebook-Document/index.ipynb`, which is a working example of everything on this page. Some nbsphinx versions have failed to create the sidebar link for raw-cell titles (nbsphinx PR #834). If a page goes missing after an upgrade, put the title in a Markdown `# Title` cell instead, and keep the label in a raw cell above it.

---

## 4. Code cells: style

The reader learns one step at a time, so plain and explicit beats short.

- **One thing per cell**: one step, one result. Show a value as the last expression, or with `print(f"{x = }")`. To show three values, use three cells.
- Write the code a user would write: named variables, plain `for` loops, no clever comprehensions, lambdas, or helper functions defined just for the demo.
- Show an expected error explicitly, one error per cell:

  ```python
  try:
      do_bad_thing()
  except ValueError as e:
      print(f"{type(e).__name__}: {e}")
  ```

- Import from the public API (`from <package>.api import X`), exactly as users would.
- Never put inline code inside bold in markdown (`**``x``**`). Some editors render it badly.
- Never write secrets, account ids, or personal paths in a cell. Read them from environment variables.

---

## 5. Editing and running

- Edit cells with the `NotebookEdit` tool, or with `nbformat` in a script. Do not hand-edit the JSON of outputs.
- Outputs are committed, because Read the Docs shows what is stored in the file. Execute the notebook locally before committing:

  ```bash
  .venv/bin/jupyter nbconvert --to notebook --execute --inplace docs/source/02-Some-Topic/index.ipynb
  ```

  The `dev` extra installs `ipykernel`, so `mise run inst` is enough to make this work.
- If a notebook needs credentials or services that Read the Docs does not have, set `nbsphinx_execute = "never"` in `conf.py`, so the build uses only the committed outputs.
- `mise run notebook-to-markdown` converts the notebooks to Markdown. Use it when an AI needs to read the docs without the JSON noise.
- Then run `mise run build-doc` and check the rendered page: cross-references resolve (no "undefined label" warnings), raw cells render, and the page is in the sidebar.
