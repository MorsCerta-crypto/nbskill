"""Use nbskill from Python for notebook-aware work in nbdev projects.

Use this skill when you need to inspect, edit, execute, or review an nbdev
notebook without changing raw `.ipynb` JSON. Start with focused context, make
one structured edit, then run the narrowest useful check.

## Read context

```python
from nbskill.read import context

print(context("nbs/01_read.ipynb", scope="nbs"))
```

`context` accepts a project, notebook, chapter, cell id, or public symbol. Use
it to identify the target cell and nearby examples before editing.

## Edit one notebook

```python
from nbskill.edit import edit_notebook

result = edit_notebook(
    "nbs/01_read.ipynb",
    [dict(op="replace_text", cell_id="cell-id", old="before", new="after")],
)
print(result["text"])
```

Use narrow operations. `edit_notebook` validates, writes, and exports nbdev
notebooks atomically.

## Verify the result

```python
from nbskill.execute import exec_nb
from nbskill.review import diff_nb, style_check

exec_nb("nbs/01_read.ipynb", check_only=True)
print(diff_nb("nbs/01_read.ipynb"))
print(style_check("nbs/01_read.ipynb", changed_only=True))
```

Use `exec_nb` for behavior, `diff_nb` for code-cell changes, and
`style_check` for notebook hygiene. The MCP server exposes the same workflow
when structured tool calls are more convenient than Python.

After loading this pyskill, use `from nbskill.skill import *` to access the
curated workflow API directly.
"""

from nbskill.edit import edit_notebook
from nbskill.execute import exec_nb
from nbskill.read import context, filter_context
from nbskill.review import diff_nb, style_check

__all__ = [
    "context", "filter_context", "edit_notebook", "exec_nb", "diff_nb", "style_check",
]
