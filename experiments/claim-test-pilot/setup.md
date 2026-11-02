# Claim-to-test pilot preparation

Common repository revision: `5e01c575579b04f2bc593c463572525ae717016f`.

Two disposable local clones, `baseline` and `enriched`, share the task prompt in `task-prompt.txt`. Neither participant inherits the parent chat. The original variant runs first; the enriched variant starts after it finishes. Each participant uses the installed `nbskill` Pyskill and records discovery calls before implementation.

The original examples excluded Markdown but did not directly assert stored-output exclusion. Both clones received the same extension to example `c4dfad92`: a real temporary notebook contains the stream output `stored-only output`, and the assertion checks its absence from the source diff. This is a shared test-coverage addition, not a behavior change. It passes before either feature implementation. The new Markdown-option test must fail before and pass after each agent's implementation.

The enriched clone additionally has one Markdown cell, `5f30b200`, immediately after the `diff_nb` definition. It maps both promises to the exact assertions in `c4dfad92` and explains the code-only default, its tradeoff, and when to revisit it. Before dispatch, removing that one cell made the notebook models identical; the two generated `nbskill/review.py` files were byte-identical.

Environment preparation was excluded from discovery measurements. The exposed MCP kernel tools were unavailable. The matching installed clikernel/gateway CLI works when the aai workspace binary directory is selected. Each clone has a separate virtual environment with an editable nbskill installation and the declared project dependencies. Installed host tooling is shared through `host_tools.pth`; VIRTUAL_ENV selects the trial dependency directory. These are disposable environment settings, not repository or user configuration changes. Initial failures included a missing build dependency, an incomplete offline cache, and missing chkstyle/remold in the host environment. Both trial dependency installations completed successfully. Preflight execution through c4dfad92 passed in the prepared baseline environment.

Discovery counts include logical source/context/search/read API invocations, excluding tool documentation and environment setup. Each agent must freeze its count with EVIDENCE_FOUND before implementation and supply an ordered ledger. Counts are agent-reported and the ledgers are retained for review. Feature correctness and red/green verification are assessed separately from discovery counts.

Main-checkout additions were verified independently with exec_nb(check_only=True, allow_new=True) on the entire nbs/04_review.ipynb: ok=True, errors=[]. style_check on changed cells and on the whole notebook both returned 0 with zero diagnostics. The existing unrelated nbskill/SKILL.md change was left untouched.
