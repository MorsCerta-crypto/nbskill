<!-- do not remove -->

## 0.0.23

- Add deterministic pure-Python hybrid project graph (`nb_graph`), mesoscale architecture report (`nb_arch`), transitive blast radius with minimal test commands (`impact`), and shortest-path tracing (`trace_path`) in `02_graph.ipynb`, with `.to_mermaid()` and `.to_json()` export.
- Upgrade `symbol_context` to use `ProjectGraph` for import-resolved vs. ambiguous callers across notebooks and handwritten Python/`tests/`, internal callees, `@patch` effective class APIs, inheritance/`@delegates` relations, and duplicate-definition warnings.
- Enable project-wide `architecture` checks in `review_nb` and `check_nb` by default (`import-cycle`, `duplicate-export`, `orphan-generated-py`, `layer-inversion`, `dead-internal-export`, transitive `untested-public-symbol`, `scattered-patch`, `stale-doc-ref`), add multi-target `#| export <mod>` sync checks, and resolve internal star imports in `_state_problems`.
- Renumber notebooks cleanly (`00_core` through `06_skill`) and remove superseded `experiments/` pilot artifacts and legacy `tools/release.py`.

## 0.0.22

- Rebuild `nbskill` as a focused standalone Python package and Pyskill (`nb_map`, `generated_owner`, `chapter_context`, `symbol_context`, `search_nb`, `review_nb`, `check_nb`, `diff_nb`, `notebook_state`, `edit_nb`, `exec_nb`) across six lean library notebooks with zero hidden-code walls.
- Add structural, execution-order, state, and narrative review diagnostics (`missing-title-header`, `heading-not-standalone`, `heading-level-jump`, `mixed-import-cell`, `eval-false-dependency`, `shared-name-reassigned`, `error-output-saved`, `excessive-hidden-code`, `hidden-implementation-run`, `chapter-missing-explanation`, `chapter-missing-example`, `distant-example`, `chapter-missing-assertion`, `example-trailing-print`, `example-try-except`) integrated directly with `chkstyle.core.check_notebook`.
- Remove legacy converter, global usage telemetry, `public-ui` diffing, and unused transitive dependencies (`remold`, `safepyrun`, `httpx2`).

## 0.0.21

- `context()` lists available headings when a chapter is missing, suggests `max_chars_per_cell` for `max_chars`, and shows how to select a cell by zero-based index.
- Export worker failures report startup stderr, the exit code, the Python interpreter, and the project root when the worker exits before returning a result. Notebook safe mode applies its subprocess restrictions to the worker.
- `exec_nb()` logs the first failing cell, exception type and message, execution environment, and number of additional failures in separate fields. With `exc_stop=True`, it still raises the original exception.
- `edit_notebook()` reports the match count and cell IDs when `replace_cell` finds zero or multiple cells. Edit limit errors suggest splitting the plan into smaller transactions.

## 0.0.20

- Explain how to run a reviewed import-only cell when project approval cannot apply. Keep the project file hint and name blocked functions where a function entry can grant approval.

## 0.0.19

- Read classes and multiple definitions with `context` and suggest close symbol matches.
- Expose supported notebook edit operations and check export capabilities before writing generated files.
- Rebuild shared exports without duplicate contributions and refresh symbol indexes.
- Report the interpreter, project environment and first failure when notebook execution fails.
- Isolate test statistics and preserve chained exception evidence in diagnostics.
- Review new notebooks before their first commit.
- Document the protected-branch release workflow and update installation pins.

## 0.0.18

- Publish the current reviewed notebook API as a versioned GitHub release.
- Document exact GitHub version pins and the local development workflow.
- Upload complete Fastship release drafts before publication.
## 0.0.10


