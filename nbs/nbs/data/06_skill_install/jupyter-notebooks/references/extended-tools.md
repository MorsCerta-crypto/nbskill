# Extended Tool Reference

The main `SKILL.md` intentionally stays focused on the core loop: MCP health, `context`, structured edit tools, and `exec_nb`. Use this reference when a task needs supporting tools.

## Reading More Context

- `context(target=..., scope=...)` prints project, notebook, chapter, cell, or symbol context.
- `context(...)` includes symbol graph payloads for cell and symbol targets in MCP.

## Review And Analysis

- `diff_nb` prints code-cell diffs without notebook output and metadata noise.
- `style_report(path)` returns structured notebook hygiene and global usage/problem data.
- `style_check` prints chkstyle hints, nbskill hygiene warnings, and private-symbol warnings.
- `doctor(scopes="warning")` includes cross-notebook calls to private helpers.

## Coordinated Editing

`edit_notebook(edits=[...])` applies deterministic edit plans with diffs and expected-hash guards. Use it when the target cells and operations are known and several changes should land together.

## Single-Notebook Agent Loop

`agent_workbench(goal=..., notebook=..., execute=True, max_steps=20, timeout=30)` runs a bounded edit loop against one notebook. Use `notebook=None` with an explicit goal for project-level decomposition when direct calls to the context, edit, and verification tools would be too verbose.
