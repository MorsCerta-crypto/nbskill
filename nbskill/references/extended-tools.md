# Extended Tool Reference

The main `SKILL.md` intentionally stays focused on the core loop: MCP, `read_nb`, `write_nb`, and `exec_nb`. Use this reference when a task needs supporting tools.

## Reading More Context

- `show_doc(notebook, symbol, source=False, show_ids=False)` collects the Markdown before a symbol, its exported definition, examples after it, and usage data when available.
- `read_nb(..., context="full")` includes neighboring explanatory Markdown and non-export example cells around a match.

## Review And Analysis

- `diff_nb` prints code-cell diffs without notebook output and metadata noise.
- `style_check` prints fast.ai style hints.
- `symbol_graph` reports definitions, callers, and callees for one symbol.
- `private_symbol_report` finds cross-notebook calls to private helpers.

## Single-Notebook Agent Loop

`execute_plan(notebook, plan, max_steps=20, timeout=30, export=True)` runs a bounded edit loop against exactly one notebook. Use it for small, contained notebook edits when direct calls to `write_nb` and `exec_nb` would be too verbose.
