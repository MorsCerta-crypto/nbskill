# nbskill CLI Fallbacks

Use the CLI when MCP is unavailable, when you need shell-friendly batch work, or when final verification must run inside the project environment with `uv run`.

Check the local install and canonical command names:

```bash
uv run nbskill_status
```

## Reading

```bash
uv run project_context .
uv run file_context notebook.ipynb
uv run file_context notebook.ipynb --include_re train
uv run file_context notebook.ipynb --exclude_re scratch
uv run chapter_context notebook.ipynb --name "Data loading"
uv run chapter_context notebook.ipynb --any_cell_id abc123
uv run symbol_context notebook.ipynb train --depth 1
```

Reader behavior:

- `project_context`: README excerpts, notebook filenames, and notebook file docstrings.
- `file_context`: imports, header docs, Markdown cells, and definition docstrings; supports include/exclude regex filters.
- `chapter_context`: notebook head plus one selected chapter.
- `symbol_context`: exact implementation context, mentioning Markdown, examples/tests, callers, and depth-controlled callees.

## Writing

```bash
uv run write_nb notebook.ipynb --cells_file /tmp/cells.txt
uv run write_nb notebook.ipynb --before_id abc123 --cells_file /tmp/doc.txt
uv run write_nb notebook.ipynb --after_id abc123 --cells_file /tmp/example.txt
uv run write_nb notebook.ipynb --chapter "Data loading" --cells_file /tmp/experiment.txt
uv run write_nb notebook.ipynb --replace --cells_file /tmp/full_notebook.txt
printf '%%markdown\nNew docs\n' | uv run write_nb notebook.ipynb --after_id abc123 -
uv run split_nb_chapter notebook.ipynb "Data loading" nbs/data_loading.ipynb --default_exp data_loading
```

Cell blocks are separated by a line containing only `---`. Prefix a block with `%%markdown`, `%%md`, `%%code`, or `%%raw` to choose its type.

`split_nb_chapter` is CLI-only. It moves one `##` chapter to a new nbdev notebook, copies imports used by the moved code, imports still-needed source definitions, and promotes referenced private source helpers when possible. It dry-runs by default; pass `--no-dry_run` to write.

Use `update_cell` for precise replacements:

```bash
uv run update_cell notebook.ipynb --cell_id abc123 --new_file /tmp/cell.txt
uv run update_cell notebook.ipynb "new text" --cell_id abc123 --old_str "old text" 
uv run update_cell notebook.ipynb "replacement line" --cell_id abc123 --line_range 3 
uv run update_cell notebook.ipynb "" --cell_id abc123 --line_range 3:5 
uv run update_cell notebook.ipynb "replacement line" --cell_id abc123 --line_range 3 --dry_run
uv run update_cell notebook.ipynb "line 1\nline 2" --cell_id abc123 --old_str "old text" 
uv run update_cell notebook.ipynb --cell_id abc123 --split_before "def next_function"
uv run update_cell notebook.ipynb --cell_id abc123 --new_file /tmp/split-cells.txt --split
```

For whole-cell replacement, the replacement text must describe exactly one cell block unless `--split` is set. With `--split`, standalone `---` separators replace the target cell with multiple cells while preserving the original id on the first replacement cell. For partial edits, prefer `--line_range` or `--old_str`.

`--line_range` is 1-based and inclusive. A single number replaces one line; `START:END` replaces or deletes multiple lines; an empty replacement deletes the selected lines.
`--split_before TEXT` splits the existing cell before the first line containing `TEXT`, or matching it as a regular expression when no literal line match exists.
Use `--dry_run` to print the target cell id and compact diff before writing.

Use `batch_edit_nb` when multiple edits should be applied together:

```bash
uv run batch_edit_nb --plan_file /tmp/nbskill-plan.json --dry_run
uv run batch_edit_nb --plan_file /tmp/nbskill-plan.json --no-dry_run
```

## Running And Verifying

```bash
uv run exec_nb notebook.ipynb
uv run exec_nb notebook.ipynb --up2id abc123 # execute up to that cell id
uv run exec_nb notebook.ipynb --chapter "Experiments" # execute up to and including <chapter>
uv run exec_nb notebook.ipynb --timeout 5
uv run exec_nb notebook.ipynb --up2id abc123 --check_only
uv run diff_nb notebook.ipynb
uv run nbdev-export
uv run nbdev-test # tests all notebooks with multiple workers
uv run nbdev-test --path nbs --n_workers 0 --verbose
```

`exec_nb` prints outputs and tracebacks. With `--check_only`, it executes in memory and leaves notebook outputs and metadata unchanged. It adds the notebook folder, detected project root, project virtualenv site packages, and `src/` when present to the execution kernel path, which helps notebooks import local packages.

Use `--cells_file`, `--new_file`, or stdin for multiline edits when shell quoting would be fragile.
