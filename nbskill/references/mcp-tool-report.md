# MCP Tool Structure Report

The MCP server exposes focused tools after merging the obvious context, reference, and conversion families. The remaining count is workable because edit, execution, review, and diagnostics keep distinct safety boundaries.

## Feature Map

| Feature area | Tools | Usefulness | Notes |
| --- | --- | --- | --- |
| Diagnostics | `healthcheck`, `doctor` | Core | `healthcheck` is a cheap liveness/schema probe; `doctor` now has `error`, `warning`, and `style` scopes. |
| Focused context | `context` | Core | One reader accepts project, notebook, chapter title, cell id, or symbol targets. |
| Notebook editing | `edit_notebook` | Core | One atomic edit surface now covers whole-cell edits, partial edits, insertion, deletion, moves, and coordinated notebook-level text replacements. |
| Verification and review | `exec_nb`, `diff_nb`, `style_check` | Core | Each answers a different post-edit question: behavior, changed code, and structural/private-symbol hygiene. |
| Symbol analysis | included in `context(...)` | Core | Cell and symbol context includes symbol graph payloads. |
| Agentic planning | `agent_workbench` | Advanced | Covers bounded notebook/project edit plans when direct structured tools are not enough. |
| Reference implementations | `reference` | Core | Add, list, ingest, and query indexed reference implementations. |
| Conversion | `convert` | Situational | Handles single-file, folder, and project conversion modes. |

## Reduction Opportunities

| Candidate | Recommendation | Rationale |
| --- | --- | --- |
| Consolidate agent planning | Done | `agent_workbench` keeps planning/editing behind one bounded MCP workflow. |
| Merge `py2nb`, `py2nbs`, and `py2nbdev` | Done | `convert` handles single-file, folder, and project modes. |
| Move `private_symbol_report` into diagnostics/review | Done | Private symbol reporting is included in `doctor(scopes="warning")` and `style_check`. |
| Hide conversion tools from the default agent instructions | Good candidate | They are useful but rare; keeping them documented as migration tools reduces normal workflow noise without removing capability. |
| Merge the edit tools | Not recommended now | A single edit tool would become broad and mode-heavy, while the current split keeps common small edits precise. |
| Merge the context tools | Done | `context` routes by target while keeping one public reader. |
| Merge `healthcheck` and `doctor` | Not recommended | The cheap probe is useful for MCP clients; `doctor` is intentionally heavier. |

## Practical Path

Keep the compact tool surface, with the MCP schema carrying:

- `description`: one sentence explaining the outcome and safe default.
- `tags`: semantic routing labels such as `read`, `edit`, `verify`, `diagnostics`, `convert`, and `agent`.
- `meta.feature`: stable feature area for higher-level grouping.
- `meta.usefulness`: `core`, `situational`, or `advanced`.
- `meta.when_to_use`: agent-facing routing guidance.
- `meta.combine_with`: consolidation note for future pruning.

Further reduction would start to merge core edit/execution/review boundaries, which would make the schemas broader again.
