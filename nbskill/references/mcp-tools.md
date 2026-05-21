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
| Focused context | `project_context`, `file_context`, `chapter_context`, `symbol_context` | Move from repository orientation to one notebook, one chapter, or one concrete implementation. |
| Notebook editing | `edit_notebook` | Apply deterministic whole-cell, line, insert/delete/move, and notebook-wide text replacement edits atomically with structured diffs. |
| Verification and review | `exec_nb`, `diff_nb`, `style_check` | Run notebooks safely, review code-cell diffs, and catch structural hygiene/private-symbol issues. |
| Symbol analysis | `symbol_graph` | Inspect definitions, callers, and callees for one symbol. |
| Agentic planning | `agent_workbench` | Run bounded notebook/project edit loops only when direct structured tools are not enough. |
| Knowledge store | `get_knowledge`, `store_knowledge`, `add_behaviour_steering` | Reuse known local rules, save repeated warning patterns, and surface project memory during style checks. |
| Conversion | `py2nb`, `py2nbdev` | Migrate Python files/folders or bootstrap nbdev projects. |

## Tool Loop

1. `healthcheck` confirms the server is alive and reports concurrency behavior.
2. `project_context` gives README excerpts, notebook filenames, and notebook file docstrings.
3. `file_context` shows imports, header docs, Markdown cells, and definition docstrings for one notebook, with regex filters.
4. `chapter_context` shows the notebook head plus one selected chapter.
5. `symbol_context` focuses on one implementation with exact source, mentioning Markdown, examples/tests, callers, and callees.
6. `edit_notebook` applies deterministic edit operations atomically. Use `replace_text`/`replace_texts` with `target="all"` for notebook-level renames, line ops for focused cell edits, and structural ops for insert/delete/move/replace cell changes.
7. `style_check` reports chkstyle output, notebook hygiene, private symbol warnings, duplicate imports, and global tool usage/problems.
8. `exec_nb` runs a notebook, a chapter, or cells up to an id. It is safe by default: fresh or changed cells are denied until they have either been run by the user or stamped by a prior nbskill execution. Pass `allow_new=True` only after explicit approval, and use `safe=False` only for deliberate legacy execution.
9. `diff_nb` reviews notebook changes in a text form.

Use `doctor(scopes="error,warning")` for fatal notebook problems and warnings. Add `style` only when chkstyle output is useful; `doctor` does not run or show chkstyle for error/warning-only scopes. Private symbol reporting is part of the warning scope.

Use `agent_workbench` for a bounded single-notebook or project-level plan when direct edits are not enough. Use `edit_notebook` when the operations are already known and should be applied deterministically.

## Concurrency

MCP calls can be issued in parallel. Calls touching the same notebook are protected by a per-notebook lock, so writes do not interleave. Calls touching different notebooks can proceed independently. Notebook execution uses a global semaphore, so execution calls wait for the currently running notebook execution to finish.

The locks are local to one MCP server process. If multiple independent MCP server processes edit the same notebook path, coordinate outside nbskill.

## Editing Safely

For nbdev projects, exported code belongs in notebook cells marked with nbdev directives such as `#| export`. Cells that should not execute during the test phase include `#| eval: false`; cells that should not appear in docs, such as test cells, start with `#| hide`. After notebook edits, use export or verification tools rather than editing generated Python directly.

## `edit_notebook`

Edit shape:

```json
{
  "edits": [
    {"op": "replace_cell", "cell_id": "abc123", "source_lines": ["value = 2"]},
    {"op": "insert_cells", "anchor_id": "abc123", "where": "after", "cells": [{"cell_type": "code", "source_lines": ["#| hide", "assert value == 2"]}]},
    {"op": "replace_text", "target": "all", "old": "old_name", "new": "new_name"}
  ]
}
```

Supported operations are `replace_cell`, `insert_cells`, `delete_cells`, `move_cells`, `replace_lines`, `insert_lines`, `delete_lines`, `replace_text`, and `replace_texts`. Prefer expected hashes when you have just read a cell and want stale context to fail.

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

In safe mode, IPython magics and `!` system escapes are rejected, destructive filesystem and subprocess calls are blocked by `safepyrun`, and live `httpx` calls fail. With `check_only=True`, execution reports outputs and failures without writing notebook outputs or metadata. With `cache_httpx=True`, cache hits from `cachy.jsonl`-compatible data are returned and cache misses still fail.

## `agent_workbench`

Signature:

```python
agent_workbench(
    goal: str,
    notebook: str | None = None,
    contract_file: str | None = None,
    execute: bool = False,
    max_steps: int = 20,
    timeout: int = 30,
) -> dict
```

Use `agent_workbench` for bounded notebook or project work when direct MCP calls would be too verbose. Pass a concrete `goal`, constrain the task with `notebook` when possible, and set `execute=True` only when the loop should run verification after editing. Prefer the direct context, edit, and verification tools for small changes.
