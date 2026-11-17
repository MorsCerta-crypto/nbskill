# Development and releases

Start from `main`, open a pull request to `main`, and merge after review and the required checks. The Fastship publisher uploads a library release from the corresponding checked commit and version tag.

See [DEVELOPMENT.md](DEVELOPMENT.md) for setup, tests, and releases and [WORKFLOW.md](WORKFLOW.md) for the shared policy.

<!-- ease-dev:start -->
## Gemeinsamer Entwicklungsablauf

Neue Arbeit beginnt auf einem `pr/<beschreibung>`-Branch vom aktuellen `main`. Führe die Projektprüfungen aus und öffne den Pull Request direkt nach `main`. Verwende den projektspezifischen Fastship-Wrapper, wenn er einen Pull Request getrennt vom Merge erstellen kann. Sonst verwende `gh pr create --base main`. Nach Review und erfolgreichen Pflichtprüfungen folgt ein Merge-Commit. In Repositories mit aktiviertem GitHub Auto-Merge kann GitHub diesen Schritt übernehmen.

Bei Anwendungen startet der erfolgreiche `main`-Lauf die eingerichtete Entwicklungsfreigabe. Ein Release-Tag beantragt die Produktionsfreigabe für den erprobten Kandidaten. Bei Bibliotheken startet der Release-Tag die Paketveröffentlichung. Die Projektanleitung nennt die Prüfkommandos, das Ziel und die Voraussetzungen. Die gemeinsame Regel steht in [WORKFLOW.md](WORKFLOW.md).
<!-- ease-dev:end -->

## Freigabepfad dieses Projekts

Veröffentliche die getestete Bibliothek unter einem numerischen Versionstag `<version>` in GitHub Releases. Die ausgelieferte Version umfasst Notebookquellen und den geprüften Export. Die automatische Veröffentlichung per Tag gehört zum Release-Workflow. GitHub Pages hat einen eigenen Dokumentationsweg.
