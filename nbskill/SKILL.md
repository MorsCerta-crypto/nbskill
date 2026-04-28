---
name: jupyter-notebooks
description: Read, edit, diff, execute, test, and style-check Jupyter/nbdev notebooks through the nbskill CLI. Prefer these tools over raw JSON or generated Python files in nbdev projects.
---

# Jupyter Notebook CLI Skill

Use this skill when you need to inspect, modify, diff, or execute `.ipynb` files without reading raw notebook JSON.

## Agent Operating Rules

When working in an nbdev project, treat notebooks as the editable source of truth:

- Prefer `read_nb`, `write_nb`, `exec_nb`, `diff_nb`, and `chstyle` over raw `.ipynb` JSON reads, ad hoc Python scripts, or edits to generated Python files.
- Use generated `.py` files only to inspect export results or understand import surfaces. Do not make feature edits there unless the user explicitly asks.
- Add new functions, classes, examples, and documentation to notebooks. Let `write_nb` run `nbdev-export` by default.
- For small behavior changes, add or update a small example/test cell after the symbol, then run `exec_nb --up2id ...` or `write_nb --run_test`.
- Prefer `read_nb --overview`, `read_nb --filter`, and targeted `--cell_range` reads before full-cell reads.
- Keep outputs visible: execution output, tracebacks, nbdev-test failures, diff output, and chstyle hints should be read and used before making the next edit.
- Prefer expressive CLI output over silent automation. If a command changes, tests, executes, or style-checks a notebook, its command-line output should explain what happened.

## Commands

The installed package provides:

```bash
read_nb notebook.ipynb
write_nb notebook.ipynb "print('hello')"
exec_nb notebook.ipynb
diff_nb notebook.ipynb
py2nb module.py
py2nbs package_or_folder
doc4symbol notebook.ipynb symbol "Markdown documentation"
example4symbol notebook.ipynb symbol "assert symbol(...) == expected"
chstyle notebook.ipynb
install-nbskill
```

You can also run the module directly from a checkout:

```bash
read_nb notebook.ipynb --overview
```

## Reading Notebooks

Prefer compact reads first:

```bash
read_nb notebook.ipynb --overview
read_nb notebook.ipynb --cell_range 3
read_nb notebook.ipynb --cell_range 2:6 --only_code
read_nb notebook.ipynb --contains "def train"
read_nb notebook.ipynb --filter "def train|class Model"
read_nb notebook.ipynb --only_markdown
read_nb notebook.ipynb --no-full
```

`read_nb` supports:

- `--overview` for one line per selected cell.
- `--cell_range 4`, `--cell_range 2:8`, or `--cell_range '[1,3,5]'`.
- `--only_code` and `--only_markdown`.
- `--contains TEXT` to find cells by source text.
- `--filter TEXT_OR_REGEX` to print only matching cells as `[cell_number]` plus cell source.
- Cell ids are shown by default; use `--no-show_ids` to hide them.
- `--no-full` for the compact outline instead of full selected cell sources.

`--no-full` gives a compact notebook overview: markdown cells with `#` or `##` headings including their prose, plus function/class definitions and `__init__` signatures with docstrings. Function bodies and unrelated cells are omitted.

## Writing Notebooks

Cells are passed as block text. Separate cells with a line containing only `---`.

```bash
write_nb notebook.ipynb "%%markdown
# Notes
---
%%code
def f(x):
    return x + 1"
```

For code containing backslash escapes such as `"\n"`, prefer `--cells_file` so the shell cannot rewrite the text before `write_nb` sees it:

```bash
write_nb notebook.ipynb --cells_file /tmp/cells.txt
```

Write modes:

- Default `--insert_at -1` appends cells.
- `--insert_at 2` inserts before cell index 2.
- `--insert_at '(2,4)'` replaces cells 2 through 3.
- `--insert_at None` replaces the full notebook.
- `--rm_idx 3` deletes one cell before inserting.
- `--rm_idx 2:5` deletes a range before inserting.

Use `%%markdown`, `%%md`, `%%code`, or `%%raw` as the first line of a block to choose the cell type. Blocks without a marker use `--cell_type`, which defaults to code.
Use `--cells_file PATH` or pass `-` as the `cells` argument to read cell text without shell quote expansion.
New Python code cells are syntax-checked before writing by default; use `--no-validate_code` only for intentionally incomplete Python snippets.
By default, `write_nb` runs `nbdev-export` after writing. Use `--no-export` for scratch notebooks or notebooks outside an nbdev project.
Use `--run_test` to run `nbdev-test` after writing; notebook execution output and failures are printed in the command line.
Use `--run_style` to print optional fast.ai style hints via `chstyle` after writing. Add `--style_strict` if hints should make the command fail.
When a written code block contains multiple top-level functions or classes, `write_nb` automatically splits them into separate code cells. A leading `#| export` directive is preserved on each split cell.

## Style Hints

`chstyle` wraps `fastaistyle`'s `chkstyle` checker and prints fast.ai style hints for `.py` and `.ipynb` files.

```bash
chstyle notebook.ipynb
chstyle nbs
chstyle notebook.ipynb --strict
```

By default, `chstyle` is advisory: it prints hints but exits successfully. Use `--strict` when style hints should produce a non-zero exit code. Use `--skip_folder_re` or `--skip_path` for generated/vendor folders.

## Executing Notebooks

Execute and save outputs back into the same notebook:

```bash
exec_nb notebook.ipynb
exec_nb notebook.ipynb --up2id 5
```

Write executed output to a different file:

```bash
exec_nb notebook.ipynb --dest executed.ipynb
```

Use `--exc_stop` when execution should stop on the first exception.
Use `--up2id N` to execute only the first `N` notebook cells, or pass a cell id to execute through that cell.
Saved cell outputs and errors are printed to the command line by default; use `--no-show_output` to suppress them.

## Diffing Notebooks

`diff_nb` uses nbdev's notebook diff helpers but only reports code-cell source changes.

```bash
diff_nb notebook.ipynb
diff_nb notebook.ipynb --ref_a HEAD~1 --ref_b HEAD
diff_nb notebook.ipynb --dels
```

By default it compares `HEAD` to the working tree, includes additions and changes, and ignores deleted cells unless `--dels` is set.

## Converting Python Files

Convert a Python file to an nbdev-style notebook:

```bash
py2nb module.py
py2nb module.py --nbs_path nbs
```

`py2nb` writes `nbs/<module-name>.ipynb` by default and adds:

- a `#| default_exp <module-name>` cell.
- one `#| export` cell for imports and top-level functions/classes.
- separate `#| export` cells for long methods split out of large classes.

For classes longer than 100 lines, regular methods longer than 10 lines are moved into `@patch` cells:

```python
@patch
def method(self: ClassName, ...):
    ...
```

Use `--class_lines` and `--method_lines` to change the splitting thresholds, and `--dest` to choose an exact notebook path.

Convert every Python file in a folder:

```bash
py2nbs nbskill --nbs_path nbs
py2nbs src --nbs_path nbs --maxdepth 2
```

`py2nbs` uses fastcore's `pglob` to find `.py` files. By default it searches recursively and preserves the folder tree under `nbs_path`.

## Documenting Symbols

In nbdev notebooks it is normal, and often useful, to keep prose documentation and small example/test outputs near the code they explain. Documentation usually belongs before the symbol. Examples, checks, and small test cells belong after the symbol so they run against the exported definition.

Insert documentation before a symbol:

```bash
doc4symbol nbs/core.ipynb py2nb "Convert one Python file into an nbdev notebook."
doc4symbol nbs/core.ipynb MyClass.method "Explain what this method is responsible for."
```

Insert an example or small test after a symbol:

```bash
example4symbol nbs/core.ipynb py2nb "out = py2nb('module.py')"
example4symbol nbs/core.ipynb add "assert add(1, 2) == 3"
```

Symbols can be functions, classes, or methods written as `Class.method`. These commands run `nbdev-export` by default; use `--no-export` when editing scratch notebooks.

## Installing This Skill

After installing the Python package, install the skill file for Codex:

```bash
install-nbskill
```

Install for Claude Code:

```bash
install-nbskill --target claude
```

Install for both:

```bash
install-nbskill --target both
```

The installer copies this `SKILL.md` into a `jupyter-notebooks` skill folder.

## Agent Memory And Hooks

For Codex, install this skill and add a short project `AGENTS.md` reminder. Codex discovers `AGENTS.md` globally under `~/.codex` and per project from the repository root down to the current directory. A good project reminder is:

```markdown
## Notebook workflow
- This is an nbdev/notebook-first project.
- Use `read_nb`, `write_nb`, `exec_nb`, `diff_nb`, and `chstyle` for notebook work.
- Do not edit generated Python files for feature work; edit `nbs/*.ipynb` and let `write_nb`/`nbdev-export` update Python.
- Add small examples or tests in notebooks after changed symbols and run them with `exec_nb` or `write_nb --run_test`.
```

Codex hooks can reinforce this when enabled in `.codex/config.toml`:

```toml
[features]
codex_hooks = true
```

Use project-local `.codex/hooks.json` for deterministic reminders or checks. A practical pattern is:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume",
        "hooks": [
          {
            "type": "command",
            "command": "printf '%s\n' 'Notebook workflow: use read_nb/write_nb/exec_nb/diff_nb/chstyle; edit nbs/*.ipynb, not generated .py files.'"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "printf '%s\n' 'Before stopping: if notebook code changed, run exec_nb or write_nb --run_test and inspect diff_nb/chstyle output.'"
          }
        ]
      }
    ]
  }
}
```

For Claude Code, install this skill and put the same rules in `CLAUDE.md` or a path-scoped `.claude/rules/*.md` file. Claude Code also supports project hooks in `.claude/settings.json`; text printed by a `SessionStart` hook is added to Claude's context, which makes it useful for compact notebook workflow reminders:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume|compact",
        "hooks": [
          {
            "type": "command",
            "command": "printf '%s\n' 'Notebook workflow: use read_nb/write_nb/exec_nb/diff_nb/chstyle; edit nbs/*.ipynb, not generated .py files. Add examples/tests in notebooks and run them.'"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "printf '%s\n' 'If that edit touched a notebook or generated Python from nbdev, inspect with read_nb/diff_nb and run exec_nb or write_nb --run_test.'"
          }
        ]
      }
    ]
  }
}
```

Keep hook commands short and deterministic. Put nuanced workflow guidance in `SKILL.md`, `AGENTS.md`, `CLAUDE.md`, or `.claude/rules/*.md`; use hooks to remind, validate, or block clear anti-patterns.
