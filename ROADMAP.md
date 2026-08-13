# Native nbskill roadmap

`aai-coding` should use `nbskill.skill` as its notebook backend. The MCP server remains available for clients that need it, but it stops being the normal path for an aai-coding session.

Each stage delivers one observable behavior. Complete its real-world test before refactoring. A stage is finished only when the refactored result passes that same test again. Unit tests support these tests; they do not replace them.

## Test environment

Run each real-world test in a disposable worktree or clone of this repository. The agent must use the installed package and normal aai-coding discovery, not direct imports from a checkout, monkeypatches, or mock implementations. Use a small, meaningful notebook change and confirm it through the repository's normal notebook-aware verification. Record the prompt, files changed, commands or tools used, and result for each run.

## 1. Use the Pyskill for the existing core notebook workflow

**Build:** An installed `nbskill.skill` can provide the current core workflow directly: inspect notebook context, make a structured notebook edit, execute the affected scope, and review the change. Its instructions explain when to use those operations without describing a second coding workflow.

**Validate:** In a clean aai-coding session in the disposable nbskill checkout, ask the agent to make one small, meaningful change to an existing notebook. It must load the Pyskill, inspect the relevant context, edit the source notebook, execute the affected scope, and review the resulting notebook diff. MCP must be disabled for this test. The source notebook changes, its generated module is updated through the normal export path, and the focused check passes.

**Refactor:** Remove duplicate explanations and accidental API surface revealed by the run. Keep the documented workflow small enough that an agent can choose the next operation without reading internal module documentation. Repeat the same test with MCP still disabled.

## 2. Route notebook-owned source automatically

**Build:** aai-coding can distinguish a hand-written file from an nbdev-generated module and route only notebook-owned work to the installed Pyskill. It uses existing source-ownership information where available. A repository-level nbdev marker alone must not send every Python file through notebook tooling.

**Validate:** Give the agent a change request that starts at a generated module in the disposable checkout. The agent must locate the owning notebook, make the requested source change there, and verify it. In the same run, ask for a small change to a hand-written file and confirm that it stays on the normal aai-coding path. The generated module must never be edited directly.

**Refactor:** Reduce the routing instruction to the smallest durable rule and remove wording that tells aai-coding to begin notebook work through MCP. Run the two-file exercise again from a fresh session.

### Stage 2 validation record

- Build exercise, 2026-08-13: in `/private/tmp/nbskill-stage2.WL9j0I/repo`, installed the copied package with `uv sync`. The exercise began at generated `nbskill/skill.py`, resolved `nbs/14_pyskill.ipynb` through normal Pyskill discovery and `generated_owner`, changed that notebook with `edit_notebook`, ran `exec_nb(check_only=True)`, and reviewed its updated context. It then changed the hand-written `STAGE2_HANDWRITTEN.py` without notebook routing. The acceptance test passed with no MCP configuration in the disposable environment.
- Refactor exercise, 2026-08-13: repeated the same installed-Pyskill exercise from fresh `/private/tmp/nbskill-stage2-final.vyuR1W/repo` after shortening the routing rule and removing the stale MCP-first repository instruction. It again passed. The focused aai-coding hook test also confirmed that a generated path produces the native-Pyskill notice while a hand-written Python path produces none.

The current aai-coding virtual environment does not yet have nbskill and all of its dependencies installed, so its hook intentionally falls back to no routing there. Stage 5 owns making this installation automatic; the disposable installed-package exercises validate the intended Stage 2 behavior now.

## 3. Let the Pyskill support a complete notebook change

**Build:** The native notebook backend can support the decisions that matter before and after a nontrivial change: narrow context, impact or ownership lookup where needed, prior-art lookup, structured editing, focused execution, and change verification. The public surface groups these by task rather than exposing every internal helper.

**Validate:** In a disposable checkout, give an agent a real feature or bugfix drawn from the nbskill backlog. The change must be large enough to require finding an existing pattern or assessing callers. The agent must use the native Pyskill path, update the notebook narrative and focused test when the behavior warrants it, and complete the smallest appropriate verification. Review the resulting notebook as a reader as well as a test runner.

**Refactor:** Keep only the operations that the successful run needed as top-level Pyskill concepts. Fold overlapping diagnostics into clear roles such as environment diagnosis and changed-source verification. Re-run the same task from a clean session, using the refactored public surface.

### Stage 3 validation record

- Build exercise, 2026-08-13: the installed workspace package completed a native Pyskill change exercise with no MCP call. `prepare_change` read `nbs/14_pyskill.ipynb` and found the existing `generated_owner` implementation as local prior art. The exercise changed a fresh notebook from `answer = 41` to `answer = 42` through `edit_notebook`; `verify_change` then returned the code-cell diff, ran the selected scope without writing outputs, and reported changed-source diagnostics. The focused acceptance test passed.
- Refactor exercise, 2026-08-13: repeated the exercise in fresh `/private/tmp/nbskill-stage3.bham7u/repo` after installing that copied checkout with `uv sync`. The test discovered `nbskill.skill` through `list_pyskills`, imported only its five public operations, resolved `nbskill/skill.py` to its notebook owner, found the same local prior art, made the same notebook change, and verified it. `uv run pytest tests/test_stage3_native_acceptance.py -q` passed with no MCP configuration or import.

## 4. Keep MCP as an adapter over the same behavior

**Build:** MCP and the Pyskill call the same application behavior for their shared operations. MCP may retain transport concerns such as request validation, locking, time limits, and response formatting. It must not contain a competing notebook workflow or capabilities that the native interface lacks.

**Validate:** Run the same small notebook change twice in separate disposable checkouts: once through aai-coding and the Pyskill, and once through MCP. Both runs must reach the same source notebook, produce equivalent exported code and verification outcomes, and report actionable failures in the same situations.

**Refactor:** Move shared behavior behind the common boundary and remove duplicated orchestration. Preserve MCP compatibility and repeat the paired exercise after the refactor.

## 5. Install one authoritative set of instructions (superseded)

**Build:** Installation gives aai-coding enough routing guidance to discover and load `nbskill.skill` when notebook-owned work appears. Standalone agent instructions draw from the same authoritative skill documentation. Installation information and MCP connection details remain separate from notebook methodology.

**Validate:** In a fresh environment with aai-coding and nbskill installed, complete a notebook change without manually configuring MCP or copying instructions into the session. In a separate generic client, confirm that MCP installation still works for users who choose that transport. Both paths must use the same notebook behavior.

**Refactor:** Delete stale instruction copies and reduce generated instructions to the routing rule plus the native skill documentation. Keep MCP optional, documented, and tested. Repeat both fresh-environment tests.

### Stage 5 validation record

- Build and refactor exercise, 2026-08-13: `install_aai_coding_integration` now keeps the routing rule only in aai-coding's persistent-Python skill. Its runtime nbdev notice points to that live skill, and the installer removes the former managed nbskill sections from `README.md` and `SETUP.md`. The packaged routing skill and bootstrap `AGENTS.md` now point to `nbskill.skill`, which owns the native workflow. The focused installer test and the real aai-coding routing-hook test both passed.
- Fresh native exercise, 2026-08-13: installed copied aai-coding and the current nbskill package into `/private/tmp/nbskill-stage5.TlulFU/runtime` with Python 3.12. The initial `uv sync` exposed a pre-existing aai-coding metadata conflict because its supported Python range still includes 3.10 although direct dependencies require 3.11. In the isolated supported runtime, aai-coding discovered `nbskill.skill`, routed a generated module to its owner, and used the registered Pyskill to edit and prove a notebook change without MCP. The acceptance test passed.
- Optional transport exercise, 2026-08-13: in the same fresh runtime, a generic skill installation copied the compact routing skill, and a separate temporary Codex workspace received a valid `nbskill_mcp` configuration. Both focused tests passed.

Stage 6 replaces this installation design. The record remains for the history of the experiment; the installer must no longer modify an `aai-coding` checkout, a README, or a setup document.

## 6. Start fresh with a direct Pyskill

**Build:** `nbskill.skill` exposes the direct operations an agent needs: route with `generated_owner`, read with `context`, find prior art with `reference_query`, mutate with `edit_notebook`, and prove the result with `exec_nb`, `diff_nb`, and `style_check`. Its generated module docstring is the operational guide. `#| exportd` supplies a compact executable example without adding it to module code.

**Validate:** Build the package, import the installed Pyskill, and use it on a freshly created notebook. The run must inspect source, make a structured change, execute the affected scope without writing outputs, and review the code-cell diff. In a separate temporary install root, run `install_nbskill` and confirm it installs only package-owned skill files and optional MCP configuration. It must not return or execute aai-coding integration work.

**Refactor:** Delete wrapper orchestration, README-derived skill generation, and all code that discovers or changes an aai-coding checkout. Keep the MCP server as a supported adapter. Run both validations again from the refactored package.

### Stage 6 validation record

- Build and refactor exercise, 2026-08-13: `uv run nbdev-test --path nbs/14_pyskill.ipynb` rebuilt and installed the package, then changed a fresh notebook from `answer = 41` to `answer = 42` through the direct Pyskill. The test executed the affected scope in check-only mode and reviewed the code-cell diff. The test was written against the old wrapper API first and failed, then passed after the direct facade replaced it.
- Installation exercise, 2026-08-13: `uv run nbdev-test --path nbs/06_skill.ipynb` installed the package skill and Codex MCP configuration in a temporary root. The test first failed because the old result exposed `aai_coding`; it passed after removing all integration paths. `uv run nbdev-test --path nbs/13_cli.ipynb` and `uv run install_nbskill --help` then confirmed that the command-line interface no longer accepts aai-coding setup options.

## Guardrails

- Do not delete, deprecate, or disable the MCP server during this roadmap.
- Do not create a generic artifact-backend framework until a second specialized backend needs the same abstraction.
- Do not add a new public ownership or impact API if an existing capability answers the immediate routing question.
- Do not count a mocked unit test as a real-world test. Every stage needs an agent-run notebook edit in a clean, disposable nbdev project.
- Keep generated Python read-only. Notebook source remains the source of truth.
