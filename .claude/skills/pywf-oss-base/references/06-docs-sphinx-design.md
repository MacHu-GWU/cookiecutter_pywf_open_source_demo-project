---
description: "The sphinx-design widgets (grid, card, tabs, code tabs, dropdown, badge, button, icon) with one copy-ready reStructuredText example each, the syntax rules that break them silently, and which widget fits which page pattern. Read when a docs page needs layout or visual elements beyond plain text: a landing page, install instructions, an FAQ, a feature overview, or a call to action."
---

# Documentation: sphinx-design Widgets

[sphinx-design](https://sphinx-design.readthedocs.io/) (enabled in `conf.py`) adds responsive layout and UI widgets to reStructuredText. Every example below renders in `docs/source/03-Sample-Sphinx-Design-Gallery/index.rst`. Copy from there, and check your result against it.

In a notebook, write these directives in a raw reST cell (see `07-docs-notebook.md`).

---

## 1. Rules that break widgets silently

- **Indent with 4 spaces.** Child directives are indented under their parent. One wrong indent ends the parent early and renders the rest as plain text, often with no warning.
- **Options go directly under the directive line, then one blank line, then the content.** A blank line between the directive and an option turns the option into body text.
- **Colors** are semantic names: `primary`, `secondary`, `success`, `info`, `warning`, `danger`, `muted`, `light`, `dark`. Avoid `light`, `dark`, `white`, and `black` for text: they disappear in furo's dark mode or light mode.
- **Icons:** use `:octicon:` or `:material-regular:` (bundled). Never use the FontAwesome roles (`:fas:`, ...): this template does not load FontAwesome, so they render as nothing.
- **Links inside widgets:** `:link:` takes a label with `:link-type: ref`, a document path without extension with `:link-type: doc`, or a URL (the default). Prefer `ref`, so links survive renames. A `doc` path is relative to the current page; start it with `/` to go from `docs/source/` (`/api/<package>/__init__`).
- **Do not decorate for its own sake.** Use a widget only when the reader gains something: a choice between alternatives (tabs), optional detail (dropdown), a map of pages (cards), or status (badges).

---

## 2. Widgets

### Grid of cards: overviews and landing pages

```rst
.. grid:: 1 2 2 3
    :gutter: 3

    .. grid-item-card:: :octicon:`rocket;1.5em;sd-text-primary` Quick Start
        :link: sample-rst-document
        :link-type: ref

        Install and run your first example in two minutes.

    .. grid-item-card:: :octicon:`book;1.5em;sd-text-info` API Reference
        :link: /api/cookiecutter_pywf_open_source_demo/__init__
        :link-type: doc

        Every public class and function.
```

- `1 2 2 3` is the number of columns at the xs / sm / md / lg screen widths. A single number applies to all widths.
- A card with `:link:` is clickable as a whole. Do not put other links inside it.

### Card with header and footer

```rst
.. card:: Greeter
    :shadow: md

    Header text
    ^^^
    Body: greets people with a configurable word.
    +++
    Footer: see :class:`~cookiecutter_pywf_open_source_demo.example_module_1.Greeter`.
```

`^^^` ends the header and `+++` starts the footer. Both are optional. The directive argument is the card title.

### Tabs: alternatives the reader chooses between

```rst
.. tab-set::

    .. tab-item:: pip
        :sync: pip

        .. code-block:: bash

            pip install cookiecutter-pywf-open-source-demo

    .. tab-item:: uv
        :sync: uv

        .. code-block:: bash

            uv add cookiecutter-pywf-open-source-demo
```

Tab items with the same `:sync:` key switch together across every tab-set on the page. Use this for an OS or package-manager choice that repeats.

### Code tabs: the same thing in several languages

```rst
.. tab-set-code::

    .. code-block:: python

        greet("Alice")

    .. code-block:: bash

        python -c 'from cookiecutter_pywf_open_source_demo.api import greet; print(greet("Alice"))'
```

Each tab is labeled with the language of its code block. `literalinclude` works inside, too.

### Dropdown: optional detail, FAQ, long output

```rst
.. dropdown:: Why does the test file name repeat the folder path?
    :icon: question
    :color: info

    pytest needs unique test module basenames.
```

Add `:open:` to start expanded. `:icon:` takes an octicon name.

### Badges: status and labels inline

```rst
:bdg-success:`stable` :bdg-warning:`beta` :bdg-secondary-line:`optional`
:bdg-link-primary:`PyPI <https://pypi.org/project/cookiecutter-pywf-open-source-demo/>`
:bdg-ref-info:`see the sample <sample-rst-document>`
```

The roles are `:bdg-<color>:` (filled), `:bdg-<color>-line:` (outlined), `:bdg-link-<color>:` (URL), and `:bdg-ref-<color>:` (label). Badges work in table cells and headings.

### Buttons: one clear call to action

```rst
.. button-ref:: sample-rst-document
    :ref-type: ref
    :color: primary
    :shadow:

    Get Started

.. button-link:: https://github.com/MacHu-GWU/cookiecutter_pywf_open_source_demo-project
    :color: secondary
    :outline:

    :octicon:`mark-github` Source
```

Use at most one or two per page.

### Icons

```rst
:octicon:`check-circle;1em;sd-text-success` done
:material-regular:`warning;1.2em;sd-text-warning` careful
```

The syntax is `name;size;classes`. Find names at <https://primer.style/octicons/> and <https://fonts.google.com/icons>.

---

## 3. Styling hooks

- Card options: `:shadow: none|sm|md|lg`, `:text-align: center`, `:img-top: path`, `:class-card: sd-border-primary`.
- Grid options: `:gutter: 0-5`, `:margin:`, `:padding:`, `:outline:`.
- CSS utility classes, usable in any `:class*:` option or in `.. div:: <classes>`: `sd-text-<color>`, `sd-bg-<color>`, `sd-border-<color>`, `sd-font-weight-bold`, `sd-shadow-md`, `sd-rounded-3`, `sd-p-3`, `sd-m-3`.

---

## 4. Which widget for which page

| Page need | Widget |
| :--- | :--- |
| Landing page, or "what's in this section" | `grid` of `grid-item-card` with `:link:` and an icon in each title |
| Install or usage that differs by tool or OS | `tab-set` with `:sync:` keys |
| The same example in Python and in the shell | `tab-set-code` |
| FAQ, troubleshooting, long or optional detail | `dropdown`, one per question |
| Feature or support matrix | `list-table` with badges in the cells |
| "Next step" at the end of a guide | one `button-ref` |
