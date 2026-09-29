---
name: creativity
description: >
  Use when the user wants to develop a creative work — a story, novel, course, lecture, article, or presentation — through open-ended exploratory ideation instead of jumping straight to a draft. Implements the Emergent Creativity Protocol (ECP): a multi-agent, artifact-based process that first expands a rich "meaning space" of interconnected ideas, then converges on a concrete text. Trigger on requests like "entwickle eine Geschichte", "brainstorme Charaktere/eine Welt für...", "hilf mir eine Geschichte zu entdecken statt zu planen", "ECP", "emergent creativity", or explicit invocation as /creativity. Do NOT trigger for ordinary coding tasks, direct-drafting requests ("just write me a story about X now"), or analytical/non-creative writing.
argument-hint: "[kreatives Vorhaben, z.B. 'eine Kurzgeschichte über eine Stadt, die das Vergessen lernt']"
license: CC0-1.0
---

# Emergent Creativity Protocol (ECP)

Du orchestrierst einen mehrstufigen, agentischen Kreativprozess. Kernprinzip: **Kreativität ist Emergenz, keine Optimierung.** Ideen werden nicht direkt zum fertigen Text verengt (`Plan → Ausführen → Prüfen → Fertig`), sondern zunächst in einem geteilten Bedeutungsraum ("Cognitive Field") vervielfacht und vernetzt. Erst danach entsteht daraus, über einen "Narrative Compiler", eine konkrete Form.

Lies vor dem ersten Lauf **[references/philosophy.md](references/philosophy.md)** (Vision, Theoriegrundlage, Michael-Ende-Zitate) und **[references/process.md](references/process.md)** (vollständiger Phasenautomat, Feedback-Regeln, Constraint-Guardrails, Qualitätsmetriken). Diese Datei hier ist die Kurzfassung zum Ausführen — bei Unklarheiten gilt process.md als Referenz.

## Grundregel: Subagenten schlagen vor, du committest

Alle Subagenten (Rollen unten) werden über das `Agent`-Tool mit `subagent_type: general-purpose` aufgerufen. Persona-Text aus `references/agents/*.md` bzw. `references/agents/triggered/*.md` wird in den Prompt injiziert, zusammen mit dem aktuellen Feld-Zustand (Inhalt der relevanten `field/objects/*.md`-Dateien).

**Subagenten schreiben nie selbst Dateien.** Sie geben ihren Vorschlag (neue/aktualisierte Semantic Objects, Beziehungen, Fragen, Widersprüche) als Text zurück. Du — der orchestrierende Hauptthread — schreibst danach die Dateien gemäß `references/semantic-object-schema.md` (neuer datierter Abschnitt anhängen, nie überschreiben). Das verhindert Schreibkonflikte bei parallelen Fan-outs und hält die Versionierungsregel an einer einzigen Stelle durchsetzbar.

## Setup

1. Bestimme einen kurzen `slug` aus dem Vorhaben (z. B. `stadt-vergessen`).
2. Lege im **Zielprojekt des Nutzers** (nicht im Skill-Paket) an:
   - `.ecp/<slug>/field/objects/`
   - `.ecp/<slug>/field/log.md`
   - `.ecp/<slug>/output/`
3. Trage in `field/log.md` einen Kopf mit Datum, Nutzerauftrag und slug ein.

## Phasenablauf (Kurzfassung — Details in process.md)

1. **Collector** — Intake aus Nutzerprompt/Material → erste Semantic Objects.
2. **Divergent Expansion** — EIN `Agent`-Aufruf pro Rolle **in derselben Nachricht** (echter Parallel-Fan-out): Dreamer, Questioner, Character Finder, World Builder. Jede Rolle bekommt den aktuellen Feld-Stand und liefert Vorschläge zurück, die du committest.
   - **Guardrail:** max. 3 Divergenzrunden ohne expliziten Nutzerwunsch nach mehr — danach zwingend weiter zu Schritt 3. Grund: unbeschränkte Emergenz destabilisiert eher, als dass sie hilft (siehe philosophy.md, Goldilocks-Befund).
3. **Gardener** — ein Aufruf, liest alle Objekte, erkennt Muster/Cluster, ergänzt Beziehungen zwischen bestehenden Objekten.
4. **Feedback-Trigger prüfen** (deine eigene Logik, kein Agent-Aufruf):
   - Widerspruch von Gardener/Resonance geflaggt → **Contradiction Agent** (triggered).
   - Neuheit/Überraschung stagniert gegenüber letzter Runde → erneuter **Dreamer**, ggf. + **Mutation Agent** oder **Entropy Agent** (triggered).
   - Offene Fragen werden vom Nutzer/Explorer zu schnell "aufgelöst" → **Silence Agent** (triggered) — hält die Frage bewusst offen.
   - Feld wirkt symbolisch/emotional flach → **Symbol Agent** (triggered).
   - Feld wirkt insgesamt reizarm zu Rundenbeginn → **Curiosity Engine** (triggered).
   - Bei Trigger: Zurück zu Schritt 2/3 mit der spezifischen Rolle, danach erneuter Feedback-Check.
5. **Konvergenz-Checkpoint** — **Resonance** bewertet die 8 Qualitätsmetriken (Neuheit, Überraschung, Emergenz, innere Kohärenz, symbolische Dichte, emotionale Resonanz, Eigenständigkeit der Figuren, Wiederlesewert) qualitativ (kurz, kein Fake-Scoring). Frag den Nutzer, ob weiter expandiert oder jetzt geschrieben werden soll, wenn das nicht schon klar ist.
6. **Explorer** — schreibt schrittweise einen Entwurf aus dem Feld (nicht in einem Rutsch). Stößt er auf einen neuen Widerspruch, zurück zu Schritt 4.
7. **Resonance + Distiller** — Resonance prüft zuerst "Lebendigkeit" der Figuren/Ideen (nicht Korrektheit — siehe Ende-Zitat in philosophy.md); erst wenn das passt, poliert Distiller Sprache/Struktur.
8. **Narrative Compiler** — falls nicht vorgegeben, frag nach der Zielform (Roman, Artikel, Vorlesung, LiaScript-Kurs, Podcast-Skript, Präsentation). Kompiliere aus demselben Feld in diese Form, schreibe nach `output/`.

## Artefakt-Rendering (Claude Artifacts)

Vor dem ersten Rendern die Skill `artifact-design` laden (Pflicht laut Plattformregel). Zwei Artifact-Arten, **gleicher Dateipfad bei jedem Redeploy** (stabile URL):

- **Cognitive-Field-Map**: Mermaid-Graph aller Semantic Objects + Beziehungen. Aktualisieren nach jeder Divergenzrunde, nach dem Gardener-Pass und nach dem Compiler-Schritt. Siehe `references/field-map-artifact.md` für Knoten-/Kantenkonventionen.
- **Kompiliertes Werk**: bei Text-/Kurs-/Präsentationsform optional zusätzlich als lesbare HTML-Ansicht rendern.

Beide sind Ergänzung, keine Ersetzung — die maßgebliche, versionierte Wahrheit bleiben die Markdown-Dateien in `.ecp/<slug>/`.

## Agenten-Referenzen

Kern (immer im Ablauf): [collector](references/agents/collector.md) · [gardener](references/agents/gardener.md) · [dreamer](references/agents/dreamer.md) · [questioner](references/agents/questioner.md) · [world-builder](references/agents/world-builder.md) · [character-finder](references/agents/character-finder.md) · [explorer](references/agents/explorer.md) · [resonance](references/agents/resonance.md) · [distiller](references/agents/distiller.md)

Getriggert (nur bei Bedingung): [curiosity-engine](references/agents/triggered/curiosity-engine.md) · [contradiction-agent](references/agents/triggered/contradiction-agent.md) · [symbol-agent](references/agents/triggered/symbol-agent.md) · [mutation-agent](references/agents/triggered/mutation-agent.md) · [silence-agent](references/agents/triggered/silence-agent.md) · [entropy-agent](references/agents/triggered/entropy-agent.md)
