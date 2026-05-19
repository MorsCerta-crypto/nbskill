---
name: jupyter-notebooks
description: Work notebook-first in nbdev projects with nbskill MCP tools for reading, writing, updating, and executing notebooks without raw JSON.
---

# Jupyter Notebooks

Use this skill when a repository treats notebooks as source files,
especially nbdev projects where `nbs/*.ipynb` exports to Python modules.
Keep the active workflow small: inspect notebooks, edit notebooks,
execute notebooks, and use references only when the task needs a
supporting tool.

## Setup

Install the local package and register the MCP server:

``` bash
uv tool install --editable . --force
codex mcp add nbskill -- nbskill_mcp
claude mcp add nbskill -- nbskill_mcp
```

Prefer the MCP server when it is available. Call `healthcheck` first to
confirm the server is alive, see the installed version, inspect
capabilities, and confirm concurrency policy. If MCP tools are missing,
run `uv run nbskill_status` to see the canonical command names and
reconnect instructions, then restart or reconnect the MCP client after
reinstalling nbskill.

## Core Workflow

1.  Use `nb_overview` for a compact map of section headers and exported
    definitions. Pass `include_markdown=True` when Markdown headings
    should be shown.
2.  Use `nb_chapter` when you know the relevant section and need the
    notebook head plus that chapter.
3.  Use `nb_cell` when you need precise, line-numbered source for one
    cell plus previous docs, examples/tests, and caller/callee context.
4.  Use
    [`write_nb`](https://MorsCerta-crypto.github.io/nbskill/write.html#write_nb)
    to add notebook cells by cell id, chapter, or full-notebook
    replacement. Use `cells_file` for multiline additions.
5.  Use
    [`update_cell`](https://MorsCerta-crypto.github.io/nbskill/write.html#update_cell)
    for precise edits to an existing cell by id, text replacement, or
    line range. Use `new_file` for multiline replacements and
    `source_hash` when stale context should fail instead of overwriting
    newer work.
6.  Use
    [`batch_edit_nb`](https://MorsCerta-crypto.github.io/nbskill/write.html#batch_edit_nb)
    for coordinated multi-cell or multi-notebook edits. Start with
    `dry_run=True`, include source hashes for guarded cells, and inspect
    the printed diffs before writing.
7.  Use
    [`style_check`](https://MorsCerta-crypto.github.io/nbskill/review.html#style_check)
    as the main hygiene report for large cells, mixed semantic cells,
    duplicate imports, cell-order problems, and global tool
    usage/problems.
8.  Use
    [`diff_nb`](https://MorsCerta-crypto.github.io/nbskill/review.html#diff_nb)
    to inspect code-cell diffs; use `git diff` for Markdown or
    documentation changes. nbskill metadata-only changes are summarized
    instead of expanded.
9.  Use
    [`exec_nb`](https://MorsCerta-crypto.github.io/nbskill/execute.html#exec_nb)
    to run a notebook, chapter, or cells up to an id, then inspect
    visible outputs and errors.

Stay notebook-first: edit `nbs/*.ipynb` source notebooks, not generated
`.py` files. Use stable cell ids and source hashes from `nb_cell` when
an edit must be guarded against stale context.
Functions beginning with `_` are notebook-local unless deliberately
promoted to a public helper.

## CLI Fallback

Use CLI commands only when MCP tools are unavailable or final
verification must run in the project environment:

``` bash
uv run nbskill_status
uv run nb_overview nbs/02_write.ipynb --include_markdown
uv run nb_chapter nbs/02_write.ipynb --name Writing
uv run nb_cell nbs/02_write.ipynb --query 'contains="def write_nb"'
uv run write_nb nbs/02_write.ipynb --after_id abc123 --cells_file /tmp/cells.txt --no-export
uv run write_nb nbs --old_str old_name --new_str new_name --dry_run --show_cells --no-export
uv run update_cell nbs/02_write.ipynb --cell_id abc123 --source_hash 7f3a91c0d422 --new_file /tmp/cell.txt --no-export
uv run batch_edit_nb --plan_file /tmp/nbskill-plan.json --dry_run
uv run diff_nb nbs/02_write.ipynb
uv run style_check nbs --delete-after-output
uv run private_symbol_report --path nbs
uv run exec_nb nbs/03_execute.ipynb --up2id abc123 --timeout 10
```

Cell blocks for
[`write_nb`](https://MorsCerta-crypto.github.io/nbskill/write.html#write_nb)
are separated by a line containing only `---`; start blocks with
`%%markdown`, `%%md`, `%%code`, or `%%raw` when the cell type matters.

## References

Open references only when the core workflow is not enough:

- `references/mcp-tools.md` for detailed MCP behavior, reconnect notes,
  and concurrency behavior.
- `references/mcp-tool-report.md` for MCP feature groups, usefulness
  tiers, and tool-count reduction candidates.
- `references/cli-fallbacks.md` for shell-friendly command patterns.
- `references/conversion.md` for converting Python files or folders with
  [`py2nb`](https://MorsCerta-crypto.github.io/nbskill/convert.html#py2nb).
- `references/extended-tools.md` for symbol docs, review, graph reports,
  and edit-interactive plans.
