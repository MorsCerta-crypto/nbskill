# Gemeinsamer Entwicklungs- und Releaseprozess

Diese Regel gilt für den Workspace, die Plattform, Libraries und alle Produkte. `ease-ws/WORKFLOW.md` ist die gemeinsame Quelle. `make policy-sync` verteilt die Regel und die zugehörigen Prüfungen. `make policy-check` erkennt Abweichungen. In `DEV.md` stehen die konkreten Entwicklungs-, Prüf- und Releasekommandos des Projekts.

## Bedeutung der Branches

| Branch | Verbindliche Bedeutung |
| --- | --- |
| `main` | Geschützter Standardbranch und dauerhafter Quellstand für Entwicklung und Releases. |
| `pr/<issue>-<beschreibung>` | Arbeitsbranch für ein Feature oder eine Korrektur. Parallele Arbeiten erhalten eigene Branches und Worktrees. |
| `deployed/dev`, `deployed/prod` | Ausschließlich von rsc verwaltete Deploymentreferenzen für Produkte. Sie werden nach erfolgreicher Laufzeitprüfung aktualisiert. Libraries benötigen diese Referenzen nicht. |

Branches benennen Quellstände. Laufzeitumgebungen, Berechtigungen und Secrets werden gesondert konfiguriert. Kein Merge, Commit oder Push auf einen Quellbranch löst ein Produktionsdeployment aus.

## Featureentwicklung und Freigabe

1. Einen Arbeitsbranch `pr/<beschreibung>` vom aktuellen `main` erstellen. Für parallele Arbeit einen eigenen Worktree verwenden und offene Dateien im bisherigen Worktree belassen.
2. Die Projektprüfungen aus `DEV.md` ausführen und einen Pull Request direkt nach `main` öffnen. Unfertige Funktionen bleiben im Arbeitsbranch oder hinter einem standardmäßig deaktivierten Featureflag. Featureflags setzen ein kompatibles Datenbankschema voraus.
3. Fastship kann ein Issue oder einen Pull Request über einen vorhandenen Repository-Wrapper erstellen. Der Wrapper setzt `main` als Ziel und überlässt den Merge den GitHub-Regeln. Wo kein Wrapper eingerichtet ist, den Pull Request mit `gh pr create --base main` öffnen. Das Standardkommando `ship-pr` versucht einen sofortigen Squash-Merge. Die EASE-Repositories verlangen Merge-Commits. Nach Review und erfolgreichen Pflichtprüfungen mergen oder GitHub Auto-Merge mit der Methode Merge-Commit verwenden. Der Prüfnachweis nennt den Commit, das Testprofil und ausgelassene Prüfungen.
4. Aus einem geprüften Commit in `main` veröffentlichen. Verbraucher übernehmen neue Libraryversionen über einen eigenen Pull Request mit aktualisiertem Lockfile. Veröffentlichte Tags und Releases bleiben unveränderlich.

Die lokalen Guards schützen `main`, veröffentlichte Tags und die rsc-Deploymentreferenzen. Auf GitHub erzwingen die Regeln für `main` Pull Requests, Pflichtprüfungen und den Schutz vor Löschung und Force-Push. Der rsc-Deployer schreibt ausschließlich seine Deploymentreferenzen.

Der Pflichtlauf im Pull Request installiert aus dem Lockfile, führt die Projektprüfungen aus und prüft bei nbdev den abweichungsfreien Notebook-Export. Ein Repository mit reiner Syntaxprüfung dokumentiert die vollständige lokale Prüfung im Pull Request, bis sein Pflichtlauf erweitert ist. Veraltete Läufe desselben Pull Requests werden abgebrochen. Der Download-Cache richtet sich nach Lockfile und Laufzeit. Auch Dokumentationsänderungen liefern den Pflichtstatus. Der Lauf auf `main` baut und prüft den tatsächlichen Merge-Stand für das Entwicklungsdeployment. Ein vorheriger Prüfnachweis gilt nur für denselben Quellbaum und dieselben Build-Eingaben.

Prüfjobs erhalten `contents: read` und speichern Checkout-Zugangsdaten nicht. Private Abhängigkeiten verwenden einen kurzlebigen GitHub-App-Installationstoken mit Leserechten für die konkreten Quellen im Lockfile. Für eine einzige private Quelle genügt ein eigener Read-only Deploy Key. Jobs mit diesen Zugangsdaten laufen nur für vertrauenswürdige Änderungen. Schreibrechte sind auf den jeweiligen Freigabejob begrenzt.

Eine Änderung über mehrere Repositories verwendet in allen denselben Branchnamen. Jeder Pull Request nennt die zugehörigen Pull Requests. Die gemeinsame Prüfung verwendet genau diese Stände. Libraries werden zuerst integriert und veröffentlicht. Der Pull Request eines Verbrauchers bleibt Entwurf, bis er den veröffentlichten Tag pinnt.

## Dev- und Produktionsdeployment

Bei einem Produkt startet ein erfolgreicher Lauf auf `main` das Entwicklungsdeployment, sobald Registry, rsc-Release-Dienst und Zielumgebung eingerichtet sind. Ein Release-Tag auf einem geprüften Commit in `main` startet die Produktionsfreigabe für denselben Kandidaten. rsc führt den Produktionsrollout nach der Freigabe aus. Bis die Voraussetzungen erfüllt sind, endet der Ablauf beim Prüfen und Bauen. In `DEV.md` stehen Tagformat, Startbedingung, Ziel und Einrichtungsstand.

Ein Produktrelease bindet Produktcommit, SDK- und Vertragsversion, Lockfiles, Manifest, Migrationsprüfsummen und Image-Digests. Aus dem freigegebenen Quellstand wird genau ein Kandidat gebaut. Dev und Prod verwenden denselben Kandidaten und dieselben Image-Digests, aber getrennte Konfigurationen und Infrastrukturpläne.

Den Kandidaten für die gemeinsamen Umgebungen Dev und Prod baut CI aus einem sauberen Checkout des Kandidatencommits. Ein auf einem Entwicklungsrechner gebautes Image ist dort kein Kandidat. Lokale Compose-Umgebungen sind davon nicht betroffen.

Dev verwendet synthetische Daten, eigene Datenbanken, Buckets, Worker-Queues, Dienstidentitäten, Secret-Versionen und Test-Mailziele. Die zentralen Core-, Identitäts- und Zahlungsdienste benötigen ebenfalls getrennte Testkonfigurationen. Entwicklungsprozesse erhalten keine Produktionszugänge.

rsc prüft den Kandidaten in Dev. Erst vollständige, dem Kandidaten zugeordnete Abnahmen und eine erneute persönliche MFA-Freigabe erlauben Produktion. Ein Merge nach `main` ersetzt diese Freigabe nicht. Beim Betrieb mehrerer verantwortlicher Personen muss eine andere Person die Produktion freigeben.

Der rsc-Releasestatus ist der maßgebliche Betriebsnachweis. Er hält Kandidat, Umgebung, Plan, Freigabe, Prüfnachweise und Ergebnis fest. Die zusätzlichen Referenzen `deployed/dev` und `deployed/prod` erleichtern die Git-Navigation. Fehlgeschlagene Git-Veröffentlichungen werden ohne erneutes Deployment wiederholt. Bereits gespeicherte Veröffentlichungen auf die alten Quellbranch-Ziele werden unter der Deploymentsperre auf die neuen Referenzen umgestellt und als eigenes Ereignis protokolliert. Historische veröffentlichte Ereignisse bleiben unverändert.

Nach dem Rollout müssen Readiness, fachliche Probe und Workerzustand zum konkreten Kandidaten passen. Ein Anwendungsrollback ist nur mit kompatiblem Schema zulässig. Ein Backup-Restore ist ein gesonderter, geprüfter Betriebsablauf.

## Library-Releases

Ein unveränderlicher Release-Tag startet Build, Installationsprobe und Veröffentlichung einer Bibliothek. Der Workflow prüft, dass der Tag zu der Paketversion passt und auf einen geprüften Commit in `main` zeigt. Bestehende Tagformate bleiben gültig.

DocAI und ease-ui veröffentlichen auf PyPI. Der Veröffentlichungsjob nutzt PyPI Trusted Publishing und erhält `id-token: write` für die Umgebung `pypi`. Interne Bibliotheken veröffentlichen die geprüften Artefakte am GitHub-Release ihres Repositorys. Nur der Job für GitHub-Releases erhält `contents: write`. Testläufe bauen und prüfen dieselben Artefakte ohne Veröffentlichung.

Fastship bereitet Release-Notizen vor und kann GitHub-Releases mit den bereits geprüften Artefakten anlegen. Wenn der Tag-Workflow die Veröffentlichung übernimmt, startet Fastship keinen zweiten Upload. In `DEV.md` stehen das Buildkommando, das Tagformat, das Ziel und der Einrichtungsstand.

## Kompatibilität und Prüfpflichten

Jedes Produkt hält seine eigene Releasefolge und gesperrten Abhängigkeiten. SDK-Paketversion, API-Vertrag, Datenbankschema und Jobformat werden getrennt versioniert. Eine Versionsabweichung ist nur mit nachgewiesener Kompatibilität freigegeben.

SDK- und Core-Änderungen benötigen Verbraucherprüfungen gegen die unterstützten Vertragsversionen. Vor einem Produktupgrade werden dessen eigener Start, Datenbankzugriff, Berechtigungen und Worker geprüft. Zentral relevante Änderungen benötigen gemeinsame Abnahmen mit betroffenen Produkten.

Core unterstützt die Vertragsversionen der aktuellen und der vorherigen SDK-Minor-Version. Ein Produkt außerhalb dieses Fensters aktualisiert sein SDK vor seiner nächsten Freigabe.

Ein Produkt verwendet Funktionen oder Daten eines anderen Produkts ausschließlich über einen im Manifest deklarierten Vertrag und die zentrale Austauschschicht von Core. Direkte Zugriffe auf Datenbank, Bucket oder Secrets eines anderen Produkts sind verboten. Daten eines Benutzers überschreiten eine Produktgrenze nur mit seiner ausdrücklichen, widerrufbaren Zustimmung. Das anbietende Produkt prüft vor seiner Freigabe die Verträge seiner deklarierten Verbraucher.

Migrationen zunächst additiv ausrollen, Daten nachziehen und Verbraucher umstellen. Alte Strukturen erst nach der Übergangsphase entfernen. Alte und neue Worker müssen gespeicherte Jobs während des Rollouts verarbeiten können. Destruktive Änderungen benötigen eine eigene Freigabe und einen geprüften Wiederherstellungsweg.

Produktfreigaben benötigen entsprechend ihrem Vertrag insbesondere Prüfungen für Anmeldung, Mandantentrennung, Zahlung beziehungsweise Kontingente, Storage, Worker-Wiederholungen, frische und bestehende Datenbanken, Export, Löschung und Restore. Nicht ausgeführte oder synthetische Providerprüfungen werden ausdrücklich benannt und gelten nicht als reale Betriebsabnahme.

## Offene Arbeit erhalten

Offene Branches und Worktrees sind zulässiger Arbeitsbestand. Der Workspace-Report unterscheidet Arbeitsdateien, unveröffentlichte Commits und bereits übernommene Änderungen.

Vor dem Entfernen eines Branches oder Worktrees müssen Dateien gesichert und die relevanten Commits dauerhaft referenziert oder nachweislich übernommen sein. Nach einem Squash-Merge reicht die Git-Abstammung für diesen Nachweis nicht aus. Es gibt keine pauschale Löschung nach Branchname oder Alter.

Git-Bundles sichern referenzierte Commits, aber keine offenen Dateien. Nicht committete und unversionierte Dateien benötigen eine zusätzliche Sicherung. Ignorierte Daten, Zugangsdaten und lokale Datenbanken werden über ihre eigenen geschützten Sicherungsverfahren erhalten.

Zusätzliche Worktrees liegen im Verzeichnis `.worktrees` des Repositories oder in einem anderen dauerhaften Verzeichnis. `/tmp` und `/private/tmp` sind dafür nicht zulässig, weil das Betriebssystem sie bereinigt. Commits eines Arbeitsbranches werden spätestens am Ende des Arbeitstags gepusht.

## Einrichtung und Kontrolle

In einem einzelnen Checkout aktiviert `python3 .github/workflow_guard.py install` die lokalen Branch-Guards und erhält die bisher konfigurierten Hookprüfungen. Der Installer ist wiederholbar. Im Workspace installiert `make hooks` die Guards für alle Repositories. Bestehende Branches, Arbeitsdateien und zusätzliche Worktrees werden dabei nicht verändert.

`python3 .github/workflow_guard.py check` prüft die zentrale Regelkopie. Der CI-Job `Source policy` führt diese Prüfung im Pull Request nach `main` aus. Die projektspezifischen Pflichtprüfungen laufen zusätzlich.

Änderungen an dieser Regel erfolgen zentral im Workspace. Anschließend `make policy-sync`, `make policy-check` und `make test` ausführen und die Änderungen in den betroffenen Repositories jeweils reviewen und übernehmen. Das Synchronisieren veröffentlicht keinen Code und verändert keine GitHub-Einstellungen.
