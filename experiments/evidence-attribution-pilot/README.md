# Second agent comparison

The helper bundle required four fewer discovery inspections in this run: 17 instead of 21. Both agents implemented the requested straight-line result/assertion association and passed the isolated contract checks in both public context modes. The trial does not establish a general improvement in speed or result quality.

The task was a real reader change: `result = twice(3)` in one notebook cell should make a later `assert result == 6` available with the symbol's examples. Direct calls, lexical exclusions, rebinding, the next exported-definition boundary, and read-only behavior had to remain intact. Both agents worked in separate installed-package checkouts without this chat's history. The [protocol](protocol.md), [identical task](task-prompt.txt), [setup](setup.md), dependency manifest, original notebook patches, and full reports are retained.

## Search effort and mistakes

| Observation | Without helper bundle, A | With helper bundle, B |
| --- | ---: | ---: |
| Inspections before the approach was fixed | 21 | 17 |
| Reported inspection total | 41 | 27 |
| Documentation/catalog invocations | 22 | 18 |
| Failed guessed symbol/chapter lookups | 2 | 1 |
| Structured edit transactions | 6 | 3 |
| Notebook execution invocations | 8 | 5 |
| Ordinary notebook-test invocations | 3 | 2 |
| Final ordinary notebook test | Passed | Passed |
| Isolated contract checks, review and edit combined | 14/14 | 14/14 |
| Module-size style diagnostic | 1,008 code lines | 1,010 code lines |

Counts come from the ordered [A ledger](a-report.md) and [B ledger](b-report.md), rather than automated telemetry. B included two style-check calls in its inspection total; A excluded diagnostics. Excluding those gives comparable source/inspection totals of 41 and 25. The pre-decision counts need no such adjustment. Queries and hash views selecting several cells count as one API invocation. The planned per-target batch measure was not recoverable uniformly from those different selectors, so no normalized cell-volume or token claim is made. Wall time was not compared.

A initially propagated attribution through `result = result + 1`. Its own final review found the error, added a failing counterexample, and corrected it. Its fixture also used a cell id equal to the symbol name, causing edit mode to resolve the cell instead of the symbol. B avoided those two mistakes but guessed a nonexistent chapter, made one incomplete-input edit attempt, and hit stale imports after export. Both used clean imports for their final proof. B also repeated its notebook test with the assigned interpreter after detecting an ambiguous launcher shebang. These are observed events, not evidence that the helper bundle caused or prevented each event.

## Independent checks and the oracle's limit

The [preregistered oracle](oracle.py) was fixed before candidate inspection. It initially failed the separated-assertion case on the unchanged implementation. Candidate A scored 12/14 and B 14/14 on that exact oracle; both original result files are preserved. The difference came from `result = twice(3)` followed by a module-level `raise` in the same cell. A deliberately clears attribution at unsupported statements, including `raise`. That input goes beyond the task's promised straight-line assignment/assertion sequence. B's broader inclusion there is not proof of higher task quality or of a valid runtime assertion.

The [supplementary contract probe](contract-oracle.py) keeps the module-level assignment simple and moves the execution trap into the called function body. Calling the example would still raise, while static retrieval must succeed. Both candidates pass all seven checks in both modes: direct calls retained, separated assertion included, unrelated and nested assertions excluded, rebinding invalidated, bundle boundary respected, and notebook bytes unchanged. The enriched candidate also retains its existing execution metadata; the baseline's absence of that metadata is not counted as a task failure. This supplementary probe was added after reviewing the original discrepancy. It does not replace or rewrite the preregistered result.

## What helped in this task

B explicitly reused the new proof in `01_read.ipynb#b0694a61` for the review/edit result structure and for checking both modes. B used `diff_nb(..., include_markdown=True)` to review its explanation together with code. Those are observed uses of the additions. The four-call discovery difference supports retaining these small aids, but one pair cannot identify how much of the difference they caused.

Direct executable proofs were useful in both conditions. They exposed the missing assertion before implementation, caught A's self-rebinding error, and verified both public modes against actual disposable notebook files. A long list of passing tests would not have revealed the fixture's cell-id collision without showing the selected ids. The durable pattern is a nearby positive example, one meaningful negative boundary, a compact displayed result, and a stable reference from the public entry point.

There is no measured benefit here for the routing-boundary example, independent-edit law, or `diff_nb` claim table. The agents did not cite them as decision evidence for this reader task. Execution freshness remained available in B but did not decide the attribution algorithm. Keep these aids where their contracts matter; this run does not justify spreading annotations or introducing a general claim graph, question language, or semantic truth checker.

## Integration and remaining diagnostics

B's bounded one-helper implementation was brought into the main source notebook. Its proof was then combined with A's explicit self-rebinding counterexample, so the observed mistake remains executable beside the tool. Its assignment rule requires a direct call on the right-hand side. The existing per-cell direct-call matcher and symbol-bundle boundary remain intact. The main notebook proof is cell `ce8a18bd`, next to `_example_test_records`; the public context handoff names both stable ids and distinguishes a static association from a passed assertion.

The proof failed on main before implementation with `AssertionError: {'result-example', 'direct-check'}`. A post-export run in the old kernel still used stale imported readers and failed the same assertion. A fresh main kernel passed all 237 code cells, the supplementary oracle passed 14/14 with execution metadata retained, and the normal assigned-interpreter `nbdev-test nbs/01_read.ipynb` returned `Success.`. Style checking still reports the 1,010-code-line module-size advisory. No module split was made as part of the bounded experiment.

A removed unrelated secondary-export and approval-cache churn; B left those generated artifacts for review. Main integration inspected and removed only that reproduced run-generated churn. Source notebook, generated reader and symbol index are the production changes. Existing user changes to project configuration, workflows and skill text remain outside the commit. `main-verification.json` records the main result, including the failed runs and remaining advisory.
