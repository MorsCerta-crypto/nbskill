# Agent Notes

This is an nbdev notebook-source repository. The nbskill MCP server is
the normal interface for notebook work here.

## Mandatory nbskill MCP Workflow

Use nbskill MCP tools for any task involving:

- `nbs/**/*.ipynb` or another source notebook.
- Python modules generated from nbdev notebooks.
- Notebook execution, order, outputs, examples, or tests.
- Symbol lookup, call impact, implementation search, or refactoring in
  notebook-owned code.
- Notebook style, review, diagnostics, conversion, or migration.

For those tasks:

1. Call `mcp__nbskill__.healthcheck` first.
2. Read with `mcp__nbskill__.context` or `mcp__nbskill__.filter_context`.
3. Search indexed prior art with `mcp__nbskill__.reference` before
   adding nontrivial parsing, notebook, AST, filesystem, or formatting
   behavior.
4. Edit notebooks only with `mcp__nbskill__.edit_notebook`, using stable
   cell ids or narrow line edits and expected hashes when available.
5. Verify with the smallest useful MCP check:
   `mcp__nbskill__.diff_nb`, `mcp__nbskill__.exec_nb(check_only=True)`,
   `mcp__nbskill__.style_check`, or `mcp__nbskill__.doctor`.

Do not edit raw notebook JSON or generated Python for normal notebook
source changes. If a generated Python file needs work, inspect and edit
the owning notebook unless the user explicitly asks otherwise.

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

## Search Before Writing

Before implementing a helper, first search for the behavior in this
package and then in indexed reference implementations. Do not write a
second near-copy just because the existing helper is private or lives in
another notebook; decide whether to reuse it, promote it, import it, or
intentionally keep a local variant.

Same-package searches:

- Use `mcp__nbskill__.context(target="<likely_symbol>", scope="nbs",
  overview=True)` when a likely symbol name exists.
- Use `mcp__nbskill__.filter_context(scope="nbs",
  include_re="<domain terms>")` when only behavior is known. Search by
  nouns, error text, data keys, AST node names, regexes, or library
  calls.
- Use `mcp__nbskill__.context` on the returned symbol to inspect callers
  and callees before deciding to add code.

Reference searches:

- Use `mcp__nbskill__.reference(action="query",
  query="<behavior and domain terms>", top_k=5)` before building
  nontrivial parsing, notebook, AST, filesystem, or formatting behavior.
- If a reference hit is from an already-direct dependency, prefer
  importing or adapting its pattern. If it would add a new dependency,
  treat it as prior art unless the dependency is explicitly acceptable.

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

1. Read with `mcp__nbskill__.context` or
   `mcp__nbskill__.filter_context`.
2. Make the smallest notebook-aware edit with
   `mcp__nbskill__.edit_notebook`.
3. Run a focused `mcp__nbskill__.exec_nb(check_only=True)`,
   `mcp__nbskill__.style_check`, `mcp__nbskill__.diff_nb`, or
   `mcp__nbskill__.doctor`.
4. Only then continue to the next edit.

Stop once the requested change is handled and verification is clear. Do
not broaden scope, reformat unrelated cells, or edit generated Python
directly when the notebook source should own the change.
