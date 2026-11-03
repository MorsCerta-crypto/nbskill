---
name: jupyter-notebooks
description: Use nbskill.skill through Python calls for nbdev notebooks and their generated modules.
---

# nbskill

`nbskill` reads, edits, executes and reviews nbdev notebooks through Python calls. It keeps cell IDs, chapter context and source diffs together. Edit the source notebook when changing generated Python.

Use a Python environment with `nbskill` installed. Load the API and read its documentation:

```python
import nbskill.skill as nbs
from pyskills import doc

doc(nbs)
```

Use `nbs.context` to read relevant cells and search for existing implementations. For a Python module, `nbs.generated_owner(path)` identifies its source notebook; a `None` result means the module is hand-written. Apply one coherent change with `nbs.edit_notebook`, then check it with `nbs.exec_nb`, `nbs.diff_nb` and `nbs.style_check`.

Read `doc()` for the selected function before calling it, for example `doc(nbs.context)`. The module and function documentation contain the workflow, examples and options.

For additional folder-local Pyskills under `_pyskills/`, the host uses `enable_local_skills` at startup. Import it with `from pyskills.core import enable_local_skills` and read `doc(enable_local_skills)` before use. `nbskill` itself is discovered through its installed package entry point.
