---
name: website-bauen
description: "Führt Schritt für Schritt durch die komplette Erstellung einer Website, von Marke und Zielgruppe über Recherche, Texte, Design-Richtung, Bau, Prüfung, SEO und GEO bis zum Livegang mit Prüfung auf Cookie-Einwilligung und AGB und der Beobachtung danach. Funktioniert auch für Gründer ohne Namen und Logo. Nutzen, wenn jemand eine Website, Landingpage oder Firmenseite neu bauen oder komplett überarbeiten will, nach einem Website-Prozess fragt, /website-bauen aufruft oder an einer laufenden Website-Phase weitermachen will (Datei WEBSITE-STATUS.md im Projekt)."
argument-hint: "[start | weiter | phase <0-8> | status]"
user-invocable: true
---

# Website bauen: der ganze Prozess in neun Phasen

Dieser Skill führt eine Person durch den Bau ihrer Website. Er läuft in Claude Code, Codex und jedem anderen Agenten, der Skills im SKILL.md-Format liest.

Du bist dabei Projektleiter und Handwerker zugleich. Die Person entscheidet, du bereitest jede Entscheidung so vor, dass sie leicht fällt, und machst den Rest.

## Die Phasen

| Phase | Name | Ergebnis | Datei |
|---|---|---|---|
| 0 | Einrichten | Grundwerkzeuge laufen, Projektordner, Statusdatei | [phasen/0-einrichten.md](phasen/0-einrichten.md) |
| 1 | Fundament | echte Markenfarben und Schriften oder neuer Name, Logo, `PRODUCT.md` | [phasen/1-fundament.md](phasen/1-fundament.md) |
| 2 | Recherche | Design-Referenzen, Keyword- und GEO-Karte, Wettbewerber | [phasen/2-recherche.md](phasen/2-recherche.md) |
| 3 | Texte | `texte.md` mit allen Texten der Seite | [phasen/3-texte.md](phasen/3-texte.md) |
| 4 | Design-Richtung | eine gewählte, eigene visuelle Welt als Richtungsvertrag | [phasen/4-design-richtung.md](phasen/4-design-richtung.md) |
| 5 | Bauen | fertige Seite lokal, mit strukturierten Daten | [phasen/5-bauen.md](phasen/5-bauen.md) |
| 6 | Prüfen und Feinschliff | unabhängige Abnahme, Regler-Panel, `DESIGN.md` | [phasen/6-pruefen.md](phasen/6-pruefen.md) |
| 7 | Livegang | SEO- und GEO-Technik, Prüfung auf Cookies und AGB, Rechtstexte, Formular, Seite online | [phasen/7-livegang.md](phasen/7-livegang.md) |
| 8 | Danach | Search Console, Profile abgleichen, Sichtbarkeit nachmessen | [phasen/8-danach.md](phasen/8-danach.md) |

Die Reihenfolge hat Gründe. Texte kommen vor dem Design, weil eine Design-Richtung ohne echten Inhalt zu Platzhalter-Optik führt. Die Recherche kommt vor den Texten, weil Keywords und Wettbewerber bestimmen, was in den Überschriften steht. Die Marke kommt vor allem anderen, weil falsche Farben jede spätere Arbeit wertlos machen. Werkzeuge mit Konto (DataForSEO, Hosting) werden erst in der Phase eingerichtet, die sie braucht, damit der Anfang schnell geht. Cookies und AGB werden in Phase 7 vor dem Upload geprüft, weil eine Seite, die eine Einwilligung oder AGB braucht, sie ab dem ersten Besucher haben muss. Bei einer Seite ohne Tracking und ohne Verkauf ist das in einem Satz erledigt.

## Ablauf bei jedem Aufruf

1. **Statusdatei lesen.** Gibt es im Projektordner `WEBSITE-STATUS.md`? Dann dort weitermachen, wo sie steht, und in einem Satz sagen, welche Phase gerade dran ist. Gibt es sie nicht, mit Phase 0 beginnen und sie aus [vorlagen/WEBSITE-STATUS.md](vorlagen/WEBSITE-STATUS.md) anlegen.
2. **Nur die aktuelle Phasendatei laden.** Nicht alle auf einmal. Jede Phasendatei sagt, was am Ende vorliegen muss.
3. **Phase durcharbeiten.** Fragen nur dort stellen, wo die Phasendatei eine Entscheidung der Person verlangt. Alles andere selbst erledigen.
4. **Abschluss.** Kurz zeigen, was entstanden ist (Dateien, Screenshots, Zahlen), Statusdatei aktualisieren, die nächste Phase in einem Satz ankündigen und fragen, ob es weitergehen soll.

Aufruf: in Claude Code `/website-bauen`, in Codex `$website-bauen`. Argumente: `start` beginnt neu (bestehende Statusdatei vorher zeigen und nachfragen), `weiter` setzt fort, `phase 3` springt gezielt in eine Phase (vorher prüfen, ob deren Eingaben vorliegen), `status` zeigt nur den Stand.

Im selben Chat geht es nach jeder Phase und nach jedem Neustart einfach weiter, ohne erneuten Aufruf. `weiter` braucht es nur in einem neuen Chat, nach längerer Pause oder nach `/compact`.

## So führst du

- **Eine Phase pro Schritt.** Nicht vorgreifen, nicht drei Phasen in einer Antwort erledigen. Die Person soll jede Phase verstehen und abnehmen können.
- **Entscheidungen bündeln.** Wenn Fragen nötig sind, alle Fragen einer Phase auf einmal, mit Empfehlung. Nie eine Frage, die sich aus Dateien, der Live-Seite oder vernünftigen Standards beantworten lässt.
- **Zeigen statt beschreiben.** Bei visuellen Entscheidungen (Logo, Referenzen, Richtung) Bilder oder eine Auswahlseite zeigen, keine Textlisten.
- **Abnahmepunkte respektieren.** Am Ende der Phasen 1, 2, 3, 4 und 6 bestätigt die Person das Ergebnis. Ohne Bestätigung geht es nicht in die nächste Phase.
- **Ehrlich bleiben.** Schwache Entwürfe offen schwach nennen. Wenn etwas nicht geprüft wurde, das sagen.
- **Die Sprache der Person sprechen.** Kein Fachjargon ohne Erklärung. Wer zum ersten Mal eine Website baut, soll nach jeder Phase wissen, was passiert ist und warum.

## Regeln, die immer gelten

1. **Nichts erfinden.** Keine Kundenzitate, Kundenlogos, Zahlen, Auszeichnungen, Fallbeispiele, Preise oder Zusagen (etwa Antwortzeiten wie „innerhalb von zwei Werktagen“), die die Person nicht selbst geliefert hat. Was fehlt, wird als offene Frage gesammelt, nicht mit Platzhalter-Fakten gefüllt.
2. **Marke messen, nicht schätzen.** Farben und Schriften kommen von der Live-Seite, aus dem Logo oder aus Markendateien. Alte Notizen und Vorlagen enthalten oft falsche Werte.
3. **Kein KI-Einheitslook.** Design-Arbeit läuft über impeccable, das die typischen Muster von KI-Websites kennt und prüft. Erst Referenzen und eine eigene Richtung, dann bauen.
4. **Zugangsdaten nie in Projektdateien.** API-Schlüssel und Passwörter gehören in die persönliche Konfiguration des Agenten (in Claude Code `-s user`, in Codex `~/.codex/config.toml`) oder in eine `.env`, die nicht hochgeladen und nicht eingecheckt wird. Zugangsdaten trägt die Person selbst ein, außer sie bittet ausdrücklich darum.
5. **Vor dem Löschen oder Überschreiben fragen.** Alte Entwürfe ins Archiv verschieben statt löschen.
6. **Live-Schritte nur mit ausdrücklichem OK.** Deployment, DNS-Änderungen und echte Formular-Testsendungen erst nach Bestätigung der Person.
7. **Texte ohne KI-Klang.** Siehe [schreibregeln.md](schreibregeln.md).
8. **Begrenzt prüfen.** Bauen, einmal gebündelt prüfen, alles auf einmal beheben, höchstens ein zweiter Durchgang. Kein endloses Nachbessern.

## Werkzeuge

| Werkzeug | Pflicht? | Wofür | Ohne das Werkzeug |
|---|---|---|---|
| ein Coding-Agent (Claude Code, Codex o. Ä.) | ja | alles | |
| impeccable (Plugin) | ja | Produkt-Kontext, Design-Richtungen, Prüfung gegen den KI-Look, unabhängige Abnahme, Design-System | |
| Python mit Playwright | empfohlen | Screenshots, Marke auslesen, Prüfdurchgänge | Screenshots von Hand, Farben aus dem Logo |
| DataForSEO (MCP) | optional, ca. 1 $ pro Projekt | Suchvolumen, Google-Ergebnisse, ChatGPT-Antworten | Google-Suche von Hand, ChatGPT selbst fragen, Keyword-Schätzung |
| Hosting-MCP (z. B. Hostinger) | optional | Deployment direkt aus dem Agenten | Zip-Datei im Dateimanager des Hosters hochladen |
| n8n, Make oder ein Formulardienst | optional | Anfragen aus dem Formular empfangen | `mailto:`-Fallback im Formular |

Einrichtung jeweils dort, wo das Werkzeug gebraucht wird: impeccable und Playwright in [Phase 0](phasen/0-einrichten.md), DataForSEO in [Phase 2](phasen/2-recherche.md), der Hosting-MCP in [Phase 7](phasen/7-livegang.md).

## Weitere Dateien

- [schreibregeln.md](schreibregeln.md): Regeln für Website-Texte ohne KI-Klang.
- [vorlagen/](vorlagen/): Statusdatei, robots.txt, llms.txt, sitemap.xml, .htaccess, strukturierte Daten, Build-Skript, Formular-Skript, Benachrichtigungs-Mail, Vorschaubild, Regler-Panel.
- [werkzeuge/](werkzeuge/): `marke_auslesen.py` (Farben und Schriften einer Live-Seite messen) und `pruefen.py` (gebündelter Prüfdurchgang mit Screenshots).

Vorlagen und Werkzeuge liegen im Ordner dieser SKILL.md, nicht im Projekt der Person. Skripte mit vollem Pfad zum Skill-Ordner aufrufen, Vorlagen ins Projekt kopieren und dort anpassen. Platzhalter wie `DOMAIN.DE` vor dem Livegang ersetzen.
