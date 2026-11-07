---
name: menschlich
description: IMMER anwenden, bevor ein deutscher Artikel, Blogpost oder längerer Fließtext geschrieben, finalisiert oder veröffentlicht wird, der nach einem Menschen klingen soll. Entfernt AI-Slop-Marker (Em-Dashes, „nicht X, sondern Y", Dreier-Listen, hohle Überschriften, Floskeln, Füllwörter, erfundene Zahlen). Trigger sind „Artikel schreiben/publishen", „klingt nach KI/Slop", „menschlich machen", „entschlacken", „humanizer drüber".
---

# menschlich — AI-Slop aus deutschen Texten rausnehmen

> **Zweck:** Kein Text geht raus, der nach KI klingt. Diese SKILL.md ist der Schnell-Check; die deutsche Muster-Referenz liegt in [references/banned-list.md](references/banned-list.md), das Prüfskript in [scripts/slop_check.py](scripts/slop_check.py).
>
> **Wann laufen:** VOR dem Veröffentlichen jedes Artikels. Auch bei Newsletter, langen Mails, allem was nach einem Menschen klingen soll. NICHT nötig bei gesprochenem Skript-Text oder internen Notizen.
>
> **Herkunft:** Die deutsche Variante der Idee aus [realrossmanngroup/no_ai_slop_writing_rules](https://github.com/realrossmanngroup/no_ai_slop_writing_rules) (englische Korpus-Analyse, >500k Wörter). Dieser Skill ist eigenständig auf Deutsch geschrieben, inspiriert von deren Ansatz.

---

## Die 3 Marker, die am häufigsten verraten (zuerst prüfen)

1. **Em-Dash / Gedankenstrich-Drama.** Das Zeichen „—" ist verboten. Auch „–" nicht für dramatische Pausen. Ersetze durch Punkt, Komma, Doppelpunkt (sparsam) oder Klammer. Mehr als ein Dash pro Absatz = Slop.
2. **Kontrast-Parallelismus.** „Es ist nicht X, es ist Y." / „nicht nur X, sondern auch Y." / „Das ist nicht Z, das ist Q." Killen. Sag direkt, was Sache ist.
3. **Die Dreier-Liste als Reflex.** Drei parallele Glieder („filtern, testen, zeigen"). Ab und zu ok, aber wenn JEDER Absatz in Dreiern denkt, brich es auf: mal zwei, mal vier, mal ein ganzer Satz.

---

## Weitere verbotene Muster

- **Hohle/teasernde Überschriften.** „Die verborgenen Kosten der Bequemlichkeit" → „Abos summieren sich". Überschrift benennt den Inhalt, sie kündigt ihn nicht spannend an.
- **Floskel-Opener.** „In der heutigen schnelllebigen Welt", „Es ist wichtig zu beachten", „Wenn es um X geht". Direkt mit dem Fakt starten.
- **Füllwörter & Intensivierer.** „eigentlich", „im Grunde", „letztlich", „absolut", „unglaublich", „deutlich", „massiv" ohne Zahl. Intensivierer sind Platzhalter für fehlende Belege → durch konkrete Zahl ersetzen oder streichen.
- **Weichmacher/Weasel.** „könnte womöglich", „kann helfen zu", „ist vielleicht in der Lage". Klare Aussage machen oder weglassen.
- **Erfundene Zahlen.** Keine Zahl dazuerfinden, die nicht in der Quelle steht. Fehlt eine Zahl, bleibt sie weg.
- **Colon-Setup als Erzähltrick.** „Du kennst den Typ: …", „Das Beispiel, das alles zeigt: …". Einmal ok, als Muster (jeder Abschnitt so) raus.
- **Rhetorische KI-Fragenpaare.** „Braucht das überhaupt zu existieren? Und wenn ja, …?" klingt nach Modell. In Aussage umbauen.
- **Struktur-Slop.** Gleich lange Absätze, gleich lange Sätze, jeder Absatz beginnt gleich. Rhythmus brechen: kurze Sätze neben lange, mal ein Ein-Wort-Satz.
- **Ein-Zeilen-Drama-Absätze.** Ein einzelner kurzer Satz als eigener Absatz („Genau darum geht es.") wirkt 1x pro Text. Als Muster (3+) ist es der KI-Drama-Trick.
- **Kicker-Opener.** „Aber jetzt kommt der Clou", „Und genau hier wird es spannend", „Aber hier ist der Haken", „Und das Beste daran". Direkt sagen, was Sache ist.
- **Fabrizierte Zitate/Haltungen.** Niemandem Aussagen in den Mund legen. Nur belegte Aussagen mit Quelle.

Vollständige deutsche Muster-Referenz: [references/banned-list.md](references/banned-list.md).

---

## Deutsch-Spezifika (Pflicht)

- **Echte Umlaute** ä ö ü ß, nie ae/oe/ue/ss.
- Kein Em-Dash „—". Der Halbgeviertstrich „–" ist im Deutschen als Einschub erlaubt, aber sparsam und NIE als KI-Drama-Pause. Im Zweifel Komma/Punkt.
- Der Ton des Autors bleibt. Der Skill nimmt die KI-Stimme raus, nicht die eigene Stimme. Nach dem Entschlacken bleibt neutral-menschlicher Text; wo es persönlich klingen soll, ruhig einen eigenen, unperfekten Satz stehen lassen.

---

## Vorher / Nachher (Beispiele)

- ❌ „Du kennst den Typ: länger in der Firma als die Versionsverwaltung, langer Zopf, ovale Brille. Du zeigst ihm fünfzig Zeilen Code — er sagt nichts und ersetzt sie durch eine."
  ✅ „Kennst du diesen einen alten Entwickler in der Firma? Du zeigst ihm 50 Zeilen Code, er guckt kurz und macht eine Zeile draus."
- ❌ „Es gibt deinem Agenten eine einzige Denkregel: Braucht das überhaupt zu existieren? Und wenn ja — was ist der kürzeste Weg, der funktioniert?"
  ✅ „Der Skill bringt der KI eine simple Frage bei, bevor sie loslegt: Geht das auch kürzer? Meistens ja."
- ❌ „Der gemeinsame Nenner ist immer derselbe: Dein bestes Modell soll denken, nicht schuften."
  ✅ „Am Ende geht es um dasselbe. Dein bestes Modell soll denken, nicht Fließbandarbeit machen."

---

## Prozess (so anwenden)

0. **Slop-Check-Skript zuerst (Pflicht):**
   ```bash
   python3 scripts/slop_check.py <datei.md>
   # ganzer Ordner: python3 scripts/slop_check.py --dir <ordner>
   ```
   (Das Skript liegt neben dieser SKILL.md unter `scripts/slop_check.py`.) Findet die mechanisch prüfbaren Verstöße: Em-Dashes (auch im Frontmatter!), verbotene Phrasen, Kontrast-Parallelismus, halluzinierte Markup-Reste, Füllwort-Häufung, Ein-Zeilen-Drama, monotone Absätze. Exit 1 = ERROR = nicht veröffentlichen. **Ausnahme:** Treffer, die als Zitat/Negativ-Beispiel im Text stehen (etwa ein Artikel ÜBER AI-Slop zitiert die Floskeln), kurz verifizieren und stehen lassen. Das Skript ersetzt das Lesen nicht: Ton, Colon-Setups, hohle Überschriften und fabrizierte Zitate bleiben Handarbeit.
1. **Draft lesen.** Den kompletten Text durchgehen.
2. **Marker markieren.** Erst die 3 Top-Marker (Em-Dash, Kontrast-Parallelismus, Dreier), dann die weiteren + Referenzliste.
3. **Umschreiben, nicht nur löschen.** Jeden Marker durch eine natürliche, konkrete Formulierung ersetzen. Rhythmus bewusst brechen.
4. **Zahlen prüfen.** Jede Zahl muss aus der Quelle stammen. Keine dazuerfinden.
5. **Report.** Am Ende 3-5 Stichpunkte: welche Slop-Muster gefunden + gefixt wurden (Transparenz).
6. **Gegencheck:** Nochmal lesen. Würde ein Mensch das so schreiben? Ist die eigene Stimme noch da?

---

## Danach

Dein Text ist entschlackt. Der Feinschliff (Ton, eigene Stimme, ob es sich richtig anfühlt) bleibt deine Entscheidung. Der Skill hebt das Niveau, den letzten Blick hast du.
