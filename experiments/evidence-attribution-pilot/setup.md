# Trial setup

The original condition is checkout `a` at `5e01c575579b04f2bc593c463572525ae717016f`. The condition with the new helper bundle is checkout `b` at `53d49c8`. Both are disposable local clones, outside the working repository. The current uncommitted user changes were not copied into either clone. The task's example-selection function has the same starting implementation; the helper bundle adds documentation, executable lessons, Markdown-aware review, and example execution evidence.

Both participants are fresh agents without parent-chat history. They receive the same task and logging instructions, a prepared editable package environment, and neutral checkout/report labels. They may not consult the roadmap, experiment artifacts, Git history, another checkout, or another participant. They run independently on the same model settings. The runs overlap, so wall time is not a speed metric.

The pre-existing disposable baseline/enriched dependency environments from the first pilot were reused, with only the editable nbskill package reinstalled against the respective new checkout. Each checkout has a `.venv` link to its environment. The first installation attempt hit a restricted uv cache; using a cache under `/private/tmp` completed both installations without additional dependency resolution. The persistent Python CLI remains necessary because the exposed MCP kernel creation schema has no Python option. Participants must verify their import path.

The independent oracle was written before either candidate was inspected. On the unchanged current implementation it passed six of seven requirements in each mode and failed the separated-assertion requirement. The required notebook includes a deliberate runtime exception; successful context retrieval is evidence that the source was analyzed without executing that notebook. The original working copy remains untouched by participant edits.

Results are one observation per condition. This compares the bundle as available to an agent; it is not an isolated causal test of each individual helper. Evidence of use will be reported separately from an improvement in outcome.


The dependency manifests match after excluding the editable nbskill source location: 60 shared entries. `dependencies.txt` preserves that common manifest. `manifest.json` fixes the task and oracle source hashes used for this trial.
