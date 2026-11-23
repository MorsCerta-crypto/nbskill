# Agent Notes

This is an nbdev notebook-source repository. Edit notebooks in `nbs/`, never generated files in `nbskill/`.

## Workflow

- Load `from nbskill.skill import *` and read `doc(nbskill.skill)` for the notebook workflow and authoring guidelines.
- Keep notebooks concise, readable top to bottom, and free of `#| hide` walls.
- After editing notebooks: run `uv run nbdev-export`, `uv run nbdev-readme` (if `nbs/index.ipynb` changed), `uv run pytest -q`, `uv run nbdev-test --n-workers 0`, and `uv run python -c "from nbskill.review import check_nb; raise SystemExit(check_nb('nbs'))"`.

<!-- ease-workflow:start -->
## Verbindlicher Entwicklungsprozess

Es gilt die gemeinsame Regel in [WORKFLOW.md](WORKFLOW.md). Die zentrale Quelle liegt in ease-ws/WORKFLOW.md. Projektspezifische Kommandos stehen in [DEV.md](DEV.md).

Von `main` auf einem Arbeitsbranch entwickeln und per Pull Request direkt nach `main` übernehmen. Die Projektprüfungen und die Notebookquellen sind verbindlich. Offene Dateien, ungemergte Branches und Worktrees bis zur Übernahme oder Sicherung erhalten.

Lokale Branch-Guards mit `python3 .github/workflow_guard.py install` aktivieren. Bestehende projektspezifische Hooks bleiben erhalten. Bei Produkten verwaltet rsc die Deploymentreferenzen.
<!-- ease-workflow:end -->
