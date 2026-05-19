# nbskill Improvements

This is a candid list of what would make `nbskill` easier and safer for coding agents to use as the primary notebook interface.

## 1. Make The MCP Server The Default Happy Path

I often used standard shell/file tools (`sed`, `rg`, small Python JSON scripts, `apply_patch`) instead of the nbskill MCP server or CLI because the MCP server was not available as a callable tool in this session. I had the `jupyter-notebooks` skill instructions, but not direct `nb_overview`, `nb_chapter`, `nb_cell`, `write_nb`, `update_cell`, or `exec_nb` MCP tool bindings.

When the MCP server is not already connected, the CLI becomes the fallback. That worked for reads and execution, but editing via CLI was still awkward for large, coordinated notebook changes.

Improvements:

- Provide an obvious “MCP connected / not connected” diagnostic in the skill workflow.
- Make `nbskill-mcp`/`nbskill_mcp` setup produce a visible tool list that agents can trust.
- Add a compact recovery instruction: if MCP tools are missing, run exactly these commands to install/reconnect.
- Consider a single `nbskill status` command that reports package version, MCP command name, available CLI tools, and whether notebook-safe edit tools are reachable.

## 2. Provide A First-Class Batch Notebook Edit Tool

The largest reason I used small Python scripts was that I needed to update several cells by id across multiple notebooks in one coordinated change. Calling `update_cell` repeatedly through shell arguments is fragile and verbose, especially when the replacement source contains quotes, indentation, or multiline code.

The old TOML `apply_nb` workflow partly solved this, but it was unused and removed. The gap it leaves is real: agents need a safe batch edit interface that is not raw notebook JSON.

Observed again while adding `agent_workbench`: passing JSON directly through `batch_edit_nb(plan=...)` from Python can be corrupted by CLI-style `\n` decoding when operation strings contain escaped newlines. `plan_file` was the reliable path.

Improvements:

- Add a supported batch edit tool, but make it notebook-native rather than TOML sidecar cleanup.
- Accept a JSON/YAML plan with operations like `set_cell_source`, `insert_after_id`, `delete_cell_id`, and `replace_text`.
- Support `dry_run=True`, source hashes, and a clear per-cell diff before writing.
- Let the tool operate on multiple notebooks while still using notebook locks.

## 3. Improve CLI Ergonomics For Multiline Edits

I avoided `write_nb`/`update_cell` for many edits because shell quoting multiline notebook cells is easy to get wrong. This is exactly the class of problem nbskill is meant to prevent.

The `cells_file`, `new_file`, and stdin paths help, and the new conservative `\n` decoding helps, but the CLI still requires too much ceremony for larger changes.

Improvements:

- Add examples for every safe multiline path: `cells_file`, `new_file`, stdin, and literal `\n`.
- Make error messages recommend the safest path based on the failed input.
- Add `--dry-run --diff` to `update_cell`, not only literal replacement mode.
- Print the target cell id, source hash, and changed line summary on every write.

## 4. Make Notebook Tests Easier To Add Without Output Churn

During this work, running notebooks was useful, but it changed notebook state and outputs. That is normal for notebook-first development, but it makes diffs larger and makes agents cautious.

Improvements:

- Add a `test_nb` or `check_nb` mode that executes tests without persisting outputs unless requested.
- Provide a standard pattern for temporary notebooks that automatically cleans scratch files.
- Make `exec_nb(..., check_only=True)` or similar run cells and report failures while leaving the notebook unchanged.

## 5. Expose Style Report Internals As Stable APIs

`style_check` is becoming the central hygiene report. That is good, but the report logic now spans `review` and `graph`, and some helpers are private.

Improvements:

- Add a structured `style_report(path) -> dict` API.
- Keep `style_check` as the printer/CLI wrapper around that structured report.
- Include problem codes, notebook path, cell id, line, symbol, and severity in the structured form.
- Make MCP return structured content for style reports, not only text.

## 6. Reduce False Positives In Symbol/Order Analysis

The new order checker is useful, but static AST analysis can easily over-warn. I already hit method-call false positives such as `(path / "x").exists()` and `"a".join(...)`.

Improvements:

- Keep adding regression tests for false positives.
- Treat only `Name(...)` and `Name.attr(...)` roots as unresolved callable symbols.
- Ignore common notebook/runtime names by default.
- Consider a per-notebook allowlist comment, for example `#| nbskill_allow_missing SymbolName`.
- Report confidence levels for hard static-analysis cases.

## 7. Clarify Generated-Vs-Source Editing Rules

The generated Python files clearly say “do not edit,” but the workflow can still drift when an agent uses standard file tools. The safest path is to make the source notebook route so much smoother that there is no temptation.

Improvements:

- Add a `nbskill guard` command that detects edits to generated files without notebook changes.
- Add docs that say exactly which notebook owns each generated module.
- Add a `show_owner nbskill/review.py` helper that points to `nbs/04_review.ipynb`.

## 8. Make The Skill Instructions Match Current CLI Names

The project removed hyphenated script aliases, so all active docs and skills should consistently use underscore names.

Improvements:

- Keep generated README, `SKILL.md`, and reference docs in sync.
- Add a test that scans docs for removed CLI names.
- Add a test that validates `[project.scripts]` examples actually exist.

## Why I Used Standard Tools So Often

Short version: because they were the most reliable tools available in the session for broad, coordinated edits.

More specifically:

- Direct MCP tools were not exposed to me as callable functions, so I could not call `nb_overview`/`nb_chapter`/`nb_cell`/`write_nb`/`update_cell` through MCP.
- CLI notebook readers were useful for inspection, but CLI editing large cells via shell arguments is fragile.
- Repeated `update_cell` CLI calls would have been slower and riskier than one explicit script when many cells across several notebooks needed updates.
- `apply_patch` is the required safe editing tool in this environment for normal files, and small temporary scripts let me make structured notebook JSON edits without hand-editing raw JSON by eye.
- `uv run` repeatedly needed escalation because uv’s cache lives outside the workspace sandbox, adding friction to CLI-first workflows.
- The notebook execution/export flow was still used for verification and generation; I used standard tools mainly for bulk source edits and searches.

The goal should be for a future agent to prefer nbskill tools naturally because they are easier than raw shell/file workflows for notebook edits. The biggest missing piece is a trustworthy batch edit tool with dry-run diffs and source-hash guards.
