# nbskill MCP Tools

The MCP server is started with `nbskill_mcp`. It is intended to be the normal interface for agents because it accepts structured parameters and returns notebook-aware text instead of raw `.ipynb` JSON.

Each MCP tool is registered with semantic metadata:

- `description` explains the outcome and safe default in one sentence.
- `tags` expose routing labels such as `read`, `edit`, `review`, `diagnostics`, `convert`, and `agent`.
- `meta.feature` groups the tool into a feature area.
- `meta.usefulness` marks the tool as `core`, `situational`, or `advanced`.
- `meta.when_to_use` and `meta.combine_with` give agent-facing guidance and consolidation notes.

See `references/mcp-tool-report.md` for the current usefulness review and reduction candidates.

## Feature Areas

| Feature area | Tools | Normal use |
| --- | --- | --- |
| Diagnostics | `healthcheck`, `doctor` | Check MCP liveness, reconnect hints, generated/source drift, and setup failures. |
| Focused reading | `nb_overview`, `nb_chapter`, `nb_cell`, `show_doc` | Move from notebook map to chapter context to one line-numbered edit target; use `show_doc` for symbol-first docs work. |
| Notebook editing | `write_nb`, `update_cell`, `batch_edit_nb` | Add cells, update one guarded cell, or apply deterministic JSON edit plans. |
| Verification and review | `exec_nb`, `diff_nb`, `style_check` | Run notebooks safely, review code-cell diffs, and catch structural hygiene issues. |
| Symbol analysis | `symbol_graph`, `private_symbol_report` | Inspect call relationships and private helper leakage. |
| Agentic planning | `execute_plan`, `execute_project_plan` | Run bounded nested edit loops only when deterministic tools are not enough. |
| Conversion | `py2nb`, `py2nbs`, `py2nbdev` | Migrate Python files/folders or bootstrap nbdev projects. |

## Tool Loop

1. `healthcheck` confirms the server is alive and reports concurrency behavior.
2. `nb_overview` gives a compact map of section headers and exported definitions.
3. `nb_chapter` shows the notebook head plus one selected chapter.
4. `nb_cell` shows one selected cell with line-numbered source, previous docs, examples/tests, and usage context.
5. `show_doc` focuses on one exported symbol and its surrounding notebook story.
6. `write_nb` inserts new cells or replaces a selected chapter/full notebook. Prefer `cells_file` for multiline additions.
7. `update_cell` changes one existing cell by id, source text, or line range. Prefer `new_file` for multiline replacements.
8. `batch_edit_nb` applies JSON edit plans with dry-run diffs, source-hash guards, and multi-notebook locks.
9. `style_check` reports notebook hygiene, cell-order warnings, duplicate imports, and global tool usage/problems.
10. `exec_nb` runs a notebook, a chapter, or cells up to an id. It is safe by default: fresh or changed cells are denied until they have either been run by the user or stamped by a prior nbskill execution. Pass `allow_new=True` only after explicit approval, and use `safe=False` only for deliberate legacy execution.
11. `diff_nb` reviews notebook changes in a text form.

Use `execute_plan` when a bounded single-notebook plan should be delegated to the edit-interactive agent loop. Use `batch_edit_nb` when the operations are already known and should be applied deterministically from a JSON plan.

## Concurrency

MCP calls can be issued in parallel. Calls touching the same notebook are protected by a per-notebook lock, so writes do not interleave. Calls touching different notebooks can proceed independently. Notebook execution uses a global semaphore, so execution calls wait for the currently running notebook execution to finish.

The locks are local to one MCP server process. If multiple independent MCP server processes edit the same notebook path, coordinate outside nbskill.

## Editing Safely

Prefer text anchors or cell ids over numeric positions. When an edit is risky or concurrent, pass `source_hash` from `nb_cell` so stale edits fail instead of overwriting newer work.

For nbdev projects, exported code belongs in notebook cells marked with nbdev directives such as `#| export`. After notebook edits, use export or verification tools rather than editing generated Python directly.

## `batch_edit_nb`

Plan shape:

```json
{
  "operations": [
    {"op": "set_cell_source", "path": "nbs/02_write.ipynb", "cell_id": "abc123", "source_hash": "7f3a91c0d422", "source": "value = 2"},
    {"op": "insert_after_id", "path": "nbs/02_write.ipynb", "cell_id": "abc123", "cells": "%%code\nassert value == 2"},
    {"op": "replace_text", "path": "nbs/02_write.ipynb", "old": "old_name", "new": "new_name"}
  ]
}
```

Supported operations are `set_cell_source`, `insert_after_id`, `insert_before_id`, `delete_cell_id`, and `replace_text`. Dry-run is enabled by default.

## `exec_nb`

Signature:

```python
exec_nb(
    notebook: str,
    chapter: str | None = None,
    up2id: str | None = None,
    timeout: int = 10,
    exc_stop: bool = True,
    show_output: bool = True,
    safe: bool = True,
    allow: str | None = None,
    ok_dests: str | None = None,
    cache_httpx: bool = False,
    cache_dir: str | None = None,
    cache_domains: str | None = None,
    allow_new: bool = False,
) -> str
```

In safe mode, IPython magics and `!` shell commands are rejected, destructive filesystem and subprocess calls are blocked by `safepyrun`, and live `httpx` calls fail. With `cache_httpx=True`, cache hits from `cachy.jsonl`-compatible data are returned and cache misses still fail.

## `execute_plan`

Signature:

```python
execute_plan(
    notebook: str,
    plan: str,
    model: str | None = None,
    max_steps: int = 20,
    timeout: int = 30,
    export: bool = True,
) -> dict
```

Model resolution is `model or NBSKILL_AGENT or "chatgpt/gpt-5.4-mini"`. The result includes `history` with the notebook tool calls and `summary` with the agent's final message. Keep plans bounded to one notebook. For broad repository changes, split work into explicit notebook-level calls or separate `execute_plan` calls.
