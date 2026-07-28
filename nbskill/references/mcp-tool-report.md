# nbskill MCP tool ranking

The default server has nine tools. Each has a distinct agent use-case.

| Rank | Tool | Use case |
| --- | --- | --- |
| 1 | `context` | Read the smallest useful notebook, symbol, caller, or callee context. |
| 2 | `edit_notebook` | Apply a deterministic, notebook-safe source change with structured diffs. |
| 3 | `exec_nb` | Check notebook behavior in an isolated execution. |
| 4 | `doctor` | Diagnose fatal setup, metadata, warning, and optional style problems. |
| 5 | `diff_nb` | Review notebook changes without raw JSON noise. |
| 6 | `filter_context` | Discover relevant code when no symbol is known yet. |
| 7 | `reference` | Find established implementations before adding nontrivial behavior. |
| 8 | `create_notebook` | Create a minimal nbdev source notebook when starting new work. |
| 9 | `healthcheck` | Confirm the MCP connection and installed capability surface. |

The server deliberately excludes `get_cells`, `move_cells`, and `style_check`. They remain Python APIs: raw-cell retrieval is covered by context for agents, moves are deliberate migrations, and doctor covers the normal diagnostic path.
