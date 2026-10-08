r"""Use for nbdev notebooks and their generated Python modules.

`nbskill.skill` is the direct API for notebook-owned code. Install `nbskill` in the same Python environment that runs the agent, then import it with `from nbskill.skill import *`. The `pyskills` entry point in `pyproject.toml` makes the module discoverable after installation. An entry point does not install the package. Use an editable install while developing this checkout.

Reference queries use the machine-level `~/.nbskill/reference_knowledge` directory across workspaces. Set `NBSKILL_REFERENCE_HOME` when a separate reference index is required.

## Notebook contract

Treat one notebook as one part of a larger problem. Split that part into H2 chapters. Each chapter tells one domain story from the motivating problem through the implementation and its evidence. Put each chapter heading in its own markdown cell so Jupyter can collapse the chapter as a unit.

Give every public function its own `#| export` definition cell. Keep its function bundle together in this order: a markdown description, the definition, one executable example, and one focused test. The description states the domain contract and the reason the function belongs in the chapter. The example ends with the value a reader should inspect. The test asserts one promised behavior. An example may contain the assertion when that keeps the story clearer, but the definition never shares a cell with imports, setup, examples, or tests.

Keep imports in import-only cells. Use `#| export` on the short markdown summaries that must appear in the Pyskill module docstring. Use `#| exportd` on compact runnable examples that must appear there as fenced Python. `#| exportd` never adds the example to the generated module.

```python
function_bundle = [
    dict(cell_type="markdown", source=r'''### `parse_order`

Convert one order row into domain values.'''),
    dict(cell_type="code", source=r'''#| export
def parse_order(row):
    return dict(row)'''),
    dict(cell_type="code", source=r'''parsed = parse_order({"total": 12})
parsed'''),
    dict(cell_type="code", source=r'''assert parsed["total"] == 12'''),]
assert [cell["cell_type"] for cell in function_bundle] == ["markdown", "code", "code", "code"]
function_bundle
```

## Read notebooks

Start with notebook structure, then narrow to the chapter or symbol that owns the work. Call `generated_owner` before touching a Python module. Call `context` to read the relevant notebook cells. Use `chapter=` for one domain story and a qualified `#symbol` target for one definition. Call `reference_query` before adding a nontrivial helper.

### `generated_owner`

`generated_owner` routes a generated Python module back to its source notebook. A `None` result means the Python file is hand-written and stays on the ordinary code path:

```python
owner = generated_owner(skill.__file__)
assert owner.name == "14_pyskill.ipynb"
owner
```

### `context`

`context` reads notebooks as cells rather than raw JSON. Start with `view="summary"`. Then request `view="full"` only for the chapter or symbol that matters:

```python
summary = context(owner, view="summary", verbose=False)
chapter = context(owner, chapter="Read notebooks", view="full", verbose=False)
assert summary["kind"] == "context"
assert chapter["selection"]["matches"]
chapter["selection"]["matches"]
```

### `reference_query`

`reference_query` searches the shared reference index and direct dependencies. It uses the optional `sentence-transformers` dependency. Install it with `pip install sentence-transformers`, or use `uv sync --dev` in a source checkout. Basic notebook operations do not import it. The following example needs a populated reference index and a locally cached embedding model.

Use `reference_query` before choosing a nontrivial parsing, notebook, abstract syntax tree, filesystem, or formatting implementation:

```python
matches = reference_query("find an nbdev notebook export helper", top_k=3)
matches["hits"]
```

## Write notebooks

Use one `edit_notebook` call for one coherent change. Read stable cell IDs and exact source text first. Submit every related operation together so validation happens before the notebook is written. Never splice notebook JSON or edit a generated Python module.

### `edit_notebook`

`edit_notebook` applies text and structural cell edits atomically. `replace_text` is the smallest edit when the old text is known. Structural operations add, move, replace, or remove whole cells:

```python
edits = [dict(op="replace_text", cell_id="6df2357f", old="direct API", new="direct notebook API")]
change = edit_notebook(owner, edits, dry_run=True)
assert change["changed"]
change["diffs"]
```

## Run notebooks

Run the smallest scope that proves the changed story. `exec_nb` accepts a chapter name or an ending cell ID. Use `check_only=True` while iterating so execution does not write outputs or metadata. Use `allow_new=True` only when the new cells are trusted and must execute.

### `exec_nb`

`exec_nb` executes the affected chapter in the project environment. Safe execution is the default. `check_only=True` keeps the run in memory:

```python
with write_demo_notebook(
    "run_lesson.ipynb", base=gettempdir(),
    cells=[mk_cell("## Answer", cell_type="markdown"), mk_cell("answer = 42\nassert answer == 42")],
) as run_path:
    run = exec_nb(run_path, chapter="Answer", check_only=True, allow_new=True, show_output=False)
    assert run["ok"], run["errors"]
    run_summary = dict(ok=run["ok"], written=run["dest"], executed=len(run["executed_cell_ids"]))
run_summary
```

### `notebook_state`

`notebook_state` compares code cells with their last recorded execution and reports likely stale downstream cells. Dynamic effects remain explicit under `uncertainty`:

```python
state = notebook_state(owner.with_name("15_state.ipynb"))
state["counts"]
```

## Validate notebooks

Validation combines execution evidence, a cell-level diff, and style diagnostics. Run `exec_nb` first. Read `diff_nb` as the source review and fix every relevant `style_check` diagnostic. Then run `nbdev-export` and verify the generated module from a clean interpreter. The notebook remains the source of truth.

### `diff_nb`

`diff_nb` shows changed cell sources without raw notebook JSON, output noise, or unrelated metadata:

```python
review = diff_nb(owner, ref_a="HEAD")
review
```

### `style_check`

`style_check` reports notebook hygiene and source diagnostics. Restrict it to changed cells while iterating, then check the whole notebook before export:

```python
diagnostics = style_check(owner, changed_only=True)
diagnostics
```

Docs: https://MorsCerta-crypto.github.io/nbskill/pyskill.html.md"""

# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/14_pyskill.ipynb.

# %% auto #0
__all__ = ['reference_query', 'diff_nb', 'style_check']

# %% ../nbs/14_pyskill.ipynb #a100cb81
from .edit import edit_notebook
from .execute import exec_nb
from .foundation import generated_owner
from .read import context

from .state import notebook_state

# %% ../nbs/14_pyskill.ipynb #f2ae8636
__all__ = [
    "context", "generated_owner", "reference_query", "edit_notebook",
    "exec_nb", "notebook_state", "diff_nb", "style_check",
]

# %% ../nbs/14_pyskill.ipynb #46e3aae1
def reference_query(*args, **kwargs):
    "Search optional local references without loading that stack for basic workflow use."
    from nbskill.knowledge import reference_query as query
    return query(*args, **kwargs)


# %% ../nbs/14_pyskill.ipynb #6594761a
def diff_nb(*args, **kwargs):
    "Show source changes without loading review dependencies until needed."
    from nbskill.review import diff_nb as review_diff
    return review_diff(*args, **kwargs)

# %% ../nbs/14_pyskill.ipynb #4fb20649
def style_check(*args, **kwargs):
    "Run style diagnostics without loading review dependencies until needed."
    from nbskill.review import style_check as check
    return check(*args, **kwargs)
