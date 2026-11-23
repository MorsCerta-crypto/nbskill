---
name: jupyter-notebooks
description: Use nbskill.skill for nbdev notebook context search, structural and narrative review, clean diffs, and standalone notebook editing or execution.
---

# nbskill

Use `nbskill.skill` when working with nbdev notebooks or generated `.py` modules. Load it in Python and read its module documentation before calling functions:

```python
from pyskills import doc
import nbskill.skill as nbs
doc(nbs)
```

## Core loop

1. **Route Python files:** Call `nbs.generated_owner(py_path)` before editing any `.py` file; if it returns a `.ipynb`, edit that notebook instead of the generated module.
2. **Orient fast:** Call `nbs.nb_map()` for the project outline (chapters, exported symbols, hidden-cell ratio).
3. **Understand before editing:** Call `nbs.symbol_context("symbol")` or `nbs.chapter_context(path, "chapter")` to inspect explanations, definitions, nearby examples, callers, and output freshness in one call.
4. **Edit and execute:** Inside `aai-coding`, use `exhash` / `aidialog` and `nbdev-test`. Standalone, use `nbs.edit_nb(path, ops)` and `nbs.exec_nb(path, chapter=...)`.
5. **Review honestly:** Run `nbs.review_nb(path)` and `nbs.diff_nb(path)` before exporting with `nbdev-export`. Fix structural errors (cell order, `#| eval: false` dependencies, mixed imports, heading hygiene) and narrative gaps (excessive `#| hide`, missing or distant chapter examples/assertions).

## Good nbdev notebook style

- Organize one concept per H2 (`##`) chapter; put every heading in its own Markdown cell; open with `# Title` and `> Subtitle`.
- Keep prose lean: explain *why*, contracts, and edge cases; never narrate code line by line.
- Place a visible example and focused assertion inside the same chapter as the exported code; let related helpers share one clear lesson.
- Use `@patch` to explain class methods beside their code, bare final expressions instead of `print(x)`, and `expect_fail`/`test_fail` instead of manual `try`/`except`.
- Never use `#| hide` to conceal substantial logic or silence style checks.
