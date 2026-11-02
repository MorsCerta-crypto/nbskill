# Native nbskill roadmap

`aai-coding` uses `nbskill.skill` as its notebook backend. The Pyskill is the only agent-facing workflow.

Each stage delivers one observable behavior. Complete its real-world test before refactoring. A stage is finished only when the refactored result passes that same test again. Unit tests support these tests; they do not replace them.

## Test environment

Run each real-world test in a disposable worktree or clone of this repository. The agent must use the installed package and normal aai-coding discovery, not direct imports from a checkout, monkeypatches, or mock implementations. Use a small, meaningful notebook change and confirm it through the repository's normal notebook-aware verification. Record the prompt, files changed, commands or tools used, and result for each run.

## 1. Use the Pyskill for the core notebook workflow

**Build:** An installed `nbskill.skill` provides the core workflow directly: inspect notebook context, make a structured notebook edit, execute the affected scope, and review the change.

**Validate:** In a clean aai-coding session in a disposable checkout, ask the agent to make one small, meaningful change to an existing notebook. It must load the Pyskill, inspect the relevant context, edit the source notebook, execute the affected scope, and review the resulting notebook diff. The source notebook changes, its generated module is updated through the normal export path, and the focused check passes.

**Refactor:** Remove duplicate explanations and accidental API surface revealed by the run. Keep the documented workflow small enough that an agent can choose the next operation without reading internal module documentation.

## 2. Route notebook-owned source automatically

**Build:** aai-coding can distinguish a hand-written file from an nbdev-generated module and route only notebook-owned work to the installed Pyskill. It uses existing source-ownership information where available. A repository-level nbdev marker alone must not send every Python file through notebook tooling.

**Validate:** Give the agent a change request that starts at a generated module in a disposable checkout. The agent must locate the owning notebook, make the requested source change there, and verify it. In the same run, ask for a small change to a hand-written file and confirm that it stays on the normal aai-coding path. The generated module must never be edited directly.

**Refactor:** Reduce the routing instruction to the smallest durable rule. Run the two-file exercise again from a fresh session.

## 3. Support a complete notebook change

**Build:** The native notebook backend supports the decisions that matter before and after a nontrivial change: narrow context, impact or ownership lookup where needed, prior-art lookup, structured editing, focused execution, and change verification. The public surface groups these by task rather than exposing every internal helper.

**Validate:** In a disposable checkout, give an agent a real feature or bugfix drawn from the nbskill backlog. The change must be large enough to require finding an existing pattern or assessing callers. The agent must use the Pyskill path, update the notebook narrative and focused test when the behavior warrants it, and complete the smallest appropriate verification. Review the resulting notebook as a reader as well as a test runner.

**Refactor:** Keep only the operations that the successful run needed as top-level Pyskill concepts. Fold overlapping diagnostics into clear roles such as environment diagnosis and changed-source verification. Re-run the same task from a clean session.

## 4. Connect behavioral claims, tests, and decisions

**Build:** Let an agent identify which exact test checks a notebook's behavioral claim and why a non-obvious decision still applies. Start with one function bundle in `nbs/04_review.ipynb`, around `diff_nb`. In nearby Markdown, state two existing promises: the default diff excludes Markdown and stored outputs. Link each promise to the actual test cell by stable cell ID. Keep the explanation in Markdown rather than duplicating it in metadata. Record the reason for the code-only default, the tradeoff, and the condition under which that decision should be revisited in two or three sentences. Inspect the implementation and tests before stating those reasons; distinguish a proposed rationale from an established constraint.

**First step:** Prepare only this bundle and use the existing `context` workflow to retrieve it. A human reviewer must confirm that each linked assertion checks the stated promise. A call to the function alone is not a behavioral test. Do not add a general annotation schema, graph layer, or public API for this experiment.

**Validate:** Give an agent this real feature task in a clean session and disposable checkout:

> Extend `diff_nb` with an opt-in Markdown source diff so a reviewer can inspect changed explanations alongside code. Preserve the current default behavior and keep stored outputs excluded. Find the existing tests that protect these promises, explain the reason for retaining the default, add a focused failing notebook test for the new option, implement it in the source notebook, and complete notebook-aware verification. Add a claim-to-test link and a short decision rationale for the new behavior.

Run the same prompt from the same starting revision in two fresh sessions, first with the original notebook and then with only the prepared claim links and rationale added. Both runs use the installed package and normal Pyskill discovery. Record context/search calls before the agent identifies the relevant tests and rationale, wrong turns, and the final verification results. Review the changed explanation as well as the code diff. Preserve the red-before/green-after evidence for the new test.

The pilot succeeds if the prepared run finds the correct evidence with fewer context/search calls and completes the feature without weakening either existing promise. Record a tie or regression as such; two runs provide initial evidence, not a general speed claim. If successful, simplify the convention and repeat the enriched task from a fresh session before automating any relationship lookup.

**First pilot:** The [recorded comparison](experiments/claim-test-pilot/README.md) needed 10 notebook/source read or search calls without the added links and rationale, and 3 with them. Both agents completed the feature and passed notebook tests and style checks. This is one run per variant; repeat on another task before automating the convention.

## 5. Try further notebook mechanisms in small steps

The [trial journal](experiments/notebook-mechanisms/README.md) records direct use, verification, and discarded alternatives. Each retained change was committed before starting the next. These are self-use trials on this repository; the first claim-link pilot remains the only controlled comparison between two agents.

| Proposal | Result and evidence |
| --- | --- |
| Review explanations with code | Retained `diff_nb(..., include_markdown=True)`; the default and stored-output exclusions remain protected. |
| Show whether example evidence is current | Review/edit context now includes `execution` from `notebook_state`; `01_read.ipynb#b0694a61` checks stale output after a dependency changes. |
| Make laws executable | `02_edit.ipynb#a1ea6a4b` checks independent edits in both orders and an order-dependent counterexample; existing preview, hash, and rollback tests have explicit references. |
| Show decision boundaries | `00_foundation.ipynb#031a8dfd` contrasts generated and hand-written Python in the same nbdev project; the routing API stays unchanged. |
| Retrieve reasons, tests, and connections | The Pyskill teaches concrete `context` recipes, with explicit links distinguished from text-match candidates and static analysis limits. |
| Check explanation and evidence together | Markdown-aware diffs support human review, while context exposes recorded execution freshness. Automatic claims of semantic agreement were rejected. |

Do not add a query language, duplicate dependency analysis, routing abstraction, or general property-testing framework unless a concrete task demonstrates what the current tools cannot answer. Repeat the controlled comparison on another real change before claiming a general agent-efficiency gain.


## Guardrails

- Do not create a generic artifact-backend framework until a second specialized backend needs the same abstraction.
- Do not add a new public ownership or impact API if an existing capability answers the immediate routing question.
- Do not count a mocked unit test as a real-world test. Every stage needs an agent-run notebook edit in a clean, disposable nbdev project.
- Keep generated Python read-only. Notebook source remains the source of truth.
