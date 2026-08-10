# Extended Tool Reference

The main `SKILL.md` intentionally stays focused on the core loop: MCP health, `context`, structured edit tools, and `exec_nb`. Use this reference when a task needs supporting tools.

## Reading More Context

- `context(target=..., scope=...)` prints project, notebook, chapter, cell, or symbol context.
- `context(...)` includes symbol graph payloads for cell and symbol targets in MCP.

## Review And Analysis

- `diff_nb` prints code-cell diffs without notebook output and metadata noise.
- `style_report(path)` returns structured notebook hygiene and global usage/problem data.
- `doctor(scopes="style")` reports chkstyle hints together with notebook hygiene warnings and private-symbol diagnostics.
- `doctor(scopes="warning")` includes cross-notebook calls to private helpers.

## Coordinated Editing

`edit_notebook(edits=[...])` applies deterministic edit plans with diffs and expected-hash guards. Use it when the target cells and operations are known and several changes should land together.
