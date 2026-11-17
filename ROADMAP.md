# Native nbskill roadmap

`nbskill.skill` handles notebook work for aai-coding. Route each Python file with `generated_owner`. Edit the owning notebook for generated modules and use the ordinary coding workflow for hand-written files.

## Validate future changes

In a clean aai-coding session with the package installed, make a real change in a disposable checkout. Find the relevant notebook and existing implementation, make a structured edit, run the affected scope, and inspect the diff and export. For routing changes, exercise both generated and hand-written files. Record the task, commands, changed files, and result. Repeat the same exercise after refactoring.

Keep claims, exact test-cell references, and decision rationale near the implementation. Use `context` to find them. Add a new abstraction when a concrete task exposes a gap in the existing tools.

## Evidence from the pilots

- The [claim-to-test trial](experiments/claim-test-pilot/README.md) recorded 10 discovery calls without claim links and rationale and 3 with them. Both runs passed notebook tests and style checks.
- The [result-attribution trial](experiments/evidence-attribution-pilot/README.md) recorded 21 discovery inspections without the helper bundle and 17 with it. Both passed the checks for the bounded task. The report preserves the scope mismatch in the initial oracle.
- The [notebook mechanism trials](experiments/notebook-mechanisms/README.md) record retained examples and rejected alternatives. Discovery counts describe those runs only.

## Where to verify behavior

| Operation | Source notebook and cell ID | What to check |
| --- | --- | --- |
| `generated_owner` | [Foundation](nbs/00_foundation.ipynb), `031a8dfd` | Generated and hand-written files in one project take different paths. |
| `context` | [Read](nbs/01_read.ipynb), `ce8a18bd` | A later assertion can be attributed to the result of a call within the supported scope. |
| `edit_notebook` | [Edit](nbs/02_edit.ipynb), `0081c5ed`, `ddd32f12` | Inspect replacement counts for a missing match. A stale hash rejects the edit. |
| `exec_nb` | [Execute](nbs/03_execute.ipynb), `347b2af2`, `624cb8c8` | `check_only=True` preserves notebook bytes. Permitted code can still write files. |
| `notebook_state` | [State](nbs/15_state.ipynb), `93b0e3f6`, `e6c567a9` | Distinguish recorded execution from likely downstream staleness and dynamic uncertainty. |
| `diff_nb` | [Review](nbs/04_review.ipynb), `86f418a7`, `c4dfad92` | Markdown is opt-in and stored outputs stay excluded. |
| `style_check` | [Review](nbs/04_review.ipynb), `e176f419` | `fix=True` previews repairs unless `dry_run=False`. |

Review an explanation alongside the code and test it describes. A source diff or fresh execution record alone cannot establish that the explanation is correct.
