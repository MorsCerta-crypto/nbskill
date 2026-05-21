# Extended Tool Reference

The main `SKILL.md` intentionally stays focused on the core loop: MCP health, focused notebook readers, structured edit tools, and `exec_nb`. Use this reference when a task needs supporting tools.

## Reading More Context

- `symbol_context(notebook, symbol, depth=1)` prints exact implementation context with nearby Markdown, examples/tests, callers, and optional callee summaries.
- `file_context(notebook, include_re=..., exclude_re=...)` narrows one notebook to matching Markdown and definition items.

## Review And Analysis

- `diff_nb` prints code-cell diffs without notebook output and metadata noise.
- `style_report(path)` returns structured notebook hygiene and global usage/problem data.
- `style_check` prints chkstyle hints, nbskill hygiene warnings, and private-symbol warnings.
- `symbol_graph` reports definitions, callers, and callees for one symbol.
- `doctor(scopes="warning")` includes cross-notebook calls to private helpers.

## Coordinated Editing

`edit_notebook(edits=[...])` applies deterministic edit plans with diffs and expected-hash guards. Use it when the target cells and operations are known and several changes should land together.

## Single-Notebook Agent Loop

`agent_workbench(goal=..., notebook=..., execute=True, max_steps=20, timeout=30)` runs a bounded edit loop against one notebook. Use `notebook=None` with an explicit goal for project-level decomposition when direct calls to the context, edit, and verification tools would be too verbose.
