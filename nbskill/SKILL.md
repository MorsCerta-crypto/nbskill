---
name: jupyter-notebooks
description: Work notebook-first in nbdev projects with nbskill MCP tools and CLI fallbacks. Read, edit, inspect symbols, execute, diff, and export notebooks without touching raw JSON or generated Python.
---

# Jupyter Notebooks

Use this skill when a repository treats notebooks as source files, especially nbdev projects where `nbs/*.ipynb` exports to Python modules. Prefer the nbskill MCP server for normal work: it reads notebooks as compact text, writes cells with structured arguments, executes notebooks, and exports through nbdev without asking the model to edit raw notebook JSON.

## Setup

Install the local package and register the MCP server:

```bash
uv tool install --editable . --force
codex mcp add nbskill -- nbskill-mcp
claude mcp add nbskill -- nbskill-mcp
```

Call `healthcheck` first when you need to confirm the server is alive. The server supports parallel calls: operations on the same notebook are serialized, operations on different notebooks can run in parallel, and notebook execution waits on a global semaphore.

## MCP Workflow

Use MCP tools directly when they are available:

- `read_nb(notebook, context="overview"|"precise"|"full", query=..., ...)` to inspect a notebook without JSON noise. Use `query` for semicolon-separated or JSON selections in one call.
- `show_doc(notebook, symbol, source=False, ...)` to inspect the documentation, exported source, and nearby examples for a symbol.
- `write_nb(notebook, cells, before_id=None, after_id=None, chapter=None, ...)` to insert or replace cells.
- `update_cell(notebook, new, cell_id=None, old_str=None, line_range=None, source_hash=None, ...)` for precise edits.
- `exec_nb(notebook, up2id=None, chapter=None, timeout=30, ...)` to execute a notebook or section.
- `diff_nb(notebook)` to review the notebook-aware diff.
- `execute_plan(notebook, plan, model=None, max_steps=20, timeout=30, export=True)` for a bounded single-notebook edit-interactive loop.

Use stable cell ids and `source_hash` when editing existing cells. Keep generated `.py` files as inspection artifacts; edit the notebook instead.

## CLI Fallback

Use CLI tools when MCP is unavailable, for batch work, or for final verification in the project environment:

```bash
uv run read_nb nbs/02_write.ipynb --context precise --query "cell_type=exported_code; cell_type=test_cell"
uv run show_doc nbs/02_write.ipynb write_nb --source
uv run write_nb nbs/02_write.ipynb --after_id abc123 --cells_file /tmp/cells.txt
uv run update_cell nbs/02_write.ipynb --cell_id abc123 --source_hash 7f3a91c0d422 --new_file /tmp/cell.txt
uv run exec_nb nbs/03_execute.ipynb --up2id abc123 --timeout 10
uv run diff_nb nbs/02_write.ipynb
uv run nbdev-export
uv run nbdev-test --path nbs --n_workers 0 --verbose
```

For multiline cells, prefer `--cells_file` or `--new_file` so shell quoting cannot corrupt code. Cell blocks for `write_nb` are separated by a line containing only `---`; start blocks with `%%markdown`, `%%md`, `%%code`, or `%%raw` when the cell type matters.

## References

Open these only when you need more detail:

- `references/mcp-tools.md` for MCP tool behavior, parallel editing, and `execute_plan`.
- `references/cli-fallbacks.md` for CLI options, cell block syntax, and verification recipes.
