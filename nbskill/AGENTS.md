# nbskill project notes

This is an nbdev notebook-source project. `nbskill.skill` is the authoritative notebook workflow.

Load the Pyskill for an `.ipynb` file or a Python module whose `generated_owner(path)` returns a notebook. Use `prepare_change`, `edit_notebook`, and `verify_change`; keep hand-written files on the ordinary coding path. Never edit generated Python directly.

Keep notebook changes literate: explain the behavior near the exported code, add a focused example or test when it protects a real behavior, and verify the result. MCP remains available for clients that choose it, but it is not the normal aai-coding path.
