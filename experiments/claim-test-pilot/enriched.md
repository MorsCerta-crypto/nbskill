# Enriched claim pilot trial

`diff_nb(..., include_markdown=True)` reviews Markdown and code source together. Default behavior remains code-only. Stored outputs and raw cells stay excluded. No commits or pushes were made.

## Frozen discovery measurement

I sent `EVIDENCE_FOUND` before implementing after **5 logical source/context calls**: 2 AGENTS instruction reads and 3 notebook context calls. Tool documentation, startup and environment preflight were excluded. No elapsed-time comparison was measured and no faster-discovery claim is made.

The imported module was `/private/tmp/nbskill-claim-pilot-deao5n6a/enriched/nbskill/skill.py`; the distribution metadata path was this checkout's `nbskill.egg-info`. No sibling checkout or parent repository was inspected.

Ordered discovery ledger:

1. `exh.open_doc(trial/'AGENTS.md')`: instruction outline.
2. `ag.view()`: full checkout instructions.
3. `ns.context('project', scope=trial, view='summary', verbose=False)`: 50 of 2017 cells, mostly irrelevant diagnostics. Wrong turn; broad and truncated.
4. `ns.context('project', scope=trial, query='diff_nb', view='summary', verbose=False)`: located 30 matching cells, including evidence/rationale.
5. `ns.context(targets=[f'{nbpath}#c4dfad92', f'{nbpath}#19bf1c4e'], scope=trial, view='full', around=1, max_chars_per_cell=12000, verbose=False)`: exact evidence and rationale. The batch counts as one invocation.

Cell `c4dfad92` asserts `"answer = 42" in code_diff and "A prose explanation" not in code_diff` and `"stored-only output" not in code_diff`, using a real stored stream output. Cell `19bf1c4e` asserts `"value = 1" in code_diff and "Original note" not in code_diff`.

Cell `5f30b200` explained the default: focus review on executable source and avoid output/prose noise. Explanations require separate review. Cell `720c5b5c` gives the same executable-behavior rationale. The preparatory example enhancement and assertions remain intact.

## Behavior and decision

The trailing option is `include_markdown: bool = False`. A shared source selector serves Git comparisons and current-source additions. Existing stable identities, addition/change/deletion flags and cell filters remain in use. The working-tree helper was generalized to `_working_tree_sources(path, f=code_source)`. Opt-in blocks say `source cell`; defaults retain their original labels/messages. The option is restricted to `surface="code"`; combining it with `surface="public-ui"` raises `ValueError`.

Keeping the option off preserves existing callers' executable-source focus. Selecting cell source retains the output exclusion. The hidden test `986d6667` uses a real temporary Git repository to verify changed Markdown, default exclusion, current code/Markdown additions, and output/raw exclusion. Cell `5f30b200` links that claim to `04_review.ipynb#986d6667`. Cell `19bf1c4e` demonstrates the option after retaining its original assertion.

All edits used `ns.edit_notebook(..., auto_feedback=False)` with stable IDs and automatic export. Transactions inserted the failing test, implemented source selection and related prose, then updated the example. No raw notebook JSON or generated Python was edited manually.

## Red and green evidence

The red call was `ns.exec_nb(nbpath, up2id='986d6667', check_only=True, allow_new=True, show_output=False)`. It executed preceding cells, reached the new test and returned `ok=False` with:

```
986d6667: TypeError: diff_nb() got an unexpected keyword argument 'include_markdown'
```

The identical call after implementation failed audit subprocess checks in `revnogit`, `revmetadiff`, `revfilters`, and `986d6667`. Full returned errors are retained below. The changed `diff_nb` no longer matched its prior source approval. I did not bless it by changing approval configuration.

The focused `ns.exec_nb(nbpath, up2id='986d6667', check_only=True, allow_new=True, show_output=False, safe=False)` then returned `ok=True`, `errors=[]`, 145 executed code cells, target executed, and `dest=None`.

After updating the example, `ns.exec_nb(nbpath, check_only=True, allow_new=True, show_output=False, safe=False)` returned `ok=True`, `errors=[]`, 171 executed code cells, and `dest=None`. These in-memory checks did not write outputs.

The command environment was:

```sh
VIRTUAL_ENV=/private/tmp/nbskill-claim-pilot-deao5n6a/enriched/.venv PATH=/private/tmp/nbskill-claim-pilot-deao5n6a/enriched/.venv/bin:/Users/macbook/Projects/aai-ws/.venv/bin:$PATH
```

`nbdev-test nbs/04_review.ipynb` passed before the final example update and again after it, exiting 0 with `Success.`. The final run after restoring unrelated tool side effects is recorded below. The commands emitted IPython/Matplotlib warnings and used temporary cache directories. No environment configuration was changed.

`nbdev-export` exited 0. It regenerated unrelated pre-existing source duplication in `nbskill/read_core.py`. Safe execution updated `nbs/.nbskill-exec-approval.json`. Both files were clean at the initial status check; I inspected their full diffs and restored only those tool-produced changes. I retained the related `_modidx.py` helper rename.

`ns.style_check(nbpath, changed_only=True)` reported 0 diagnostics across 4 changed code cells. Whole-notebook `ns.style_check(nbpath)` reported 0 diagnostics, including after the final example update. All returned status 0. The implementation transaction warned about 6 touched cells and the existing long `diff_nb` cell growing to 56 lines; final style diagnostics were zero.

`ns.diff_nb(nbpath, ref_a='HEAD')` reviewed code changes. After clean-process testing and reloading the review API, `ns.diff_nb(nbpath, include_markdown=True)` reviewed code and explanations together. `git diff --check` exited 0.

## Post-discovery reading ledger

The frozen discovery count remained 5. Later source/context reads were:

6. `ns.context(nbpath, scope=trial, view='summary', max_matches=300, verbose=False)`: 233 of 233 cells; rendered display truncated.
7. `ns.context(nbpath, query='^## ', cell_type='markdown', view='full', verbose=False)`: no matches. Wrong turn: bare query used literal text.
8. `ns.context(f'{nbpath}#diff_nb', view='full', around=2, max_chars_per_cell=16000, verbose=False)`: implementation and truncated associated prose.
9. `ns.context(targets=[f'{nbpath}#_working_tree_code_sources', f'{nbpath}#_diff_filter_ids', f'{nbpath}#revfilters'], view='full', max_chars_per_cell=12000, verbose=False)`: selector/filter evidence.
10. `ns.context(nbpath, query='## ', cell_type='markdown', view='summary', verbose=False)`: 14 chapter/API headings.
11. `ns.context(targets=[f'{nbpath}#code_source', f'{nbpath}#e69d0ca1', f'{nbpath}#3cff0f46', f'{nbpath}#d185a451', f'{nbpath}#b69312bd'], view='full', max_chars_per_cell=12000, verbose=False)`: selector, helper, imports, Git reader. Large output truncated.
12. `ns.context('project', scope=trial, query='markdown', include_re='source', view='summary', max_matches=30, verbose=False)`: searched prior operations; 30 of 46 matches. No reusable diff selector beyond `code_source` found.
13. `ns.context('project', scope=trial, query='op="insert"', view='full', max_matches=3, verbose=False)`: failed with `ValueError: Unknown query key 'op'`. Wrong query syntax.
14. `ns.context(f'{nbpath}#_committed_review_notebook', view='full', max_chars_per_cell=10000, verbose=False)`: Git fixture.
15. `ns.context('project', scope=trial, query={'contains':'op="insert"'}, view='full', max_matches=2, verbose=False)`: one budget example; did not establish insertion schema.
16. `info_md(ne.NotebookEditor.insert, source=True)`: API documentation showed `insert_cells` schema. Tool documentation is excluded from the metric; retained here for reproducibility.
17. `ns.context(f'{nbpath}#29035109', view='full', verbose=False)`: fixed-argument Git commit fixture while investigating audit failures.
18. `ns.diff_nb(nbpath, ref_a='HEAD')`: source verification.
19. `ns.diff_nb(nbpath, include_markdown=True)`: final code and prose verification.
20. `git diff -- nbs/.nbskill-exec-approval.json nbskill/_modidx.py nbskill/read_core.py`: inspected side effects before restoring unrelated changes.

Kernel startup, tool/module docs, `list_pyskills()`, environment verification and status calls are excluded. One accidental no-op `edit_notebook(... dry_run=True)` preceded the actual example update; it returned `changed=False` and wrote nothing. One oversized attempt to send this report through `write_stdin` was rejected; smaller cells succeeded. These were implementation/reporting wrong turns after the frozen measurement.

21. `exh.open_doc(trial/'TRIAL_REPORT.md')` verified the completed experiment artifact outline. The artifact contains the full failure output. This post-verification read does not change the frozen discovery metric.

## Final state

The final clean-process `nbdev-test nbs/04_review.ipynb` after cleanup exited 0 with `Success.`. Changed files are `nbs/04_review.ipynb`, its generated `nbskill/review.py`, the generated `nbskill/_modidx.py`, and this report. Initial preparation changes to the example were preserved.

The whole repository test suite was not run. Safe `exec_nb` still fails the changed Git-diff path under the prior source approval. Ordinary full-notebook execution and clean-process notebook tests pass. No approval/configuration changes remain.

## Complete safe-run errors

```text
revnogit: PermissionError: Audit: subprocess.Popen blocked in sandbox with args: ('git', ['git', '-C', '/var/folders/6_/45pyyxdd7hz3wz33p813bx_c0000gn/T/nbskill-exec-t_obk31_', 'rev-parse', '--show-toplevel'], None, None)
Call chain: threading.Thread._bootstrap -> threading.Thread._bootstrap_inner -> ipymini.term.io._ThreadLocalIO._install_thread_context.<locals>._start.<locals>._run -> threading.Thread.run -> nbskill.execute._run_async.<locals>.target -> asyncio.runners.run -> asyncio.runners.Runner.run -> asyncio.base_events.BaseEventLoop.run_until_complete -> asyncio.base_events.BaseEventLoop.run_forever -> asyncio.base_events.BaseEventLoop._run_once -> asyncio.events.Handle._run -> asyncio.tasks.wait_for -> nbskill.execute.run.<locals>.call_runner -> safepyrun.core.RunPython.__call__ -> safepyrun.core._run_python -> nbskill.execute._eval_notebook_source -> __main__.<module> -> nbskill.diagnostics.track_call.<locals>.tracked -> __main__.diff_nb -> __main__._git_ref_path_error -> subprocess.run -> subprocess.Popen.__init__ -> subprocess.Popen._execute_child
```

```text
revmetadiff: PermissionError: Audit: subprocess.Popen blocked in sandbox with args: ('git', ['git', '-C', '/var/folders/6_/45pyyxdd7hz3wz33p813bx_c0000gn/T/nbskill-exec-t_obk31_/nbskill/04_review_git_metadata', 'rev-parse', '--show-toplevel'], None, None)
Call chain: threading.Thread._bootstrap -> threading.Thread._bootstrap_inner -> ipymini.term.io._ThreadLocalIO._install_thread_context.<locals>._start.<locals>._run -> threading.Thread.run -> nbskill.execute._run_async.<locals>.target -> asyncio.runners.run -> asyncio.runners.Runner.run -> asyncio.base_events.BaseEventLoop.run_until_complete -> asyncio.base_events.BaseEventLoop.run_forever -> asyncio.base_events.BaseEventLoop._run_once -> asyncio.events.Handle._run -> asyncio.tasks.wait_for -> nbskill.execute.run.<locals>.call_runner -> safepyrun.core.RunPython.__call__ -> safepyrun.core._run_python -> nbskill.execute._eval_notebook_source -> __main__.<module> -> nbskill.diagnostics.track_call.<locals>.tracked -> __main__.diff_nb -> __main__._git_ref_path_error -> subprocess.run -> subprocess.Popen.__init__ -> subprocess.Popen._execute_child
```

```text
revfilters: PermissionError: Audit: subprocess.Popen blocked in sandbox with args: ('git', ['git', '-C', '/var/folders/6_/45pyyxdd7hz3wz33p813bx_c0000gn/T/nbskill-exec-t_obk31_/nbskill/04_review_git_filters', 'rev-parse', '--show-toplevel'], None, None)
Call chain: threading.Thread._bootstrap -> threading.Thread._bootstrap_inner -> ipymini.term.io._ThreadLocalIO._install_thread_context.<locals>._start.<locals>._run -> threading.Thread.run -> nbskill.execute._run_async.<locals>.target -> asyncio.runners.run -> asyncio.runners.Runner.run -> asyncio.base_events.BaseEventLoop.run_until_complete -> asyncio.base_events.BaseEventLoop.run_forever -> asyncio.base_events.BaseEventLoop._run_once -> asyncio.events.Handle._run -> asyncio.tasks.wait_for -> nbskill.execute.run.<locals>.call_runner -> safepyrun.core.RunPython.__call__ -> safepyrun.core._run_python -> nbskill.execute._eval_notebook_source -> __main__.<module> -> nbskill.diagnostics.track_call.<locals>.tracked -> __main__.diff_nb -> __main__._git_ref_path_error -> subprocess.run -> subprocess.Popen.__init__ -> subprocess.Popen._execute_child
```

```text
986d6667: PermissionError: Audit: subprocess.Popen blocked in sandbox with args: ('git', ['git', '-C', '/var/folders/6_/45pyyxdd7hz3wz33p813bx_c0000gn/T/nbskill-exec-t_obk31_/nbskill/04_review_markdown_diff', 'rev-parse', '--show-toplevel'], None, None)
Call chain: threading.Thread._bootstrap -> threading.Thread._bootstrap_inner -> ipymini.term.io._ThreadLocalIO._install_thread_context.<locals>._start.<locals>._run -> threading.Thread.run -> nbskill.execute._run_async.<locals>.target -> asyncio.runners.run -> asyncio.runners.Runner.run -> asyncio.base_events.BaseEventLoop.run_until_complete -> asyncio.base_events.BaseEventLoop.run_forever -> asyncio.base_events.BaseEventLoop._run_once -> asyncio.events.Handle._run -> asyncio.tasks.wait_for -> nbskill.execute.run.<locals>.call_runner -> safepyrun.core.RunPython.__call__ -> safepyrun.core._run_python -> nbskill.execute._eval_notebook_source -> __main__.<module> -> nbskill.diagnostics.track_call.<locals>.tracked -> __main__.diff_nb -> __main__._git_ref_path_error -> subprocess.run -> subprocess.Popen.__init__ -> subprocess.Popen._execute_child
```
