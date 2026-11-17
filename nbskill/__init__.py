"""Notebook-aware context, editing, execution, and review for Python agents

`nbskill` gives Python agents and maintainers tools to read, edit, run, and review nbdev notebooks by chapter, symbol, or cell ID.

```python
from pyskills import doc, list_pyskills
from nbskill import skill
from nbskill.foundation import cell_source, parse_cells
from nbskill.graph import notebook_knowledge_graph_data
from nbskill.read import context
```

## Why it exists

`nbskill` validates notebook edits before writing and keeps existing cell IDs stable. Use focused execution and source diffs to check what changed.

## Load the Pyskill

Install `nbskill==0.0.21` from its GitHub release tag in the Python environment used by the agent. With uv, pin both the package version and its release source:

```toml
[project]
dependencies = ["nbskill==0.0.21"]

[tool.uv.sources]
nbskill = {git = "https://github.com/MorsCerta-crypto/nbskill.git", tag = "0.0.21"}
```

Authenticate private-repository access with `gh auth login` and `gh auth setup-git`, commit `uv.lock`, and install with `uv sync --locked`. For development inside this repository, use `uv sync --locked` and the checks in [DEVELOPMENT.md](DEVELOPMENT.md). The package registers `nbskill.skill` in the `pyskills` entry-point group. Discovery lists its scope without importing every problem area. Inspect the module and then the selected operation:

```python
assert "nbskill.skill" in list_pyskills()
doc(skill.context)
```

Modules:

- `nbskill.convert`: Move Python source into numbered nbdev notebooks without losing source order.
- `nbskill.diagnostics`: Record tool usage, resolve project inputs and bound diagnostic output.
- `nbskill.edit`: Apply and review one atomic plan of notebook cell changes.
- `nbskill.execute`: Run a notebook scope and inspect execution evidence without losing the source.
- `nbskill.fixtures`: Own scratch paths and test notebooks for one example or test lifetime.
- `nbskill.foundation`: Model notebook data, metadata, chapters and Python structure consistently.
- `nbskill.graph`: Find notebook definitions, callers, and likely reuse before changing code.
- `nbskill.nbskill`: Copy the nbskill routing instructions to a chosen agent skills directory.
- `nbskill.parallel`: Serialize writes to the same notebook while allowing unrelated notebooks to proceed.
- `nbskill.parser`: Normalize notebook text, directives and Python syntax without a notebook model.
- `nbskill.read`: Find notebook implementations with their explanations, examples, and edit guards.
- `nbskill.review`: Review code changes and notebook contracts without output or metadata noise.
- `nbskill.skill`: Use for nbdev notebooks and their generated Python modules.
- `nbskill.state`: Explain which notebook work is current, changed, or likely affected by an upstream change.
- `nbskill.write`: Create and revise notebook cells while preserving their identities and evidence."""

__version__ = "0.0.21"
