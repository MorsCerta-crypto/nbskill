---
name: nbskill
description: Use for any nbdev, nbs/*.ipynb, notebook source, generated nbskill/*.py, notebook execution, notebook review, symbol lookup, or notebook refactor task. Use nbskill MCP tools before shell or raw notebook access.
---

# nbskill MCP

This repository treats notebooks as source. For notebook work, use the
nbskill MCP server as the normal interface for reading, editing,
executing, reviewing, and diagnosing notebooks.

## When To Use

Use this skill for any task involving:

- `nbs/**/*.ipynb` or another source notebook.
- Python modules generated from nbdev notebooks.
- Notebook execution, order, outputs, examples, or tests.
- Symbol lookup, call impact, or implementation search inside notebooks.
- Notebook style, review, diagnostics, conversion, or refactoring.

For generated Python files, first inspect the owning notebook and make
the change there unless the user explicitly asks for generated-file-only
work.

## MCP Workflow

1. Call `mcp__nbskill__.healthcheck` before notebook work.
2. Read with `mcp__nbskill__.context` for project, notebook, chapter,
   cell id, or public symbol targets.
3. Search with `mcp__nbskill__.filter_context` for behavior, error text,
   data keys, AST patterns, or library calls.
4. Check prior art with `mcp__nbskill__.reference` before adding
   nontrivial parsing, notebook, AST, filesystem, or formatting logic.
5. Edit notebooks only with `mcp__nbskill__.edit_notebook`, using stable
   cell ids or narrow line edits and expected hashes when available.
6. Verify with the smallest useful MCP check: `mcp__nbskill__.diff_nb`,
   `mcp__nbskill__.exec_nb(check_only=True)`,
   `mcp__nbskill__.style_check`, or `mcp__nbskill__.doctor`.

Do not edit raw notebook JSON or generated Python for normal notebook
source changes.
