# Notebook mechanism trials

These changes are evaluated by using the installed notebook tools on this repository. A retained change gets its own commit after focused notebook execution, a source review, style checks, and a clean-process notebook test. The initial claim-link experiment is recorded in `../claim-test-pilot/README.md`.

## Review explanations together with code: retained

The earlier pilot implemented an opt-in Markdown source view in two disposable checkouts. The enriched implementation was brought into the source notebook using `edit_notebook`, with the new test added first. Cell `04_review.ipynb#23ca95b1` initially failed with `TypeError: diff_nb() got an unexpected keyword argument 'include_markdown'`. The implementation then passed all 171 code cells with `exec_nb(check_only=True, allow_new=True, allow='subprocess.run')`. Whole-notebook style diagnostics were zero, and `nbdev-test nbs/04_review.ipynb` printed `Success.` in the isolated environment containing this checkout's editable installation.

A fresh kernel used `diff_nb('nbs/04_review.ipynb', include_markdown=True)` to review this implementation in the actual repository. The result showed the changed decision rationale, the claim-to-test reference, the implementation, and its example together. The default remains code-only; stored outputs and raw cells remain excluded. This closes the earlier gap where the review tool omitted the explanation being changed.

No generic semantic-consistency checker was added. A source diff makes changed explanations reviewable; it does not prove that arbitrary prose agrees with behavior. The historical candidate patches remain as experiment artifacts. Three extra blank lines at the ends of the pilot reports were removed after the first staged whitespace check reported them; meaningful unified-diff whitespace in the patch artifacts was preserved.


## Execution evidence beside stored examples: retained

Task: decide whether the examples returned for `diff_nb` still describe the current source before relying on their stored output. Previously, `context(..., mode="review")` returned the example source and saved output without execution evidence. Review and edit views now attach `execution` from the existing public `notebook_state` operation: state, stale predecessors, uncertainty, and source/execution hashes. The text view prints the state and predecessor ids beside the example. No second dependency analyzer was introduced.

The focused test `01_read.ipynb#b0694a61` first failed with `KeyError: 'execution'`. It records execution hashes for a function and its example, changes the function, and checks that both context modes retain the saved result while identifying its stale dependency. After implementation, all 234 code cells passed `exec_nb(check_only=True, allow_new=True)`, the whole-notebook style report had zero diagnostics, and a clean `nbdev-test nbs/01_read.ipynb` passed.

A fresh kernel used the installed tool on `nbs/04_review.ipynb#diff_nb`. It reported cell `c4dfad92` as dirty and cells `099cf3f9`, `revnogit`, `d79acb1c`, and `revmetadiff` as stale, including `fe9b3c86` among the changed predecessors. This answers the concrete evidence question without a separate state lookup. A check-only run intentionally does not refresh saved execution metadata, so this warning can remain after a successful in-memory run. No speed claim follows from this self-use trial.

Repeated exports exposed an existing nbdev issue with this notebook's explicitly named second module: unchanged sections were appended to `read_core.py`. The generated duplicate additions were inspected and restored from the committed version; the changed default module `read.py` was exported normally. Unrelated concurrent repository edits were excluded from the commit. This trial does not fix the exporter.

## Executable laws and counterexamples: retained as a notebook lesson

Task: determine whether two planned cell edits may be combined in either order. Cell `02_edit.ipynb#a1ea6a4b` executes both orders through `edit_notebook` on real scratch notebooks and compares persisted ids and sources. It also checks a counterexample: a text replacement that creates the input of another replacement is order-dependent. This describes an existing, bounded behavior, so no production behavior was changed and no failing implementation test was manufactured.

The surrounding Markdown names the independence condition and points to the exact cell. Existing dry-run, stale-hash, and controlled rollback assertions received explicit references; they were reused instead of adding a property-testing framework or duplicating their fixtures. A dry-run on the actual `nbs/02_edit.ipynb` returned the proposed wording diff and left its bytes unchanged.

The isolated new lesson passed safe `exec_nb` using the installed public editing functions. Full safe execution of `02_edit.ipynb` reported `1ab147c1: AssertionError` in the existing feedback example and an audit denial of `_thread.start_joinable_thread` in existing concurrent-edits cell `a4d98276`. The ordinary clean-process `nbdev-test nbs/02_edit.ipynb` passed, as did whole-notebook style checking. These runner limitations were recorded, not hidden or repaired as part of a documentation change.

## Examples at the routing boundary: retained

Task: choose the source to edit when starting from a Python file in this repository. The existing generated-file example in `00_foundation.ipynb#031a8dfd` now puts a generated module and a hand-written module in the same real scratch nbdev project. Its assertion checks the two different ownership results together. Nearby Markdown explains why a repository marker is insufficient and links the separate multiline-header regression test.

Direct use on this checkout resolved `nbskill/foundation.py` to `nbs/00_foundation.ipynb` and returned `None` for `tests/test_exported_api.py`. All 203 code cells passed safe `exec_nb`; the normal notebook test also passed. The routing implementation and public API needed no change. The useful addition is the paired executable example, not another routing layer.

## Question-oriented retrieval: recipes retained, new query language rejected

Task: explain the code-only default of `diff_nb`, identify the assertion protecting it, and inspect a concrete implementation connection. `context(..., mode="review")` returned the claim table and decision rationale. `query="checks=true", include_re="diff_nb"` returned nine test/example candidates; `mode="exact"` on `c4dfad92` showed the two actual assertions. The static connection from `diff_nb` to `_working_tree_sources` was found. A query for the imported `nbs_pair` returned no connection, which illustrates the scope limit rather than proving independence.

`14_pyskill.ipynb` now teaches these three questions through the existing operations, distinguishes explicit claim links from source-text candidates, and warns that missing links or static chains are not evidence of absence. Its repository-specific code recipe is marked `eval: false` and was exercised manually against this checkout. No natural-language question parser, extra context mode, claim metadata schema, or impact API was added: the concrete task needed none of them. Markdown-aware review is also documented at the top-level Pyskill entry point.

Whole-notebook style checking passed. Safe `exec_nb` through the changed reading chapter passed all six selected code cells. Full safe execution exposed existing nested-runner restrictions: `pyskills.allow`, Git subprocesses, and environment restoration were denied. Full native `exec_nb(safe=False)` also failed the existing usage-statistics cells `7772ba16` and `84b4a538` with `FileNotFoundError: .../usage.json`; these tests need the ordinary execution context for their usage recording. The complete clean-process `nbdev-test nbs/14_pyskill.ipynb` passed. No runner policy was changed.

## Interpretation

The initial claim-link pilot remains the only controlled two-agent comparison. These follow-up trials establish that the additions work on real notebook files and answer concrete repository questions; they do not establish a general speed or accuracy improvement. Kept changes are the opt-in prose diff, visible execution evidence, bounded executable laws, a paired routing example, and explicit retrieval recipes. Rejected additions are automatic semantic truth checks, a second dependency analyzer, a property-testing framework, another routing layer, and a new question language.
