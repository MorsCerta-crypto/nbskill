---
name: jupyter-notebooks
description: Route nbdev notebook source and generated modules to nbskill.skill.
---

# Notebook routing

`nbskill.skill` is the authoritative documentation and API for native notebook work. Load it before changing an `.ipynb` file or a Python module whose `generated_owner(path)` returns a notebook.

Use `prepare_change` for a nontrivial task, `edit_notebook` for the source mutation, and `verify_change` for the proof. Keep hand-written files on the ordinary coding path. Never edit a generated module directly.

MCP remains an optional transport for clients that use it. Its installation and connection settings are separate from this notebook workflow.
