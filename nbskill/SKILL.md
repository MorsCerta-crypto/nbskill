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
codex mcp add nbskill -- nbskill-mcp
claude mcp add nbskill -- nbskill-mcp
```

Prefer the MCP server when it is available. Call `healthcheck` first to
confirm the server is alive, see the installed version, inspect
capabilities, and confirm concurrency policy. After reinstalling or
exporting new MCP tool signatures, fully restart or reconnect the MCP
client so it refreshes cached schemas.

## Core Workflow

1.  Use
    [`read_nb`](https://MorsCerta-crypto.github.io/nbskill/read.html#read_nb)
    to inspect notebooks without raw JSON. Start with
    `context="overview"` and use `context="precise"` when you need
    numbered source for a selected cell. Quote query values with spaces,
    such as `query='contains="def write_nb"'`.
2.  Use
    [`write_nb`](https://MorsCerta-crypto.github.io/nbskill/write.html#write_nb)
    to add notebook cells by cell id, chapter, or full-notebook
    replacement. Use `cells_file` for multiline additions.
3.  Use
    `write_nb(path, old_str="old", new_str="new", dry_run=True, show_cells=True)`
    to preview exact literal replacements with touched cell ids and
    compact diffs before writing.
4.  Use
    [`update_cell`](https://MorsCerta-crypto.github.io/nbskill/write.html#update_cell)
    for precise edits to an existing cell by id, text replacement, or
    line range. Use `source_hash` when stale context should fail instead
    of overwriting newer work.
5.  Use
    [`diff_nb`](https://MorsCerta-crypto.github.io/nbskill/review.html#diff_nb)
    to inspect code-cell diffs; use `git diff` for Markdown or
    documentation changes. nbskill metadata-only changes are summarized
    instead of expanded.
6.  Use
    [`exec_nb`](https://MorsCerta-crypto.github.io/nbskill/execute.html#exec_nb)
    to run a notebook, chapter, or cells up to an id, then inspect
    visible outputs and errors. Execution is safe by default: fresh or
    changed cells are denied unless the user already ran them or nbskill
    has a matching execution stamp. Use `allow_new=True` only after the
    user has explicitly approved that source; use `safe=False` only when
    unsafe legacy execution is deliberately required.

Stay notebook-first: edit `nbs/*.ipynb` source notebooks, not generated
`.py` files. Use stable cell ids and source hashes from
`read_nb --show_ids` when an edit must be guarded against stale context.
Functions beginning with `_` are notebook-local unless deliberately
promoted to a public helper.

## CLI Fallback

Use CLI commands only when MCP tools are unavailable or final
verification must run in the project environment:

``` bash
uv run read_nb nbs/02_write.ipynb --context overview --show_ids
uv run read_nb nbs/02_write.ipynb --context precise --query 'contains="def write_nb"'
uv run write_nb nbs/02_write.ipynb --after_id abc123 --cells_file /tmp/cells.txt --no-export
uv run write_nb nbs --old_str old_name --new_str new_name --dry_run --show_cells --no-export
uv run update_cell nbs/02_write.ipynb "replacement line" --cell_id abc123 --line_range 3 --source_hash 7f3a91c0d422 --no-export
uv run diff_nb nbs/02_write.ipynb
uv run private-symbol-report --path nbs
uv run exec_nb nbs/03_execute.ipynb --up2id abc123 --timeout 10 --allow_new
```

Cell blocks for
[`write_nb`](https://MorsCerta-crypto.github.io/nbskill/write.html#write_nb)
are separated by a line containing only `---`; start blocks with
`%%markdown`, `%%md`, `%%code`, or `%%raw` when the cell type matters.

## References

Open references only when the core workflow is not enough:

- `references/mcp-tools.md` for detailed MCP behavior, reconnect notes,
  and concurrency behavior.
- `references/cli-fallbacks.md` for shell-friendly command patterns.
- `references/conversion.md` for converting Python files or folders with
  [`py2nb`](https://MorsCerta-crypto.github.io/nbskill/convert.html#py2nb).
- `references/extended-tools.md` for symbol docs, review, graph reports,
  and edit-interactive plans.
