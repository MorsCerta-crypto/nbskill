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
3. Nach Review und erfolgreichen Pflichtprüfungen mergen. GitHub Auto-Merge kann den Merge übernehmen, sobald die Regeln des Repositories erfüllt sind. Der Prüfnachweis nennt den geprüften Commit, das Testprofil und ausgelassene Prüfungen.
4. Aus einem geprüften Commit in `main` veröffentlichen. Verbraucher übernehmen neue Libraryversionen über einen eigenen Pull Request mit aktualisiertem Lockfile. Veröffentlichte Tags und Releases bleiben unveränderlich.

Die lokalen Guards schützen `main`, veröffentlichte Tags und die rsc-Deploymentreferenzen. Auf GitHub erzwingen die Regeln für `main` Pull Requests, Pflichtprüfungen und den Schutz vor Löschung und Force-Push. Der rsc-Deployer schreibt ausschließlich seine Deploymentreferenzen.

Pflichtprüfungen umfassen die Installation aus dem Lockfile, die Projekttests und bei nbdev-Projekten den abweichungsfreien Notebook-Export. Solange das Repository in GitHub Actions nur Syntax prüft, gehört der lokale Prüfnachweis in den Pull Request. Tests erhalten standardmäßig `contents: read`. Private Abhängigkeiten verwenden bei Bedarf ein kurzlebiges GitHub-App-Token mit Leserechten für die konkreten Paket-Repositories. CI bricht veraltete Pull-Request-Läufe ab und verwendet den Download-Cache des Paketmanagers. Die Pflichtprüfungen müssen auch für Dokumentationsänderungen ein Ergebnis liefern.

Eine Änderung über mehrere Repositories verwendet in allen denselben Branchnamen. Jeder Pull Request nennt die zugehörigen Pull Requests. Die gemeinsame Prüfung verwendet genau diese Stände. Libraries werden zuerst integriert und veröffentlicht. Der Pull Request eines Verbrauchers bleibt Entwurf, bis er den veröffentlichten Tag pinnt.

## Dev- und Produktionsdeployment

Bei einem Produkt mit eingerichtetem Deployment startet ein erfolgreicher Lauf für `main` den Rollout nach `development-deployment`. Ein ausdrücklich gesetzter Release-Tag auf einem geprüften Commit in `main` startet die Produktionsfreigabe für den bereits in Dev geprüften Kandidaten. rsc führt den Produktionsrollout nach der Freigabe aus. In `DEV.md` stehen das zulässige Tagformat, die Startbedingung und der Einrichtungsstand des Projekts.

Ein Produktrelease bindet Produktcommit, SDK- und Vertragsversion, Lockfiles, Manifest, Migrationsprüfsummen und Image-Digests. Aus dem freigegebenen Quellstand wird genau ein Kandidat gebaut. Dev und Prod verwenden denselben Kandidaten und dieselben Image-Digests, aber getrennte Konfigurationen und Infrastrukturpläne.

Den Kandidaten für die gemeinsamen Umgebungen Dev und Prod baut CI aus einem sauberen Checkout des Kandidatencommits. Ein auf einem Entwicklungsrechner gebautes Image ist dort kein Kandidat. Lokale Compose-Umgebungen sind davon nicht betroffen.

Dev verwendet synthetische Daten, eigene Datenbanken, Buckets, Worker-Queues, Dienstidentitäten, Secret-Versionen und Test-Mailziele. Die zentralen Core-, Identitäts- und Zahlungsdienste benötigen ebenfalls getrennte Testkonfigurationen. Entwicklungsprozesse erhalten keine Produktionszugänge.

rsc prüft den Kandidaten in Dev. Erst vollständige, dem Kandidaten zugeordnete Abnahmen und eine erneute persönliche MFA-Freigabe erlauben Produktion. Ein Merge nach `main` ersetzt diese Freigabe nicht. Beim Betrieb mehrerer verantwortlicher Personen muss eine andere Person die Produktion freigeben.

Der rsc-Releasestatus ist der maßgebliche Betriebsnachweis. Er hält Kandidat, Umgebung, Plan, Freigabe, Prüfnachweise und Ergebnis fest. Die zusätzlichen Referenzen `deployed/dev` und `deployed/prod` erleichtern die Git-Navigation. Fehlgeschlagene Git-Veröffentlichungen werden ohne erneutes Deployment wiederholt. Bereits gespeicherte Veröffentlichungen auf die alten Quellbranch-Ziele werden unter der Deploymentsperre auf die neuen Referenzen umgestellt und als eigenes Ereignis protokolliert. Historische veröffentlichte Ereignisse bleiben unverändert.

Nach dem Rollout müssen Readiness, fachliche Probe und Workerzustand zum konkreten Kandidaten passen. Ein Anwendungsrollback ist nur mit kompatiblem Schema zulässig. Ein Backup-Restore ist ein gesonderter, geprüfter Betriebsablauf.

## Library-Releases

DocAI und ease-ui veröffentlichen ihre freigegebenen Pakete öffentlich. Interne Libraries veröffentlichen die für Verbraucher vorgesehenen Git-Tags und Artefakte mit den Zugriffsrechten des jeweiligen Repositories. Der Tag muss auf einen geprüften Commit in `main` zeigen und zur Paketversion passen.

Fastship übernimmt die Paket- und GitHub-Releases, soweit das Projekt seinen Build damit abbildet. Der Workspace stellt dafür `scripts/library_publish.py` für bereits gebaute Artefakte bereit. Im jeweiligen `DEV.md` stehen das Buildkommando, die Version von Fastship und der tatsächlich eingerichtete Veröffentlichungsweg. Veröffentlichungsschritte laufen mit separaten Schreibrechten. Paket- und Produktionsfreigaben erfolgen über den jeweiligen Releaseweg.

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
