---
name: jupyter-notebooks
description: Work notebook-first in nbdev projects with nbskill MCP tools and CLI fallbacks. Read, edit, inspect symbols, execute, diff, and export notebooks without touching raw JSON or generated Python.
---

# Jupyter Notebook Skill

Use notebooks as the source of truth. In nbdev projects, edit `nbs/*.ipynb`, let `write_nb` export Python, and use generated `.py` files only to inspect the export result.

Prefer the nbskill MCP server when it is available. MCP tools accept multiline cell text as structured arguments, so they avoid shell quoting and temporary file workarounds.

Write notebooks as a co-creation story:

```text
rationale/docs -> exported code -> show-off example
```

For each exported function/class worth understanding, add a small non-exported code cell below it that calls the symbol and shows what it does. These show-off cells are part example, part executable documentation, and part lightweight test.

The package itself is organized as a notebook story:

```text
foundation -> reading/inspection -> writing/changing -> execution -> review -> conversion -> skill installation -> MCP integration
```

The matching public modules are `nbskill.foundation`, `nbskill.read`, `nbskill.write`, `nbskill.execute`, `nbskill.review`, `nbskill.convert`, `nbskill.skill`, and `nbskill.mcp`. Treat `nbskill.core` as obsolete.

## MCP Setup

Install the package as an editable tool, then register the local MCP server:

```bash
uv tool install --editable . --force
codex mcp add nbskill -- nbskill-mcp
claude mcp add nbskill -- nbskill-mcp
```

The MCP server is implemented in `nbs/07_mcp.ipynb` and exported to `nbskill.mcp`. It exposes `read_nb`, `show_doc`, `write_nb`, `update_cell`, `exec_nb`, `diff_nb`, `chstyle`, `py2nb`, `py2nbs`, and the archived `apply_nb` fallback.

When MCP is available, call those MCP tools directly instead of writing scratch `.py` files or shell-quoting notebook cells. Use the CLI examples below only when MCP is not available.

## MCP Best Practices

- Keep MCP tools small, explicit, and boring: one notebook action per tool call, typed parameters, readable docstrings, and plain-text return values that include the command output a human would need.
- Prefer structured MCP arguments for multiline notebook cells. Do not route multiline code through shell arguments unless MCP is unavailable.
- Return notebook output, tracebacks, export/test messages, and useful IDs/hashes directly from the tool result. Do not hide failures in side files.
- Keep tool names stable and aligned with the CLI names: `read_nb`, `show_doc`, `write_nb`, `update_cell`, and `exec_nb` are the primary loop.
- Avoid long-running hidden background processes. `nbskill-mcp` should run as a stdio MCP server started by Codex or Claude Code.
- Treat `apply_nb` as an archived fallback for clients without MCP support, not as the preferred interface.
- In nbdev notebooks, any function used from a different exported Python module must be public: do not start its name with `_`. Nbdev only adds non-underscore symbols to `__all__`, so cross-module helpers need names like `capture_call`, not `_capture_call`.

## Daily Loop

1. Orient:

```bash
read_nb nbs/02_write.ipynb
read_nb nbs/02_write.ipynb --scope outline
show_doc nbs/02_write.ipynb write_nb --source
```

2. Edit:

```bash
update_cell nbs/02_write.ipynb "new source" --cell_id abc123 --source_hash 7f3a91c0d422
write_nb nbs/02_write.ipynb --after_id abc123 --cells_file /tmp/new_cells.txt
write_nb nbs/02_write.ipynb --chapter "Experiments" --cells_file /tmp/check.txt
```

3. Run and review:

```bash
exec_nb nbs/03_execute.ipynb --up2id abc123
write_nb nbs/02_write.ipynb --cells_file /tmp/check.txt --run_test
diff_nb nbs/02_write.ipynb
```

Keep documentation and small examples in the notebook. Documentation/rationale goes before a symbol; exported code is the implementation; executable show-off examples/tests go after it as non-exported cells.

## Reading

`read_nb` hides notebook JSON and defaults to a compact overview:

```bash
read_nb notebook.ipynb
read_nb notebook.ipynb --scope outline
read_nb notebook.ipynb --scope full --cell_id abc123 --show_ids
read_nb notebook.ipynb --filter "def train|class Model" --context 1
read_nb notebook.ipynb --cell_type md
read_nb notebook.ipynb --cell_type code,md --chapter "Training"
```

Scopes:

- `overview`: one line per cell, the default.
- `outline`: markdown headings/prose plus function/class signatures and docstrings.
- `full`: full selected cell sources.

Cell type filters:

- `code`, `py`, or `python` for code cells.
- `md`, `markdown`, `doc`, or `docs` for markdown cells.
- `raw` for raw cells.
- `export` or `exported` for nbdev exported code cells.

Cell ids are shown by default. Add `--show_ids` when you need source hashes for safe edits.

Use `--context 1` or higher when you want the full local story around a cell: markdown rationale/docs before it and non-exported code/show-off cells below it. This is the replacement for separate doc/example insertion helpers; write normal markdown/code cells with `write_nb`, then read the story with context.

## Inspecting Symbols

Use `show_doc` when a human or agent needs shared context for a function, class, or method:

```bash
show_doc nbs/02_write.ipynb write_nb
show_doc nbs/02_write.ipynb update_cell --source --show_ids
```

It prints the full symbol story: rationale/docs before the export, the exported signature/docstring, optional source, and nearby non-exported show-off examples after the symbol.

## Writing

Prefer stable IDs and chapter names over positions:

```bash
write_nb notebook.ipynb --cells_file /tmp/cells.txt
write_nb notebook.ipynb --before_id abc123 --cells_file /tmp/doc.txt
write_nb notebook.ipynb --after_id abc123 --cells_file /tmp/example.txt
write_nb notebook.ipynb --chapter "Data loading" --cells_file /tmp/experiment.txt
write_nb notebook.ipynb --replace --cells_file /tmp/full_notebook.txt
```

Cell blocks are separated by a line containing only `---`. Start a block with `%%markdown`, `%%md`, `%%code`, or `%%raw` to choose its type. Use `--cells_file` for anything non-trivial so shell quoting cannot corrupt strings like `"\n"`.

## Archived File Workflow

The old scratch-file bridge is archived in `SKILL.archive.md`. Use it only when MCP is not available and shell stdin is unreliable.

Create `dev/nbskill-op.toml` with native file tools, then run `apply_nb`. The manifest is TOML and is removed automatically after a successful operation, along with `cells_file` or `new_file` sidecars inside the same `dev/` folder. Name scratch sidecars like `dev/nbskill-cells.txt` or `dev/nbskill-new.py` so they are clearly disposable.

```toml
tool = "write_nb"
path = "nbs/02_write.ipynb"
after_id = "abc123"
export = true
cells = """
%%markdown
Why this change exists.
---
%%code
#| export
def f(x):
    return x + 1
---
%%code
assert f(1) == 2
"""
```

Use MCP first. Use `write_nb notebook.ipynb -` only when the agent runtime can stream stdin reliably. Otherwise, `apply_nb` keeps multiline code out of shell arguments and avoids lingering `/tmp` files.

When adding exported code, also add a non-exported show-off cell below it. Good show-off cells call the exported function with tiny concrete inputs, print or assert the result, and make the behavior obvious to a human reading the notebook. Add documentation and examples as ordinary neighboring cells with `write_nb`; retrieve them with `read_nb --context` or `show_doc`.

By default `write_nb` runs `nbdev-export`. Use `--no-export` only for scratch notebooks.

Use `update_cell` for precise replacements:

```bash
update_cell notebook.ipynb "replacement source" --cell_id abc123 --source_hash 7f3a91c0d422
update_cell notebook.ipynb "new text" --cell_id abc123 --old_str "old text" --source_hash 7f3a91c0d422
```

## Running

```bash
exec_nb notebook.ipynb
exec_nb notebook.ipynb --up2id abc123
exec_nb notebook.ipynb --chapter "Experiments"
```

Outputs and tracebacks are printed to the command line. `write_nb --run_test` executes the notebook through `execnb`, prints outputs, and avoids nbdev worker-pool semaphore issues in restricted environments.

`exec_nb` also prepares local imports for notebook-first projects: it adds the notebook folder, detected project root, and `src/` when present to the execution kernel path. This lets notebooks under `nbs/` import local packages without adding temporary `sys.path` boilerplate cells.

## Failure Map

nbskill records friction globally in `~/.nbskill/nbskill-errors.json`, or in `NBSKILL_FAILURE_MAP` if that environment variable is set. It records failed tool uses and rapid/repeated calls. Treat this file as workflow telemetry: if the same command keeps failing or getting retried, improve the notebook, command, or this skill.

## Other Tools

```bash
diff_nb notebook.ipynb
chstyle notebook.ipynb
py2nb module.py
py2nbs src
apply_nb dev/nbskill-op.toml
install-nbskill --target both
```

Keep these secondary. The core co-creation workflow is MCP `read_nb`, `show_doc`, `write_nb`, `update_cell`, and `exec_nb`; use CLI `apply_nb` only as the archived fallback.
