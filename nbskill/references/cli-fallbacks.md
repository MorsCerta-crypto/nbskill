# nbskill CLI Fallbacks

Use the CLI when MCP is unavailable, when you need shell-friendly batch work, or when final verification must run inside the project environment with `uv run`.

## Reading

```bash
uv run read_nb notebook.ipynb
uv run read_nb notebook.ipynb --scope outline
uv run read_nb notebook.ipynb --scope full --cell_id abc123 --show_ids
uv run read_nb notebook.ipynb --filter "def train|class Model" --context 1
uv run show_doc notebook.ipynb symbol --source --show_ids
```

Scopes:

- `overview`: compact one-line cell summaries.
- `outline`: markdown headings, prose, signatures, and docstrings.
- `full`: full source for selected cells.

## Writing

```bash
uv run write_nb notebook.ipynb --cells_file /tmp/cells.txt
uv run write_nb notebook.ipynb --before_id abc123 --cells_file /tmp/doc.txt
uv run write_nb notebook.ipynb --after_id abc123 --cells_file /tmp/example.txt
uv run write_nb notebook.ipynb --chapter "Data loading" --cells_file /tmp/experiment.txt
uv run write_nb notebook.ipynb --replace --cells_file /tmp/full_notebook.txt
```

Cell blocks are separated by a line containing only `---`. Prefix a block with `%%markdown`, `%%md`, `%%code`, or `%%raw` to choose its type.

Use `update_cell` for precise replacements:

```bash
uv run update_cell notebook.ipynb --cell_id abc123 --source_hash 7f3a91c0d422 --new_file /tmp/cell.txt
uv run update_cell notebook.ipynb "new text" --cell_id abc123 --old_str "old text" --source_hash 7f3a91c0d422
uv run update_cell notebook.ipynb "replacement line" --cell_id abc123 --line_range 3 --source_hash 7f3a91c0d422
uv run update_cell notebook.ipynb "" --cell_id abc123 --line_range 3:5 --source_hash 7f3a91c0d422
```

`--line_range` is 1-based and inclusive. A single number replaces one line; `START:END` replaces or deletes multiple lines; an empty replacement deletes the selected lines.

## Running And Verifying

```bash
uv run exec_nb notebook.ipynb
uv run exec_nb notebook.ipynb --up2id abc123
uv run exec_nb notebook.ipynb --chapter "Experiments"
uv run exec_nb notebook.ipynb --timeout 5
uv run diff_nb notebook.ipynb
uv run nbdev-export
uv run nbdev-test --path nbs --n_workers 0 --verbose
```

`exec_nb` prints outputs and tracebacks. It adds the notebook folder, detected project root, and `src/` when present to the execution kernel path, which helps notebooks import local packages.

Keep `apply_nb` as an archived fallback for runtimes that cannot call MCP and cannot stream multiline shell input reliably.
