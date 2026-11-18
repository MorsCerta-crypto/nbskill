# Development and releases

Use the shared Fastship command below to open a pull request and clean up its branch after the merge. Push a new version tag on the reviewed `main` commit to build and publish the private GitHub release.

See [DEVELOPMENT.md](DEVELOPMENT.md) for setup, tests, and releases and [WORKFLOW.md](WORKFLOW.md) for the shared policy.

<!-- ease-dev:start -->
## Gemeinsamer Entwicklungsablauf

Neue Arbeit beginnt auf einem `pr/<beschreibung>`-Branch vom aktuellen `main`. Führe im Projekt die Pflichtprüfungen aus und pushe den Arbeitsbranch. Wechsle danach in den Workspace `ease-ws` und öffne den Pull Request mit dem gemeinsamen Fastship-Helfer. Gib den Pfad zu deinem Projekt-Checkout oder Worktree an.

```sh
uv run scripts/open_pr.py <projekt-checkout> "<titel>" --body-file <beschreibung.md>
```

Der Pull Request geht direkt nach `main`. Nach Review und erfolgreichen Pflichtprüfungen folgt ein Merge-Commit. GitHub löscht danach den Remote-Branch. Der Fastship-Helfer wartet auf den Merge und entfernt den lokalen Arbeitsbranch, sobald der geprüfte Commit in `main` liegt und der Worktree sauber ist. Mit `--open-only` kehrt der Aufruf sofort zurück. Starte für die spätere lokale Bereinigung `uv run scripts/open_pr.py <projekt-checkout>` im Workspace.

Bei Anwendungen startet der erfolgreiche `main`-Lauf die eingerichtete Entwicklungsfreigabe. Ein Release-Tag beantragt die Produktionsfreigabe für den erprobten Kandidaten. Bei Bibliotheken startet der Release-Tag die Paketveröffentlichung. Die Projektanleitung nennt die Prüfkommandos, das Ziel und die Voraussetzungen. Die gemeinsame Regel steht in [WORKFLOW.md](WORKFLOW.md).
<!-- ease-dev:end -->

## Freigabepfad dieses Projekts

Veröffentliche die getestete Bibliothek unter einem numerischen Versionstag `<version>` in GitHub Releases. Die ausgelieferte Version umfasst Notebookquellen und den geprüften Export. Die automatische Veröffentlichung per Tag gehört zum Release-Workflow. GitHub Pages hat einen eigenen Dokumentationsweg.
