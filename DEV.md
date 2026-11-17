# Development and releases

Start from `main`, open a pull request to `main`, and merge after review and the required checks. The Fastship publisher uploads a library release from the corresponding checked commit and version tag.

See [DEVELOPMENT.md](DEVELOPMENT.md) for setup, tests, and releases and [WORKFLOW.md](WORKFLOW.md) for the shared policy.

<!-- ease-dev:start -->
## Gemeinsamer Entwicklungsablauf

Neue Arbeit beginnt auf einem `pr/<beschreibung>`-Branch vom aktuellen `main`. Führe die Prüfungen des Projekts aus und öffne einen Pull Request direkt nach `main`. Nach Review und erfolgreichen Pflichtprüfungen kann GitHub Auto-Merge übernehmen.

Bei einem Produkt startet ein erfolgreicher `main`-Lauf das eingerichtete Entwicklungsdeployment. Ein Release-Tag für den geprüften Commit startet die Produktionsfreigabe für denselben Kandidaten. Bibliotheken veröffentlichen ihre Version aus einem geprüften Commit in `main`. Der jeweilige Build- und Veröffentlichungsweg steht in dieser Anleitung und in den Workflows des Projekts. Die gemeinsame Regel und der Fastship-Ablauf stehen in [WORKFLOW.md](WORKFLOW.md).
<!-- ease-dev:end -->
