---
name: changelog
description: Erstellt oder aktualisiert ein Changelog aus der Git-Historie, gruppiert nach Versionen und kategorisiert nach Feature-Typ. Nutze diesen Skill wenn der Benutzer ein Changelog erstellen, aktualisieren oder generieren möchte.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Skill: changelog

Erstellt oder aktualisiert ein Changelog aus der Git-Historie, gruppiert nach Versionen und kategorisiert nach Feature-Typ.

## Auslöser

- `/changelog` - Changelog erstellen oder aktualisieren
- "Erstelle ein Changelog", "Aktualisiere das Changelog", "Was hat sich geändert seit..."

## Parameter

Frage den Benutzer nach folgenden Informationen, falls nicht angegeben:

1. **Zielgruppe** (bestimmt auch die Standarddatei)
   - **Anwender** → `Changelog.md` (vereinfacht, Nutzen beschreiben)
   - **Entwickler** → `Changelog-Dev.md` (technisch, mit Commit-Details)

2. **Modus**
   - **Aktualisieren** (Standard): Nur neue Änderungen seit letztem Eintrag hinzufügen
   - **Neu erstellen**: Komplettes Changelog ab einem Zeitpunkt erstellen

3. **Zeitraum** (nur bei "Neu erstellen")
   - Beispiele: "seit März 2025", "seit v2.3.0"

## Workflow

### 1. Bestehenden Changelog prüfen

```bash
# Prüfen ob Changelog existiert
ls Changelog.md Changelog-Dev.md 2>/dev/null
```

Falls Changelog existiert:
- Letzten dokumentierten Stand ermitteln (Version oder Commit)
- Nach dem Marker `## 🔮 In Entwicklung` den letzten bekannten Commit suchen
- Oder die letzte dokumentierte Insiders/Stable-Version als Referenz nehmen

### 2. Git-Daten sammeln

```bash
# Tags mit Datum abrufen
git for-each-ref --sort=-creatordate --format='%(refname:short) %(creatordate:short)' refs/tags

# Letzten Tag ermitteln
git describe --tags --abbrev=0

# Commits seit letztem Tag (für "In Entwicklung")
git log $(git describe --tags --abbrev=0)..HEAD --pretty=format:"%h %ad %s" --date=short

# Commits seit bestimmter Version
git log v2.3.0..HEAD --pretty=format:"%h %ad %s" --date=short
```

### 3. Commits kategorisieren

Analysiere die Commit-Messages und ordne sie zu:

| Kategorie | Schlüsselwörter |
|-----------|-----------------|
| **Neue Funktionen** | Add, Feat, Feature, New, Implement |
| **Fehlerbehebungen** | Fix, Bugfix, Hotfix, Resolve |
| **Performance** | Performance, Optimize, Speed |
| **Technisch** | Bump, Update, Refactor, Chore, Deps |

**Ignorieren:**
- Merge-Commits ("Merge branch", "Merge pull request")
- Release-Commits ("Release v", "Bump version")
- WIP-Commits, Build-Fixes

### 4. Versionen zuordnen

**Wichtig:** Features durchlaufen die Phasen sequentiell:

```
🔮 In Entwicklung  →  🧪 Insiders  →  ✅ Stable
     (Ausblick)        (Early Adopter)    (Alle Nutzer)
```

- Ein Feature kann nur in **einer** Phase gelistet werden
- Wenn es in Stable ist, war es vorher in Insiders
- Wenn es in Insiders ist, war es vorher in Entwicklung
- Jeder Abschnitt zeigt nur **neue** Änderungen gegenüber der vorherigen Version

### 5. Changelog aktualisieren

**Bei Aktualisierung:**
1. Bestehende Datei lesen
2. Abschnitt "In Entwicklung" mit neuen Commits aktualisieren
3. Bei neuem Release: "In Entwicklung" → "Insiders" oder "Insiders" → "Stable" verschieben
4. Datei speichern

**Bei Neuerstellung:**
1. Komplettes Template mit allen Versionen erstellen

## Standard-Dateien

| Zielgruppe | Datei | Inhalt |
|------------|-------|--------|
| **Anwender** | `Changelog.md` | Nutzen beschreiben, keine technischen Details, keine Commit-Hashes |
| **Entwickler** | `Changelog-Dev.md` | Technische Details, Commit-Hashes, PR-Nummern, Breaking Changes |

## Ausgabe-Template (Anwender)

```markdown
# Changelog [Projektname]

---

## 🔮 In Entwicklung (Ausblick auf nächstes Release)

*Diese Features sind nach [LETZTER_TAG] hinzugekommen und werden im nächsten Release enthalten sein.*

### Neue Funktionen
- Feature-Beschreibung aus Anwendersicht

### Fehlerbehebungen
- Fix-Beschreibung aus Anwendersicht

---

## 🧪 Insiders vX.Y.Z-insiders.N (DD.MM.YYYY)

*Vorschau-Version mit neuen Features gegenüber Stable vX.Y.Z.*

### Neue Funktionen (gegenüber vX.Y.Z)
- Feature-Beschreibung

---

## ✅ Stable vX.Y.Z (DD.MM.YYYY)

*Stabile Version - enthält alle Features aus vX.Y.Z-insiders.1 bis vX.Y.Z-insiders.N.*

### Neue Funktionen (gegenüber vX.Y-1.Z)
- Feature-Beschreibung *(seit insiders.N)*

### Fehlerbehebungen (gegenüber vX.Y-1.Z)
- Fix-Beschreibung *(seit insiders.M)*

---

## Release-Prozess

Features durchlaufen drei Phasen, bevor sie alle Nutzer erreichen:

```
🔮 In Entwicklung  →  🧪 Insiders  →  ✅ Stable
     (Ausblick)        (Early Adopter)    (Alle Nutzer)
```

| Phase | Zielgruppe | Beschreibung |
|-------|------------|--------------|
| 🔮 **In Entwicklung** | Entwickler | Ausblick auf kommende Features. Noch in keinem Release enthalten. |
| 🧪 **Insiders** | Early Adopter | Vorschau-Versionen zum Testen neuer Features vor dem Stable-Release. |
| ✅ **Stable** | Alle Nutzer | Produktionsreife Version. Features sind vollständig getestet und freigegeben. |

**Hinweis:** Jeder Abschnitt listet nur die Änderungen, die **neu** in dieser Phase sind.
```

## Ausgabe-Template (Entwickler)

```markdown
# Changelog (Entwickler)

---

## 🔮 In Entwicklung

*Commits seit [LETZTER_TAG]*

### Neue Funktionen
- `abc1234` Feature X hinzugefügt (#123)

### Fehlerbehebungen
- `def5678` Bug Y behoben (#456)

### Technische Änderungen
- `ghi9012` Dependency Z aktualisiert

---

## 🧪 Insiders vX.Y.Z-insiders.N (DD.MM.YYYY)

### Breaking Changes
- Beschreibung der Breaking Changes

### Neue Funktionen
- `abc1234` Feature-Beschreibung (#123)

### Fehlerbehebungen
- `def5678` Fix-Beschreibung (#456)

---

## ✅ Stable vX.Y.Z (DD.MM.YYYY)

*Enthält Insiders .1 bis .N*

### Breaking Changes
- Beschreibung

### Commits
- Liste aller Commits seit letzter Stable
```

## Beispiele

### Beispiel 1: Changelog aktualisieren (Standard)

**Benutzer:** "Aktualisiere das Changelog"

**Vorgehen:**
1. Prüfen ob `Changelog.md` existiert
2. Letzten dokumentierten Stand ermitteln
3. `git log [LETZTER_STAND]..HEAD --pretty=format:"%h %ad %s" --date=short`
4. Neue Commits kategorisieren
5. Abschnitt "In Entwicklung" aktualisieren

### Beispiel 2: Changelog für Entwickler

**Benutzer:** "Erstelle ein Entwickler-Changelog"

**Vorgehen:**
1. Prüfen ob `Changelog-Dev.md` existiert
2. Git-Historie mit Commit-Hashes und PR-Nummern sammeln
3. Technische Details und Breaking Changes dokumentieren
4. In `Changelog-Dev.md` speichern

### Beispiel 3: Neues Release dokumentieren

**Benutzer:** "Wir haben v2.4.0-insiders.3 released"

**Vorgehen:**
1. Changelog.md lesen
2. Inhalte von "In Entwicklung" nach "Insiders v2.4.0-insiders.3" verschieben
3. Neuen leeren "In Entwicklung"-Abschnitt erstellen
4. Datum hinzufügen

## Tipps

- Bei langen Commit-Messages den ersten Satz verwenden
- PR-Nummern (#123) nur im Entwickler-Changelog behalten
- Zusammengehörige Commits gruppieren (z.B. mehrere Commits für ein Feature)
- Bei vielen Commits den `head`-Befehl verwenden, um die Ausgabe zu begrenzen
- Beim Aktualisieren immer den bestehenden Changelog als Basis verwenden
