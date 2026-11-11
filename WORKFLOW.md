# Gemeinsamer Entwicklungs- und Releaseprozess

Diese verbindliche Regel gilt für den Workspace, die Plattform, Libraries und alle Produkte. Die Quelle liegt in `ease-ws/WORKFLOW.md`; `make policy-sync` verteilt identische Kopien und die zugehörigen Prüfungen. `make policy-check` erkennt Abweichungen. Projektspezifische Entwicklungsanleitungen ergänzen diese Regel um ihre Prüfkommandos.

## Bedeutung der Branches

| Branch | Verbindliche Bedeutung |
| --- | --- |
| `development` | Integrationszweig für geprüfte Featureänderungen. Er kann unfertige, deaktivierte Features enthalten und ist kein Nachweis eines Deployments. |
| `main` | Freigegebener, reproduzierbar geprüfter Quellstand. Er ist die Grundlage stabiler Releases und kein Zeiger auf die laufende Produktion. |
| `codex/<issue>-<beschreibung>` | Arbeitsbranch für ein Feature oder eine Korrektur. Parallele Arbeiten erhalten eigene Branches und Worktrees. |
| `codex/hotfix/<beschreibung>` | Dringende Korrektur auf Basis von `main`. Nach der Freigabe wird sie auch per Pull Request nach `development` übernommen. |
| `deployed/dev`, `deployed/prod` | Ausschließlich von rsc verwaltete Deploymentreferenzen für Produkte. Sie werden nach erfolgreicher Laufzeitprüfung aktualisiert. Libraries benötigen diese Referenzen nicht. |

Branches benennen Quellstände. Laufzeitumgebungen, Berechtigungen und Secrets werden gesondert konfiguriert. Kein Merge, Commit oder Push auf einen Quellbranch löst ein Produktionsdeployment aus.

## Featureentwicklung und Freigabe

1. Ziel und Abnahmekriterien in einem Issue festhalten. Einen Arbeitsbranch vom passenden aktuellen Integrationsstand erstellen. Vorhandene offene Dateien niemals durch einen Branchwechsel, Reset oder automatisches Stashing verdrängen.
2. Änderungen auf dem Arbeitsbranch entwickeln und früh einen Draft-Pull-Request nach `development` erstellen. Zwischenstände regelmäßig committen und pushen. Lokale Experimente mit Nachbarbibliotheken sind zulässig, ersetzen aber keine Releaseprüfung.
3. Die projektspezifischen Prüfungen aus einem reproduzierbaren Stand ausführen. Der Prüfnachweis nennt Commit, Abhängigkeiten, Testprofil, Ergebnis und übersprungene Prüfungen. Ein Syntaxcheck allein ist keine fachliche Freigabe.
4. Nach Review nach `development` integrieren. Unfertige Funktionen bleiben im Arbeitsbranch oder hinter einem standardmäßig deaktivierten Featureflag. Featureflags dürfen fehlende Datenbankkompatibilität nicht verdecken.
5. Den freizugebenden Stand über einen Pull Request von `development` nach `main` übernehmen. Zwischen diesen beiden dauerhaften Branches Merge-Commits verwenden, damit ihre gemeinsame Historie erhalten bleibt. Einen Hotfix über einen eigenen geprüften Pull Request nach `main` und anschließend nach `development` übernehmen.
6. Libraries aus einem sauberen freigegebenen Stand versionieren und veröffentlichen. Produkte übernehmen Libraryversionen bewusst in eigenen Pull Requests. Bestehende Releases und Tags niemals ersetzen.

Die lokalen Guards verbieten direkte Commits auf `development` und `main` sowie direkte Pushes und Löschungen dieser Remote-Branches. Das gilt auch für Libraries und unabhängig von `deployments = false`. Serverregeln müssen Reviews, Pflichtprüfungen und den Schutz vor Löschung und Force-Push zusätzlich erzwingen. Für rsc ist nur der Namensraum `deployed/*` freizugeben; der Deployer benötigt keine Ausnahme für Quellbranches.

Pflichtprüfungen in CI umfassen mindestens die Installation aus dem Lockfile, bei nbdev-Projekten den abweichungsfreien Notebook-Export und die Tests des Projekts. Ein Workflow, der nur Syntax prüft, erfüllt diese Pflicht nicht. Bis ein Repository diese Prüfungen in CI ausführt, nennt jeder Pull Request den lokalen Prüfnachweis nach Schritt 3. Ein Repository ohne erzwungene Serverregeln erhält keine Produktionsfreigabe.

Eine Änderung über mehrere Repositories verwendet in allen denselben Branchnamen. Jeder Pull Request nennt die zugehörigen Pull Requests. Die gemeinsame Prüfung verwendet genau diese Stände. Libraries werden zuerst integriert und veröffentlicht. Der Pull Request eines Verbrauchers bleibt Entwurf, bis er den veröffentlichten Tag pinnt.

## Dev- und Produktionsdeployment

Ein Produktrelease bindet Produktcommit, SDK- und Vertragsversion, Lockfiles, Manifest, Migrationsprüfsummen und Image-Digests. Aus dem freigegebenen Quellstand wird genau ein Kandidat gebaut. Dev und Prod verwenden denselben Kandidaten und dieselben Image-Digests, aber getrennte Konfigurationen und Infrastrukturpläne.

Den Kandidaten für die gemeinsamen Umgebungen Dev und Prod baut CI aus einem sauberen Checkout des Kandidatencommits. Ein auf einem Entwicklungsrechner gebautes Image ist dort kein Kandidat. Lokale Compose-Umgebungen sind davon nicht betroffen.

Dev verwendet synthetische Daten, eigene Datenbanken, Buckets, Worker-Queues, Dienstidentitäten, Secret-Versionen und Test-Mailziele. Die zentralen Core-, Identitäts- und Zahlungsdienste benötigen ebenfalls getrennte Testkonfigurationen. Entwicklungsprozesse erhalten keine Produktionszugänge.

rsc prüft den Kandidaten in Dev. Erst vollständige, dem Kandidaten zugeordnete Abnahmen und eine erneute persönliche MFA-Freigabe erlauben Produktion. Ein Merge nach `main` ersetzt diese Freigabe nicht. Beim Betrieb mehrerer verantwortlicher Personen muss eine andere Person die Produktion freigeben.

Der rsc-Releasestatus ist der maßgebliche Betriebsnachweis. Er hält Kandidat, Umgebung, Plan, Freigabe, Prüfnachweise und Ergebnis fest. Die zusätzlichen Referenzen `deployed/dev` und `deployed/prod` erleichtern die Git-Navigation. Fehlgeschlagene Git-Veröffentlichungen werden ohne erneutes Deployment wiederholt. Bereits gespeicherte Veröffentlichungen auf die alten Quellbranch-Ziele werden unter der Deploymentsperre auf die neuen Referenzen umgestellt und als eigenes Ereignis protokolliert. Historische veröffentlichte Ereignisse bleiben unverändert.

Nach dem Rollout müssen Readiness, fachliche Probe und Workerzustand zum konkreten Kandidaten passen. Ein Anwendungsrollback ist nur mit kompatiblem Schema zulässig. Ein Backup-Restore ist ein gesonderter, geprüfter Betriebsablauf.

## Kompatibilität und Prüfpflichten

Jedes Produkt hält seine eigene Releasefolge und gesperrten Abhängigkeiten. SDK-Paketversion, API-Vertrag, Datenbankschema und Jobformat werden getrennt versioniert. Eine Versionsabweichung ist nur mit nachgewiesener Kompatibilität freigegeben.

SDK- und Core-Änderungen benötigen Verbraucherprüfungen gegen die unterstützten Vertragsversionen. Vor einem Produktupgrade werden dessen eigener Start, Datenbankzugriff, Berechtigungen und Worker geprüft. Zentral relevante Änderungen benötigen gemeinsame Abnahmen mit betroffenen Produkten.

Core unterstützt die Vertragsversionen der aktuellen und der vorherigen SDK-Minor-Version. Ein Produkt außerhalb dieses Fensters aktualisiert sein SDK vor seiner nächsten Freigabe.

Ein Produkt verwendet Funktionen oder Daten eines anderen Produkts ausschließlich über einen im Manifest deklarierten Vertrag und die zentrale Austauschschicht von Core. Direkte Zugriffe auf Datenbank, Bucket oder Secrets eines anderen Produkts sind verboten. Daten eines Benutzers überschreiten eine Produktgrenze nur mit seiner ausdrücklichen, widerrufbaren Zustimmung. Das anbietende Produkt prüft vor seiner Freigabe die Verträge seiner deklarierten Verbraucher.

Migrationen zunächst additiv ausrollen, Daten nachziehen und Verbraucher umstellen. Alte Strukturen erst nach der Übergangsphase entfernen. Alte und neue Worker müssen gespeicherte Jobs während des Rollouts verarbeiten können. Destruktive Änderungen benötigen eine eigene Freigabe und einen geprüften Wiederherstellungsweg.

Produktfreigaben benötigen entsprechend ihrem Vertrag insbesondere Prüfungen für Anmeldung, Mandantentrennung, Zahlung beziehungsweise Kontingente, Storage, Worker-Wiederholungen, frische und bestehende Datenbanken, Export, Löschung und Restore. Nicht ausgeführte oder synthetische Providerprüfungen werden ausdrücklich benannt und gelten nicht als reale Betriebsabnahme.

## Offene Arbeit erhalten

Offene Branches und Worktrees sind zulässiger Arbeitsbestand. Ihre Anzahl oder ein Vorsprung von `development` gegenüber `main` ist allein kein Fehler. Der Workspace-Report unterscheidet Arbeitsdateien, unveröffentlichte Commits und Integrationsstände.

Vor dem Entfernen eines Branches oder Worktrees müssen Dateien gesichert und die relevanten Commits dauerhaft referenziert oder nachweislich übernommen sein. Nach einem Squash-Merge reicht die Git-Abstammung für diesen Nachweis nicht aus. Es gibt keine pauschale Löschung nach Branchname oder Alter.

Git-Bundles sichern referenzierte Commits, aber keine offenen Dateien. Nicht committete und unversionierte Dateien benötigen eine zusätzliche Sicherung. Ignorierte Daten, Zugangsdaten und lokale Datenbanken werden über ihre eigenen geschützten Sicherungsverfahren erhalten.

Zusätzliche Worktrees liegen im Verzeichnis `.worktrees` des Repositories oder in einem anderen dauerhaften Verzeichnis. `/tmp` und `/private/tmp` sind dafür nicht zulässig, weil das Betriebssystem sie bereinigt. Commits eines Arbeitsbranches werden spätestens am Ende des Arbeitstags gepusht.

## Einrichtung und Kontrolle

In einem einzelnen Checkout aktiviert `python3 .github/workflow_guard.py install` die lokalen Branch-Guards und erhält die bisher konfigurierten Hookprüfungen. Der Installer ist wiederholbar. Im Workspace installiert `make hooks` die Guards für alle Repositories. Bestehende Branches, Arbeitsdateien und zusätzliche Worktrees werden dabei nicht verändert.

`python3 .github/workflow_guard.py check` prüft die zentrale Regelkopie. Der zusätzliche CI-Job `Source policy` prüft bei Pull Requests nach `main` auch den Freigabeweg. Die vorhandenen projektspezifischen Qualitätsprüfungen bleiben erforderlich.

Änderungen an dieser Regel erfolgen zentral im Workspace. Anschließend `make policy-sync`, `make policy-check` und `make test` ausführen und die Änderungen in den betroffenen Repositories jeweils reviewen und übernehmen. Das Synchronisieren veröffentlicht keinen Code und verändert keine GitHub-Einstellungen.
