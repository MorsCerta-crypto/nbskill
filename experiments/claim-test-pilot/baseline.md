# Baseline agent trial

`diff_nb` now accepts `include_markdown=True` to review Markdown source alongside code. The default remains code-only. Stored outputs and raw cells remain excluded. The focused test, full notebook execution, standard notebook test command, and notebook style checks passed.

This is an experiment artifact. Work stayed in `/private/tmp/nbskill-claim-pilot-deao5n6a/baseline`. I did not inspect sibling directories, request implementation help, commit this checkout, or push changes. Existing tests create commits only in disposable fixture repositories.

## Discovery measurement

The frozen discovery count was **12 logical source/context/search calls**, including two reads of this checkout's `AGENTS.md`. The notebook/source-only subtotal was **10**. Documentation, startup, and environment preflight were excluded. I sent `EVIDENCE_FOUND` immediately after call 12, before implementation. No speed improvement was measured or claimed.

Existing evidence in `nbs/04_review.ipynb`:

- `c4dfad92`: `assert "answer = 42" in code_diff and "A prose explanation" not in code_diff` and `assert "stored-only output" not in code_diff`. This common preparatory example enhancement was preserved unchanged.
- `19bf1c4e`: `assert "value = 1" in code_diff and "Original note" not in code_diff`.
- `revmetadiff`: `assert "No code cell changes" in text` and `assert "Ignored nbskill metadata changes in 1 cell" in text`.
- `720c5b5c`: the reason for the default was to keep Markdown and metadata churn out of the main diff so reviewers can see executable behavior changes.

The ordered discovery ledger follows. `context` means `nbskill.skill.context`; `nbrg` means `rgapi.skill.nbrg`.

1. `open_doc(Path('AGENTS.md'))` returned the checkout instruction outline.
2. `agent_notes.view()` read the complete instructions.
3. `context('project', view='summary')` returned 50 of 2016 matches. It was too broad and rendered truncated.
4. `nbrg(r'def diff_nb', root='nbs')` located `04_review.ipynb#fe9b3c86`.
5. `context('nbs/04_review.ipynb', view='summary', max_matches=250)` returned 232 cells. Its rendering was truncated.
6. `context('nbs/04_review.ipynb', view='summary', query=r'diff_nb|## ', max_matches=100)` returned zero matches. I incorrectly treated the literal query field as a regular expression.
7. `context('nbs/04_review.ipynb', view='summary', include_re=r'diff_nb|^## ', max_matches=100)` returned 25 relevant summary rows.
8. `context('nbs/04_review.ipynb', view='full', include_re=r'deliberately compares|review_diff_lesson|revmetadiff|outputs|markdown', cell_type='code', max_chars_per_cell=6000, max_matches=40)` matched 25 cells. It was too broad and rendered truncated before the needed tests.
9. `context('nbs/04_review.ipynb#19bf1c4e', view='full', around=1, max_chars_per_cell=9000)` exposed the Markdown-exclusion test and neighboring rationale `720c5b5c`.
10. `context('nbs/04_review.ipynb#revmetadiff', view='full', around=1, max_chars_per_cell=10000)` exposed metadata-exclusion and neighboring filter assertions.
11. `context('nbs/04_review.ipynb', view='summary', include_re=r'outputs|output', chapter='Public UI text surface', max_matches=30)` narrowed output-related evidence to 11 rows.
12. `context('nbs/04_review.ipynb#c4dfad92', view='full', max_chars_per_cell=12000)` exposed stored-output exclusion. Evidence discovery was complete and the count was frozen.

Before these reads, I accidentally attempted `cat /Users/macbook/.codex/skills/rubbish`. It failed because the path did not exist. This unsuccessful skill-documentation read is excluded from the source-discovery count. The overbroad reads and literal-query mistake above are the other discovery wrong turns. They remain counted.

## Environment and reproducible execution

The authorized CLI kernel command was:

```sh
VIRTUAL_ENV=/private/tmp/nbskill-claim-pilot-deao5n6a/baseline/.venv PATH=/private/tmp/nbskill-claim-pilot-deao5n6a/baseline/.venv/bin:/Users/macbook/Projects/aai-ws/.venv/bin:$PATH /private/tmp/nbskill-claim-pilot-deao5n6a/baseline/.venv/bin/python /Users/macbook/Projects/aai-ws/.venv/bin/clikernel
```

It ran with `tty:true`, this checkout as `workdir`, and the trial-authorized local gateway escalation. I followed startup documentation, ran `list_pyskills()`, and loaded `nbskill.skill` and selected callable documentation. The first kernel used delimiter `--Jwqjb`; the clean verification kernel used `--n9ef9`.

Both `Path(ns.__file__).resolve()` and `importlib.metadata.distribution('nbskill').locate_file('nbskill/skill.py').resolve()` resolved to `/private/tmp/nbskill-claim-pilot-deao5n6a/baseline/nbskill/skill.py`. The fresh kernel imported `nbskill.review` from this checkout too. I did not change `sys.path`, monkeypatch dependencies, or edit raw notebook JSON or generated Python source.

## Test first, then implementation

The first `edit_notebook` transaction used `op='insert_cells'`, `anchor_id='revfilters'`, `where='after'`, and `auto_feedback=False`. It added hidden test cell `7bfde57f`. The cell changes code, Markdown, and raw source in a disposable Git notebook containing stored output. It compares the default, opt-in Git changes, and opt-in current additions. It asserts promised source inclusion and output/raw exclusion rather than a complete formatted report.

The actual red call was:

```python
ns.exec_nb('nbs/04_review.ipynb', up2id='7bfde57f', check_only=True,
           allow_new=True, exc_stop=True, show_output=False)
```

It raised at line 14 of the new cell before implementation:

```text
TypeError: diff_nb() got an unexpected keyword argument 'include_markdown'
```

The statement was `markdown_diff = diff_nb(path, include_markdown=True)`. Earlier fixtures and default checks reached that point successfully. The exception prevented a returned result dictionary.

The implementation used a second atomic `edit_notebook` call with 11 related `replace_text` operations across four cells:

- `e69d0ca1` generalized the loader to `_working_tree_sources(path, f=code_source)`.
- `fe9b3c86` appended `include_markdown: bool = False`, selected Markdown when requested, used the same selector for Git and current additions, and used `source cell` report labels in opt-in mode. Default labels and empty-report wording stay unchanged.
- `5b4d2328` documented the option and the existing exclusions.
- `720c5b5c` recorded the rationale and links to tests `7bfde57f` and `c4dfad92`.

Both edit transactions exported `nbskill/review.py` with no drift. The implementation transaction emitted a `large-code-cell` craft warning for the existing large `diff_nb` cell. Later changed-source and full notebook diagnostics reported zero diagnostics.

A trailing Boolean option permits code and explanation review together while retaining existing surface values and positional calls. The option applies to the code surface. Combining it with `surface='public-ui'` raises `ValueError("include_markdown requires surface='code'")`, because that surface extracts text from Python calls. The default stays code-only to keep executable changes easy to inspect without prose or metadata churn. Both modes compare source only. The notebook links the opt-in claim to `04_review.ipynb#7bfde57f` and the default/output promises to `04_review.ipynb#c4dfad92`.

## Verification results

Two attempted green runs encountered safe-runner subprocess audit errors after the notebook function changed. The first used no explicit `allow`. The second used a clean kernel and `allow='nbskill.review.diff_nb'`. Each returned `ok=False` with four `PermissionError` entries at `revnogit`, `revmetadiff`, `revfilters`, and `7bfde57f`. A representative error was:

```text
PermissionError: Audit: subprocess.Popen blocked in sandbox with args: ('git', ['git', '-C', '<scratch notebook directory>', 'rev-parse', '--show-toplevel'], None, None)
```

The generated execution policy marks the changed function as unapproved for external effects. The documented `allow` parameter granted `subprocess.run` for local Git fixtures in subsequent runs. Safe execution stayed enabled. No project policy was manually weakened.

Exact final calls and results:

```python
green_subprocess = ns.exec_nb('nbs/04_review.ipynb', up2id='7bfde57f',
    check_only=True, allow_new=True, allow='subprocess.run', show_output=False)
# {'ok': True, 'errors': [], 'executed': 145, 'dest': None}

source_review = ns.diff_nb('nbs/04_review.ipynb', include_markdown=True)
# Reviewed implementation, test, changed Markdown, and prepared example.
# Included "Ignored nbskill metadata changes in 1 cell."

changed_style = ns.style_check('nbs/04_review.ipynb', changed_only=True)
# 0 diagnostic(s) across 4 changed cell(s).
# Notebook craft: 0 diagnostic(s). Return value: 0.

full_run = ns.exec_nb('nbs/04_review.ipynb', check_only=True,
    allow_new=True, allow='subprocess.run', show_output=False)
# {'ok': True, 'errors': [], 'executed': 171, 'dest': None}

full_style = ns.style_check('nbs/04_review.ipynb')
# 0 diagnostic(s). Notebook craft: 0 diagnostic(s). Return value: 0.
```

The full run includes existing default, metadata, filter, and public-UI checks plus the new opt-in test. `check_only=True` did not write execution outputs or metadata into the notebook file. I re-read the changed rationale and test with their neighboring cells. The clean verification kernel called the installed Pyskill's exported `ns.diff_nb(..., include_markdown=True)` for the source review.

The standard commands ran with the same `VIRTUAL_ENV` and `PATH` prefix as the kernel command:

```sh
nbdev-export
nbdev-test nbs/04_review.ipynb
```

`nbdev-export` exited 0 with no output. `nbdev-test nbs/04_review.ipynb` exited 0 and printed `Success.` IPython and Matplotlib warned that they used temporary writable cache directories, and Matplotlib built a font cache. There were no failures in this standard test run.

## Changed files and cleanup

The parent confirmed that initial dispatch status contained changes only in `nbs/04_review.ipynb` and `nbskill/review.py` from common preparation. Final intended files are:

- `nbs/04_review.ipynb`: implementation, focused test, explanation, rationale, and claim-to-test links. The prepared example remains unchanged.
- `nbskill/review.py`: regenerated notebook export.
- `nbskill/_modidx.py`: regenerated helper-name entry.
- `nbs/.nbskill-exec-approval.json`: automatically regenerated execution-policy evidence. The changed `diff_nb` hash is marked `allowed: false` for external effects. This is retained as trial evidence.
- `TRIAL_REPORT.md`: this report.

The repository-wide exporter also appended 353 unrelated lines to generated `nbskill/read_core.py`. `generated_owner` routed it to `nbs/01_read.ipynb`. I inspected the complete Git diff and found duplicated read/context definitions. After the parent confirmed the file was clean at dispatch, I restored only `nbskill/read_core.py` with `Git.restore`. No unrelated source notebook was edited. Re-running the repository-wide exporter can reproduce that pre-existing export drift; this trial does not fix it.

`Git.diff(check=True)` produced no whitespace errors. No checkout commit or push was made. The default safe runner still needs explicit trust for subprocess calls from the changed function; the successful verification arguments above record that requirement. A single large report payload was rejected by terminal transport size checking before execution. I split the payload and saved this report.

