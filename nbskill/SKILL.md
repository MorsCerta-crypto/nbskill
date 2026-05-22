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
    public symbol targets. Verbose cell and symbol targets include
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
