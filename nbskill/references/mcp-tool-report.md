# MCP Tool Structure Report

The MCP server exposes focused tools after merging the obvious advanced and conversion pairs. The remaining count is workable because the core notebook workflow stays split by context level and safety boundary.

## Feature Map

| Feature area | Tools | Usefulness | Notes |
| --- | --- | --- | --- |
| Diagnostics | `healthcheck`, `doctor` | Core | `healthcheck` is a cheap liveness/schema probe; `doctor` now has `error`, `warning`, and `style` scopes. |
| Focused context | `project_context`, `file_context`, `chapter_context`, `symbol_context` | Core | The context family intentionally separates repository, file, chapter, and implementation views. |
| Notebook editing | `edit_cell`, `edit_cell_range`, `insert_cells`, `apply_notebook_edits` | Core | These should stay separate because whole-cell edits, partial edits, insertion, and coordinated plans have different safe defaults. |
| Verification and review | `exec_nb`, `diff_nb`, `style_check` | Core | Each answers a different post-edit question: behavior, changed code, and structural/private-symbol hygiene. |
| Symbol analysis | `symbol_graph` | Situational | Useful for impact analysis around one public or private symbol. |
| Agentic planning | `agent_workbench` | Advanced | Covers bounded notebook/project edit plans when direct structured tools are not enough. |
| Knowledge store | `get_knowledge`, `store_knowledge`, `add_behaviour_steering` | Core | Reuses known local rules and warning patterns before an agent re-solves them. |
| Conversion | `py2nb`, `py2nbdev` | Situational | `py2nb` accepts a file or folder; `py2nbdev` remains project bootstrap. |

## Reduction Opportunities

| Candidate | Recommendation | Rationale |
| --- | --- | --- |
| Consolidate agent planning | Done | `agent_workbench` keeps planning/editing behind one bounded MCP workflow. |
| Merge `py2nb` and `py2nbs` | Done | `py2nb` accepts either one file or a folder. |
| Move `private_symbol_report` into diagnostics/review | Done | Private symbol reporting is included in `doctor(scopes="warning")` and `style_check`; `symbol_graph` remains for focused graph analysis. |
| Hide conversion tools from the default agent instructions | Good candidate | They are useful but rare; keeping them documented as migration tools reduces normal workflow noise without removing capability. |
| Merge the edit tools | Not recommended now | A single edit tool would become broad and mode-heavy, while the current split keeps common small edits precise. |
| Merge the context tools | Not recommended | The current split gives the agent clear context levels without overloading one broad reader. |
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
