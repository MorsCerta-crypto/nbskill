# Candidate B report

`context` now includes a later module-level assertion on a value assigned by a direct symbol call. The candidate is implemented in `nbs/01_read.ipynb` and is uncommitted. The focused proof, full `exec_nb` run, and normal notebook test pass. `style_check` reports one module-size diagnostic.

Assigned checkout: `/var/folders/6_/45pyyxdd7hz3wz33p813bx_c0000gn/T/nbskill-evidence-pilot-t465_4_g/b`.

## Behavior

The existing `_example_test_records` selector still uses `_following_examples` to stop at the next exported code cell. It preserves `_cell_calls_symbol` for direct-call examples and tests. New local helper `_assigned_result_check` walks module-body statements in source order, tracks simple name targets of direct call assignments, and selects assertions referencing tracked names. Stores, deletions, definitions, and imports invalidate attribution. Compound statement bodies do not establish result evidence. Unparseable source clears tracking. Aliases, mutation effects, and dynamic execution are outside this lookup.

The helper is cell `45b9ae61`, modified selector `472048bb`, rationale `6f72982c`, and compact executable proof `771dab13`. The disposable-notebook proof checks both review and edit views. It includes the separate result assertion and direct calls, excludes unrelated assertions, function/class assertions, assertions after rebinding, and evidence beyond the bundle. Its execution trap stays unexecuted and notebook bytes remain unchanged. No generated Python was edited directly; `edit_notebook` exported the notebook.

## Measurement

There were 17 logical repository source/context/search/read invocations before the implementation decision and `EVIDENCE_FOUND`. This includes two `AGENTS.md` reads and generated-owner routing; excluding those gives 14. The final ledger contains 27 invocations, including source review, style diagnostics, and an execution-approval metadata diff. Each API invocation counts once, independently of host envelopes or internal file accesses. Mutations, executions, documentation, and setup have separate ledgers.

No `experiments/`, `ROADMAP.md`, Git history, other checkout, or other participant's result was inspected. Working-tree diffs were used for required review and verification-artifact inspection. This report describes one execution without comparative conclusions.

## Ordered source/context/search/read ledger

Paths below are relative to the assigned checkout. Before decision means before `EVIDENCE_FOUND`, rather than before the first mutation. `ids(...)` abbreviates the explicit list of `dict(id=...)` query arguments.

| Order | Tool and arguments or scope | Reason | Result | Before decision |
| --- | --- | --- | --- | --- |
| S01 | `open_doc(Path('AGENTS.md'))` | Read current instructions. | Six-section outline. | Yes |
| S02 | `ag.view()` | Read complete instructions. | Notebook ownership, search, atomic edits, verification requirements. | Yes |
| S03 | `generated_owner(nbs.context.__code__.co_filename)` | Route exposed callable. | Returned `00_diagnostics.ipynb` because callable is wrapped; ordinary search was still needed. | Yes |
| S04 | `nbrg(r'def context|symbol.bundle|symbol_bundle|assertion', root='nbs', skip_dir='experiments', maxlen=200)` | Locate reader and evidence mechanisms. | Found reader, scoped foundation assertions, review cross-cell evidence. | Yes |
| S05 | `context('nbs/01_read.ipynb', view='summary')` | Orient. | First 50 of 287 cells; later narrowed reads. | Yes |
| S06 | `context('nbs/04_review.ipynb', query='checks=true', include_re='evidence|named|result', view='summary')` | Find executable precedents. | Cross-cell, mutation, context, property, local-binding fixtures. | Yes |
| S07 | `context('nbs/01_read.ipynb#context', mode='review', view='full', max_chars_per_cell=12000)` | Read routing and evidence contract. | Public function and review/edit rationale; long output truncated after examples. | Yes |
| S08 | `nbrg(r'evidence|bundle|rebind|binding|scoped_nodes', root=[read,review,foundation notebooks])` | Find attribution and scope tools. | Direct-call helper, result origins, scoped checks, relevant prose. | Yes |
| S09 | `context(read_path, include_re=r'def .*context|def .*symbol|related|bundle', view='summary', max_matches=100)` | Find selector by stable id. | Located `472048bb` and `c65a6118`; broad output truncated. | Yes |
| S10 | `context(review_path, chapter='Public API examples and tests', view='full')` | Attempt chapter read. | `ValueError: No chapter matches 'Public API examples and tests'`. Guessed name was a mistake; subsequent reads used observed ids. | Yes |
| S11 | `context(read_path, query=ids(contextcalls,d09929ba,c65a6118,472048bb), view='full')` | Read responsible code and prose. | Every selected cell currently needed a direct call; callback checks already handled. | Yes |
| S12 | `context(review_path, query=ids(380d3909,9b4b0884,65233518,f06cc4ae,f6d15aea), view='full')` | Inspect cross-cell precedent. | Result-origin tracking, mutation handling, separated assertion fixture. | Yes |
| S13 | `nbrg(r'def _following_examples|def _public_names_in_node|def .*bind|ast\.(Assign|AugAssign|NamedExpr|Delete)|result_origins', root=[foundation,read,review,graph,state notebooks])` | Search before adding helper. | Local assignment target extraction and private graph binding helpers. | Yes |
| S14 | `context(read_path, mode='overview')` | Confirm ownership and chapters. | Reader/public/Python/exact-cell chapters; 287 cells. | Yes |
| S15 | `context(read_path, query=ids(120bd75e,a16d35a9,ba6f8956,727ac178), view='full')` | Inspect bundle boundary, local target helper, imports. | Next exported cell ends bundle. Local target helper is narrower than needed rebinding invalidation. AST/scope tools already imported. | Yes |
| S16 | `context('nbs/10_graph.ipynb', query=ids(ed9ffabe,677472eb), view='full')` | Inspect package binding mechanism. | Private graph helpers address broader control flow; not imported across notebooks. | Yes |
| S17 | `context(review_path, query=ids(fd0a5028,b09c3c00), view='full')` | Inspect origins/check combination. | Whole-cell origin updates and wider evidence did not fit ordered bounded selector. | Yes |
| S18 | `context(read_path, query='headers', view='full')` | Place proof in narrative. | All 14 headings and handoff description. | No |
| S19 | `context(read_path, query=ids(fe440442,b0694a61), view='full')` | Check fixture imports/result structure. | Reused `write_demo_notebook`, `mk_cell`, `_example_context`, and `selection['examples']`; precedent checks review/edit. | No |
| S20 | `context(read_path, view='summary', max_matches=400)`; display `['text']` | Whole-notebook summary before editing. | All 287 rows returned; transport truncated a small middle portion. Responsible cells separately read in full. | No |
| S21 | `context('nbs/01_read.ipynb#472048bb', mode='edit')` | Refresh source and edit guard. | Exact source; expected hash used in implementation transaction. | No |
| S22 | `context('nbs/01_read.ipynb#6974d49f', mode='exact')` | Read adjacent claim before revision. | Existing claim described direct calls only. | No |
| S23 | `diff_nb(read_path, include_markdown=True)` | Review source/rationale changes. | New helper, modified selector, rationale, proof; metadata noise omitted. | No |
| S24 | `style_check(read_path, changed_only=True)` | Changed-source diagnostics. | One `large-generated-py` diagnostic, 1010 generated code lines. | No |
| S25 | `style_check(read_path)` | Whole notebook diagnostics. | Same module-size diagnostic; no private-helper diagnostic. | No |
| S26 | `context(read_path, query=ids(45b9ae61,472048bb,6f72982c,771dab13,6974d49f), view='full')` | Reread finished section. | Contract, proof, and neighboring claim consistent and adjacent. | No |
| S27 | `Git('.').diff(__='nbs/.nbskill-exec-approval.json')` | Inspect unexpected verification artifact before overwriting. | New helper approval and many reader hashes/line offsets refreshed. Long diff truncated; artifact left intact because no initial status snapshot established prior changes. | No |

`EVIDENCE_FOUND` was sent immediately after S17 with the count, responsible selector, preserved bundle boundary, and proposed ordered static tracking. Work continued after the message.

## Evidence that influenced decisions

- `472048bb` and `120bd75e` established that the missing assertion came from the per-cell evidence filter and that the local bundle boundary should remain intact.
- `d09929ba` and `c65a6118` explained the direct-call and callback cases. The matcher was preserved.
- Review cells `9b4b0884`, `b09c3c00`, and `f6d15aea` demonstrated cross-cell named-result evidence. Their broader whole-cell/mutation handling was rejected for this ordered, narrower request; no private helpers were imported across notebooks.
- Local assignment-target and private graph binding helpers were inspected before implementing invalidation. Existing public `scoped_nodes`, parsing, and call-name tools were reused.
- `b0694a61` supplied the review/edit result structure and precedent for checking both modes. Imported example readers also made clean post-export imports necessary.

## Documentation and setup

Documentation/catalog calls are separate: two host skill loads followed by 16 Python documentation/catalog invocations, in this order.

1. Host persistent-Python, Pyskills, coding-patterns skills. One guessed skill path was missing; the correct skill was loaded in this and the next call.
2. Host plugin persistent-Python, nbdev-editing, write-prose, jupyter-notebooks, kernel-notebook-editing skills.
3. `doc(clik, pysk, edsk)`.
4. `doc(dsk, exh, rgsk)`.
5. `doc(acp)`.
6. `list_pyskills()`.
7. `doc(nbs, nbds, open_doc, view_file)`.
8. `doc(nbs.context, nbs.generated_owner)`.
9. `doc(rgsk.nbrg)`.
10. `doc(nbs.edit_notebook, nbs.exec_nb, nbs.diff_nb, nbs.style_check)`.
11. `doc(nbe, write_demo_notebook)`.
12. `doc(nbe.NotebookEditor, nbe.NotebookEditor.insert)`.
13. `info_md(nbe.NotebookEditor.insert, source=True)` to recover structured insert-operation shape absent from the brief facade documentation. Counted as API documentation inspection.
14. `doc(ghs)`.
15. `doc(Git, file_exhash, wdocs, wsummary)`.
16. `doc(git.status)`.
17. `doc(git.diff)`.
18. `doc(exmagic.exhash_magic)`.

The exact requested persistent clikernel CLI command used the assigned checkout's `VIRTUAL_ENV`, `PATH`, interpreter, and working directory. The first launch failed because the sandbox prevented the gateway binding a local port. A reviewed escalated retry succeeded. Startup imports and delimiter protocol were followed. One post-export restart removed stale imports. Both kernels reported `nbskill.__file__` inside the assigned checkout. Setup and identity checks are excluded from source counts.

The normal test launcher's shebang printed a different prepared environment path despite the requested environment variables. That run returned `Success.`. The authoritative repeat explicitly invoked the assigned `.venv/bin/python` on the assigned `.venv/bin/nbdev-test`; it also returned `Success.` and printed paths under the assigned environment. No other checkout was inspected to diagnose this.

## Edits, mistakes, verification

Three `edit_notebook` transactions succeeded: add rationale/proof, shorten the proof and add an informative failure message, and add the helper plus modify selector/adjacent claim. An attempted proof revision had an unclosed triple-quoted argument and failed with IPython incomplete-input before any API call or mutation. The corrected transaction succeeded. The first proof exceeded the craft size threshold; shortening it to 20 lines removed that warning.

The first oversized report-save input was rejected by terminal input review before execution. The report was then saved through smaller exhash append calls.

| Execution/test invocation | Result |
| --- | --- |
| `exec_nb(read_path, up2id='771dab13', check_only=True, allow_new=True, show_output=False)` before implementation | Failed in the new proof with `AssertionError`. |
| Same red run with informative message | Failed with `771dab13: AssertionError: {'direct-check', 'result-example'}`. The separate assertion was absent. |
| Same run immediately after implementation/export in old kernel | Failed with the same evidence set because pre-export imports remained loaded. |
| Same run after clean kernel restart | Succeeded. |
| `exec_nb(read_path, check_only=True, allow_new=True, show_output=False)` | Succeeded for the full notebook without writing notebook outputs. |
| `nbdev-test nbs/01_read.ipynb` with requested `VIRTUAL_ENV` and `PATH` | `Success.`, but launcher output named another prepared interpreter environment. |
| Assigned `.venv/bin/python` executing assigned `.venv/bin/nbdev-test nbs/01_read.ipynb`, with requested environment | `Success.` |

The normal test emitted IPython and Matplotlib cache-directory warnings and used temporary caches. No test failed in the final assigned-interpreter run.

Both style checks reported exactly one diagnostic:

```text
large-generated-py: nbs/01_read.ipynb exported_py_path='<assigned-checkout>/nbskill/read.py' line_count=1010 1010 generated Python code lines; split this notebook/module with the split tool
```

Splitting the reader module is outside the bounded attribution request. It was not performed. Behavior verification passes with this module-size diagnostic still reported.

Final `git status --short` showed `nbs/01_read.ipynb`, regenerated `nbskill/read.py`, `nbskill/read_core.py`, `nbskill/_modidx.py`, and `nbs/.nbskill-exec-approval.json`. Safe execution regenerated approval metadata during verification. Its working-tree diff was inspected and reported to the parent. It was left intact because there was no initial status snapshot; restoring the entire file could discard an unknown earlier change. No commit was created.
