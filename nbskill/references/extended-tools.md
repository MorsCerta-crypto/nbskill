# Extended Tool Reference

The main `SKILL.md` intentionally stays focused on the core loop: MCP, focused notebook readers, `write_nb`, `batch_edit_nb`, and `exec_nb`. Use this reference when a task needs supporting tools.

## Reading More Context

- `show_doc(notebook, symbol, source=False, show_ids=False)` prints a compact symbol card: location, nearby Markdown, signature/docstring, optional source and examples, and grouped usage.
- `nb_cell(notebook, id=...)` includes neighboring explanatory Markdown, examples/tests, and usage context around a selected cell.

## Review And Analysis

- `diff_nb` prints code-cell diffs without notebook output and metadata noise.
- `style_report(path)` returns structured notebook hygiene and global usage/problem data.
- `style_check` prints chkstyle hints, nbskill hygiene warnings, and private-symbol warnings.
- `symbol_graph` reports definitions, callers, and callees for one symbol.
- `doctor(scopes="warning")` includes cross-notebook calls to private helpers.

## Batch Editing

`batch_edit_nb(plan_file="/tmp/plan.json", dry_run=True)` applies deterministic JSON edit plans with diffs. Use it when the target cells and operations are known and repeated `update_cell` calls would be fragile.

## Single-Notebook Agent Loop

`execute_plan(scope="notebook", notebook=..., plan=..., max_steps=20, timeout=30)` runs a bounded edit loop against exactly one notebook. Use `scope="project"` with `notebooks=...` for project-level decomposition when direct calls to `write_nb` and `exec_nb` would be too verbose.
