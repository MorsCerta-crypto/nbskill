# Agent Notes

Use the nbskill MCP server for notebook work in this repository. It keeps agents out of raw `.ipynb` JSON, preserves the nbdev workflow, and gives you notebook-aware reads, edits, execution, diffs, style checks, and shared project knowledge.

## Notebook Workflow

Work notebook-first and keep each change small. Prefer this shape for new or revised behavior:

1. Markdown docs explain the behavior and name the public symbol.
2. Exported code implements the behavior in a focused cell.
3. A small example cell calls the behavior and shows useful output.
4. A small test cell checks one thing at a time.

Notebook directives matter:

- Cells exported to Python start with `#| export`.
- Cells that should not execute during the test phase include `#| eval: false`.
- Cells that should not appear in documentation, such as test cells, start with `#| hide`.

Keep edits surgical. Read the nearby notebook context, edit one coherent piece, then immediately check whether the result is what you wanted before continuing. Avoid huge edit batches that only reveal problems after a long run.

## MCP Tool Guide

- Start with `healthcheck` when you need to confirm the MCP server is alive or discover current capabilities.
- Use `doctor` for scoped project health: errors, warnings, style, or all diagnostics.
- Use `style_check` for notebook hygiene, changed-cell style deltas, private-symbol warnings, duplicate imports, and stored knowledge warnings.
- Use `file_context` for a compact notebook map: imports, Markdown, public definitions, and docstrings.
- Use `chapter_context` to read one section around a heading, query, or cell id.
- Use `symbol_context` when starting from a public symbol and you need exact implementation context.
- Use `edit_notebook` for notebook edits instead of touching raw JSON. It handles whole-cell edits, line edits, insertion, deletion, moves, and notebook-wide `replace_text`/`replace_texts` refactors.
- Use `exec_nb` for focused execution. Prefer `check_only=True` while validating edits, and execute only the needed cell range or chapter when possible.
- Use `diff_nb` to review code-cell changes without notebook metadata noise.
- Use `symbol_graph` when you need definitions, callers, callees, or cross-notebook symbol impact.
- Use `agent_workbench` for a bounded notebook edit plan when the change spans multiple cells or needs the MCP server to coordinate reads, edits, export, and checks.

When editing cells after reading them, use the MCP server's stale-context protections when available, such as expected hashes, so newer user or agent edits are not overwritten.

## Knowledge Store

Use the nbskill knowledge store before solving a problem from scratch. Someone may already have recorded the local rule, warning pattern, or preferred fix.

- Query existing knowledge with `get_knowledge` before making a nontrivial notebook or style change.
- Store reusable findings with `store_knowledge` after you discover a rule that would save future agents time.
- Use `add_behaviour_steering` for recurring style or workflow guidance that should surface during later checks.
- Treat knowledge warnings from `style_check` as project memory, not noise. Read the note, decide whether it applies, and either follow it or record why this case is different.

Good knowledge entries are concrete: mention the notebook or symbol family, the warning pattern, the preferred fix, and the reason.

## Small Edit Loops

Prefer a tight loop:

1. Read with `file_context`, `chapter_context`, `symbol_context`, or another focused read tool.
2. Check the knowledge store.
3. Make the smallest notebook-aware edit.
4. Run a focused `exec_nb`, `style_check changed_only`, or `diff_nb`.
5. Only then continue to the next edit.

Stop once the requested change is handled and verification is clear. Do not broaden scope, reformat unrelated cells, or edit generated Python directly when the notebook source should own the change.
