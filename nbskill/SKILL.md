---
name: jupyter-notebooks
description: Route nbdev notebook source and generated modules to nbskill.skill.
---

# Notebook routing

`nbskill.skill` is the authoritative documentation and API for native notebook work. Load it before changing an `.ipynb` file. For each Python module, call `generated_owner(path)` after loading the API; edit the returned notebook when present and keep hand-written modules on the ordinary coding path.

## Load nbskill in clikernel

Create a Python kernel with the clikernel MCP tool `create(kernel="python3")`, or select an existing kernel with `use_kernel`. Read the startup reply and follow its bootstrap instructions. Run Python in `exec(code=...)`; the older `py` tool name is not available in the current MCP interface.

Check the interpreter and try the import in that kernel:

```python
import sys
from pathlib import Path
sys.executable
Path.cwd()
import nbskill.skill as nbs
from pyskills import doc, list_pyskills
doc(nbs)
from nbskill.skill import *
```

The installed `SKILL.md` supplies instructions. It does not install the Python package. `nbskill` must be importable by the interpreter shown in `sys.executable`. A successful import from the nbskill checkout can depend on the current directory. Its local `nbskill.egg-info` can also make `list_pyskills()` show the skill without an environment installation. Verify from another directory in a fresh kernel before concluding that installation works.

If the import raises `ModuleNotFoundError: No module named 'nbskill'`, install the checkout into that interpreter. Run this terminal command with the actual paths obtained above:

```sh
uv pip install --python <kernel-python> -e <nbskill-checkout>
```

Use normal dependency resolution. Importing the lightweight skill module alone does not prove that execution and review dependencies are installed. In a shared development environment, preserve existing editable dependency sources by including their checkout paths in the same installation command. For this machine's aai-ws kernel, the tested paths are:

```sh
uv pip install --python /Users/macbook/Projects/aai-ws/.venv/bin/python -e /Users/macbook/Projects/nbskill -e /Users/macbook/Projects/aai-ws/fastcore
```

Restart a kernel created for this task after installation, then repeat the imports. Ask before restarting a user-owned kernel with live work; use a fresh kernel for verification instead. A restart processes editable-install path hooks and clears cached imports. In the fresh kernel, run `%cd /private/tmp` before importing `nbskill` to test independence from the checkout directory. Inspect `nbs.__file__` and `list_pyskills().get("nbskill.skill")`, then read `doc(nbs)` and the selected callable's `doc()` before using it.

## Local Pyskill discovery

The installed pyskills API provides `pyskills.core.enable_local_skills(folder)`. There is no `enable_local_pyskills` callable in the inspected version. Read `doc(pyskills.core.enable_local_skills)` before activation. It discovers modules or packages in `_pyskills/` under the opening folder and its ancestors. It does not install an ordinary nbskill checkout or its dependencies. This repository's package entry point becomes available through the Python installation above.

Local discovery belongs to the host's kernel startup. Its folder scope stays fixed after `%cd`; selecting another folder after activation requires a fresh kernel. Repeated activation for the same folder is allowed. Conflicts with other importable module names raise `ValueError`. Discovery grants no execution permissions. The shared XDG Pyskill directory is another mechanism; adding it to `sys.path` does not expose a checkout stored elsewhere.

Inspect the live API when editable package metadata and source disagree. In this environment, `pyskills.__version__` is `0.0.36` while `importlib.metadata.version("pyskills")` reports `0.0.35`. A metadata version alone does not prove which callables the running source provides.

## Notebook workflow

Use `context` to inspect source and search the current package before a nontrivial implementation choice. Use one structured `edit_notebook` mutation with stable cell IDs. Prove it with `exec_nb`, `diff_nb`, and `style_check`. Never edit a generated module directly. `reference_query` is not part of the current `nbskill.skill` API.

For a smoke test, use the disposable-notebook example in `doc(nbs)` and isolate temporary files for cleanup. A single-notebook `style_check` builds its private-symbol graph from that file and adjacent notebooks for its directly imported private helpers. Unrelated neighbors do not consume the graph budget. Directory reviews still apply the limit of 80 notebooks to the selected directory.

The direct workflow does not require `dialoghelper.core`. If that import fails on `jupywire.session.serialize_binary_message`, use compatible versions of `jupyasyncclient` and `jupywire`, then verify in a fresh kernel. The tested combination is `dialoghelper 0.2.47`, `jupyasyncclient 0.2.22`, and `jupywire 0.1.14`: the client uses `to_frame` and `from_frame` instead of the removed serialization imports. This client also requires `fastspec>=0.2.6`. Refresh stale editable-install metadata when the local source already meets that requirement; preserve the editable source paths during dependency resolution.
