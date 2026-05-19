# MCP Tool Structure Report

The MCP server currently exposes 19 tools. The count is workable if each tool has strong routing metadata, but the surface reads large because several tools share broad feature areas. I recommend keeping the core notebook workflow split and only considering merges for advanced or migration-oriented tools.

## Feature Map

| Feature area | Tools | Usefulness | Notes |
| --- | --- | --- | --- |
| Diagnostics | `healthcheck`, `doctor` | Core | `healthcheck` is a cheap liveness/schema probe; `doctor` is the deeper drift and setup report. |
| Focused reading | `nb_overview`, `nb_chapter`, `nb_cell`, `show_doc` | Core, except `show_doc` is situational | The three `nb_*` tools intentionally replace one broad reader with progressively richer context. |
| Notebook editing | `write_nb`, `update_cell`, `batch_edit_nb` | Core | These should stay separate because insertion, guarded single-cell updates, and deterministic plans have different safe defaults. |
| Verification and review | `exec_nb`, `diff_nb`, `style_check` | Core | Each answers a different post-edit question: behavior, changed code, and structural hygiene. |
| Symbol analysis | `symbol_graph`, `private_symbol_report` | Situational | Useful for impact analysis and API hygiene, but not needed on every edit. |
| Agentic planning | `execute_plan`, `execute_project_plan` | Advanced | Powerful but specialized; dry-run defaults matter because these run nested edit loops. |
| Conversion | `py2nb`, `py2nbs`, `py2nbdev` | Situational | Valuable for migration/bootstrap workflows, but distracting during normal notebook maintenance. |

## Reduction Opportunities

| Candidate | Recommendation | Rationale |
| --- | --- | --- |
| Merge `execute_plan` and `execute_project_plan` | Good candidate | A single `execute_plan(scope="notebook"|"project")` would preserve semantics while removing one advanced tool. |
| Merge `py2nb` and `py2nbs` | Good candidate | Their behavior overlaps; a single Python-to-notebooks converter could switch file/folder behavior from the path. |
| Merge `symbol_graph` and `private_symbol_report` | Possible | One `analyze_symbols(mode="graph"|"private-report")` would reduce surface area, though the outputs are different. |
| Hide conversion tools from the default agent instructions | Good candidate | They are useful but rare; keeping them documented as migration tools reduces normal workflow noise without removing capability. |
| Merge `write_nb`, `update_cell`, and `batch_edit_nb` | Not recommended now | A single edit tool would become broad and mode-heavy, which is the problem the focused readers just fixed. |
| Merge `nb_overview`, `nb_chapter`, and `nb_cell` | Not recommended | The current split gives the agent clear context levels and keeps line numbers limited to `nb_cell`. |
| Merge `healthcheck` and `doctor` | Not recommended | The cheap probe is useful for MCP clients; `doctor` is intentionally heavier. |

## Practical Path

Keep the 19 tools for now, but make the MCP schema more self-describing with:

- `description`: one sentence explaining the outcome and safe default.
- `tags`: semantic routing labels such as `read`, `edit`, `verify`, `diagnostics`, `convert`, and `agent`.
- `meta.feature`: stable feature area for higher-level grouping.
- `meta.usefulness`: `core`, `situational`, or `advanced`.
- `meta.when_to_use`: agent-facing routing guidance.
- `meta.combine_with`: consolidation note for future pruning.

If the next goal is reducing count, the lowest-risk target is 19 to 16 tools by merging `execute_plan`/`execute_project_plan`, `py2nb`/`py2nbs`, and `symbol_graph`/`private_symbol_report`.
