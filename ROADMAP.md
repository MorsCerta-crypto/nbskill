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

## Guardrails

- Do not create a generic artifact-backend framework until a second specialized backend needs the same abstraction.
- Do not add a new public ownership or impact API if an existing capability answers the immediate routing question.
- Do not count a mocked unit test as a real-world test. Every stage needs an agent-run notebook edit in a clean, disposable nbdev project.
- Keep generated Python read-only. Notebook source remains the source of truth.
