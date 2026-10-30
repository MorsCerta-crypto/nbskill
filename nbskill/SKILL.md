---
name: jupyter-notebooks
description: Use nbskill.skill through Python calls for nbdev notebooks and their generated modules.
---

# Notebook routing

Use `nbskill` through Python calls. `nbskill.skill` is the authoritative documentation and API for notebook work. Load it before changing an `.ipynb` file. For each Python module, call `generated_owner(path)` after loading the API. Edit the returned notebook when present; keep hand-written modules on the ordinary coding path.

## Load the Python API

Use the Python environment where `nbskill` and its dependencies are installed. Read the module documentation, then read `doc()` for each selected callable before using it:

```python
import sys
import nbskill.skill as nbs
from pyskills import doc, list_pyskills
from nbskill.skill import *

sys.executable
nbs.__file__
list_pyskills().get("nbskill.skill")
doc(nbs)
```

The installed `SKILL.md` supplies instructions; it does not install the Python package. If importing `nbskill` raises `ModuleNotFoundError`, check `sys.executable` and ensure the package is installed in that interpreter's environment. Verify the import from outside the checkout in a fresh Python session. The checkout's current directory and local package metadata can otherwise make imports or discovery succeed without an environment installation.

## Enable local Pyskills

For modules or packages under `_pyskills/` in the opening folder or its ancestors, call `pyskills.core.enable_local_skills` at host startup before loading the tool layer. Each public top-level module or package supplies one local Pyskill. Give it a module docstring and a curated public API; no package installation or entry point is needed for these folder-local skills:

```python
from pathlib import Path
from pyskills.core import enable_local_skills

doc(enable_local_skills)
enable_local_skills(Path.cwd())
```

Local discovery does not install an ordinary `nbskill` checkout or its dependencies. The installed package registers `nbskill.skill` in the `pyskills` entry-point group. Read `doc(enable_local_skills)` before activation. The opening folder fixes the discovery scope for that Python session; later working-directory changes do not alter it. Repeated activation for the same folder is allowed. Use a fresh session to select another folder. Conflicting importable module names raise `ValueError`, and discovery grants no execution permissions.

## Notebook workflow

Use `context` to inspect the relevant cells and search the current package before a nontrivial implementation choice. Read `doc(nbs.context)` for its selection options. Make one coherent `edit_notebook` call using stable cell IDs, then verify with `exec_nb`, `diff_nb`, and `style_check`. Never edit raw notebook JSON or generated Python for normal notebook source changes.

For a behavior change, revise or add a focused notebook test when a useful reproducer exists. Run it before and after the implementation change. Keep the reason for a bug fix or a non-obvious tradeoff in nearby markdown. Use the disposable-notebook example in `doc(nbs)` for a smoke test, and keep temporary files isolated for cleanup.
