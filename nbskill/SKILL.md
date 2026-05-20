---
name: jupyter-notebooks
description: Work notebook-first in nbdev projects with nbskill MCP tools for reading, writing, updating, and executing notebooks without raw JSON.
---

# Jupyter Notebooks

Use this skill when a repository treats notebooks as source files,
especially nbdev projects where `nbs/*.ipynb` exports to Python modules.
Prefer the nbskill MCP server as the normal interface: inspect, edit,
execute, review, and diagnose notebooks through MCP tools instead of raw
`.ipynb` JSON, generated `.py` files, or ad hoc shell commands.

## Setup

Install the local package and register the MCP server:

``` bash
uv tool install --editable . --force
codex mcp add nbskill -- nbskill_mcp
claude mcp add nbskill -- nbskill_mcp
```

Call `healthcheck` first when MCP is available. If tools are missing,
run `uv run nbskill_status`, reconnect the MCP server, and then return
to the MCP workflow.

## Core Workflow

1.  Use `healthcheck` before notebook work or after
    reinstalling/exporting tool signatures.
2.  Use
    [`nb_overview`](https://MorsCerta-crypto.github.io/nbskill/read.html#nb_overview),
    then
    [`nb_chapter`](https://MorsCerta-crypto.github.io/nbskill/read.html#nb_chapter),
    then
    [`nb_cell`](https://MorsCerta-crypto.github.io/nbskill/read.html#nb_cell)
    as context needs become more precise.
3.  Use
    [`show_doc`](https://MorsCerta-crypto.github.io/nbskill/read.html#show_doc)
    for symbol-first rationale and
    [`symbol_graph`](https://MorsCerta-crypto.github.io/nbskill/graph.html#symbol_graph)
    for caller/callee impact.
4.  Keep notebook craft in the loop: preserve the story, add rationale
    before code, and put examples or tests after the behavior they
    exercise.
5.  Use
    [`write_nb`](https://MorsCerta-crypto.github.io/nbskill/write.html#write_nb),
    [`update_cell`](https://MorsCerta-crypto.github.io/nbskill/write.html#update_cell),
    or
    [`batch_edit_nb`](https://MorsCerta-crypto.github.io/nbskill/write.html#batch_edit_nb)
    for notebook edits; MCP tools apply requested changes directly.
    Use `split_before` or `split=True` on `update_cell` when breaking a
    large cell into focused smaller cells.
6.  Use
    [`exec_nb`](https://MorsCerta-crypto.github.io/nbskill/execute.html#exec_nb)
    for the narrowest behavior check, preferably with `check_only=True`
    when outputs do not need to be written.
7.  Finish with
    [`diff_nb`](https://MorsCerta-crypto.github.io/nbskill/review.html#diff_nb)
    plus `doctor(scopes="error,warning,style")` or
    [`style_check`](https://MorsCerta-crypto.github.io/nbskill/review.html#style_check)
    on touched notebooks.

Stay notebook-first: edit `nbs/*.ipynb` source notebooks, not generated
`.py` files. Functions beginning with `_` are notebook-local unless
deliberately promoted to a public helper.

## Notebook Craft

A good notebook has a story. Move one step at a time: describe the
problem, show the small behavior, export the implementation, demonstrate
it with visible output when useful, then protect it with a small test.
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

## CLI Fallback

Use CLI commands only when MCP tools are unavailable or final
verification must run inside the project environment. Reconnect MCP as
soon as practical; the CLI is a fallback, not the normal agent
interface.

``` bash
uv run nbskill_status
uv run nb_overview nbs/02_write.ipynb --include_docs
uv run nb_cell nbs/02_write.ipynb --query 'contains="def write_nb"'
uv run batch_edit_nb --plan_file /tmp/nbskill-plan.json --dry_run
uv run style_check nbs/02_write.ipynb --delete-after-output
uv run exec_nb nbs/03_execute.ipynb --up2id abc123 --timeout 10 --check_only
```

Use `cells_file`, `new_file`, or stdin when multiline shell quoting
would be fragile.

## References

Open references only when the core workflow is not enough:

- `references/mcp-tools.md` for detailed MCP behavior, reconnect notes,
  and concurrency behavior.
- `references/mcp-tool-report.md` for MCP feature groups and tool-count
  reduction candidates.
- `references/cli-fallbacks.md` for shell-friendly command patterns.
- `references/conversion.md` for converting Python files or folders with
  [`py2nb`](https://MorsCerta-crypto.github.io/nbskill/convert.html#py2nb).
- `references/extended-tools.md` for symbol docs, review, graph reports,
  and edit-interactive plans.
