# nbskill MCP Tools

The MCP interface is the normal interface for agents because it accepts structured parameters and returns notebook-aware text instead of raw `.ipynb` JSON. It provides both code references and reusable problem-solving memory.

Each MCP tool is registered with semantic metadata:

- `description` explains the outcome and safe default in one sentence.
- `tags` expose routing labels such as `read`, `edit`, `review`, `diagnostics`, `convert`, and `agent`.
- `meta.feature` groups the tool into a feature area.
- `meta.usefulness` marks the tool as `core`, `situational`, or `advanced`.
- `meta.when_to_use` and `meta.combine_with` give agent-facing guidance and consolidation notes.

See `references/mcp-tool-report.md` for the current ranked tool surface.

## Feature Areas

| Feature area | Tools | Normal use |
| --- | --- | --- |
| Diagnostics | `healthcheck`, `doctor` | Check MCP liveness, fatal notebook errors, warnings, private symbol leaks, optional style diagnostics, reconnect hints, and setup failures. |
| Focused context | `context` | Read project, notebook, chapter title, cell id, or public symbol targets. |
| Notebook editing | `edit_notebook` | Apply deterministic whole-cell, line, insert/delete/move, and notebook-wide text replacement edits atomically with structured diffs. |
| Verification and review | `exec_nb`, `diff_nb`, `verify_change` | Run notebooks safely, review code-cell diffs, or bundle the diff, focused check-only execution, and diagnostics for explicitly changed notebooks. |
| Symbol analysis | included in `context(...)` | Inspect definitions, callers, and callees for a cell or symbol target. |
| Reference implementations | `reference` | Discover local repositories, add/list/ingest indexed references, query implementations, and propose reuse work. |
| Setup | `create_notebook` | Start a new minimal nbdev source notebook. |

## Python-only operations

`convert`, `problem_memory`, `visible_text_inventory`, `move_cells`, and `style_check` remain Python APIs. They are not registered in the MCP schema because they are broad migrations or specialized local review. Use `context(target="notebook.ipynb#cell-id", mode="exact")` for a complete selected cell.

| Python API | Use |
| --- | --- |
| `convert` | Migrate Python files or folders, or create a small nbdev project. |
| `problem_memory` | Query, add, or list reusable problem-solution pairs. |
| `visible_text_inventory` | List likely user-visible text from notebook code cells. |
| `move_cells` | Perform deliberate cross-notebook migrations. |
| `style_check` | Run specialized local hygiene review; use MCP `doctor(scopes="style")` for normal diagnostics. |

## Problem-solving memory

`problem_memory` manages reusable problem-solution pairs beside the code-reference index. Query it from Python before solving a nontrivial task, then record a pair after verification. Every pair needs at least four normalized tags. Prefer tags that identify the topic, sub-topic, library, problem category, solution category, runtime, and deployment surface. Query tags are exact all-of filters, so a query with `tags="notebook,fastcore,testing,solution-category"` returns only pairs carrying every requested tag.

Signature:

```python
problem_memory(
    action="query",
    query=None,
    top_k=5,
    problem=None,
    solution=None,
    task="",
    project=None,
    evidence="",
    outcome="applied",
    tags=None,
    path=None,
    limit=20,
)
```

Use `action="query"` before implementation, `action="add"` after a verified solution, and `action="list"` to inspect recent memories. For `add`, `tags` must contain at least four comma-separated values.

## Tool Loop

1. `healthcheck` confirms the server is alive and reports concurrency behavior.
2. `context` gives the smallest useful project, notebook, chapter, cell, or symbol view. Cell and symbol targets include symbol graph payloads.
3. `reference` provides reusable implementation evidence before a change.
4. `edit_notebook` applies deterministic edit operations atomically. Use `replace_text`/`replace_texts` with `target="all"` for notebook-level renames, line ops for focused cell edits, and structural ops for insert/delete/move/replace cell changes.
5. `doctor(scopes="style")` adds chkstyle output to notebook hygiene, private symbol warnings, duplicate imports, and global tool usage/problems.
6. `exec_nb` runs a notebook, a chapter, or cells up to an id. It is safe by default: fresh or changed cells are denied until they have either been run by the user or stamped by a prior nbskill execution.
7. `diff_nb` reviews notebook changes in a text form. Use `verify_change` for explicitly affected notebooks when the same review should also include focused check-only execution and `doctor` diagnostics.

Use `doctor(scopes="error,warning")` for fatal notebook problems and warnings. Add `style` only when chkstyle output is useful; `doctor` does not run or show chkstyle for error/warning-only scopes. Private symbol reporting is part of the warning scope.

Use `edit_notebook` when the operations are already known and should be applied deterministically.

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
    path: str,
    up2id: str | None = None,
    chapter: str | None = None,
    timeout: int = 30,
    show_output: bool = True,
    allow_new: bool = False,
    check_only: bool = False,
) -> str
```

The MCP wrapper keeps safe defaults and exposes only the common focused-execution controls. Use `check_only=True` to report outputs and failures without writing notebook outputs or metadata. Use the Python execution API directly for trusted broader execution settings.
