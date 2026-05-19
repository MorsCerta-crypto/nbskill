# nbskill CLI Fallbacks

Use the CLI when MCP is unavailable, when you need shell-friendly batch work, or when final verification must run inside the project environment with `uv run`.

Check the local install and canonical command names:

```bash
uv run nbskill_status
```

## Reading

```bash
uv run nb_overview notebook.ipynb
uv run nb_overview notebook.ipynb --include_docs
uv run nb_chapter notebook.ipynb --name "Data loading"
uv run nb_chapter notebook.ipynb --any_cell_id abc123
uv run nb_cell notebook.ipynb --id abc123
uv run nb_cell notebook.ipynb --query 'contains="def train"'
uv run show_doc notebook.ipynb symbol --source --show_ids
```

Reader behavior:

- `nb_overview`: Markdown headings, imports, signatures, and docstrings; no line numbers.
- `nb_chapter`: notebook head plus one selected chapter; no line numbers.
- `nb_cell`: one selected cell with previous docs, examples/tests, usage context, and line numbers.

## Writing

```bash
uv run write_nb notebook.ipynb --cells_file /tmp/cells.txt
uv run write_nb notebook.ipynb --before_id abc123 --cells_file /tmp/doc.txt
uv run write_nb notebook.ipynb --after_id abc123 --cells_file /tmp/example.txt
uv run write_nb notebook.ipynb --chapter "Data loading" --cells_file /tmp/experiment.txt
uv run write_nb notebook.ipynb --replace --cells_file /tmp/full_notebook.txt
uv run split_nb_chapter notebook.ipynb "Data loading" nbs/data_loading.ipynb --default_exp data_loading
```

Cell blocks are separated by a line containing only `---`. Prefix a block with `%%markdown`, `%%md`, `%%code`, or `%%raw` to choose its type.

`split_nb_chapter` is CLI-only. It moves one `##` chapter to a new nbdev notebook, copies imports used by the moved code, imports still-needed source definitions, and promotes referenced private source helpers when possible. It dry-runs by default; pass `--no-dry_run` to write.

Use `update_cell` for precise replacements:

```bash
uv run update_cell notebook.ipynb --cell_id abc123 --source_hash 7f3a91c0d422 --new_file /tmp/cell.txt
uv run update_cell notebook.ipynb "new text" --cell_id abc123 --old_str "old text" --source_hash 7f3a91c0d422
uv run update_cell notebook.ipynb "replacement line" --cell_id abc123 --line_range 3 --source_hash 7f3a91c0d422
uv run update_cell notebook.ipynb "" --cell_id abc123 --line_range 3:5 --source_hash 7f3a91c0d422
```

`--line_range` is 1-based and inclusive. A single number replaces one line; `START:END` replaces or deletes multiple lines; an empty replacement deletes the selected lines.

Use `batch_edit_nb` when multiple guarded edits should be applied together:

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
uv run diff_nb notebook.ipynb
uv run nbdev-export
uv run nbdev-test # tests all notebooks with multiple workers
uv run nbdev-test --path nbs --n_workers 0 --verbose
```

`exec_nb` prints outputs and tracebacks. It adds the notebook folder, detected project root, and `src/` when present to the execution kernel path, which helps notebooks import local packages.

Use `--cells_file`, `--new_file`, or stdin for multiline edits when shell quoting would be fragile.
