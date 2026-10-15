---
description: "Sphinx itself, independent of theme and extensions: conf.py, reStructuredText heading and label rules, the exact :mod: / :class: / :meth: / :func: / :attr: / :ref: / :doc: cross-reference forms and why a target can silently fail to resolve, the small built-in extensions (intersphinx, viewcode, copybutton, sphinx-jinja), and how to build and check the docs, including the AI visual check. Read when writing any reStructuredText, docstring cross-reference, or docs build check."
---

# Sphinx

The docs are a Sphinx project in `docs/source/`, configured by `docs/source/conf.py`. Pages are reStructuredText. The theme and each larger extension have their own reference.

---

## 1. reStructuredText conventions

Heading underlines are exactly **78 characters**, at three levels:

```rst
Page Title
==============================================================================

Section
------------------------------------------------------------------------------

Subsection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
```

- **Labels.** Put a label right above a title when other pages link to it. Labels are kebab-case, and unique across the whole project:

  ```rst
  .. _getting-started:

  Getting Started
  ==============================================================================
  ```

- **Code.** Inline code uses double backticks, ``` ``code`` ```. Code blocks use `.. code-block:: python`.
- **Links.** External links use `` `text <https://...>`_ ``.
- **Admonitions** (`.. note::`, `.. warning::`): use them sparingly.

---

## 2. Cross-references

These roles work the same way in `.rst` pages, in docstrings, and anywhere else reStructuredText is parsed. The sample page `docs/source/01-Sample-RestructuredText-Document/index.rst` of a template repo uses every form below.

### 2.1 Python objects

Always write the **full dotted path from the defining module**, not from the `api.py` re-export. Then pick the display form that reads best in the sentence:

| Target | Full path, displayed as written | Preferred display form | Renders as |
| :--- | :--- | :--- | :--- |
| Module | ``:mod:`<package_name>.module_name` `` | (same) | `<package_name>.module_name` |
| Class | ``:class:`<package_name>.module_name.ClassName` `` | ``:class:`~<package_name>.module_name.ClassName` `` | `ClassName` |
| Method | ``:meth:`<package_name>.module_name.ClassName.method_name` `` | ``:meth:`ClassName.method_name <<package_name>.module_name.ClassName.method_name>` `` | `ClassName.method_name()` |
| Function | ``:func:`<package_name>.module_name.func_name` `` | ``:func:`~<package_name>.module_name.func_name` `` | `func_name()` |
| Function, with its module | | ``:func:`module_name.func_name <<package_name>.module_name.func_name>` `` | `module_name.func_name()` |
| Module-level constant | ``:attr:`<package_name>.module_name.CONSTANT_NAME` `` | ``:attr:`~<package_name>.module_name.CONSTANT_NAME` `` | `CONSTANT_NAME` |
| Class attribute, field, or property | ``:attr:`<package_name>.module_name.ClassName.attr_name` `` | ``:attr:`ClassName.attr_name <<package_name>.module_name.ClassName.attr_name>` `` | `ClassName.attr_name` |

- `~` keeps only the last name. Use it when the context already makes the module obvious.
- `title <target>` displays any text you like. For a method, show `ClassName.method_name`, because a bare `method_name` loses its class.
- **Use the role that matches the object type:** `:meth:` for methods, `:func:` for functions, `:attr:` for constants, attributes, and fields. Sphinx may still resolve a mismatched role, but the rendering (for example, a trailing `()`) is wrong.

### 2.2 Why a target silently fails

A Python target resolves only if autodoc documented the object. That means:

- a function, class, or method needs a docstring;
- a constant or a field needs a `#:` doc comment (see `09-code-style.md`).

An unresolved target renders as plain code, not as a link, and **Sphinx gives no warning**. After a build, run:

```bash
python ${CLAUDE_SKILL_DIR}/../pywf-oss-base/scripts/check_doc_xrefs.py
```

It lists every reference that is not a link.

### 2.3 Pages, sections, and the standard library

| Target | Syntax |
| :--- | :--- |
| A labeled section or page | ``:ref:`getting-started` ``, or ``:ref:`custom text <getting-started>` `` |
| Another doc file, relative to the current page | ``:doc:`../03-Some-Topic/index` `` |
| Another doc file, from `docs/source/` | ``:doc:`/03-Some-Topic/index` `` |
| Python standard library (through intersphinx) | ``:class:`pathlib.Path` ``, ``:func:`json.dumps` `` |

---

## 3. Small extensions

These are enabled in `conf.py` and need no reference of their own:

| Extension | What it does |
| :--- | :--- |
| `sphinx.ext.intersphinx` | Resolves standard library cross-references |
| `sphinx.ext.viewcode` | Adds "[source]" links next to API entries |
| `sphinx-copybutton` | Adds a copy button to code blocks |
| `sphinx-jinja` | Renders data from code, through `.. jinja:: doc_data`. `doc_data` comes from `<package_name>/docs/__init__.py`. |

`rst_prolog` includes `_static/.custom-style.rst`, which defines the custom roles (colors, strike, and so on) available on every page.

---

## 4. Build and check

```bash
mise run build-doc   # clean build into docs/build/html
mise run view-doc    # open it in the browser
```

A docs change is done when:

- `build-doc` finishes with no new warnings;
- the cross-reference check reports 0 unresolved;
- the page appears in the sidebar with the right title and order.

**Visual check by an AI.**

- In the Claude desktop app, open the built site with the browser pane's `preview_start` and the `docs-html` configuration in `.claude/launch.json`. That configuration serves `docs/build/html` over HTTP, on the port the pane assigns.
- Do not open the files with `file://`. The pane then shows a static snapshot without CSS, so layout and theme cannot be judged.
- Humans keep using `mise run view-doc`: their browser loads CSS from `file://` without trouble.
