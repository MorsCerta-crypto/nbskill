# Development and releases

Verbindlich ist [WORKFLOW.md](WORKFLOW.md). development integriert geprüfte Änderungen; main enthält freigegebenen Quellcode. Deployments werden gesondert dokumentiert. Offene Branches und Worktrees bleiben bis zur nachgewiesenen Übernahme oder Sicherung erhalten. Die gemeinsame Regel ersetzt ältere Branch- und Bereinigungsanweisungen; die folgenden fachlichen Prüfkommandos bleiben gültig.

The maintained development guide is [DEVELOPMENT.md](DEVELOPMENT.md). It covers local hooks, notebook tests, documentation deployment, and the Fastship-based GitHub release process. README contains the exact version and source-tag pins for consumers.

## Entwicklungsablauf nach dem Enterprise-Umzug

Dieser Abschnitt beschreibt den Ablauf im neuen Repository. Bis zur Umstellung gilt der bestehende Freigabeweg in [WORKFLOW.md](WORKFLOW.md).

1. Starte `feat/*` oder `fix/*` vom geschützten `main` und öffne mit `gh pr create` einen Pull Request gegen `main`. Führe vorher die projektspezifischen Prüfungen aus. Bei Änderungen über mehrere Repositories kannst du mit `fastws` gemeinsam gegen lokale Nachbarpakete testen; die CI prüft jedes Repository mit seinen eigenen gesperrten Abhängigkeiten.
2. GitHub Actions installiert aus dem Lockfile und führt die projektspezifischen Tests aus. Bei nbdev-Änderungen zusätzlich `nbdev-prepare` lokal und in CI den Export auf Abweichungen prüfen.
3. Nach Review und grünen Pflichtprüfungen den Pull Request in GitHub per Squash Merge übernehmen und den Featurebranch entfernen. `main` ist der dauerhafte Quellbranch. Staging und Produktion sind Umgebungen.
4. Veröffentliche Bibliotheksversionen aus einem geprüften `main`-Commit. `ship-bump` und `ship-changelog` können den Release-PR vorbereiten. Erst nach Veröffentlichung des Pakets oder des unveränderlichen Git-Pins aktualisieren Verbraucher ihren Pin und ihr Lockfile in einem eigenen Pull Request.

Prüfe Notebook-Lesen, Bearbeiten und Ausführen gegen die unterstützte nbdev-Version.
