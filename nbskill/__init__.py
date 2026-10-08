"""Notebook-aware context, editing, execution, and review for Python agents

`nbskill` is a Python Pyskill for agents and maintainers working on nbdev notebooks. It keeps stable cell identities, chapter context, execution evidence, and source diffs together. The notebooks teach the same workflow that the installed functions implement.

```python
from pyskills import doc, list_pyskills
from nbskill import skill
from nbskill.foundation import cell_source, parse_cells
from nbskill.graph import notebook_knowledge_graph_data
from nbskill.read import context
```

## Why it exists

A notebook contains more than Python source. Explanations, examples, outputs, and cell metadata matter when changing a library. `nbskill` selects chapters and symbols before editing and validates a batch before writing it. A failed edit leaves the file unchanged; successful edits retain the source cell IDs and produce reviewable diffs.

`nbformat` handles notebook data, `execnb` executes cells, and nbdev exports and publishes the library. `nbskill` combines those tasks for an agent that must choose a small scope, make a structured change, and check its evidence. Use it when these notebook boundaries matter.

## Load the Pyskill

Install `nbskill` in the Python environment used by the agent (`pip install nbskill`, or `pip install -e .` for this checkout). The package registers `nbskill.skill` in the `pyskills` entry-point group. Discovery lists its scope without importing every problem area. Inspect the module and then the selected operation:

```python
assert "nbskill.skill" in list_pyskills()
doc(skill.context)
```

Modules:

- `nbskill.convert`: Move Python source into numbered nbdev notebooks without losing source order.
- `nbskill.edit`: Apply and review one atomic plan of notebook cell changes.
- `nbskill.execute`: Run a notebook scope and inspect execution evidence without losing the source.
- `nbskill.foundation`: Read, validate, model, and commit notebook data consistently.
- `nbskill.graph`: Find notebook definitions, callers, and likely reuse before changing code.
- `nbskill.knowledge`: Find reusable source and verified problem solutions at the version a workspace uses.
- `nbskill.nbskill`: Copy the nbskill routing instructions to a chosen agent skills directory.
- `nbskill.parallel`: Serialize writes to the same notebook while allowing unrelated notebooks to proceed.
- `nbskill.read`: Find notebook implementations with their explanations, examples, and edit guards.
- `nbskill.review`: Review code changes and notebook contracts without output or metadata noise.
- `nbskill.skill`: Use for nbdev notebooks and their generated Python modules.
- `nbskill.state`: Explain which notebook work is current, changed, or likely affected by an upstream change.
- `nbskill.write`: Create and revise notebook cells while preserving their identities and evidence."""

__version__ = "0.0.16"
