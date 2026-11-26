# nbskill roadmap

`nbskill` stays standalone as a Python package and Pyskill, focused as a lean complement to `aai-coding` around three pillars:

1. **Structural architecture & focused context:** `nb_graph`, `nb_arch`, `impact`, `trace_path`, `nb_map`, `generated_owner`, `chapter_context`, `symbol_context`, and `search_nb`.
2. **Honest structural, architectural, and narrative review:** `review_nb` / `check_nb` combining `chkstyle` with cell-order, `#| eval: false`, resolved internal star imports, shared-state, heading-hygiene, hide-balance, chapter-local lesson, and project-wide architecture checks, paired with `diff_nb` and `notebook_state`.
3. **Compact standalone workflow & authoring skill:** `edit_nb`, `exec_nb`, `nbskill.skill`, and `SKILL.md` guiding agents to write slim, human-readable nbdev notebooks.

## Guardrails

- Do not rebuild general-purpose file editors, query languages, converters, or telemetry systems.
- Every notebook in `nbs/` must pass `nbdev-test`, `chkstyle`, and `review_nb` without `#| hide` workarounds.
- Keep generated Python in `nbskill/` strictly derived from `nbs/` via `nbdev-export`.
