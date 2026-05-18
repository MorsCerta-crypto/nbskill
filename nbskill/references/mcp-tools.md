# nbskill MCP Tools

The MCP server is started with `nbskill-mcp`. It is intended to be the normal interface for agents because it accepts structured parameters and returns notebook-aware text instead of raw `.ipynb` JSON.

## Tool Loop

1. `healthcheck` confirms the server is alive and reports concurrency behavior.
2. `read_nb` gives compact or precise notebook context. Use `context="overview"` for summaries, `context="precise"` for matched source, and `context="full"` when you also need contiguous markdown before and non-export code after matches.
3. `show_doc` focuses on one exported symbol and its surrounding notebook story.
4. `write_nb` inserts new cells or replaces a selected chapter/full notebook.
5. `update_cell` changes one existing cell by id, source text, or line range.
6. `exec_nb` runs a notebook, a chapter, or cells up to an id. It is safe by default: fresh or changed cells are denied until they have either been run by the user or stamped by a prior nbskill execution. Pass `allow_new=True` only after explicit approval, and use `safe=False` only for deliberate legacy execution.
7. `diff_nb` reviews notebook changes in a text form.

Use `execute_plan` when a bounded single-notebook plan should be delegated to the edit-interactive agent loop. The inner agent sees only the plan and one compact notebook view, and edits through notebook-scoped tools.

## Concurrency

MCP calls can be issued in parallel. Calls touching the same notebook are protected by a per-notebook lock, so writes do not interleave. Calls touching different notebooks can proceed independently. Notebook execution uses a global semaphore, so execution calls wait for the currently running notebook execution to finish.

The locks are local to one MCP server process. If multiple independent MCP server processes edit the same notebook path, coordinate outside nbskill.

## Editing Safely

Prefer text anchors or cell ids over numeric positions. When an edit is risky or concurrent, pass `source_hash` from `read_nb --show_ids` or the MCP `read_nb` result so stale edits fail instead of overwriting newer work.

For nbdev projects, exported code belongs in notebook cells marked with nbdev directives such as `#| export`. After notebook edits, use export or verification tools rather than editing generated Python directly.

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
) -> str
```

Model resolution is `model or NBSKILL_EDIT_MODEL or "openai/gpt-4.1"`. Keep plans bounded to one notebook. For broad repository changes, split work into explicit notebook-level calls or separate `execute_plan` calls.
