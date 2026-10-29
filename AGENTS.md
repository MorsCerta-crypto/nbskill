# Agent Notes

This is an nbdev notebook-source repository. `nbskill.skill` is the
authoritative notebook workflow here.

## Native nbskill Pyskill workflow

`nbskill.skill` owns the notebook workflow for aai-coding. Load its module documentation before notebook work; it defines the public operations and their order.

Route each file separately. A notebook goes to `nbskill.skill` directly. For a Python module, call `generated_owner(path)`: edit the returned notebook when it exists, and keep the file on the ordinary aai-coding path when it does not. A repository-level nbdev marker never routes every Python file through notebook tooling.

For notebook-owned work, use `context` to read the relevant cells and search the current package before a nontrivial implementation choice. Make one structured `edit_notebook` mutation using stable cell ids, then prove it with `exec_nb`, `diff_nb`, and `style_check`. For a behavior change, add or revise a focused notebook test before implementation when a useful reproducer exists. Run it before and after the edit; assert promised behavior rather than formatting or incidental order.

Do not edit raw notebook JSON or generated Python for normal notebook source changes. If a generated Python file needs work, inspect and edit the owning notebook unless the user explicitly asks otherwise.

Functions beginning with `_` are local to their notebook. If `style_check` reports a cross-notebook private-symbol call, promote the helper deliberately or remove the call before completing the task.

## Notebook Workflow

Work notebook-first and keep each change small. Prefer this shape for new
or revised behavior:

1. Markdown docs explain the behavior and name the public symbol.
2. Exported code implements the behavior in a focused cell.
3. A small example cell calls the behavior and shows useful output.
4. A small test cell checks one thing at a time.

Use the strength of notebooks. Markdown cells and example cells are part
of the implementation surface: they explain why the code exists, exercise
it in place, and show off how it is meant to work. When you edit a
notebook because of a bug, design constraint, production failure, or
surprising behavior, mention that reason in nearby markdown. A bugfix
should leave a small notebook artifact, such as "Here we have to do X
because Y", so future agents can see the current problem and the rationale
without rediscovering it.

Prefer markdown for durable context: name the problem being solved, record
important tradeoffs, and explain non-obvious implementation choices such
as using multiprocessing instead of asyncio. Keep it short and useful;
do not turn notebooks into a changelog, but do preserve the reasoning a
future maintainer needs.

Notebook directives matter:

- Cells exported to Python start with `#| export`.
- Cells that should not execute during the test phase include
  `#| eval: false`.
- Cells that should not appear in documentation, such as test cells,
  start with `#| hide`.

Keep edits surgical. Read the nearby notebook context, edit one coherent
piece, then immediately check whether the result is what you wanted
before continuing.

## Rewrite Incentive

Surgical does not mean timid. It is good to be unhappy with code that is
confusing, duplicated, brittle, or fighting the problem. When the existing
shape is the problem, prefer deleting it and rewriting the small scoped
behavior clearly instead of layering more patches on top.

Treat deletion as a first-class improvement when it removes needless
complexity. A rewrite should still be bounded: name the reason in nearby
markdown, keep the public contract intentional, add or update the focused
example/test, and verify the new shape. Do not preserve bad code merely
because it already exists.

## nbdev Development Shape

When creating or revising nbdev notebooks, keep the literate-programming
shape visible to the next reader:

- New source notebooks should declare their export target near the top with
  `#| default_exp module_name`. Add common imports such as
  `from nbdev.showdoc import show_doc` and `from fastcore.test import *`
  only when the notebook actually uses them.
- Keep imports in their own cell. The cell may contain several import lines, but no definitions, setup, examples, or tests.
- Public functions, classes, and methods live in `#| export` cells. Internal
  helpers that must be exported but should stay out of `__all__` use
  `#| exporti`. Do not add export directives to scratch, example, or test
  cells.
- Prefer small, typed public APIs with concise docstrings. Use nbdev
  docments comments on parameters and return values when they clarify the
  public contract, but preserve nearby style for existing code.
- Keep explanatory detail in markdown cells rather than long docstrings.
  Markdown should say why the behavior exists, what tradeoff is being made,
  and where future maintainers should look next.
- Put usage examples close to the behavior they demonstrate. Examples should
  be executable and useful; mark slow, flaky, external-service, or purely
  illustrative examples with `#| eval: false`.
- Put focused tests directly after the implementation or example they protect.
  Use `fastcore.test` helpers such as `test_eq`, `test_ne`, `test_close`,
  `test_is`, and `test_fail` where they fit. Test cells should normally start
  with `#| hide` so they validate the notebook without cluttering docs.
- For classes, keep the base class small. When a class grows across multiple
  concepts, prefer nbdev's `@patch` pattern in separate exported cells, with
  `self:ClassName` annotated on patched methods.
- Use visual examples only when the output helps understanding. Always pair a
  visual check with at least one programmatic assertion when the behavior can
  be asserted.

Common directives:

- `#| default_exp module_name`: notebook exports to this module.
- `#| export`: public exported code.
- `#| exporti`: internal exported code, omitted from `__all__`.
- `#| exports`: exported code that should show source in docs.
- `#| hide`: hide setup or tests from docs.
- `#| hide_input`: hide code while showing useful output.
- `#| hide_output`: hide noisy output while showing code.
- `#| eval: false`: skip execution during automated notebook tests.
- `#| exec_doc`: re-execute dynamic documentation content.

Do not add a manual `nbdev.nbdev_export()` cell to every notebook by default.
Use the repository's normal export and test commands, or the direct
verification functions from `nbskill.skill`, unless a notebook already follows that pattern.

## Search Before Writing

Before implementing a helper, search this package and its direct dependencies. Reuse or promote an existing operation when its contract fits.

Same-package searches:

- Use `context` for relevant source and search this package before a nontrivial notebook task.
- When only behavior is known, first locate the likely source with ordinary
  project search, then switch to the Pyskill before inspecting or changing
  notebook-owned code.

Examples found in this repo:

- `nbs/01_read.ipynb` has chapter helpers
  (`_chapter_title_from_cell`, `_chapter_spans_for_nb`,
  `_chapter_matches`, `_selected_chapter_span`) that are very similar to
  `nbs/00_foundation.ipynb` helpers (`_chapter_title`, `_chapter_spans`,
  `_matching_chapters`, `one_chapter`, `chapter_index_set`).
- `nbs/01_read.ipynb` repeats AST definition checks around
  `ast.FunctionDef`, `ast.AsyncFunctionDef`, and `ast.ClassDef` even
  though `nbs/00_foundation.ipynb` defines `is_definition_node`.

## Small Edit Loops

Prefer a tight loop:

1. Read with `context` and search the current package for prior implementations.
2. Make the smallest notebook-aware edit with `edit_notebook`.
3. Run `exec_nb`, `diff_nb`, and `style_check` for the behavior check, code diff,
   and changed-source diagnostics.
4. Only then continue to the next edit.

After exporting a library change, verify it in a clean process or restart the active kernel. Reloading one module can leave direct imports and patched classes stale.

Stop once the requested change is handled and verification is clear. Do
not broaden scope, reformat unrelated cells, or edit generated Python
directly when the notebook source should own the change.
