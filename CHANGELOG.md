<!-- do not remove -->

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


