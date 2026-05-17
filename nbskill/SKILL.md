---
name: jupyter-notebooks
description: Work notebook-first in nbdev projects with nbskill CLI tools. Read, edit, inspect symbols, execute, diff, and export notebooks without touching raw JSON or generated Python.
---

# Jupyter Notebook Skill

Use notebooks as the source of truth. In nbdev projects, edit `nbs/*.ipynb`, let `write_nb` export Python, and use generated `.py` files only to inspect the export result.

Write notebooks as a co-creation story:

```text
rationale/docs -> exported code -> show-off example
```

For each exported function/class worth understanding, add a small non-exported code cell below it that calls the symbol and shows what it does. These show-off cells are part example, part executable documentation, and part lightweight test.

## Daily Loop

1. Orient:

```bash
read_nb nbs/core.ipynb
read_nb nbs/core.ipynb --scope outline
show_doc nbs/core.ipynb some_function --source
```

2. Edit:

```bash
update_cell nbs/core.ipynb "new source" --cell_id abc123 --source_hash 7f3a91c0d422
write_nb nbs/core.ipynb --after_id abc123 --cells_file /tmp/new_cells.txt
write_nb nbs/core.ipynb --chapter "Experiments" --cells_file /tmp/check.txt
```

3. Run and review:

```bash
exec_nb nbs/core.ipynb --up2id abc123
write_nb nbs/core.ipynb --cells_file /tmp/check.txt --run_test
diff_nb nbs/core.ipynb
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

Use `--context 1` or higher when you want the full local story around a cell: markdown rationale/docs before it and non-exported code/show-off cells below it.

## Inspecting Symbols

Use `show_doc` when a human or agent needs shared context for a function, class, or method:

```bash
show_doc nbs/core.ipynb write_nb
show_doc nbs/core.ipynb Trainer.fit --source --show_ids
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

When adding exported code, also add a non-exported show-off cell below it. Good show-off cells call the exported function with tiny concrete inputs, print or assert the result, and make the behavior obvious to a human reading the notebook.

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
doc4symbol notebook.ipynb symbol "Markdown docs"
example4symbol notebook.ipynb symbol "assert symbol(...) == expected"
install-nbskill --target both
```

Keep these secondary. The core co-creation workflow is `read_nb`, `show_doc`, `write_nb`, `update_cell`, and `exec_nb`.
