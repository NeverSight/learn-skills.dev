---
name: repo-doku
description: "Erstellt oder aktualisiert die Dokumentation (in der Regel README.md, bei größeren Projekten zusätzlich DEVELOPMENT.md) direkt im Quell-Repo — als Source of Truth. Quellen sind die vorhandene Doku, Changelog-Dateien, Git-Commits seit dem letzten Doku-Stand und der Quellcode. Nutze diesen Skill, wenn der Benutzer in einem Repo die Doku schreiben, das README aktualisieren, neue Features/Änderungen dokumentieren oder die Doku auf Stand bringen möchte. Trigger-Begriffe: Doku erstellen, README aktualisieren, dokumentieren, Doku auf Stand bringen, Changelog dokumentieren."
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Repo-Doku: Dokumentation im Quell-Repo erstellen

## Zweck

Dieser Skill erzeugt oder aktualisiert die Dokumentation **direkt im Quell-Repo** — als
**Source of Truth**, aus der nachgelagerte Doku-Systeme (Doku-Portal, Website) sie übernehmen können.
Geschrieben wird in die `README.md`, bei größeren Projekten zusätzlich in eine `DEVELOPMENT.md`.

- **Output bleibt im Repo**: `README.md` immer; `DEVELOPMENT.md` nur bei größeren Projekten.
- **Kein Auto-Commit**: Niemals selbstständig committen oder pushen — nur einen Conventional-Commit
  vorschlagen.

## Workflow

### 1. Doku-Ziel bestimmen
- Projekt-Typ und Umfang einschätzen (Bibliothek/Client, größere Anwendung, CLI, …).
- Doku-Ziel festlegen: nur `README.md` oder `README.md` + `DEVELOPMENT.md`.
- → Details in [references/doku-ziel.md](references/doku-ziel.md).

### 2. Letzten Doku-Stand finden (Git)
Den Punkt finden, bis zu dem zuletzt dokumentiert wurde, um nur die Lücke zu schließen:
```bash
git log -1 --format='%H %ci' -- README.md   # letzte Änderung am README
git log --oneline <letzter-stand>..HEAD      # Commits seitdem
```
- Conventional Commits nach Typ gruppieren (`feat`, `fix`, `BREAKING CHANGE` …).
- `feat`/`BREAKING CHANGE` sind dokumentationsrelevant, reine `chore`/`ci`/`test` meist nicht.

### 3. Quellen sammeln (in dieser Reihenfolge)
1. **Vorhandene Doku** (`README.md`, ggf. `DEVELOPMENT.md`) als Ausgangsbasis — fortschreiben,
   nicht von Null neu schreiben.
2. **Changelog-Dateien** als strukturierte Quelle für Neuerungen (auf die exakte Schreibweise im
   Repo achten, z.B. `Changelog.md` vs. `CHANGELOG.md`).
3. **Git-Commits** seit letztem Stand (Schritt 2) für Änderungen ohne Changelog-Eintrag.
4. **Quellcode** für die Details: öffentliche API, Optionen, Signaturen, realistische Beispiele.

### 4. Doku schreiben/aktualisieren
- Konventionen einhalten → [references/konventionen.md](references/konventionen.md)
  (Sprache, Code/Kommentar-Sprache, Changelog, Diagramme, projekt-spezifische Regeln).
- Minimal-invasiv: nur ergänzen/korrigieren, was die neuen Commits/Features betreffen.
- Beispiele aus echtem Code ableiten, **keine erfundenen APIs**.

### 5. Abschluss
Wenn Doku geändert wurde:
- Aufgaben in einer Aufgabenliste nachverfolgen (z.B. `todos/<thema>/todo.md`), falls im Projekt üblich.
- **Conventional-Commit vorschlagen** (z.B. `docs: README um Feature X ergänzen`),
  aber nicht selbst committen.
- Kurze Zusammenfassung der Änderungen geben.

**"Kein Gap" ist ein gültiges Endergebnis.** Wenn die Auswertung zeigt, dass die vorhandene Doku
bereits aktuell und vollständig ist (z.B. nur interne Bugfixes/Tests/Releases seit dem letzten
Stand), dann **keine Änderung erzwingen**: keine erfundenen Inhalte, keine Aufgabenliste, kein
Commit-Vorschlag. Stattdessen die ausgewerteten Quellen und den Befund kurz berichten — inklusive
ggf. einzelner Grenzfälle, deren Bewertung der Benutzer entscheidet.

## Referenzen
- [references/doku-ziel.md](references/doku-ziel.md) — Doku-Ziel wählen (README vs. README+DEVELOPMENT),
  Umfang und was rein- bzw. nicht reingehört.
- [references/konventionen.md](references/konventionen.md) — Schreib-, Changelog- und Diagramm-Regeln
  sowie projekt-spezifische Konventionen.
