# MCP Tool Structure Report

The MCP server currently exposes 16 tools after merging the obvious advanced and conversion pairs. The remaining count is workable because the core notebook workflow stays split by context level and safety boundary.

## Feature Map

| Feature area | Tools | Usefulness | Notes |
| --- | --- | --- | --- |
| Diagnostics | `healthcheck`, `doctor` | Core | `healthcheck` is a cheap liveness/schema probe; `doctor` now has `error`, `warning`, and `style` scopes. |
| Focused reading | `nb_overview`, `nb_chapter`, `nb_cell`, `show_doc` | Core, except `show_doc` is situational | The three `nb_*` tools intentionally replace one broad reader with progressively richer context. |
| Notebook editing | `write_nb`, `update_cell`, `batch_edit_nb` | Core | These should stay separate because insertion, guarded single-cell updates, and deterministic plans have different safe defaults. |
| Verification and review | `exec_nb`, `diff_nb`, `style_check` | Core | Each answers a different post-edit question: behavior, changed code, and structural/private-symbol hygiene. |
| Symbol analysis | `symbol_graph` | Situational | Useful for impact analysis around one public or private symbol. |
| Agentic planning | `execute_plan` | Advanced | Covers both notebook and project plans via `scope`; project mode defaults to dry-run. |
| Conversion | `py2nb`, `py2nbdev` | Situational | `py2nb` accepts a file or folder; `py2nbdev` remains project bootstrap. |

## Reduction Opportunities

| Candidate | Recommendation | Rationale |
| --- | --- | --- |
| Merge `execute_plan` and `execute_project_plan` | Done | `execute_plan(scope="notebook"|"project")` preserves the distinction without exposing two tools. |
| Merge `py2nb` and `py2nbs` | Done | `py2nb` accepts either one file or a folder. |
| Move `private_symbol_report` into diagnostics/review | Done | Private symbol reporting is included in `doctor(scopes="warning")` and `style_check`; `symbol_graph` remains for focused graph analysis. |
| Hide conversion tools from the default agent instructions | Good candidate | They are useful but rare; keeping them documented as migration tools reduces normal workflow noise without removing capability. |
| Merge `write_nb`, `update_cell`, and `batch_edit_nb` | Not recommended now | A single edit tool would become broad and mode-heavy, which is the problem the focused readers just fixed. |
| Merge `nb_overview`, `nb_chapter`, and `nb_cell` | Not recommended | The current split gives the agent clear context levels and keeps line numbers limited to `nb_cell`. |
| Merge `healthcheck` and `doctor` | Not recommended | The cheap probe is useful for MCP clients; `doctor` is intentionally heavier. |

## Practical Path

Keep the 16 tools for now, with the MCP schema carrying:

- `description`: one sentence explaining the outcome and safe default.
- `tags`: semantic routing labels such as `read`, `edit`, `verify`, `diagnostics`, `convert`, and `agent`.
- `meta.feature`: stable feature area for higher-level grouping.
- `meta.usefulness`: `core`, `situational`, or `advanced`.
- `meta.when_to_use`: agent-facing routing guidance.
- `meta.combine_with`: consolidation note for future pruning.

Further reduction would start to merge core edit/read boundaries, which would make the schemas broader again.
