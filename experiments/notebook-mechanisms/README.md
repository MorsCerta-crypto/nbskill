# Notebook mechanism trials

These changes are evaluated by using the installed notebook tools on this repository. A retained change gets its own commit after focused notebook execution, a source review, style checks, and a clean-process notebook test. The initial claim-link experiment is recorded in `../claim-test-pilot/README.md`.

## Review explanations together with code: retained

The earlier pilot implemented an opt-in Markdown source view in two disposable checkouts. The enriched implementation was brought into the source notebook using `edit_notebook`, with the new test added first. Cell `04_review.ipynb#23ca95b1` initially failed with `TypeError: diff_nb() got an unexpected keyword argument 'include_markdown'`. The implementation then passed all 171 code cells with `exec_nb(check_only=True, allow_new=True, allow='subprocess.run')`. Whole-notebook style diagnostics were zero, and `nbdev-test nbs/04_review.ipynb` printed `Success.` in the isolated environment containing this checkout's editable installation.

A fresh kernel used `diff_nb('nbs/04_review.ipynb', include_markdown=True)` to review this implementation in the actual repository. The result showed the changed decision rationale, the claim-to-test reference, the implementation, and its example together. The default remains code-only; stored outputs and raw cells remain excluded. This closes the earlier gap where the review tool omitted the explanation being changed.

No generic semantic-consistency checker was added. A source diff makes changed explanations reviewable; it does not prove that arbitrary prose agrees with behavior. The historical candidate patches remain as experiment artifacts. Three extra blank lines at the ends of the pilot reports were removed after the first staged whitespace check reported them; meaningful unified-diff whitespace in the patch artifacts was preserved.
