# Symbol result evidence candidate

`context` now includes a later module-level assertion on a name assigned by the requested symbol. I implemented the change in `nbs/01_read.ipynb`, added a nearby executable disposable-notebook proof, and left the candidate uncommitted. The focused execution and normal notebook test pass. Style checks report one module-size diagnostic and no changed-source style hints.

## Scope and behavior

The assigned checkout is `/var/folders/6_/45pyyxdd7hz3wz33p813bx_c0000gn/T/nbskill-evidence-pilot-t465_4_g/a`. All repository work stayed there. The imported package path was confirmed in three kernels as `/private/var/folders/6_/45pyyxdd7hz3wz33p813bx_c0000gn/T/nbskill-evidence-pilot-t465_4_g/a/nbskill/__init__.py`. The `/private/var` spelling is the resolved macOS temporary-directory path.

The implementation leaves `_cell_calls_symbol` and `_following_examples` intact. `_example_test_records` now also runs an ordered module-body pass. A simple assignment whose value calls the symbol records its target names. A later module-level assertion reading a current recorded name contributes its cell to the same evidence records used by review and edit views. Every assignment must contain its own symbol call; `result = result + 1` invalidates the previous attribution. Unsupported statements, complex assignment targets, assignment expressions, and unparseable source clear the recorded names. This bounded pass does not follow aliases, function or class bodies, control flow, mutation, or dynamic execution.

The existing bundle boundary remains the next exported code cell. The proof checks review and edit modes, retains the direct-call example and direct-call assertion, includes the separate `assert result == 6`, excludes unrelated and nested assertions, excludes constant and self-rebinding assertions, and excludes usage after the next exported definition. A fixture cell raises if executed. The proof also compares the fixture's bytes before and after both context calls.

Final changed files are `nbs/01_read.ipynb`, `nbskill/read.py`, and `nbskill/_modidx.py`. The two Python files changed through exports. I did not manually edit generated Python.

## Evidence and decisions

I sent `EVIDENCE_FOUND` after 21 repository source/search/read invocations and before the implementation decision. The final ordered ledger contains 41 such invocations. It includes failed lookups, repeated summaries, ownership routing, and working-tree diff reviews. It excludes tool documentation, environment setup, notebook execution, diagnostics, mutations, in-memory inspection of results already read, and the report artifact itself.

The counts by tool are: `context` 22, `lnhashview_cells` 4, working-tree `git.diff` 4, `open_doc` 3, `nbrg` 2, `diff_nb` 2, `generated_owner` 2, `view_file` 1, and `summary_nb` 1. There were 22 documentation/catalog invocations, counted per call: 21 documentation loads or API/source-documentation requests and one `list_pyskills` catalog request. A batched documentation call counts once. Environment setup and identity checks account for seven operations: four CLI launches and three package-path confirmations. One launch failed because the sandbox blocked the local gateway socket; three launches succeeded with the requested environment after escalation. No dependency installation was needed.

The reader's direct-call example rationale and `_cell_calls_symbol` influenced the decision to preserve callback checks and lexical-scope exclusions. `_following_examples` established the existing local boundary and was retained. `_assignment_target_names`, `parse_code_cell`, and `scoped_nodes` supplied existing mechanisms. The nearby collector lesson identified where to put the durable explanation and executable proof.

The review notebook's `_update_result_origins` and `_public_function_reference_sets` demonstrated existing cross-cell attribution. I rejected calling those private helpers across notebooks. Their handling of scoped constructs, named inputs, and aliases is broader than this task's bounded assignment/assertion requirement. I did not copy that wider algorithm. The compact summary of all 286 reader cells established the source notebook's structure and placement. No evidence from another checkout, `experiments/`, `ROADMAP.md`, Git history, or another participant was consulted.

## Red, green, and verification

1. I added the disposable-notebook proof before implementation and ran `exec_nb` through its ending cell, `bd83cd2b`, with `check_only=True`, `allow_new=True`, and `show_output=False`. It failed with `bd83cd2b: AssertionError:` because the later assertion was absent.
2. The first implementation run still failed. A clean kernel reproduced the failure. Adding the mode and selected IDs to the assertion showed `('edit', set())`. The fixture had assigned its definition cell the ID `twice`, identical to the requested symbol. Edit mode resolved that qualified request as a cell. I changed the fixture ID to `twice-definition`; both requested symbol views then passed.
3. A final contract review found that my first pass also propagated attribution through `result = result + 1`. I added a focused self-rebinding case before tightening implementation. The relevant clean-kernel red run included `self-rebound-check` in the review evidence and failed the exclusion assertion. I changed assignment attribution to require a fresh call to the symbol.
4. The final clean-kernel `exec_nb('nbs/01_read.ipynb', up2id='bd83cd2b', check_only=True, allow_new=True, show_output=False)` succeeded without writing notebook outputs. The final normal command `nbdev-test nbs/01_read.ipynb`, run with the assigned `VIRTUAL_ENV` and `PATH`, exited zero and printed `Success.`
5. I reviewed the cell-level source diff with `diff_nb`. Both changed-only and whole-notebook `style_check` runs reported only `large-generated-py`: the generated reader module has 1,008 code lines. I left a module split outside this bounded change. Earlier semicolon, closing-bracket, and long-example hints introduced during this task were corrected.

Across the full task there were eight `exec_nb` invocations, five style-check invocations, three normal notebook-test invocations, six structured notebook-edit transactions, two cell-diff reviews, one targeted normal CLI export, and one clean `nb_export` API export. All normal notebook-test invocations printed `Success.` The final source was verified in a fresh process after export.

## Mistakes, rejected approaches, and cleanup

I guessed two reader helper names instead of using their search-returned cell IDs. Both lookups failed and are retained in the ledger. The default reader summary selected only 50 cells. Raising `max_matches` selected all cells but still exceeded the display budget; `summary_nb(maxlen=55)` supplied a complete compact summary. One in-memory display inspection incorrectly treated a string as a dictionary and raised `AttributeError`; it read no additional repository source.

The initial proof omitted diagnostic assertion values, which delayed identifying its cell-ID collision. I also ran one later boundary test from the original stale kernel; that failure omitted the positive result assertion and was not used as evidence for the self-rebinding fix. The same test in the clean kernel produced the relevant self-rebinding failure described above. These stale-kernel runs are included in the execution count. A fresh kernel alone did not fix the earlier fixture collision.

Working-tree inspection found secondary generated-module growth from repeated structured-edit exports. The normal targeted export appended another copy. Dependency API documentation showed that `nb_export` creates non-default modules with `is_new=False`. A clean `ModuleMaker` export with `is_new=True` removed the accumulated copies but also removed secondary content already present in the original checkout. I rejected retaining that unrelated generated-file change. I restored `nbskill/read_core.py` to the current index and discarded execution-run changes to `nbs/.nbskill-exec-approval.json`. The final normal notebook test passed after that cleanup. The final status contains only the source notebook, generated reader, and generated symbol index. The export issue was not fixed as part of this task.

The first report-writing terminal input was rejected as too large for safe approval review. I retried with smaller kernel inputs and created this report. No required verification step was skipped. I did not commit, publish, or send content to an external service.

## Ordered source and search ledger

Each entry records a logical repository inspection invocation. The before-decision field refers to the implementation decision reported in `EVIDENCE_FOUND`, rather than the later first code mutation.

1. `open_doc` with scope `AGENTS.md`. Before implementation decision: yes. Reason: Read current repository instructions. Result: Outline opened.

2. `view_file` with scope `AGENTS.md full`. Before implementation decision: yes. Reason: Read all repository instructions. Result: Read notebook-first workflow and required checks.

3. `nbrg` with scope `pattern='def context|symbol.*bundle|assertion', root='nbs', max_results=25`. Before implementation decision: yes. Reason: Locate responsible source notebook and existing evidence machinery. Result: Located reader context cells and review/foundation evidence lessons.

4. `context` with scope `'nbs/01_read.ipynb', view='summary'`. Before implementation decision: yes. Reason: Read complete notebook structure before edits. Result: Default selection showed only 50 of 286 cells; display also truncated.

5. `context` with scope `'nbs/01_read.ipynb', view='summary', max_matches=400, verbose=False`. Before implementation decision: yes. Reason: Complete summary after default limit omitted cells. Result: Selected all 286 cells but 6000-character display budget still truncated; full compact summary read in invocation 19.

6. `nbrg` with scope `pattern='evidence|bundle|assign|bound_names|scoped_nodes', root=['nbs/01_read.ipynb','nbs/00_foundation.ipynb','nbs/04_review.ipynb'], max_results=45`. Before implementation decision: yes. Reason: Find reusable static evidence and binding logic. Result: Located direct-call predicate, assignment-target helper, scope primitive, and reviewer origins machinery.

7. `context` with scope `'nbs/01_read.ipynb#_cell_calls_context_symbol', mode='review', max_chars_per_cell=12000`. Before implementation decision: yes. Reason: Inspect existing usage inclusion and local symbol bundle. Result: Failed: guessed helper name did not exist; switched to search-returned cell id.

8. `context` with scope `'nbs/01_read.ipynb#c65a6118', mode='exact'`. Before implementation decision: yes. Reason: Read exact usage predicate from stable search identity. Result: Usage predicate and call matching.

9. `context` with scope `'nbs/04_review.ipynb', query={'cell_id': '9b4b0884'}, around=2, view='full', max_chars_per_cell=12000`. Before implementation decision: yes. Reason: Inspect reusable reviewer assignment attribution. Result: Public-call and evidence-source helpers.

10. `context` with scope `'nbs/01_read.ipynb#_cell_calls_symbol', mode='review'`. Before implementation decision: yes. Reason: Inspect predicate callers and nearby notebook explanation. Result: Found _example_test_records caller and direct-call scope exclusions.

11. `context` with scope `'nbs/01_read.ipynb#_symbol_related_cells', mode='edit'`. Before implementation decision: yes. Reason: Read bundle collection and stopping boundary. Result: Failed: guessed bundle helper name did not exist; next read caller by stable id.

12. `context` with scope `'nbs/01_read.ipynb#472048bb', mode='exact'`. Before implementation decision: yes. Reason: Read actual caller found in symbol graph. Result: Collector delegates to _following_examples with the full notebook length; retains only matching cells.

13. `context` with scope `'nbs/01_read.ipynb#a16d35a9', mode='exact'`. Before implementation decision: yes. Reason: Inspect existing binding target extraction. Result: Assignment helper handles simple and tuple/list names.

14. `context` with scope `'nbs/04_review.ipynb#_tested_public_names', mode='edit'`. Before implementation decision: yes. Reason: Inspect reviewer attribution integration. Result: Scopes checks and follows recorded origins.

15. `context` with scope `'nbs/01_read.ipynb#_following_examples', mode='edit'`. Before implementation decision: yes. Reason: Read current local boundary that must remain intact. Result: Stops at the next exported code cell; headings do not stop this collector.

16. `context` with scope `'nbs/01_read.ipynb#_example_test_records', mode='review'`. Before implementation decision: yes. Reason: Read inclusion callers and nearby guidance. Result: Edit/review contexts consume shared evidence records.

17. `context` with scope `'nbs/01_read.ipynb', query={'cell_id':'d09929ba'}, view='full'`. Before implementation decision: yes. Reason: Read nearby usage rationale. Result: Preserve notebook-level callback tests and avoid unrelated definitions.

18. `context` with scope `'nbs/04_review.ipynb#b09c3c00', mode='exact'`. Before implementation decision: yes. Reason: Read evidence reuse scope and compare requirements. Result: Review analysis follows origins but broader than straight-line requirement.

19. `summary_nb` with scope `'nbs/01_read.ipynb', maxlen=55`. Before implementation decision: yes. Reason: Read every cell summary without context display budget truncation. Result: Complete compact notebook summary.

20. `context` with scope `'nbs/01_read.ipynb#1584953f', mode='exact'`. Before implementation decision: yes. Reason: Inspect exact shared edit/review payload fields for proof assertions. Result: Shared symbol payload stores records under examples.

21. `context` with scope `'nbs/01_read.ipynb#727ac178', mode='exact'`. Before implementation decision: yes. Reason: Confirm existing imports for module-level parsing and reuse. Result: cell_analysis and scoped_nodes already imported.

22. `context` with scope `'nbs/01_read.ipynb#fe440442', mode='exact'`. Before implementation decision: no. Reason: Check proof imports before adding nearby lesson. Result: See dedicated hidden imports.

23. `open_doc` with scope `nbs/01_read.ipynb`. Before implementation decision: no. Reason: Establish notebook address view before structured edit. Result: Notebook outline.

24. `context` with scope `'nbs/01_read.ipynb#5f8917fd', mode='exact'`. Before implementation decision: no. Reason: Use documented edit-view evidence fields in proof. Result: Edit result exposes related records under examples.

25. `lnhashview_cells` with scope `nbs/01_read.ipynb: 472048bb, 6974d49f`. Before implementation decision: no. Reason: Read exact addressed source and nearby rationale before edit. Result: Ready for one coherent proof mutation.

26. `lnhashview_cells` with scope `nbs/01_read.ipynb:472048bb,bd83cd2b`. Before implementation decision: no. Reason: Review current implementation and proof after red run before implementation edit. Result: Fresh sources for coherent implementation and proof split.

27. `diff_nb` with scope `nbs/01_read.ipynb working-tree diff`. Before implementation decision: no. Reason: Review source change after first green. Result: Implementation/proof diff reviewed after implementation run still failed; no green claimed.

28. `context` with scope `'nbs/01_read.ipynb#bd83cd2b', mode='exact'`. Before implementation decision: no. Reason: Read failing proof before adding informative assertion values. Result: Current proof has no assertion detail.

29. `context` with scope `'nbs/01_read.ipynb#cde103db', mode='exact'`. Before implementation decision: no. Reason: Trace why edit view lacks evidence after review proof succeeds. Result: Definition-focused context calls _context_symbol at depth=1; implementation-only branch omits examples.

30. `context` with scope `'nbs/01_read.ipynb#8f5d77f5', mode='exact'`. Before implementation decision: no. Reason: Inspect edit/review depth policy. Result: Symbol graph helper unrelated to the empty edit evidence; no decision drawn from it.

31. `context` with scope `'nbs/01_read.ipynb#1ba93a84', mode='exact'`. Before implementation decision: no. Reason: Trace qualified symbol handling in edit mode. Result: Symbol edit routing passes symbol to _context_edit_result; fixture cell-id collision remained the cause.

32. `lnhashview_cells` with scope `nbs/01_read.ipynb:709085ae,7f8943ac,bd83cd2b`. Before implementation decision: no. Reason: Review exact cells before proof-identity and style corrections. Result: Fixture used symbol name as cell id; edit routed as a cell request.

33. `lnhashview_cells` with scope `nbs/01_read.ipynb:fb96764a,709085ae,7f8943ac,bd83cd2b,6974d49f`. Before implementation decision: no. Reason: Review final contract against rebinding requirement. Result: Detected inherited attribution through self-rebinding; tighten to fresh call assignments.

34. `diff_nb` with scope `nbs/01_read.ipynb final working-tree diff`. Before implementation decision: no. Reason: Review final implementation and executable proof. Result: Bounded two-helper change and adjacent lesson.

35. `git.diff` with scope `stat for current working tree (no history traversal)`. Before implementation decision: no. Reason: Confirm final changed-file scope. Result: Unexpected generated/approval churn: notebook, approval file, read.py, read_core.py and _modidx.py modified; investigated through normal export.

36. `git.diff` with scope `stat after nbdev-export --path nbs/01_read.ipynb`. Before implementation decision: no. Reason: Check whether normal export removes secondary-module growth. Result: Secondary-module additions grew from 2118 to 2471; targeted normal export appended another copy.

37. `generated_owner` with scope `nbskill/read_core.py`. Before implementation decision: no. Reason: Confirm secondary generated target ownership before clean regeneration. Result: Owned by nbs/01_read.ipynb.

38. `generated_owner` with scope `nbskill/read.py`. Before implementation decision: no. Reason: Confirm primary generated target ownership before clean regeneration. Result: Owned by nbs/01_read.ipynb.

39. `git.diff` with scope `stat after clean ModuleMaker export`. Before implementation decision: no. Reason: Verify secondary-module accumulation removed. Result: Fresh ModuleMaker export removed accumulation but produced 1413 deletions against pre-existing secondary content; rejected this unrelated generated change.

40. `open_doc` with scope `nbs/.nbskill-exec-approval.json`. Before implementation decision: no. Reason: Inspect execution-approval cache before discarding run-only changes. Result: Tool-owned approval mapping.

41. `git.diff` with scope `stat after discarding secondary export and approval cache churn`. Before implementation decision: no. Reason: Confirm candidate scope after cleanup. Result: Only nbs/01_read.ipynb, nbskill/read.py, and nbskill/_modidx.py remain changed.
