---
name: motion-fabrik
description: Richtet alles ein, um mit Claude Code (oder Codex) Motion-Graphics-Videos per Code zu bauen, und hilft danach, einen guten Video-Prompt zu schreiben. Fragt, ob HyperFrames, Remotion, Tesseract oder nichts installiert werden soll, verbindet auf Wunsch Higgsfield für Bilder, Videos, Stimmen und Musik und führt dann durch ein kurzes Interview (Länge, Format, Ziel, Branding, Referenz, Erfolgskriterium). Nutze diesen Skill, sobald jemand „Motion Fabrik“ sagt, den Link zu diesem Repo schickt, mit Claude Videos, Erklärvideos, Werbespots, Shorts oder Motion Graphics machen will oder HyperFrames, Remotion, Tesseract oder Higgsfield einrichten möchte. Also use it in English when someone wants to set up AI video creation with code.
license: MIT
---

# Motion Fabrik

Dieser Skill bringt jemanden in drei Teilen vom leeren Rechner zum ersten Video:

1. **Einrichten:** Voraussetzungen prüfen, Video-Framework wählen, Higgsfield verbinden
2. **Prompt bauen:** kurzes Interview, daraus ein Prompt, der das Ziel beschreibt
3. **Loslegen:** Prompt abnicken lassen, Video bauen, Tipps fürs Nachbessern

Sprich in der Sprache der Person. Die Texte hier sind deutsch, das ist keine
Vorgabe. Die meisten Nutzer kommen aus einem deutschen YouTube-Video und sind
keine Entwickler: Erkläre Fachbegriffe in einem Halbsatz, frag immer nur das
Nötige und installiere nie etwas, ohne vorher zu fragen.

## Fragen stellen

In Claude Code gibt es ein Auswahl-Werkzeug für Fragen (AskUserQuestion): Nutze
es, mit der Empfehlung als erste Option und „(Empfohlen)“ im Namen. Gibt es so
ein Werkzeug nicht (z. B. in Codex), stelle die Frage als nummerierte Liste und
warte auf die Antwort. Nie mehrere Entscheidungen in einen Satz packen.

## Gespeicherte Einstellungen

Prüfe zuerst, ob `~/.motion-fabrik.json` existiert. Wenn ja, ist die Einrichtung
schon erledigt: Zeig in einer Zeile, was drinsteht (Framework, Higgsfield ja/nein,
Stimme), frag, ob das noch stimmt, und spring zu Teil 2. Wenn nein, beginne mit
Teil 1. Die Datei sieht so aus:

```json
{
  "framework": "hyperframes",
  "higgsfield": "cli",
  "voice": "",
  "language": "de",
  "setup_done": "2026-11-02"
}
```

`framework`: `hyperframes` | `remotion` | `tesseract` | `none`.
`higgsfield`: `cli` | `mcp` | `no`.

## Teil 1: Einrichten

Ablauf, Befehle und Sonderfälle stehen in [references/setup.md](references/setup.md).
Kurzfassung:

1. **Voraussetzungen prüfen** und als kleine Tabelle zeigen (da / fehlt / wofür).
2. **Framework fragen:** HyperFrames (Empfohlen), Remotion, Tesseract oder nichts.
   Dazu je ein Satz, was es ist. Erwähne, dass Claude Motion in der Claude-App
   gar nichts installieren muss, aber nur auf Team- und Enterprise-Plänen läuft.
3. **Higgsfield fragen:** Bilder, Videoclips, Stimmen, Musik und Soundeffekte
   generieren? (Empfohlen: Ja.) Bei Ja fragen, ob schon ein Konto da ist. Nur wenn
   nicht, den Affiliate-Link zeigen, mit Kennzeichnung (genauer Text in setup.md).
4. **Einstellungen speichern** in `~/.motion-fabrik.json`.
5. **Neustart-Hinweis:** Neu installierte Skills und Plugins sieht der Agent erst
   in einer neuen Sitzung. Wenn etwas installiert wurde: kurz zusammenfassen und
   sagen „Starte eine neue Sitzung und schreib dort ‚Motion Fabrik‘, dann geht es
   mit dem Prompt weiter.“ Wenn nichts installiert wurde, direkt mit Teil 2 weiter.

Was fehlschlägt, klar benennen und den Befehl zum Nachholen nennen. Eine halb
eingerichtete Umgebung, die als fertig gemeldet wird, kostet später mehr Zeit.

## Teil 2: Prompt bauen

Fragen, Reihenfolge, Beispiele und die Prompt-Vorlage stehen in
[references/prompt-interview.md](references/prompt-interview.md). Gefragt wird:

- **Worum geht es?** Thema, Produkt, Link oder Text. Bei einem fertigen Video, das
  umgeschnitten werden soll (z. B. Longform → Short): der Pfad zur Datei.
- **Ziel und Zielgruppe:** erklären, verkaufen, Social Media, Schulung …
- **Länge**
- **Seitenverhältnis:** 16:9, 9:16, 1:1 oder 4:5
- **Farben, Muster, Branding:** Logo, Brand Guide, eine Webseite als Vorbild, oder freie Hand
- **Referenz:** ein Video oder Bild, das schon gefällt
- **Ton:** Sprecherstimme (Sprache), Musik, Soundeffekte
- **Wann ist es gut?** Ein Kriterium, ab dem das Ziel erreicht ist

Daraus wird ein Prompt, der Ziel, Rahmen, Geschmack und Erfolgskriterium nennt,
aber keine Arbeitsschritte vorschreibt. Neuere Modelle liefern bessere Videos,
wenn sie das Ziel kennen, als wenn man ihnen jeden Schritt diktiert.

## Teil 3: Loslegen

1. Prompt zeigen und als `prompt.md` in einen neuen Projektordner speichern
   (Name aus dem Thema, z. B. `video-gps-erklaert/`).
2. Fragen: „Soll ich so loslegen?“ Änderungen einarbeiten, bis die Person Ja sagt.
3. Bevor etwas Geld kostet (Higgsfield-Credits): zeigen, was generiert wird und
   was es ungefähr kostet (`higgsfield generate cost …`), und auf ein Ja warten.
4. Dann den Prompt ausführen, als wäre er gerade vom Nutzer gekommen, mit dem
   gewählten Framework. Zwischenstände selbst prüfen (Einzelbilder rendern und
   ansehen), bevor das fertige Video gemeldet wird.
5. Am Ende kurz die Tipps aus prompt-interview.md nennen (Aufwand, neuer Chat,
   Feedback geben).

Klemmt etwas: [references/troubleshooting.md](references/troubleshooting.md).
