---
name: jupyter-notebooks
description: Work notebook-first in nbdev projects with nbskill MCP tools for reading, writing, updating, and executing notebooks without raw JSON.
---

# Jupyter Notebooks

Use this skill when a repository treats notebooks as source files,
especially nbdev projects where `nbs/*.ipynb` exports to Python modules.
Prefer the nbskill MCP server as the normal interface: inspect, edit,
execute, review, and diagnose notebooks through MCP tools instead of raw
`.ipynb` JSON, generated `.py` files, or ad hoc file manipulation.

## Setup

Call `healthcheck` first when MCP tools are available. It confirms the
server is alive, reports capabilities, and gives reconnect hints when
the client is using stale tool metadata.

## Core Workflow

1.  Use `healthcheck` before notebook work or after
    reinstalling/exporting tool signatures.
2.  Use `context` for project, notebook, chapter title, cell id, or
    public symbol targets. Cell and symbol targets include
    graph-oriented caller/callee impact.
3.  Keep notebook craft in the loop: preserve the story, add rationale
    before code, and put examples or tests after the behavior they
    exercise.
4.  Use `edit_notebook` for notebook edits. It supports whole-cell
    replacement, line edits, cell insertion/deletion/moves, and
    notebook-wide `replace_text`/`replace_texts` refactors with
    expected-hash guards and structured diffs.
5.  Use
    [`exec_nb`](https://MorsCerta-crypto.github.io/nbskill/execute.html#exec_nb)
    for the narrowest behavior check, preferably with `check_only=True`
    when outputs do not need to be written.
6.  Finish with
    [`diff_nb`](https://MorsCerta-crypto.github.io/nbskill/review.html#diff_nb)
    plus `doctor(scopes="error,warning,style")` or
    [`style_check`](https://MorsCerta-crypto.github.io/nbskill/review.html#style_check)
    on touched notebooks.

Stay notebook-first: edit `nbs/*.ipynb` source notebooks, not generated
`.py` files. Functions beginning with `_` are notebook-local unless
deliberately promoted to a public helper.

## Search Before Writing

Before adding a helper, search for an existing implementation in both
the current package and indexed reference packages. Prefer reusing,
promoting, or lightly adapting known code over writing a parallel helper
with a new name.

For same-package searches, start with symbol and behavior queries:

- Use `context(target="<likely_symbol>", scope="nbs", overview=True)`
  when you can guess a symbol name.
- Use `filter_context(scope="nbs", include_re="<domain terms>")` when
  you only know the behavior, data shape, AST pattern, error message, or
  important library calls.

For external prior art, use
`reference(action="query", query="<behavior and domain terms>", top_k=5)`.
Treat results as examples to inspect, not code to copy blindly; prefer
direct imports only when the dependency is already appropriate.

Concrete duplication patterns to avoid:

- Chapter helpers in `nbs/01_read.ipynb` (`_chapter_title_from_cell`,
  `_chapter_spans_for_nb`, `_chapter_matches`, `_selected_chapter_span`)
  are close to `nbs/00_foundation.ipynb` helpers (`_chapter_title`,
  `_chapter_spans`, `_matching_chapters`, `one_chapter`,
  `chapter_index_set`). Queries that would have found them:
  `context(target="_chapter_spans", scope="nbs", overview=True)` and
  `filter_context(scope="nbs", include_re="chapter.*span|_chapter_spans|one_chapter|chapter_index_set")`.
- AST definition checks recur under different names. Before writing
  `isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))`
  or another symbol-discovery loop, search for
  `context(target="is_definition_node", scope="nbs", overview=True)` and
  `filter_context(scope="nbs", include_re="is_definition_node|FunctionDef|AsyncFunctionDef|ClassDef")`.
- Notebook/source mapping and AST-location logic has useful external
  prior art. Queries such as
  `reference(action="query", query="notebook cells markdown headings chapter spans start end title", top_k=5)`
  and
  `reference(action="query", query="ast FunctionDef AsyncFunctionDef ClassDef definition node helper", top_k=5)`
  surface implementations like `fastaistyle` notebook-cell mapping and
  AST helpers from other nbdev-style packages.

## Notebook Craft

A good notebook has a story. Move one step at a time: describe the
problem in Markdown, export the implementation, demonstrate it with a
small example and visible output when useful, then protect it with a
small test.
Larger features should grow from earlier cells rather than appear as one
big code block.

Keep cells small and semantic. A cell should usually be one of these
things: Markdown rationale, imports, exported code, private
implementation, a visible example, or a focused test. Avoid cells that
mix several jobs, duplicate imports, hide unused code, or bundle many
assertions together.

Documentation should explain the shape of the code, not just repeat it.
Say why the behavior exists, what problem it solves, what tradeoff it
chooses, and why an obvious alternative is not being used. For shared
helpers, include cross-references: where the symbol is called, why those
callers need it, and whether a private helper should be promoted before
another notebook imports it.

Examples should be executable and useful to a reader. Prefer short
examples close to the feature they demonstrate, with visible outputs
when the output helps understanding. Tests should be small, local, and
named by the single behavior they protect.

Notebook directives matter:

- Cells exported to Python start with `#| export`.
- Cells that should not execute during the test phase include
  `#| eval: false`.
- Cells that should not appear in documentation, such as test cells,
  start with `#| hide`.

## References

Open references only when the core workflow is not enough:

- `references/mcp-tools.md` for detailed MCP behavior, reconnect notes,
  and concurrency behavior.
- `references/mcp-tool-report.md` for MCP feature groups and tool-count
  reduction candidates.
- `references/conversion.md` for converting Python files, folders, or
  projects with `convert`.
- `references/extended-tools.md` for symbol docs, review, graph reports,
  and edit-interactive plans.
