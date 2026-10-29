# Extended Tool Reference

The main `SKILL.md` intentionally stays focused on the core loop: `context`, structured edit tools, and `exec_nb`. Use this reference when a task needs supporting tools.

## Reading More Context

- `context(target=..., scope=...)` prints project, notebook, chapter, cell, or symbol context.
- `context(...)` can include symbol graph payloads for cell and symbol targets.

## Review And Analysis

- `diff_nb` prints code-cell diffs without notebook output and metadata noise.
- `style_report(path)` returns structured notebook hygiene and global usage/problem data.
- `style_check(path)` reports style, metadata, and private-boundary diagnostics. Use `fix=True, dry_run=False` to apply deterministic repairs.
- `style_report(path, include_unused=True)` returns advisory candidates without claiming that external callers are absent.

## Coordinated Editing

`edit_notebook(edits=[...])` applies deterministic edit plans with diffs and expected-hash guards. Use it when the target cells and operations are known and several changes should be committed together.
