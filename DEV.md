# Development and releases

Verbindlich ist [WORKFLOW.md](WORKFLOW.md). development integriert geprüfte Änderungen; main enthält freigegebenen Quellcode. Deployments werden gesondert dokumentiert. Offene Branches und Worktrees bleiben bis zur nachgewiesenen Übernahme oder Sicherung erhalten. Die gemeinsame Regel ersetzt ältere Branch- und Bereinigungsanweisungen; die folgenden fachlichen Prüfkommandos bleiben gültig.

The maintained development guide is [DEVELOPMENT.md](DEVELOPMENT.md). It covers local hooks, notebook tests, documentation deployment, and the Fastship-based GitHub release process. README contains the exact version and source-tag pins for consumers.

## Änderungen und Freigaben

Das Repository bleibt im persönlichen GitHub-Konto. Erstelle Arbeitsbranches nach dem Muster `pr/<issue>-<beschreibung>` von `development` und öffne Pull Requests gegen `development`. Gib den geprüften Stand per Pull Request von `development` nach `main` mit einem Merge-Commit frei. Veröffentliche Bibliotheksversionen aus dem geprüften `main`-Commit. Verbraucher aktualisieren Paketpin und Lockfile nach der Veröffentlichung in einem eigenen Pull Request.

GitHub Actions führt den Syntaxcheck und die Source-Policy-Prüfung aus. Führe die in [DEVELOPMENT.md](DEVELOPMENT.md) beschriebenen Projektprüfungen lokal aus und halte das Ergebnis im Pull Request fest.

Prüfe Notebook-Lesen, Bearbeiten und Ausführen gegen die unterstützte nbdev-Version.
