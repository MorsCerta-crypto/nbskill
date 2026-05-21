# Agent Notes

Use the nbskill MCP server for notebook work in this repository. It keeps agents out of raw `.ipynb` JSON and preserves the nbdev workflow.

## Install the MCP server

From this directory:

```bash
uv tool install --editable . --force
codex mcp add nbskill -- nbskill_mcp
```

After installing or updating nbskill, reconnect or restart the MCP client so it launches the current `nbskill_mcp` command.

## Use nbskill

- Call `healthcheck` first to confirm the MCP server is alive and to see available capabilities.
- Prefer notebook-aware MCP tools over editing notebook JSON directly.
- Start reads with `nb_overview`, then use `nb_chapter` or `nb_cell` for focused context.
- Edit with `edit_cell`, `edit_cell_range`, `insert_cells`, or `apply_notebook_edits`.
- Use `expected_hash` when editing a cell after reading it, so stale context fails instead of overwriting newer work.
- Run `exec_nb`, `diff_nb`, `style_check`, or `doctor` for verification.

## Fallback CLI

If MCP tools are unavailable, check the install and use the CLI equivalents:

```bash
uv run nbskill_status
uv run nb_overview nbs/00_foundation.ipynb
uv run nb_cell nbs/00_foundation.ipynb --id <cell-id>
uv run exec_nb nbs/00_foundation.ipynb --timeout 10
uv run style_check nbs --changed_only --max_diagnostics 80
```

Keep edits surgical: notebooks in `nbs/` are the source of truth, generated Python should stay in sync through the nbskill write path.
