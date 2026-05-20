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
| Diagnostics | `healthcheck`, `doctor` | Check MCP liveness, fatal notebook errors, warnings, private symbol leaks, optional style diagnostics, reconnect hints, and setup failures. |
| Focused reading | `nb_overview`, `nb_chapter`, `nb_cell`, `show_doc` | Move from notebook map to chapter context to one line-numbered edit target; use `show_doc` for symbol-first docs work. |
| Notebook editing | `write_nb`, `update_cell`, `batch_edit_nb` | Add cells, update one existing cell, or apply deterministic JSON edit plans. |
| Verification and review | `exec_nb`, `diff_nb`, `style_check` | Run notebooks safely, review code-cell diffs, and catch structural hygiene/private-symbol issues. |
| Symbol analysis | `symbol_graph` | Inspect definitions, callers, and callees for one symbol. |
| Agentic planning | `execute_plan` | Run bounded nested edit loops for one notebook or a project scope only when deterministic tools are not enough. |
| Conversion | `py2nb`, `py2nbdev` | Migrate Python files/folders or bootstrap nbdev projects. |

## Tool Loop

1. `healthcheck` confirms the server is alive and reports concurrency behavior.
2. `nb_overview` gives a compact map of Markdown headings, imports, signatures, and docstrings.
3. `nb_chapter` shows the notebook head plus one selected chapter.
4. `nb_cell` shows one selected cell with line-numbered source, previous docs, examples/tests, and usage context.
5. `show_doc` focuses on one exported symbol and its surrounding notebook story.
6. `write_nb` inserts new cells or replaces a selected chapter/full notebook. Inline multiline MCP cell text is routed through a temporary `cells_file` so backslash escapes inside code are preserved.
7. `update_cell` changes one existing cell by id, source text, or line range. Prefer `line_range` for partial edits. Use `split_before="def name"` to split an existing cell before a matching line, or `split=True` with `---` cell blocks to replace one cell with several smaller cells.
8. `batch_edit_nb` applies JSON edit plans with compact operation details and multi-notebook locks.
9. `style_check` reports chkstyle output, notebook hygiene, private symbol warnings, duplicate imports, and global tool usage/problems.
10. `exec_nb` runs a notebook, a chapter, or cells up to an id. It is safe by default: fresh or changed cells are denied until they have either been run by the user or stamped by a prior nbskill execution. Pass `allow_new=True` only after explicit approval, and use `safe=False` only for deliberate legacy execution.
11. `diff_nb` reviews notebook changes in a text form.

Use `doctor(scopes="error,warning")` for fatal notebook problems and warnings. Add `style` only when chkstyle output is useful; `doctor` does not run or show chkstyle for error/warning-only scopes. Private symbol reporting is part of the warning scope.

Use `execute_plan(scope="notebook", notebook=...)` for a bounded single-notebook plan, or `execute_plan(scope="project", notebooks=...)` for project-level decomposition. Use `batch_edit_nb` when the operations are already known and should be applied deterministically from a JSON plan.

## Concurrency

MCP calls can be issued in parallel. Calls touching the same notebook are protected by a per-notebook lock, so writes do not interleave. Calls touching different notebooks can proceed independently. Notebook execution uses a global semaphore, so execution calls wait for the currently running notebook execution to finish.

The locks are local to one MCP server process. If multiple independent MCP server processes edit the same notebook path, coordinate outside nbskill.

## Editing Safely

For nbdev projects, exported code belongs in notebook cells marked with nbdev directives such as `#| export`. After notebook edits, use export or verification tools rather than editing generated Python directly.

## `batch_edit_nb`

Plan shape:

```json
{
  "operations": [
    {"op": "set_cell_source", "path": "nbs/02_write.ipynb", "cell_id": "abc123", "source": "value = 2"},
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
    check_only: bool = False,
) -> str
```

In safe mode, IPython magics and `!` shell commands are rejected, destructive filesystem and subprocess calls are blocked by `safepyrun`, and live `httpx` calls fail. With `check_only=True`, execution reports outputs and failures without writing notebook outputs or metadata. With `cache_httpx=True`, cache hits from `cachy.jsonl`-compatible data are returned and cache misses still fail.

## `execute_plan`

Signature:

```python
execute_plan(
    plan: str,
    notebook: str | None = None,
    scope: str = "notebook",
    notebooks: str | None = None,
    model: str | None = None,
    max_steps: int = 20,
    timeout: int = 30,
) -> dict
```

Model resolution is `model or NBSKILL_AGENT or "chatgpt/gpt-5.4-mini"`. With `scope="notebook"`, pass `notebook` and the result includes `history` with notebook tool calls plus the agent's final `summary`. With `scope="project"`, pass `notebooks` to constrain decomposition; MCP execution tools apply requested changes directly.
