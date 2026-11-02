# Claim-to-test pilot, 2026-11-02

The agent with explicit claim-to-test links and a nearby decision rationale found the relevant evidence in 3 notebook/source read or search calls. The agent without that addition needed 10. Both independently implemented `diff_nb(..., include_markdown=True)` and passed notebook tests and style checks. This measures discovery effort in one pair of runs, not overall task speed.

| Recorded result | Original notebook | Enriched notebook |
| --- | --- | --- |
| Notebook/source read and search calls before evidence was identified | 10 | 3 |
| Repository instruction reads, counted separately | 2 | 2 |
| Total frozen discovery calls | 12 | 5 |
| Full `exec_nb` execution after implementation | 171 cells, no errors | 171 cells, no errors |
| Whole-notebook `style_check` | 0 diagnostics | 0 diagnostics |
| `nbdev-test nbs/04_review.ipynb` | Exit 0, `Success.` | Exit 0, `Success.` |

## What was compared

Two disposable clones started from `5e01c575579b04f2bc593c463572525ae717016f`. Both received the same small extension to existing example `nbs/04_review.ipynb#c4dfad92`: a stored stream output and an assertion that this output stays out of the diff. The existing examples already checked Markdown exclusion but lacked a direct stored-output assertion. This common preparation already passed on the existing implementation.

Only the enriched clone received an additional Markdown cell immediately after the `diff_nb` definition. It mapped the two promises to the exact assertions in `c4dfad92` and stated the code-only default's reason, tradeoff, and condition for reconsideration. Before dispatch, the notebook models were identical after removing this one cell; their generated Python files were byte-identical.

The original trial ran first. The enriched trial used a separate fresh agent without the original conversation, solution, or measurements. Both used the same [task prompt](task-prompt.txt), installed package discovery, and prepared dependency environments. Neither changed `sys.path` or used dependency monkeypatches. The [setup record](setup.md) describes the local kernel and dependency preparation.

Each agent froze its discovery ledger before implementation. A logical API invocation counted as one call, including a batched read. Tool documentation and environment setup were excluded. The counts are agent-reported; the ordered ledgers are preserved in the [original run](baseline.md) and [enriched run](enriched.md).

The original agent made several broad or truncated requests and used a regex in a literal query. It inspected separate cells before locating the stored-output assertion. The enriched agent narrowed one broad project summary to `diff_nb`, then checked the referenced example cells in one batched read. The intervention combined explicit links, a clearer rationale, and placement near the definition; this experiment does not isolate their individual effects.

## Verification and limits

Both new feature tests first failed with `TypeError: diff_nb() got an unexpected keyword argument 'include_markdown'`. The original test is cell `7bfde57f`; the enriched test is `986d6667`. Both exercise real temporary Git notebooks, opt-in Markdown changes, current-source additions, and stored-output/raw-cell exclusion. Their final whole-notebook runs passed 171 cells. Exports and normal clean-process notebook tests succeeded. Validation covered the affected review notebook; the repository-wide test suite was not run.

The default safe runner blocked Git subprocess calls after each implementation changed. The original agent completed `exec_nb` with `allow='subprocess.run'`; the enriched agent completed it with `safe=False` for the trusted local notebook. Normal `nbdev-test` also passed for both. These execution-policy differences and the failed attempts are recorded in the run reports. They prevent treating these runs as an end-to-end timing comparison.

Repository-wide export also exposed unrelated duplicated output in `nbskill/read_core.py`. Each agent inspected and restored that exporter-produced drift rather than changing unrelated notebook source. The candidate patches retain the intended generated exports.

The main checkout contains the claim links, rationale, and shared example enhancement. Its independent `exec_nb` verification passed all 170 code cells with `safe=True`, no errors, no warnings, and no skipped cells. Changed-source and whole-notebook style checks returned 0. The [verification record](main-verification.json) retains the executed cell IDs. The two feature implementations remain separate [original](baseline.patch) and [enriched](enriched.patch) patches against the common repository revision.

One unblinded run per variant is initial evidence. Different navigation choices can affect the count. No elapsed-time or token-cost advantage was measured. Repeat the comparison on another real task, with the order reversed, before automating relationship lookup or introducing a general schema.
